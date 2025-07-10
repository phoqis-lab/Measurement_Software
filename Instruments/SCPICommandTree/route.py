class Route():
    def __init__(self,instrument):
        self.instrument = instrument
   

    def close_route_channel(self, channel_list: str):
        """Closes specific individual channels.
        Parameters:
        channel_list: A string representing the channel list (e.g., '(@101,102)', '(@1:3)')."""
        self.instrument.write(f"ROUT:CLOS {channel_list}")

    def get_route_close_state(self, channel_list: str = None) -> list[int]:
        """Queries the condition of individual switches.
        Parameters:
        channel_list: (Optional) A string representing the channel list to query.
                      If omitted, returns a list of all closed switches in the instrument.
        Returns: A list of integers (1 for closed, 0 for open) for each channel in the list,
                 or a list of all closed channels if channel_list is omitted."""
        if channel_list:
            response = self.instrument.query(f"ROUT:CLOS? {channel_list}").strip()
            # Assuming response is comma-separated 0s and 1s
            return [int(x) for x in response.split(',')]
        else:
            response = self.instrument.query("ROUT:CLOS:STATE?").strip()
            # The response for STATE? is an IEEE 488.2 definite length block
            # For simplicity, assuming a simple comma-separated channel list string for now.
            # Real implementation might need to parse the block header first.
            if response.startswith('#'):
                num_digits = int(response[1])
                length_str = response[2 : 2 + num_digits]
                data_length = int(length_str)
                channel_list_str = response[2 + num_digits:].strip()
            else:
                channel_list_str = response.strip()

            if channel_list_str:
                # Example: "(@101,102,103)" -> ["@101", "102", "103"]
                # Need to strip parentheses and split by comma
                channels_raw = channel_list_str.strip('()').split(',')
                # This function is meant to return "1" or "0" for the state,
                # but the query form for STATE? returns the list of closed switches.
                # Adjusting to return the list of closed channels as strings.
                return [ch.strip() for ch in channels_raw if ch.strip()]
            return []


    def get_route_module_catalog(self) -> list[str]:
        """Returns a list of all currently defined module names.
        Returns: A list of module names as strings."""
        response = self.instrument.query("ROUT:MOD:CAT?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., '"MyModule1","MyModule2"')
        # Split by comma and strip quotes/whitespace.
        return [name.strip().strip("'\"") for name in response.split(',')]

    def define_route_module(self, module_name: str, module_address: str):
        """Assigns a user-defined name to a module address.
        Parameters:
        module_name: The user-defined name for the module.
        module_address: The hardware-dependent address (e.g., VME address)."""
        self.instrument.write(f"ROUT:MOD:DEF '{module_name}','{module_address}'")

    def get_route_module_define(self, module_name: str) -> str:
        """Returns the module address bound to the specified module name.
        Parameters:
        module_name: The name of the module to query.
        Returns: The module address as a string."""
        response = self.instrument.query(f"ROUT:MOD:DEF? '{module_name}'").strip()
        return response

    def delete_route_module_all(self):
        """Deletes all module name bindings.
        Notes: This is an event command; no query."""
        self.instrument.write("ROUT:MOD:DEL:ALL")


    def delete_route_module_name(self, module_name: str):
        """Removes a module name binding.
        Parameters:
        module_name: The name of the module to remove."""
        self.instrument.write(f"ROUT:MOD:DEL:NAME '{module_name}'")

    def open_route_channel(self, channel_list: str):
        """Opens specific channels.
        Parameters:
        channel_list: A string representing the channel list (e.g., '(@101,102)', '(@1:3)')."""
        self.instrument.write(f"ROUT:OPEN {channel_list}")

    def get_route_open_state(self, channel_list: str) -> list[int]:
        """Queries the condition of individual switches.
        Parameters:
        channel_list: A string representing the channel list to query.
        Returns: A list of integers (1 for open, 0 for closed) for each channel in the list."""
        response = self.instrument.query(f"ROUT:OPEN? {channel_list}").strip()
        # Assuming response is comma-separated 0s and 1s
        return [int(x) for x in response.split(',')]

    def open_route_all_channels(self):
        """Opens all channels in the instrument.
        Notes: This is an event command; no query."""
        self.instrument.write("ROUT:OPEN:ALL")

    def get_route_path_catalog(self) -> list[str]:
        """Returns a list of all currently defined path names.
        Returns: A list of path names as strings."""
        response = self.instrument.query("ROUT:PATH:CAT?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., '"MyPath1","MyPath2"')
        # Split by comma and strip quotes/whitespace.
        return [name.strip().strip("'\"") for name in response.split(',')]

    def define_route_path(self, path_name: str, channel_list: str):
        """Assigns a <path_name> as a user-specified way of referring to a <channel_list>.
        Parameters:
        path_name: The user-defined name for the path.
        channel_list: A string representing the channel list associated with the path."""
        self.instrument.write(f"ROUT:PATH:DEF '{path_name}',{channel_list}")

    def get_route_path_define(self, path_name: str) -> str:
        """Returns the channel list bound to the specified path name.
        Parameters:
        path_name: The name of the path to query.
        Returns: The channel list as a string (e.g., '(@101,102,103)')."""
        response = self.instrument.query(f"ROUT:PATH:DEF? '{path_name}'").strip()
        # The response is described as a block containing the <channel_list>.
        # Assuming direct return of the channel list string for simplicity.
        # Real implementation might need to parse the block header first.
        if response.startswith('#'):
            num_digits = int(response[1])
            length_str = response[2 : 2 + num_digits]
            data_length = int(length_str)
            channel_list_str = response[2 + num_digits:].strip()
            return channel_list_str
        return response

    def delete_route_path_all(self):
        """Deletes all path name bindings.
        Notes: This is an event command; no query."""
        self.instrument.write("ROUT:PATH:DEL:ALL")

    def delete_route_path_name(self, path_name: str):
        """Removes a path name binding.
        Parameters:
        path_name: The name of the path to remove."""
        self.instrument.write(f"ROUT:PATH:DEL:NAME '{path_name}'")

    def get_route_sample_catalog(self) -> list[str]:
        """Returns a comma-separated list of strings containing available sample points.
        Returns: A list of sample point names as strings."""
        response = self.instrument.query("ROUT:SAMP:CAT?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., '"BAG","DILute"')
        return [sp.strip().strip("'\"") for sp in response.split(',')]

    def set_route_sample_open(self, sample_point: str):
        """Causes flow from the specified sample point to the selected instrument(s).
        Parameters:
        sample_point: The sample point (e.g., BAG, DILute, PRE, POST, MID, CEFFiciency, NONE, ZERO, SPAN, VERify, MANifold)."""
        valid_sample_points = {
            "BAG", "DILUTE", "PRE", "POST", "MID", "CEFFICIENCY",
            "NONE", "ZERO", "SPAN", "VERIFY", "MANIFOLD",
            "DIL", "CEFF", "VER"
        }
        sample_point_upper = sample_point.upper()
        if sample_point_upper not in valid_sample_points:
            raise ValueError(f"Invalid sample point: '{sample_point}'.")

        # Use abbreviations for SCPI command if available
        if sample_point_upper == "DILUTE": scpi_value = "DIL"
        elif sample_point_upper == "CEFFICIENCY": scpi_value = "CEFF"
        elif sample_point_upper == "VERIFY": scpi_value = "VER"
        else: scpi_value = sample_point_upper

        self.instrument.write(f"ROUT:SAMP:OPEN {scpi_value}")

    def get_route_sample_open(self) -> str:
        """Queries the currently selected sample point.
        Returns: The currently selected sample point as a string (e.g., 'BAG', 'NONE')."""
        response = self.instrument.query("ROUT:SAMP:OPEN?").strip().strip("'\"")
        # Normalize to full name if an abbreviation was returned
        if response.upper() == "DIL": return "DILUTE"
        if response.upper() == "CEFF": return "CEFFICIENCY"
        if response.upper() == "VER": return "VERIFY"
        return response.upper()


    def set_route_scan(self, channel_list: str):
        """Specifies a list of channels for the instrument to sequence through.
        Parameters:
        channel_list: A string representing the channel list (e.g., '(@1,3:5,9)')."""
        self.instrument.write(f"ROUT:SCAN {channel_list}")

    def get_route_scan_list(self) -> str:
        """Returns the scan list.
        Returns: The scan list as a string (e.g., '(@1,3,4,5,9)')."""
        response = self.instrument.query("ROUT:SCAN?").strip()
        # The response is described as an IEEE 488.2 definite length block.
        # Assuming direct return of the channel list string for simplicity.
        # Real implementation might need to parse the block header first.
        if response.startswith('#'):
            num_digits = int(response[1])
            length_str = response[2 : 2 + num_digits]
            data_length = int(length_str)
            channel_list_str = response[2 + num_digits:].strip()
            return channel_list_str
        return response

    def set_route_terminals(self, terminal_type: str):
        """Configures the terminal connections.
        Parameters:
        terminal_type: FRONT|REAR|BOTH|NONE"""
        valid_types = {"FRONT", "REAR", "BOTH", "NONE", "FRON", "REAR"}
        type_upper = terminal_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid terminal type: '{terminal_type}'. Must be 'FRONT', 'REAR', 'BOTH', or 'NONE'.")

        if type_upper == "FRONT": scpi_value = "FRON"
        elif type_upper == "REAR": scpi_value = "REAR"
        else: scpi_value = type_upper

        self.instrument.write(f"ROUT:TERM {scpi_value}")

    def get_route_terminals(self) -> str:
        """Returns the current terminal connection setting ('FRONT', 'REAR', 'BOTH', or 'NONE')."""
        response = self.instrument.query("ROUT:TERM?").strip().upper()
        if response.startswith("FRON"):
            return "FRONT"
        elif response.startswith("REAR"):
            return "REAR"
        return response
