class Mandatory():
    def __init__(self, instrument):
        self.instrument = instrument
    def clear_event_registers(self):
        """
        Clear all the event registers and clear the error queue (*CLS).
        """
        self.instrument.write("*CLS")
    
    def set_enable_event_status(self, value):
        """
        Set the enable register for the standard event status register set (*ESE).

        Parameters:
        value (int): An integer value where bit 1 and bit 6 are not used (always 0).
                     The range corresponds to binary numbers X0XXXX0X.
        """
        # Basic validation for the value based on the description
        if isinstance(value, int) and 0 <= value <= 255: # Max 255 for an 8-bit register
            # Further validation for bits 1 and 6 being 0 could be added:
            # if (value & 0b01000010) == 0: # Check if bit 1 (0b00000010) or bit 6 (0b01000000) are set
            self.instrument.write(f"*ESE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 1 and 6 effectively 0).")
    
    def get_standard_event_status_enable(self):
        """
        Query the enable register for the standard event status register set (*ESE?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have
             already been set in the register.
        """
        response = self.instrument.query("*ESE?")
        return int(response.strip())
    
    def get_and_clear_standard_event_status_register(self):
        """
        Query and clear the event register for the standard event status register (*ESR?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
             The value of the register is set to 0 after this command is executed.
        """
        response = self.instrument.query("*ESR?")
        return int(response.strip())
    
    def get_id(self):
        """
        Query the ID string of the instrument (*IDN?).

        Returns:
        str: The ID string in the format "RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>".
        """
        response = self.instrument.query("*IDN?")
        return response.strip()
    
    def set_operation_complete(self):
        """
        Set the Operation Complete bit (bit 0) in the standard event status register to 1
        after the current operation is finished.
        """
        self.instrument.write("*OPC")

    def is_operation_complete(self):
        """
        Query whether the current operation is finished.

        Returns:
        bool: True (1) if the current operation is finished; False (0) otherwise.
        """
        response = self.instrument.query("*OPC?")
        return bool(int(response.strip()))


    def reset_instrument(self):
            """
            Restore the instrument to the default state .
            """
            self.instrument.write("*RST")

    def set_enable_service_request(self, value):
        """
        Set the enable register for the status byte register set (*SRE).

        Parameters:
        value (int): An integer value from 0 to 255. Bit 0 and bit 1 of the status byte register
                     are not used and are always treated as 0.
        """
        # Basic validation for the value
        if isinstance(value, int) and 0 <= value <= 255:
            # Further validation for bits 0 and 1 being 0 could be added:
            # if (value & 0b00000011) == 0: # Check if bit 0 (0b00000001) or bit 1 (0b00000010) are set
            self.instrument.write(f"*SRE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 0 and 1 effectively 0).")

    def get_enable_service_request(self):
        """
        Query the enable register for the status byte register set (*SRE?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have
             already been set in the register.
        """
        response = self.instrument.query("*SRE?")
        return int(response.strip())
    
    def read_status_byte(self):
        """
        Query the event register for the status byte register (*STB?).
        The value of the status byte register is set to 0 after this command is executed.

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
        """
        response = self.instrument.query("*STB?")
        return int(response.strip())

    def self_test(self):
        """
        Perform a self-test and then return the self-test results (*TST?).

        Returns:
        int: A decimal integer representing the self-test results.
        """
        response = self.instrument.query("*TST?")
        return int(response.strip())

    def wait_for_operation_finish(self):
        """
        Wait for the current operation to finish (*WAI).
        The subsequent command can only be carried out after the current command has been executed.
        """
        self.instrument.write("*WAI")
    
    #Required commands
    def get_system_error(self) -> str:
        """
        Queries the next error from the error queue, returning its code and message.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:ERR:NEXT?").strip()
        return response
    
    def get_system_version(self) -> str:
        """
        Returns the SCPI version supported by the instrument.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:VERS?").strip()
        return response
    
    def set_status_operation_enable(self, value: int):
        """
        Sets the enable mask for the OPERation register.
        :param value: The integer value of the enable mask (range: 0 through 65535).
        
        """
        #TODO: Fix value to be boolean?
        self._set_status_enable(":STAT:OPER:ENAB", value)

    def get_status_operation_enable(self) -> int:
        """
        Returns the contents of the enable mask for the OPERation register.
        
        """
        return self._get_status_enable(":STAT:OPER:ENAB?")