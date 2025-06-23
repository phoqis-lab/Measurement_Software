class Memory():
    def __init__(self):
        self.instrument = None

    def get_memory_catalog(self) -> tuple[int, int, list[dict]]:
        """Returns information on the current contents and state of the instrument's memory.
        Returns: A tuple containing (bytes_used: int, bytes_available: int, directory_list: list[dict]).
                 Each dictionary in directory_list contains 'name', 'type', and 'size'."""
        response = self.instrument.query("MEM:CAT?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        # The directory list starts from index 2, in triplets of name, type, size
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"") # Remove potential quotes
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def get_memory_catalog_all(self) -> tuple[int, int, list[dict]]:
        """Returns a directory list and memory sizes related to all allocatable items in instrument memory."""
        response = self.instrument.query("MEM:CAT:ALL?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog all: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def get_memory_catalog_ascii(self) -> tuple[int, int, list[dict]]:
        """Returns the directory list related only to ASCii items in instrument memory."""
        response = self.instrument.query("MEM:CAT:ASC?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog ASCII: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def get_memory_catalog_binary(self) -> tuple[int, int, list[dict]]:
        """Returns the directory list related only to BINary items in instrument memory."""
        response = self.instrument.query("MEM:CAT:BIN?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog BINary: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def get_memory_catalog_macro(self) -> tuple[int, int, list[dict]]:
        """Returns the directory list related only to MACRO items in instrument memory."""
        response = self.instrument.query("MEM:CAT:MACR?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog MACRO: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def get_memory_catalog_state(self) -> tuple[int, int, list[dict]]:
        """Returns the directory list related only to STATE items in instrument memory."""
        response = self.instrument.query("MEM:CAT:STAT?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog STATE: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list


    def get_memory_catalog_table(self) -> tuple[int, int, list[dict]]:
        """Returns the directory list related only to TABLE items in instrument memory."""
        response = self.instrument.query("MEM:CAT:TABL?").strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog TABLE: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        directory_list = []
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                name = parts[i].strip().strip("'\"")
                mem_type = parts[i+1].strip().strip("'\"")
                size = parts[i+2].strip().strip("'\"")
                directory_list.append({"name": name, "type": mem_type, "size": size})
        return bytes_used, bytes_available, directory_list

    def clear_memory_name(self, name: str):
        """Removes all data from the instrument memory associated with <name>.
        Notes: This is an event command; no query."""
        self.instrument.write(f"MEM:CLE:NAME '{name}'")

    def clear_memory_table(self):
        """Removes the data values from all element lists in the SELected TABLe.
        Notes: This is an event command; no query."""
        self.instrument.write(f"MEM:CLE:TABL")

    def copy_memory_name(self, source_name: str, destination_name: str):
        """Copies the data contents from a source memory item to a destination memory item.
        Parameters:
        source_name: The name of the source memory item.
        destination_name: The name of the destination memory item."""
        self.instrument.write(f"MEM:COPY:NAME '{source_name}','{destination_name}'")

    def copy_memory_table(self, table_name: str):
        """Copies the data values of all element lists from the SELected TABLe to the specified memory table.
        Parameters:
        table_name: The name of the destination memory table."""
        self.instrument.write(f"MEM:COPY:TABL '{table_name}'")

    def set_memory_data(self, name: str, data: bytes):
        """Loads data into the specified memory location.
        Parameters:
        name: The name of the memory location (character data).
        data: The data to load (bytes in 488.2 block format)."""
        num_bytes = len(data)
        num_digits = len(str(num_bytes))
        self.instrument.write(f"MEM:DATA '{name}',#{num_digits}{num_bytes}" + data.decode('latin-1'))

    def get_memory_data(self, name: str) -> bytes:
        """Returns the data from the specified memory location.
        Parameters:
        name: The name of the memory location.
        Returns: The associated data in bytes (488.2 block format)."""
        response = self.instrument.query(f"MEM:DATA? '{name}'").strip()
        if not response.startswith('#'):
            raise ValueError(f"Unexpected response format for memory data: '{response}'")

        num_digits = int(response[1])
        length_str = response[2 : 2 + num_digits]
        data_length = int(length_str)

        data_start_index = 2 + num_digits
        return response[data_start_index:].encode('latin-1')

    def delete_memory_all(self):
        """Removes all memory names, key definitions, and data, returning memory to "available."
        Notes: This is an event command; no query."""
        self.instrument.write(f"MEM:DEL:ALL")

    def delete_memory_name(self, name: str):
        """Deletes the definition associated with <name>.
        Parameters:
        name: The name of the definition to delete."""
        self.instrument.write(f"MEM:DEL:NAME '{name}'")


    def exchange_memory_name(self, name1: str, name2: str):
        """Swaps the data contents between two memory items.
        Parameters:
        name1: The name of the first memory item.
        name2: The name of the second memory item."""
        self.instrument.write(f"MEM:EXCH:NAME '{name1}','{name2}'")

    def exchange_memory_table(self, table_name: str):
        """Swaps the data contents between the SELected TABLe and the specified memory table.
        Parameters:
        table_name: The name of the memory table to exchange with."""
        self.instrument.write(f"MEM:EXCH:TABL '{table_name}'")

    def get_memory_free(self) -> tuple[int, int]:
        """Returns information on the user memory space (bytes available, bytes in use)."""
        response = self.instrument.query("MEM:FREE?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free values from: '{response}'")

    def get_memory_free_all(self) -> tuple[int, int]:
        """Returns memory sizes related to all items in instrument memory."""
        response = self.instrument.query("MEM:FREE:ALL?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free all: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free all values from: '{response}'")

    def get_memory_free_ascii(self) -> tuple[int, int]:
        """Returns memory usage and availability for ASCii data types."""
        response = self.instrument.query("MEM:FREE:ASC?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free ASCII: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free ASCII values from: '{response}'")

    def get_memory_free_binary(self) -> tuple[int, int]:
        """Returns memory usage and availability for BINary data types."""
        response = self.instrument.query("MEM:FREE:BIN?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free BINary: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free BINary values from: '{response}'")

    def get_memory_free_macro(self) -> tuple[int, int]:
        """Returns memory usage and availability for MACRO data types."""
        response = self.instrument.query("MEM:FREE:MACR?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free MACRO: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free MACRO values from: '{response}'")

    
    def get_memory_free_state(self) -> tuple[int, int]:
        """Returns memory usage and availability for STATE data types."""
        response = self.instrument.query("MEM:FREE:STAT?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free STATE: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free STATE values from: '{response}'")

    def get_memory_free_table(self) -> tuple[int, int]:
        """Returns memory usage and availability for TABLE data types."""
        response = self.instrument.query("MEM:FREE:TABL?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for memory free TABLE: '{response}'")
        try:
            bytes_available = int(parts[0])
            bytes_in_use = int(parts[1])
            return bytes_available, bytes_in_use
        except ValueError:
            raise ValueError(f"Failed to parse memory free TABLE values from: '{response}'")

    def get_memory_nstates(self) -> int:
        """Returns the number of *SAV/*RCL states available in the instrument."""
        response = self.instrument.query("MEM:NSTAT?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for number of states (not integer): '{response}'")

    def get_memory_state_catalog(self) -> list[str]:
        """Requests a list of defined names in the MEMory:STATe subsystem.
        Returns: A list of defined names as strings."""
        response = self.instrument.query("MEM:STAT:CAT?").strip()
        if not response:
            return []
        # Response is comma-separated quoted strings. Split by comma and strip quotes/whitespace.
        return [name.strip().strip("'\"") for name in response.split(',')]

    def set_memory_state_define(self, name: str, register_number: int):
        """Associates a <name> with a *SAV/*RCL register number.
        Parameters:
        name: The name (character data format).
        register_number: The register number (numeric value)."""
        self.instrument.write(f"MEM:STAT:DEF '{name}',{register_number}")

    def get_memory_state_define(self, name: str) -> int:
        """Returns the *SAV/*RCL register number associated with a defined name.
        Parameters:
        name: The name to query.
        Returns: The associated register number."""
        response = self.instrument.query(f"MEM:STAT:DEF? '{name}'").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for memory state define (not integer): '{response}'")

    def get_memory_type(self, name: str) -> str:
        """Requests information about a defined name, returning the subsystem where it was defined.
        Parameters:
        name: The name to query.
        Returns: A string indicating the subsystem (e.g., "ROUT:MOD:") or a null string if not defined."""
        response = self.instrument.query(f"MEM:TYPE? '{name}'").strip().strip("'\"")
        return response

    def set_memory_table_bnumber(self, bnumbers: list[int]):
        """Sets the gas bottle number(s) in a table.
        Parameters:
        bnumbers: A list of positive integers representing gas bottle numbers."""
        if not all(isinstance(n, int) and n > 0 for n in bnumbers):
            raise ValueError("All BNUMber values must be positive integers.")
        data_str = ",".join(map(str, bnumbers))
        self.instrument.write(f"MEM:TABL:BNUM {data_str}")

    def get_memory_table_bnumber_points(self) -> int:
        """Returns the number of points in the BNUMber column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:BNUM:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1 # Or raise specific error, or return float('nan')
            raise ValueError(f"Unexpected response for table BNUMber points (not integer): '{response}'")

    def set_memory_table_ccurve(self, concentrations: list[float]):
        """Sets the value of concentration in ppm using the current curve in linearization tables.
        Parameters:
        concentrations: A list of numeric values representing concentrations in ppm."""
        data_str = ",".join(map(str, concentrations))
        self.instrument.write(f"MEM:TABL:CCUR {data_str}")

    def get_memory_table_ccurve_points(self) -> int:
        """Returns the number of points in the CCURve column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:CCUR:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CCURve points (not integer): '{response}'")

    def set_memory_table_concentration(self, concentrations: list[float]):
        """Sets the gas concentration in ppm.
        Parameters:
        concentrations: A list of numeric values representing gas concentrations in ppm."""
        data_str = ",".join(map(str, concentrations))
        self.instrument.write(f"MEM:TABL:CONC {data_str}")

    def get_memory_table_concentration_points(self) -> int:
        """Returns the number of points in the CONCentration column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:CONC:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CONCentration points (not integer): '{response}'")

    
    def set_memory_table_condition_magnitude(self, booleans: list[bool]):
        """Specifies the CONDition[:MAGNitude] points of the TABLE.
        Parameters:
        booleans: A list of boolean values."""
        data_str = ",".join(["1" if b else "0" for b in booleans])
        self.instrument.write(f"MEM:TABL:COND:MAGN {data_str}")

    def get_memory_table_condition_magnitude_points(self) -> int:
        """Returns the number of points in the CONDition[:MAGNitude] list of the SELected TABLE."""
        response = self.instrument.query("MEM:TABL:COND:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CONDition MAGNitude points (not integer): '{response}'")

    def set_memory_table_cpoint(self, cpoints: list[float]):
        """Sets the linearization gas dilution percentage or "cut point".
        Parameters:
        cpoints: A list of numeric values representing cut points."""
        data_str = ",".join(map(str, cpoints))
        self.instrument.write(f"MEM:TABL:CPO {data_str}")

    def get_memory_table_cpoint_points(self) -> int:
        """Returns the number of points in the CPOint column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:CPO:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CPOint points (not integer): '{response}'")

    def set_memory_table_current_magnitude(self, magnitudes: list[float]):
        """Specifies the CURRent[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing current magnitudes (default units are current units)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:CURR:MAGN {data_str}")

    def get_memory_table_current_magnitude_points(self) -> int:
        """Returns the number of points in the CURRent[:MAGNitude] list of the SELected TABLE."""
        response = self.instrument.query("MEM:TABL:CURR:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CURRent MAGNitude points (not integer): '{response}'")

    def set_memory_table_current_phase(self, phases: list[float]):
        """Specifies the CURRent:PHASe points of the TABLE.
        Parameters:
        phases: A list of numeric values representing current phases (default units are angle units)."""
        data_str = ",".join(map(str, phases))
        self.instrument.write(f"MEM:TABL:CURR:PHAS {data_str}")

    
    def get_memory_table_current_phase_points(self) -> int:
        """Returns the number of points in the CURRent:PHASe list of the SELected TABLE."""
        response = self.instrument.query("MEM:TABL:CURR:PHAS:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table CURRent PHASe points (not integer): '{response}'")

    def set_memory_table_dfactory(self, values: list[float]):
        """Sets the maximum allowable drift from factory settings (Zero or Span factory setting).
        Parameters:
        values: A list of numeric values."""
        data_str = ",".join(map(str, values))
        self.instrument.write(f"MEM:TABL:DFAC {data_str}")

    def get_memory_table_dfactory_points(self) -> int:
        """Returns the number of points in the DFACtory column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:DFAC:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table DFACtory points (not integer): '{response}'")

    def set_memory_table_dlast(self, values: list[float]):
        """Sets the maximum allowable drift from the most recently saved zero and set point.
        Parameters:
        values: A list of numeric values."""
        data_str = ",".join(map(str, values))
        self.instrument.write(f"MEM:TABL:DLAST {data_str}")

    def get_memory_table_dlast_points(self) -> int:
        """Returns the number of points in the DLASt column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:DLAST:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table DLASt points (not integer): '{response}'")

    
    def set_memory_table_dlinearize(self, values: list[float]):
        """Sets the maximum allowable drift from the most recent linearization.
        Parameters:
        values: A list of numeric values."""
        data_str = ",".join(map(str, values))
        self.instrument.write(f"MEM:TABL:DLIN {data_str}")

    def get_memory_table_dlinearize_points(self) -> int:
        """Returns the number of points in the DLINearize column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:DLIN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table DLINearize points (not integer): '{response}'")

    def set_memory_table_expected(self, values: list[float]):
        """Sets the expected value (e.g., expected gas concentration in ppm for emissions benches).
        Parameters:
        values: A list of numeric values."""
        data_str = ",".join(map(str, values))
        self.instrument.write(f"MEM:TABL:EXP {data_str}")

    def get_memory_table_expected_points(self) -> int:
        """Returns the number of points in the EXPected column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:EXP:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table EXPected points (not integer): '{response}'")

    
    def define_memory_table(self, structure_string: str, size: int = None):
        """Allocates space and defines the structure of a TABLE in the instrument memory.
        Parameters:
        structure_string: A comma-separated list of elements defining the table structure.
        size: (Optional) The maximum number of points in each of the lists (numeric value)."""
        if size is None:
            self.instrument.write(f"MEM:TABL:DEF '{structure_string}'")
        else:
            self.instrument.write(f"MEM:TABL:DEF '{structure_string}',{size}")

    def get_memory_table_define(self) -> tuple[str, int]:
        """Returns the structure string and size (in points) of memory allocated for the table."""
        response = self.instrument.query("MEM:TABL:DEF?").strip()
        parts = response.split(',')
        if len(parts) < 1:
            raise ValueError(f"Unexpected response format for table define: '{response}'")
        
        structure_string = parts[0].strip().strip("'\"")
        table_size = 0
        if len(parts) > 1:
            try:
                table_size = int(parts[1].strip())
            except ValueError:
                pass # Size might not be a valid integer
        return structure_string, table_size

    def set_memory_table_force_magnitude(self, magnitudes: list[float]):
        """Specifies the FORCe[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing force magnitudes (default units are newtons)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:FORC:MAGN {data_str}")

    def get_memory_table_force_magnitude_points(self) -> int:
        """Returns the number of points in the FORCe[:MAGNitude] list of the selected TABLE."""
        response = self.instrument.query("MEM:TABL:FORC:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table FORCe MAGNitude points (not integer): '{response}'")

    
    def set_memory_table_frequency(self, frequencies: list[float]):
        """Specifies the FREQuency points of the TABLE.
        Parameters:
        frequencies: A list of numeric values representing frequencies."""
        data_str = ",".join(map(str, frequencies))
        self.instrument.write(f"MEM:TABL:FREQ {data_str}")

    def get_memory_table_frequency_points(self) -> int:
        """Returns the number of points in the FREQuency list of the SELected TABLE."""
        response = self.instrument.query("MEM:TABL:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table FREQuency points (not integer): '{response}'")

    def set_memory_table_label(self, labels: list[str]):
        """Sets the label name(s) in a table in character string format.
        Parameters:
        labels: A list of string values representing labels."""
        # Enclose each label in double quotes for SCPI character data
        quoted_labels = [f'"{label}"' for label in labels]
        data_str = ",".join(quoted_labels)
        self.instrument.write(f"MEM:TABL:LAB {data_str}")

    def get_memory_table_label_points(self) -> int:
        """Returns the number of points in the LABel column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:LAB:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table LABel points (not integer): '{response}'")

    def set_memory_table_llimit(self, limits: list[float]):
        """Sets the lower limit value(s).
        Parameters:
        limits: A list of numeric values representing lower limits."""
        data_str = ",".join(map(str, limits))
        self.instrument.write(f"MEM:TABL:LLIM {data_str}")

    def get_memory_table_llimit_points(self) -> int:
        """Returns the number of points in the LLIMit column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:LLIM:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table LLIMit points (not integer): '{response}'")

    def set_memory_table_log(self, logs: list[str]):
        """Sets a series of string data elements for logging.
        Parameters:
        logs: A list of string values."""
        # Enclose each log entry in double quotes for SCPI character data
        quoted_logs = [f'"{log}"' for log in logs]
        data_str = ",".join(quoted_logs)
        self.instrument.write(f"MEM:TABL:LOG {data_str}")

    
    def get_memory_table_log_points(self) -> int:
        """Returns the number of points in the LOG column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:LOG:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table LOG points (not integer): '{response}'")

    def set_memory_table_loss_magnitude(self, magnitudes: list[float]):
        """Specifies the LOSS[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing loss magnitudes (default unit is DB)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:LOSS:MAGN {data_str}")

    def get_memory_table_loss_magnitude_points(self) -> int:
        """Returns the number of points in the LOSS[:MAGNitude] list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:LOSS:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table LOSS MAGNitude points (not integer): '{response}'")

    def set_memory_table_loss_phase(self, phases: list[float]):
        """Specifies the LOSS:PHASe points of the TABLE.
        Parameters:
        phases: A list of numeric values representing loss phases (default units are angle units)."""
        data_str = ",".join(map(str, phases))
        self.instrument.write(f"MEM:TABL:LOSS:PHAS {data_str}")

    def get_memory_table_loss_phase_points(self) -> int:
        """Returns the number of points in the LOSS:PHASe list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:LOSS:PHAS:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table LOSS PHASe points (not integer): '{response}'")

    def set_memory_table_ncurve(self, concentrations: list[float]):
        """Sets the value of concentration in ppm using the newly calculated curve (New CURve) in linearization tables.
        Parameters:
        concentrations: A list of numeric values representing concentrations in ppm."""
        data_str = ",".join(map(str, concentrations))
        self.instrument.write(f"MEM:TABL:NCUR {data_str}")

    def get_memory_table_ncurve_points(self) -> int:
        """Returns the number of points in the NCURve column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:NCUR:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table NCURve points (not integer): '{response}'")

    
    def set_memory_table_power_magnitude(self, magnitudes: list[float]):
        """Specifies the POWer[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing power magnitudes (default units are power units)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:POW:MAGN {data_str}")

    def get_memory_table_power_magnitude_points(self) -> int:
        """Returns the number of points in the POWer[:MAGNitude] list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:POW:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table POWer MAGNitude points (not integer): '{response}'")

    def set_memory_table_raw(self, raw_values: list[float]):
        """Sets a collection of points in instrument internal units (e.g., raw gas concentration).
        Parameters:
        raw_values: A list of numeric values."""
        data_str = ",".join(map(str, raw_values))
        self.instrument.write(f"MEM:TABL:RAW {data_str}")

    def get_memory_table_raw_points(self) -> int:
        """Returns the number of points in the RAW column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:RAW:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table RAW points (not integer): '{response}'")

    def set_memory_table_resistance_magnitude(self, magnitudes: list[float]):
        """Specifies the RESistance[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing resistance magnitudes."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:RES:MAGN {data_str}")

    def get_memory_table_resistance_magnitude_points(self) -> int:
        """Returns the number of points in the RESistance[:MAGNitude] list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:RES:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table RESistance MAGNitude points (not integer): '{response}'")

    
    def select_memory_table(self, name: str):
        """Sets or queries the name of the TABLE selected.
        Parameters:
        name: The name of the TABLE (character data)."""
        self.instrument.write(f"MEM:TABL:SEL '{name}'")

    def get_selected_memory_table(self) -> str:
        """Returns the name of the currently selected TABLE."""
        response = self.instrument.query("MEM:TABL:SEL?").strip().strip("'\"")
        return response

    def set_memory_table_speed_magnitude(self, magnitudes: list[float]):
        """Specifies the SPEed[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing speed magnitudes (default units are meters per second)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:SPE:MAGN {data_str}")

    def get_memory_table_speed_magnitude_points(self) -> int:
        """Returns the number of points in the SPEed[:MAGNitude] list of the selected TABLE."""
        response = self.instrument.query("MEM:TABL:SPE:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table SPEed MAGNitude points (not integer): '{response}'")

    def set_memory_table_time_magnitude(self, magnitudes: list[float]):
        """Specifies the TIME[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing time magnitudes (default units are seconds)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:TIME:MAGN {data_str}")

    def get_memory_table_time_magnitude_points(self) -> int:
        """Returns the number of points in the TIME[:MAGNitude] list of the selected TABLE."""
        response = self.instrument.query("MEM:TABL:TIME:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table TIME MAGNitude points (not integer): '{response}'")

    def set_memory_table_tolerance(self, tolerances: list[float]):
        """Sets a series of tolerance values (e.g., allowable deviation in gas concentration).
        Parameters:
        tolerances: A list of numeric values representing tolerance percentages (%FS)."""
        data_str = ",".join(map(str, tolerances))
        self.instrument.write(f"MEM:TABL:TOL {data_str}")

    
    def get_memory_table_tolerance_points(self) -> int:
        """Returns the number of points in the TOLerance column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:TOL:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table TOLerance points (not integer): '{response}'")

    def set_memory_table_ulimit(self, limits: list[float]):
        """Sets the upper limit value(s).
        Parameters:
        limits: A list of numeric values representing upper limits."""
        data_str = ",".join(map(str, limits))
        self.instrument.write(f"MEM:TABL:ULIM {data_str}")

    def get_memory_table_ulimit_points(self) -> int:
        """Returns the number of points in the ULIMit column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:ULIM:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table ULIMit points (not integer): '{response}'")

    def set_memory_table_voltage_magnitude(self, magnitudes: list[float]):
        """Specifies the VOLTage[:MAGNitude] points of the TABLE.
        Parameters:
        magnitudes: A list of numeric values representing voltage magnitudes (default units are voltage units)."""
        data_str = ",".join(map(str, magnitudes))
        self.instrument.write(f"MEM:TABL:VOLT:MAGN {data_str}")

    def get_memory_table_voltage_magnitude_points(self) -> int:
        """Returns the number of points in the VOLTage[:MAGNitude] list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:VOLT:MAGN:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table VOLTage MAGNitude points (not integer): '{response}'")

    def set_memory_table_voltage_phase(self, phases: list[float]):
        """Specifies the VOLTage:PHASe points of the TABLE.
        Parameters:
        phases: A list of numeric values representing voltage phases (default units are angle units)."""
        data_str = ",".join(map(str, phases))
        self.instrument.write(f"MEM:TABL:VOLT:PHAS {data_str}")

    
    def get_memory_table_voltage_phase_points(self) -> int:
        """Returns the number of points in the VOLTage:PHASe list of the SELected TABLe."""
        response = self.instrument.query("MEM:TABL:VOLT:PHAS:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table VOLTage PHASe points (not integer): '{response}'")

    def set_memory_table_wfactor(self, wfactors: list[float]):
        """Sets weighting factors in a table.
        Parameters:
        wfactors: A list of numeric values representing weighting factors."""
        data_str = ",".join(map(str, wfactors))
        self.instrument.write(f"MEM:TABL:WFAC {data_str}")

    def get_memory_table_wfactor_points(self) -> int:
        """Returns the number of points in the WFACtor column for the currently selected table."""
        response = self.instrument.query("MEM:TABL:WFAC:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            if response.upper() == "NAN":
                return -1
            raise ValueError(f"Unexpected response for table WFACtor points (not integer): '{response}'")
