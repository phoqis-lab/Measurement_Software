class Mmemory():
    def __init__(self,instrument):
        self.instrument = instrument
    
    def get_mmemory_catalog(self, msus: str = None) -> tuple[int, int, list[dict]]:
        """Returns information on the current contents and state of the mass storage media.
        Parameters:
        msus: (Optional) The mass storage unit selector string.
        Returns: A tuple containing (bytes_used: int, bytes_available: int, file_entries: list[dict]).
                 Each dictionary in file_entries contains 'file_name', 'file_type', and 'file_size'."""
        query_cmd = ":MMEM:CAT?"
        if msus:
            query_cmd += f" '{msus}'"

        response = self.instrument.query(query_cmd).strip()
        parts = response.split(',')
        if len(parts) < 2:
            raise ValueError(f"Unexpected response format for memory catalog: '{response}'")

        try:
            bytes_used = int(parts[0])
            bytes_available = int(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse memory usage/available from: '{response}'")

        file_entries = []
        # File entries start from index 2, in triplets of file_name, file_type, file_size
        for i in range(2, len(parts), 3):
            if i + 2 < len(parts):
                file_name = parts[i].strip().strip("'\"")  # Remove potential quotes
                file_type = parts[i + 1].strip().strip("'\"")
                file_size = parts[i + 2].strip().strip("'\"")
                file_entries.append({"file_name": file_name, "file_type": file_type, "file_size": file_size})
        return bytes_used, bytes_available, file_entries

    
    def set_mmemory_cdirectory(self, directory_name: str = None):
        """Changes the default directory for a mass memory file system.
        Parameters:
        directory_name: (Optional) The directory name as a string. If omitted, sets to *RST value."""
        if directory_name is None:
            self.instrument.write(":MMEM:CDIR")
        else:
            self.instrument.write(f":MMEM:CDIR '{directory_name}'")

    def close_mmemory_file(self):
        """Closes the selected file specified in NAME.
        Notes: This is an event command; no query. An error is generated if the file was not open."""
        self.instrument.write(":MMEM:CLOS")

    def copy_mmemory_file(self, src_file: str, dest_file: str, src_msus: str = None, dest_msus: str = None):
        """Copies an existing file to a new file.
        Parameters:
        src_file: The name of the source file.
        dest_file: The name of the destination file.
        src_msus: (Optional) The mass storage unit selector for the source file.
        dest_msus: (Optional) The mass storage unit selector for the destination file."""
        if src_msus and dest_msus:
            self.instrument.write(f":MMEM:COPY '{src_file}','{src_msus}','{dest_file}','{dest_msus}'")
        else:
            self.instrument.write(f":MMEM:COPY '{src_file}','{dest_file}'")

    def set_mmemory_data(self, file_name: str, data: bytes):
        """Loads data into the specified file.
        Parameters:
        file_name: The name of the file (string data).
        data: The data to load (bytes in 488.2 block format)."""
        num_bytes = len(data)
        num_digits = len(str(num_bytes))
        # Assuming data is convertible to Latin-1 for byte representation in SCPI
        self.instrument.write(f":MMEM:DATA '{file_name}',#{num_digits}{num_bytes}" + data.decode('latin-1'))

    def get_mmemory_data(self, file_name: str) -> bytes:
        """Returns the data from the specified file.
        Parameters:
        file_name: The name of the file.
        Returns: The associated data in bytes (488.2 block format)."""
        response = self.instrument.query(f":MMEM:DATA? '{file_name}'").strip()
        if not response.startswith('#'):
            raise ValueError(f"Unexpected response format for memory data: '{response}'")

        num_digits = int(response[1])
        length_str = response[2 : 2 + num_digits]
        data_length = int(length_str)

        data_start_index = 2 + num_digits
        # Encode back to bytes using Latin-1
        return response[data_start_index:].encode('latin-1')

    def delete_mmemory_file(self, file_name: str, msus: str = None):
        """Removes a file from the specified mass storage device.
        Parameters:
        file_name: The name of the file to be removed.
        msus: (Optional) The mass storage unit selector."""
        if msus:
            self.instrument.write(f":MMEM:DEL '{file_name}','{msus}'")
        else:
            self.instrument.write(f":MMEM:DEL '{file_name}'")

    
    def set_mmemory_feed(self, data_handle: str):
        """Sets the <data_handle> to be used to feed data into the file specified by NAME.
        Parameters:
        data_handle: The data handle string."""
        self.instrument.write(f":MMEM:FEED '{data_handle}'")

    def get_mmemory_feed(self) -> str:
        """Returns the <data_handle> currently used to feed data into the file."""
        response = self.instrument.query(":MMEM:FEED?").strip().strip("'\"")
        return response

    def initialize_mmemory(self, msus: str = None, media_type: str = None, numeric_value: float = None):
        """Initializes the specified mass storage media.
        Parameters:
        msus: (Optional) The mass storage unit selector. If omitted, the default is used.
        media_type: (Optional) The type of media to be formatted (LIF|DOS|HFS).
        numeric_value: (Optional) Used to specify format, interleave, sector sizes, etc."""
        command = ":MMEM:INIT"
        params = []
        if msus:
            params.append(f"'{msus}'")
            if media_type:
                valid_media_types = {"LIF", "DOS", "HFS"}
                media_type_upper = media_type.upper()
                if media_type_upper not in valid_media_types:
                    raise ValueError(f"Invalid media type: '{media_type}'. Must be one of {list(valid_media_types)}.")
                params.append(media_type_upper)
                if numeric_value is not None:
                    params.append(str(numeric_value))
        
        if params:
            self.instrument.write(f"{command} {','.join(params)}")
        else:
            self.instrument.write(command)

        # Note: The PDF lists both LOAD and STORE under these entries.
    # I'll create separate methods for LOAD and STORE for clarity and adherence to user request.

    def load_mmemory_dinterchange(self, label: str, file_name: str, msus: str = None):
        """Loads DINTerchange formatted data from mass memory device to internal memory.
        Parameters:
        label: An internal identifier for the instrument trace or macro.
        file_name: The name of the file (quoted string).
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:DINT '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_dinterchange(self, label: str, file_name: str, msus: str = None):
        """Stores DINTerchange formatted data from internal memory to mass memory device.
        Parameters:
        label: An internal identifier for the instrument trace or macro.
        file_name: The name of the file (quoted string).
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:DINT '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def load_mmemory_dinterchange_trace(self, label: str, file_name: str, msus: str = None):
        """Loads a specified trace or array in DINTerchange format.
        Parameters:
        label: An internal identifier for the trace or array.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:DINT:TRAC '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_dinterchange_trace(self, label: str, file_name: str, msus: str = None):
        """Stores a specified trace or array in DINTerchange format.
        Parameters:
        label: An internal identifier for the trace or array.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:DINT:TRAC '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def load_mmemory_macro(self, label: str, file_name: str, msus: str = None):
        """Loads a specified macro from mass memory device to internal memory.
        Parameters:
        label: An internal identifier for the macro.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:MACR '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_macro(self, label: str, file_name: str, msus: str = None):
        """Stores a specified macro from internal memory to mass memory device.
        Parameters:
        label: An internal identifier for the macro.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:MACR '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def load_mmemory_state(self, state_number: int, file_name: str, msus: str = None):
        """Loads a specified instrument state from mass memory device to internal memory.
        Parameters:
        state_number: The state number (corresponds to *SAV and *RCL).
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:STAT {state_number},'{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_state(self, state_number: int, file_name: str, msus: str = None):
        """Stores a specified instrument state from internal memory to mass memory device.
        Parameters:
        state_number: The state number (corresponds to *SAV and *RCL).
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:STAT {state_number},'{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def load_mmemory_table(self, label: str, file_name: str, msus: str = None):
        """Loads a specified memory table from mass memory device to internal memory.
        Parameters:
        label: An internal identifier for the table.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:TABL '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_table(self, label: str, file_name: str, msus: str = None):
        """Stores a specified memory table from internal memory to mass memory device.
        Parameters:
        label: An internal identifier for the table.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:TABL '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def load_mmemory_trace(self, label: str, file_name: str, msus: str = None):
        """Loads a specified trace or array from mass memory device to internal memory.
        Parameters:
        label: An internal identifier for the trace or array.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:LOAD:TRAC '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    def store_mmemory_trace(self, label: str, file_name: str, msus: str = None):
        """Stores a specified trace or array from internal memory to mass memory device.
        Parameters:
        label: An internal identifier for the trace or array.
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        command = f":MMEM:STOR:TRAC '{label}','{file_name}'"
        if msus:
            command += f",'{msus}'"
        self.instrument.write(command)

    
    def set_mmemory_msis(self, msus: str = None):
        """Selects a default mass storage device.
        Parameters:
        msus: (Optional) The mass storage unit selector. If omitted, the device-dependent default is used."""
        if msus:
            self.instrument.write(f":MMEM:MSIS '{msus}'")
        else:
            self.instrument.write(":MMEM:MSIS")

    def get_mmemory_msis(self) -> str:
        """Returns the currently selected default mass storage device."""
        response = self.instrument.query(":MMEM:MSIS?").strip().strip("'\"")
        return response

    def move_mmemory_file(self, src_file: str, dest_file: str, src_msus: str = None, dest_msus: str = None):
        """Moves an existing file to another file name, optionally across mass storage devices.
        Parameters:
        src_file: The name of the source file.
        dest_file: The new name of the file.
        src_msus: (Optional) The mass storage unit selector for the source file.
        dest_msus: (Optional) The mass storage unit selector for the destination file."""
        if src_msus and dest_msus:
            self.instrument.write(f":MMEM:MOVE '{src_file}','{src_msus}','{dest_file}','{dest_msus}'")
        else:
            self.instrument.write(f":MMEM:MOVE '{src_file}','{dest_file}'")

    def set_mmemory_name(self, file_name: str, msus: str = None):
        """Sets the name of the file specification used by the CLOSE and OPEN commands.
        Parameters:
        file_name: The name of the file.
        msus: (Optional) The mass storage unit selector."""
        if msus:
            self.instrument.write(f":MMEM:NAME '{file_name}','{msus}'")
        else:
            self.instrument.write(f":MMEM:NAME '{file_name}'")

    def get_mmemory_name(self) -> str:
        """Returns the name of the file specification used by the CLOSE and OPEN commands."""
        response = self.instrument.query(":MMEM:NAME?").strip().strip("'\"")
        return response

    def open_mmemory_file(self):
        """Opens the selected file specified in NAME.
        Notes: This is an event command; no query. If the file is non-existent, it is created."""
        self.instrument.write(":MMEM:OPEN")

    def pack_mmemory_device(self, msus: str = None):
        """Causes the mass storage device to be packed, recovering unused memory.
        Parameters:
        msus: (Optional) The mass storage unit selector. If not specified, the default is used."""
        if msus:
            self.instrument.write(f":MMEM:PACK '{msus}'")
        else:
            self.instrument.write(":MMEM:PACK")