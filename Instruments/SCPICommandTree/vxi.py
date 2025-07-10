import re

class VXI:
    """
    
    """
    def __init__(self, instrument):
        """
       
        """
        self.instrument = instrument

    
    def get_vxi_configure_dnumber(self) -> int:
        """
        Returns the number of devices in the system.
        :return: The number of devices (1 to 256 inclusive).
        """
        response = self.instrument.query(":VXI:CONF:DNUM?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI DNUMber (not integer): '{response}'")

    def get_vxi_configure_hierarchy(self) -> dict:
        """
        Returns current hierarchy configuration information about the selected logical address.
        :return: A dictionary containing hierarchy information.
                 Fields: 'logical_address', 'commander_logical_address', 'interrupt_handlers',
                         'interrupters', 'pass_failed', 'manufacturer_comment'.
        """
        response = self.instrument.query(":VXI:CONF:HIER?").strip()
        parts = response.split(',')
        if len(parts) < 13: # Minimum expected parts based on documentation
            raise ValueError(f"Unexpected response format for VXI HIERarchy: '{response}'")

        try:
            logical_address = int(parts[0])
            commander_logical_address = int(parts[1])
            # Interrupt Handlers (7 NR1s)
            interrupt_handlers = [int(p) for p in parts[2:9]]
            # Interrupters (7 NR1s)
            interrupters = [int(p) for p in parts[9:16]]
            pass_failed = int(parts[16]) # This is tricky, might be quoted string then int
            
            # Manufacturer comment is a quoted string, might span multiple comma-separated parts
            manufacturer_comment_parts = parts[17:]
            manufacturer_comment = ""
            if manufacturer_comment_parts:
                # Reconstruct the original string and then strip quotes
                full_comment_str = ",".join(manufacturer_comment_parts).strip()
                if full_comment_str.startswith('"') and full_comment_str.endswith('"'):
                    manufacturer_comment = full_comment_str[1:-1]
                else:
                    manufacturer_comment = full_comment_str # Assume no quotes if not present

            return {
                'logical_address': logical_address,
                'commander_logical_address': commander_logical_address,
                'interrupt_handlers': interrupt_handlers,
                'interrupters': interrupters,
                'pass_failed': pass_failed,
                'manufacturer_comment': manufacturer_comment
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error parsing VXI HIERarchy response '{response}': {e}")

    def get_vxi_configure_hierarchy_all(self) -> list[dict]:
        """
        When issued to a resource manager, returns configuration information about all logical addresses.
        If received by a non-resource manager, returns info about destination device and its immediate servants.
        Information for multiple logical addresses is semicolon-separated.
        :return: A list of dictionaries, each containing hierarchy information for a device.
        """
        response = self.instrument.query(":VXI:CONF:HIER:ALL?").strip()
        device_configs = []
        # Responses for multiple devices are semicolon-separated
        raw_devices = response.split(';')
        for raw_device_response in raw_devices:
            if not raw_device_response.strip():
                continue
            parts = raw_device_response.strip().split(',')
            if len(parts) < 13:
                # Log a warning or handle incomplete data appropriately
                print(f"Warning: Skipping incomplete hierarchy data: {raw_device_response}")
                continue
            try:
                logical_address = int(parts[0])
                commander_logical_address = int(parts[1])
                interrupt_handlers = [int(p) for p in parts[2:9]]
                interrupters = [int(p) for p in parts[9:16]]
                pass_failed = int(parts[16])
                
                manufacturer_comment_parts = parts[17:]
                manufacturer_comment = ""
                if manufacturer_comment_parts:
                    full_comment_str = ",".join(manufacturer_comment_parts).strip()
                    if full_comment_str.startswith('"') and full_comment_str.endswith('"'):
                        manufacturer_comment = full_comment_str[1:-1]
                    else:
                        manufacturer_comment = full_comment_str

                device_configs.append({
                    'logical_address': logical_address,
                    'commander_logical_address': commander_logical_address,
                    'interrupt_handlers': interrupt_handlers,
                    'interrupters': interrupters,
                    'pass_failed': pass_failed,
                    'manufacturer_comment': manufacturer_comment
                })
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing device hierarchy response '{raw_device_response}': {e}")
                continue
        return device_configs


    def get_vxi_configure_hierarchy_verbose(self) -> str:
        """
        Returns a quoted string indicating the device information for the selected device.
        The format of this string is manufacturer specific.
        :return: The verbose hierarchy information string.
        """
        response = self.instrument.query(":VXI:CONF:HIER:VERB?").strip()
        # The response is a quoted string
        if response.startswith('"') and response.endswith('"'):
            return response[1:-1]
        return response

    def get_vxi_configure_hierarchy_verbose_all(self) -> list[str]:
        """
        Returns a semi-colon separated sequence of strings indicating the device information for all devices.
        The format of each string is manufacturer specific.
        :return: A list of verbose hierarchy information strings.
        """
        response = self.instrument.query(":VXI:CONF:HIER:VERB:ALL?").strip()
        # Responses for multiple devices are semicolon-separated, and each is a quoted string.
        raw_strings = response.split(';')
        return [s.strip().strip('"') for s in raw_strings if s.strip()]

    
    def get_vxi_configure_information(self) -> dict:
        """
        Returns static information about the selected logical address.
        :return: A dictionary containing information: 'logical_address', 'manufacturer_id', 'model_code',
                 'device_class', 'address_space', 'a16_memory_offset', 'a24_memory_offset',
                 'a32_memory_offset', 'a16_memory_size', 'a24_memory_size', 'a32_memory_size',
                 'slot_number', 'slot0_logical_address', 'subclass', 'attribute', 'manufacturer_comment'.
        """
        response = self.instrument.query(":VXI:CONF:INF?").strip()
        parts = response.split(',')
        if len(parts) < 15: # Minimum expected parts
            raise ValueError(f"Unexpected response format for VXI INF (too few parts): '{response}'")

        try:
            logical_address = int(parts[0])
            manufacturer_id = int(parts[1])
            model_code = int(parts[2])
            device_class = int(parts[3])
            address_space = int(parts[4])
            a16_memory_offset = int(parts[5])
            a24_memory_offset = int(parts[6])
            a32_memory_offset = int(parts[7])
            a16_memory_size = int(parts[8])
            a24_memory_size = int(parts[9])
            a32_memory_size = int(parts[10])
            slot_number = int(parts[11])
            slot0_logical_address = int(parts[12])
            subclass = int(parts[13])
            attribute = int(parts[14])

            # Manufacturer comment is a quoted string, might span multiple comma-separated parts
            manufacturer_comment_parts = parts[15:]
            manufacturer_comment = ""
            if manufacturer_comment_parts:
                full_comment_str = ",".join(manufacturer_comment_parts).strip()
                if full_comment_str.startswith('"') and full_comment_str.endswith('"'):
                    manufacturer_comment = full_comment_str[1:-1]
                else:
                    manufacturer_comment = full_comment_str

            return {
                'logical_address': logical_address,
                'manufacturer_id': manufacturer_id,
                'model_code': model_code,
                'device_class': device_class,
                'address_space': address_space,
                'a16_memory_offset': a16_memory_offset,
                'a24_memory_offset': a24_memory_offset,
                'a32_memory_offset': a32_memory_offset,
                'a16_memory_size': a16_memory_size,
                'a24_memory_size': a24_memory_size,
                'a32_memory_size': a32_memory_size,
                'slot_number': slot_number,
                'slot0_logical_address': slot0_logical_address,
                'subclass': subclass,
                'attribute': attribute,
                'manufacturer_comment': manufacturer_comment
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error parsing VXI INFormation response '{response}': {e}")


    def get_vxi_configure_information_all(self) -> list[dict]:
        """
        When issued to a resource manager, returns static information about all logical addresses.
        If received by a non-resource manager, returns info about destination device and its immediate servants.
        Information for multiple logical addresses is semicolon-separated.
        :return: A list of dictionaries, each containing static information for a device.
        """
        response = self.instrument.query(":VXI:CONF:INF:ALL?").strip()
        device_infos = []
        raw_devices = response.split(';')
        for raw_device_response in raw_devices:
            if not raw_device_response.strip():
                continue
            parts = raw_device_response.strip().split(',')
            if len(parts) < 15:
                print(f"Warning: Skipping incomplete information data: {raw_device_response}")
                continue
            try:
                logical_address = int(parts[0])
                manufacturer_id = int(parts[1])
                model_code = int(parts[2])
                device_class = int(parts[3])
                address_space = int(parts[4])
                a16_memory_offset = int(parts[5])
                a24_memory_offset = int(parts[6])
                a32_memory_offset = int(parts[7])
                a16_memory_size = int(parts[8])
                a24_memory_size = int(parts[9])
                a32_memory_size = int(parts[10])
                slot_number = int(parts[11])
                slot0_logical_address = int(parts[12])
                subclass = int(parts[13])
                attribute = int(parts[14])

                manufacturer_comment_parts = parts[15:]
                manufacturer_comment = ""
                if manufacturer_comment_parts:
                    full_comment_str = ",".join(manufacturer_comment_parts).strip()
                    if full_comment_str.startswith('"') and full_comment_str.endswith('"'):
                        manufacturer_comment = full_comment_str[1:-1]
                    else:
                        manufacturer_comment = full_comment_str

                device_infos.append({
                    'logical_address': logical_address,
                    'manufacturer_id': manufacturer_id,
                    'model_code': model_code,
                    'device_class': device_class,
                    'address_space': address_space,
                    'a16_memory_offset': a16_memory_offset,
                    'a24_memory_offset': a24_memory_offset,
                    'a32_memory_offset': a32_memory_offset,
                    'a16_memory_size': a16_memory_size,
                    'a24_memory_size': a24_memory_size,
                    'a32_memory_size': a32_memory_size,
                    'slot_number': slot_number,
                    'slot0_logical_address': slot0_logical_address,
                    'subclass': subclass,
                    'attribute': attribute,
                    'manufacturer_comment': manufacturer_comment
                })
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing device information response '{raw_device_response}': {e}")
                continue
        return device_infos

    def get_vxi_configure_information_verbose(self) -> str:
        """
        Returns a quoted string indicating the device information for the selected device.
        The format of this string is manufacturer specific.
        :return: The verbose information string.
        """
        response = self.instrument.query(":VXI:CONF:INF:VERB?").strip()
        if response.startswith('"') and response.endswith('"'):
            return response[1:-1]
        return response

    def get_vxi_configure_information_verbose_all(self) -> list[str]:
        """
        Returns a semi-colon separated sequence of quoted strings indicating the device information for all devices.
        The format of each string is manufacturer specific.
        :return: A list of verbose information strings.
        """
        response = self.instrument.query(":VXI:CONF:INF:VERB:ALL?").strip()
        raw_strings = response.split(';')
        return [s.strip().strip('"') for s in raw_strings if s.strip()]

    
    def get_vxi_configure_laddress(self) -> list[int]:
        """
        When issued to a resource manager, returns a comma separated list of logical addresses
        of the devices in the system. The logical address of the responding device is first.
        If received by non-resource manager, contains logical address of destination device
        followed by list of immediate servants.
        :return: A list of logical addresses (0 to 255 inclusive).
        """
        response = self.instrument.query(":VXI:CONF:LADD?").strip()
        try:
            return [int(addr) for addr in response.split(',') if addr.strip()]
        except ValueError:
            raise ValueError(f"Unexpected response for VXI LADDress (not comma-separated integers): '{response}'")

    def get_vxi_configure_number(self) -> int:
        """
        When issued to a resource manager, returns the number of devices in the system.
        If received by non-resource manager, returns the number of immediate servants
        including the destination device itself.
        :return: The number of devices (1 to 256 inclusive).
        """
        response = self.instrument.query(":VXI:CONF:NUMB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI NUMBer (not integer): '{response}'")

    
    def get_vxi_register_read(self, register_id):
        """
        Returns the contents of the specified 16-bit register at the selected logical address.
        :param register_id: The byte address (even number from 0 to 62) or register name (string).
                            Supported names: A24Low, A24High, A32Low, A32High, ATTRibute, DHIGh,
                            DLOW, DTYPE, ICONtrol, ID, ISTatus, MODid, OFFSet, PROTocol,
                            RESPonse, SNLow, SNHigh, STATus, SUBClass, VNUMber.
        :return: The integer content of the register.
        """
        if isinstance(register_id, str):
            # Ensure proper capitalization as per SCPI standard if needed
            register_id_map = {
                "A24LOW": "A24Low", "A24HIGH": "A24High", "A32LOW": "A32Low",
                "A32HIGH": "A32High", "ATTRIBUTE": "ATTR", "DHIGH": "DHIGh",
                "DLOW": "DLOW", "DTYPE": "DTYP", "ICONTROL": "ICON", "ID": "ID",
                "ISTATUS": "IST", "MODID": "MODid", "OFFSET": "OFFS",
                "PROTOCOL": "PROT", "RESPONSE": "RESP", "SNLOW": "SNLow",
                "SNHIGH": "SNHigh", "STATUS": "STAT", "SUBCLASS": "SUBC",
                "VNUMBER": "VNUM"
            }
            mapped_id = register_id_map.get(register_id.upper(), register_id)
            query_cmd = f":VXI:REG:READ? {mapped_id}"
        elif isinstance(register_id, int):
            if register_id % 2 != 0 or not (0 <= register_id <= 62):
                raise ValueError("Register byte address must be an even number from 0 to 62.")
            query_cmd = f":VXI:REG:READ? {register_id}"
        else:
            raise TypeError("register_id must be an integer (byte address) or a string (register name).")

        response = self.instrument.query(query_cmd).strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI REGister READ? (not integer): '{response}'")

    def get_vxi_register_read_verbose(self, register_id):
        """
        Returns a quoted string indicating the register contents for the selected device in a human-readable format.
        :param register_id: The byte address (even number from 0 to 62) or register name (string).
        :return: The verbose register contents string.
        """
        if isinstance(register_id, str):
            register_id_map = {
                "A24LOW": "A24Low", "A24HIGH": "A24High", "A32LOW": "A32Low",
                "A32HIGH": "A32High", "ATTRIBUTE": "ATTR", "DHIGH": "DHIGh",
                "DLOW": "DLOW", "DTYPE": "DTYP", "ICONTROL": "ICON", "ID": "ID",
                "ISTATUS": "IST", "MODID": "MODid", "OFFSET": "OFFS",
                "PROTOCOL": "PROT", "RESPONSE": "RESP", "SNLOW": "SNLow",
                "SNHIGH": "SNHigh", "STATUS": "STAT", "SUBCLASS": "SUBC",
                "VNUMBER": "VNUM"
            }
            mapped_id = register_id_map.get(register_id.upper(), register_id)
            query_cmd = f":VXI:REG:READ:VERB? {mapped_id}"
        elif isinstance(register_id, int):
            if register_id % 2 != 0 or not (0 <= register_id <= 62):
                raise ValueError("Register byte address must be an even number from 0 to 62.")
            query_cmd = f":VXI:REG:READ:VERB? {register_id}"
        else:
            raise TypeError("register_id must be an integer (byte address) or a string (register name).")

        response = self.instrument.query(query_cmd).strip()
        if response.startswith('"') and response.endswith('"'):
            return response[1:-1]
        return response

    
    def set_vxi_register_write(self, register_id, data):
        """
        Writes data to the specified register on the selected logical address.
        :param register_id: The byte address (even number from 0 to 62) or register name (string).
                            Supported names: CONTrol, DEXTended, DHIGH, DLOW, ICONtrol, MODid,
                            LADDress, OFFSet, SIGNal.
        :param data: A 16-bit value (-32768 to 32767).
        """
        if not (-32768 <= data <= 32767):
            raise ValueError("Data for register write must be a 16-bit value (-32768 to 32767).")

        if isinstance(register_id, str):
            register_id_map = {
                "CONTROL": "CONT", "DEXTENDED": "DEXT", "DHIGH": "DHIGh",
                "DLOW": "DLOW", "ICONTROL": "ICON", "MODID": "MODid",
                "LADDRESS": "LADD", "OFFSET": "OFFS", "SIGNAL": "SIGN"
            }
            mapped_id = register_id_map.get(register_id.upper(), register_id)
            write_cmd = f":VXI:REG:WRITE {mapped_id},{data}"
        elif isinstance(register_id, int):
            if register_id % 2 != 0 or not (0 <= register_id <= 62):
                raise ValueError("Register byte address must be an even number from 0 to 62.")
            write_cmd = f":VXI:REG:WRITE {register_id},{data}"
        else:
            raise TypeError("register_id must be an integer (byte address) or a string (register name).")

        self.instrument.write(write_cmd)

    
    def get_vxi_reset(self) -> int:
        """
        Resets the selected logical address.
        The command waits for five seconds or until the selected device has indicated passed (whichever occurs first).
        :return: The state of the selected device after reset (FAIL=0, PASS=2, READY=3).
        """
        response = self.instrument.query(":VXI:RES?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI RESet (not integer): '{response}'")

    def get_vxi_reset_verbose(self) -> str:
        """
        Returns a quoted string indicating the state of the specified device after reset.
        The format of this string is manufacturer specific.
        :return: The verbose reset state string.
        """
        response = self.instrument.query(":VXI:RES:VERB?").strip()
        if response.startswith('"') and response.endswith('"'):
            return response[1:-1]
        return response

    
    def set_vxi_select(self, logical_address: int):
        """
        Specifies the logical address which is to be used by all subsequent commands in the VXI subsystem.
        :param logical_address: The logical address (0 to 255).
        Notes: *RST default value for logical_address is that no logical address is selected.
               Other commands requiring a logical_address will error if none is selected.
        """
        if not (0 <= logical_address <= 255):
            raise ValueError("Logical address must be between 0 and 255.")
        self.instrument.write(f":VXI:SEL {logical_address}")

    def get_vxi_select(self) -> int:
        """
        Queries the currently selected logical address.
        :return: The logical address (0 to 255), or -1 if no logical address has been selected.
        """
        response = self.instrument.query(":VXI:SEL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI SELect (not integer): '{response}'")

    
    def vxi_wsprotocol_command_any(self, data: int):
        """
        Sends the specified word serial command to the selected logical address.
        :param data: The numeric or non-decimal value specifying the command to be sent.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(f":VXI:WSPR:COMM:ANY {data}")

    def vxi_wsprotocol_command_ahiline(self, hand_id: int, line_number: int):
        """
        Sends an Assign Handler Line command to the selected logical address.
        :param hand_id: Handler ID (1 to 7 inclusive).
        :param line_number: Line number (0 to 7 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (1 <= hand_id <= 7):
            raise ValueError("hand_id must be between 1 and 7.")
        if not (0 <= line_number <= 7):
            raise ValueError("line_number must be between 0 and 7.")
        self.instrument.write(f":VXI:WSPR:COMM:AHIL {hand_id},{line_number}")

    def vxi_wsprotocol_command_ailine(self, int_id: int, line_number: int):
        """
        Sends an Assign Interrupter Line command to the selected logical address.
        :param int_id: Interrupter ID (1 to 7 inclusive).
        :param line_number: Line number (0 to 7 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (1 <= int_id <= 7):
            raise ValueError("int_id must be between 1 and 7.")
        if not (0 <= line_number <= 7):
            raise ValueError("line_number must be between 0 and 7.")
        self.instrument.write(f":VXI:WSPR:COMM:AIL {int_id},{line_number}")

    
    def vxi_wsprotocol_command_amcontrol(self, response_mask: int):
        """
        Sends an Asynchronous Mode Control command to the selected logical address.
        :param response_mask: Response mask (0 to 15 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (0 <= response_mask <= 15):
            raise ValueError("response_mask must be between 0 and 15.")
        self.instrument.write(f":VXI:WSPR:COMM:AMCON {response_mask}")

    def vxi_wsprotocol_command_ano(self):
        """
        Sends an Abort Normal Operation command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:ANO")

    def vxi_wsprotocol_command_bavailable(self, boolean_field: bool, byte_value: int):
        """
        Sends a Byte Available command to the selected logical address.
        :param boolean_field: Selects whether the END bit is set in the command.
        :param byte_value: Byte value (0 to 255 inclusive).
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= byte_value <= 255):
            raise ValueError("byte_value must be between 0 and 255.")
        self.instrument.write(f":VXI:WSPR:COMM:BAV {scpi_bool},{byte_value}")

    def vxi_wsprotocol_command_bno(self, boolean_field: bool):
        """
        Sends a Begin Normal Operation command to the selected logical address.
        :param boolean_field: Selects whether the Top_level bit is set in the command.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        scpi_bool = "1" if boolean_field else "0"
        self.instrument.write(f":VXI:WSPR:COMM:BNO {scpi_bool}")

    def vxi_wsprotocol_command_brq(self):
        """
        Sends a Byte Request command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:BRQ")

    def vxi_wsprotocol_command_cevent(self, boolean_field: bool, event_number: int):
        """
        Sends a Control Event command to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param event_number: Event number (0 to 127 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= event_number <= 127):
            raise ValueError("event_number must be between 0 and 127.")
        self.instrument.write(f":VXI:WSPR:COMM:CEV {scpi_bool},{event_number}")

    def vxi_wsprotocol_command_clr(self):
        """
        Sends a Clear command to the selected logical address.
        """
        self.instrument.write(":VXI:WSPR:COMM:CLR")

    
    def vxi_wsprotocol_command_clock(self):
        """
        Sends a Clear Lock command to the selected logical address.
        """
        self.instrument.write(":VXI:WSPR:COMM:CLOC")

    def vxi_wsprotocol_command_cresponse(self, response_mask: int):
        """
        Sends a Control Response command to the selected logical address.
        :param response_mask: Response mask (0 to 127 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (0 <= response_mask <= 127):
            raise ValueError("response_mask must be between 0 and 127.")
        self.instrument.write(f":VXI:WSPR:COMM:CRES {response_mask}")

    def vxi_wsprotocol_command_eno(self):
        """
        Sends an End Normal Operation command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:ENO")

    def vxi_wsprotocol_command_gdevice(self, logical_address: int):
        """
        Sends a Grant Device command to the selected logical address.
        :param logical_address: Logical address (0 to 255 inclusive).
        """
        if not (0 <= logical_address <= 255):
            raise ValueError("logical_address must be between 0 and 255.")
        self.instrument.write(f":VXI:WSPR:COMM:GDEV {logical_address}")

    def vxi_wsprotocol_command_icommand(self, logical_address: int):
        """
        Sends an Identify Commander command to the selected logical address.
        :param logical_address: Logical address (0 to 255 inclusive).
        """
        if not (0 <= logical_address <= 255):
            raise ValueError("logical_address must be between 0 and 255.")
        self.instrument.write(f":VXI:WSPR:COMM:ICOM {logical_address}")

    def vxi_wsprotocol_command_rdevice(self, logical_address: int):
        """
        Sends a Release Device command to the selected logical address.
        :param logical_address: Logical address (0 to 255 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (0 <= logical_address <= 255):
            raise ValueError("logical_address must be between 0 and 255.")
        self.instrument.write(f":VXI:WSPR:COMM:RDEV {logical_address}")

    def vxi_wsprotocol_command_rhandlers(self):
        """
        Sends a Read Handlers command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RHAN")

    
    def vxi_wsprotocol_command_rhline(self, hand_id: int):
        """
        Sends a Read Handler Line command to the selected logical address.
        :param hand_id: Handler ID (1 to 7 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (1 <= hand_id <= 7):
            raise ValueError("hand_id must be between 1 and 7.")
        self.instrument.write(f":VXI:WSPR:COMM:RHL {hand_id}")

    def vxi_wsprotocol_command_riline(self, int_id: int):
        """
        Sends a Read Interrupter Line command to the selected logical address.
        :param int_id: Interrupter ID (1 to 7 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        if not (1 <= int_id <= 7):
            raise ValueError("int_id must be between 1 and 7.")
        self.instrument.write(f":VXI:WSPR:COMM:RIL {int_id}")

    def vxi_wsprotocol_command_rinterrupter(self):
        """
        Sends a Read Interrupters command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RINT")

    def vxi_wsprotocol_command_rmodid(self):
        """
        Sends a Read MODid command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RMOD")

    def vxi_wsprotocol_command_rperror(self):
        """
        Sends a Read Protocol Error command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RPER")

    def vxi_wsprotocol_command_rprotocol(self):
        """
        Sends a Read Protocol command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RPR")

    def vxi_wsprotocol_command_rstb(self):
        """
        Sends a Read Status Byte command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RSTB")

    
    def vxi_wsprotocol_command_rsarea(self):
        """
        Sends a Read Servant Area command to the selected logical address.
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        self.instrument.write(":VXI:WSPR:COMM:RSAR")

    def vxi_wsprotocol_command_slmodid(self, boolean_field: bool, modid_value: int):
        """
        Sends a Set Lower MODid command to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param modid_value: MODID 6-0 field (0 to 127 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= modid_value <= 127):
            raise ValueError("MODID 6-0 value must be between 0 and 127.")
        self.instrument.write(f":VXI:WSPR:COMM:SLMOD {scpi_bool},{modid_value}")

    def vxi_wsprotocol_command_slock(self):
        """
        Sends a Set Lock command to the selected logical address.
        """
        self.instrument.write(":VXI:WSPR:COMM:SLOC")

    def vxi_wsprotocol_command_sumodid(self, boolean_field: bool, modid_value: int):
        """
        Sends a Set Upper MODid command to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param modid_value: MODID 12-7 field (0 to 63 inclusive).
        Notes: The response can be read with VXI:WSPRotocol:RESPonse?.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= modid_value <= 63):
            raise ValueError("MODID 12-7 value must be between 0 and 63.")
        self.instrument.write(f":VXI:WSPR:COMM:SUMOD {scpi_bool},{modid_value}")

    def vxi_wsprotocol_command_trigger(self):
        """
        Sends a Trigger command to the selected logical address.
        """
        self.instrument.write(":VXI:WSPR:COMM:TRIG")

    
    def get_vxi_wsprotocol_message_receive(self, count_or_terminator):
        """
        Receives a message from the selected logical address using both word serial and byte transfer protocols.
        The command always terminates on the End bit being set.
        :param count_or_terminator: Optional. A specified number of bytes (int) or a terminator (str, e.g., "LF", "CRLF", "END").
        :return: The received message as a string.
        """
        if count_or_terminator is None:
            query_cmd = ":VXI:WSPR:MESS:REC?"
        elif isinstance(count_or_terminator, int):
            query_cmd = f":VXI:WSPR:MESS:REC? {count_or_terminator}"
        elif isinstance(count_or_terminator, str):
            query_cmd = f":VXI:WSPR:MESS:REC? {count_or_terminator.upper()}"
        else:
            raise TypeError("count_or_terminator must be an integer or a string.")
        
        response = self.instrument.query(query_cmd).strip()
        return response

    def vxi_wsprotocol_message_send(self, message_string: str, end_bit: str = "END"):
        """
        Sends the specified message string to the selected logical address using word serial and byte transfer protocols.
        :param message_string: The message string to send.
        :param end_bit: Optional. "END" (default) sets the End bit on the last byte. "NEND" does not set it.
        """
        valid_end_bits = {"END", "NEND"}
        end_bit_upper = end_bit.upper()
        if end_bit_upper not in valid_end_bits:
            raise ValueError(f"Invalid end_bit: '{end_bit}'. Must be 'END' or 'NEND'.")
        
        send_cmd = f":VXI:WSPR:MESS:SEND '{message_string}'"
        if end_bit_upper == "NEND":
            send_cmd += ",NEND"
        self.instrument.write(send_cmd)

    
    def get_vxi_wsprotocol_query_any(self, data: int) -> int:
        """
        Sends the specified word serial query to the selected logical address.
        :param data: The numeric or non-decimal value specifying the query to be sent.
        :return: The response to the word serial query as an integer.
        """
        response = self.instrument.query(f":VXI:WSPR:QUER:ANY? {data}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy ANY? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_ahiline(self, hand_id: int, line_number: int) -> int:
        """
        Sends an Assign Handler Line command query to the selected logical address.
        :param hand_id: Handler ID (1 to 7 inclusive).
        :param line_number: Line number (0 to 7 inclusive).
        :return: The response to the command as an integer.
        """
        if not (1 <= hand_id <= 7):
            raise ValueError("hand_id must be between 1 and 7.")
        if not (0 <= line_number <= 7):
            raise ValueError("line_number must be between 0 and 7.")
        response = self.instrument.query(f":VXI:WSPR:QUER:AHIL? {hand_id},{line_number}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy AHILine? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_ailine(self, int_id: int, line_number: int) -> int:
        """
        Sends an Assign Interrupter Line command query to the selected logical address.
        :param int_id: Interrupter ID (1 to 7 inclusive).
        :param line_number: Line number (0 to 7 inclusive).
        :return: The response to the command as an integer.
        """
        if not (1 <= int_id <= 7):
            raise ValueError("int_id must be between 1 and 7.")
        if not (0 <= line_number <= 7):
            raise ValueError("line_number must be between 0 and 7.")
        response = self.instrument.query(f":VXI:WSPR:QUER:AIL? {int_id},{line_number}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy AILine? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_amcontrol(self, response_mask: int) -> int:
        """
        Sends an Asynchronous Mode Control command query to the selected logical address.
        :param response_mask: Response mask (0 to 15 inclusive).
        :return: The response to the command as an integer.
        """
        if not (0 <= response_mask <= 15):
            raise ValueError("response_mask must be between 0 and 15.")
        response = self.instrument.query(f":VXI:WSPR:QUER:AMCON? {response_mask}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy AMControl? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_ano(self) -> int:
        """
        Sends an Abort Normal Operation command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:ANO?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy ANO? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_bno(self, boolean_field: bool) -> int:
        """
        Sends a Begin Normal Operation command query to the selected logical address.
        :param boolean_field: Selects whether the Top_level bit is set in the command.
        :return: The response to the command as an integer.
        """
        scpi_bool = "1" if boolean_field else "0"
        response = self.instrument.query(f":VXI:WSPR:QUER:BNO? {scpi_bool}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy BNO? (not integer): '{response}'")

    
    def get_vxi_wsprotocol_query_brq(self) -> int:
        """
        Sends a Byte Request command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:BRQ?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy BRQ? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_cevent(self, boolean_field: bool, event_number: int) -> int:
        """
        Sends a Control Event command query to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param event_number: Event number (0 to 127 inclusive).
        :return: The response to the command as an integer.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= event_number <= 127):
            raise ValueError("event_number must be between 0 and 127.")
        response = self.instrument.query(f":VXI:WSPR:QUER:CEV? {scpi_bool},{event_number}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy CEVent? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_cresponse(self, response_mask: int) -> int:
        """
        Sends a Control Response command query to the selected logical address.
        :param response_mask: Response mask (0 to 127 inclusive).
        :return: The response to the command as an integer.
        """
        if not (0 <= response_mask <= 127):
            raise ValueError("response_mask must be between 0 and 127.")
        response = self.instrument.query(f":VXI:WSPR:QUER:CRES? {response_mask}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy CRESponse? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_eno(self) -> int:
        """
        Sends an End Normal Operation command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:ENO?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy ENO? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rdevice(self, logical_address: int) -> int:
        """
        Sends a Release Device command query to the selected logical address.
        :param logical_address: Logical address (0 to 255 inclusive).
        :return: The response to the command as an integer.
        """
        if not (0 <= logical_address <= 255):
            raise ValueError("logical_address must be between 0 and 255.")
        response = self.instrument.query(f":VXI:WSPR:QUER:RDEV? {logical_address}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RDEVice? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rhandlers(self) -> int:
        """
        Sends a Read Handlers command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RHAN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RHANdlers? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rhline(self, hand_id: int) -> int:
        """
        Sends a Read Handler Line command query to the selected logical address.
        :param hand_id: Handler ID (1 to 7 inclusive).
        :return: The response to the command as an integer.
        """
        if not (1 <= hand_id <= 7):
            raise ValueError("hand_id must be between 1 and 7.")
        response = self.instrument.query(f":VXI:WSPR:QUER:RHL? {hand_id}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RHLine? (not integer): '{response}'")

    
    def get_vxi_wsprotocol_query_riline(self, int_id: int) -> int:
        """
        Sends a Read Interrupter Line command query to the selected logical address.
        :param int_id: Interrupter ID (1 to 7 inclusive).
        :return: The response to the command as an integer.
        """
        if not (1 <= int_id <= 7):
            raise ValueError("int_id must be between 1 and 7.")
        response = self.instrument.query(f":VXI:WSPR:QUER:RIL? {int_id}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RILine? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rinterrupter(self) -> int:
        """
        Sends a Read Interrupters command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RINT?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RINTerrupter? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rmodid(self) -> int:
        """
        Sends a Read MODid command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RMOD?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RMODid? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rperror(self) -> int:
        """
        Sends a Read Protocol Error command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RPER?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RPERror? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rprotocol(self) -> int:
        """
        Sends a Read Protocol command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RPR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RPRotocol? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rstb(self) -> int:
        """
        Sends a Read Status Byte command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RSTB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RSTB? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_rsarea(self) -> int:
        """
        Sends a Read Servant Area command query to the selected logical address.
        :return: The response to the command as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:QUER:RSAR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy RSARea? (not integer): '{response}'")

    
    def get_vxi_wsprotocol_query_slmodid(self, boolean_field: bool, modid_value: int) -> int:
        """
        Sends a Set Lower MODid command query to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param modid_value: MODID 6-0 field (0 to 127 inclusive).
        :return: The response to the command as an integer.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= modid_value <= 127):
            raise ValueError("MODID 6-0 value must be between 0 and 127.")
        response = self.instrument.query(f":VXI:WSPR:QUER:SLMOD? {scpi_bool},{modid_value}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy SLModid? (not integer): '{response}'")

    def get_vxi_wsprotocol_query_sumodid(self, boolean_field: bool, modid_value: int) -> int:
        """
        Sends a Set Upper MODid command query to the selected logical address.
        :param boolean_field: Selects whether the Enable bit is set in the command.
        :param modid_value: MODID 12-7 field (0 to 63 inclusive).
        :return: The response to the command as an integer.
        """
        scpi_bool = "1" if boolean_field else "0"
        if not (0 <= modid_value <= 63):
            raise ValueError("MODID 12-7 value must be between 0 and 63.")
        response = self.instrument.query(f":VXI:WSPR:QUER:SUMOD? {scpi_bool},{modid_value}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol QUERy SUModid? (not integer): '{response}'")

    
    def get_vxi_wsprotocol_response(self) -> int:
        """
        Returns one word of data from the data low register on the selected logical address.
        :return: The data word as an integer.
        """
        response = self.instrument.query(":VXI:WSPR:RESP?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for VXI WSPRotocol RESPonse? (not integer): '{response}'")
