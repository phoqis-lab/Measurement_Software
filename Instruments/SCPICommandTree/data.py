class Data:
    """
    A class to encapsulate SCPI commands for instrument control related to :DATA.
    Assumes 'self.instrument' is an object with 'write' and 'query' methods
    that handle communication with the physical instrument.
    """
    def __init__(self, instrument):
        """
        Initializes the InstrumentControl with an instrument connection.
        :param instrument_connection: An object capable of sending/receiving
                                      SCPI commands (e.g., pyvisa resource).
        """
        self.instrument = instrument

    
    def get_data_catalog(self) -> list[str]:
        """
        Queries and returns a comma-separated list of strings containing the names of all data areas.
        If no data areas are defined, a single empty string is returned.
        :return: A list of data area names (strings).
        """
        response = self.instrument.query(":DATA:CAT?").strip()
        if not response:
            return []
        # The document says "comma-separated list of strings".
        # Assuming the strings themselves might be quoted, and removing them.
        return [name.strip().strip('"') for name in response.split(',') if name.strip()]

    def data_copy(self, destination_data_name: str, source: str):
        """
        Sets the data values in the destination data area from internal data stores in the instrument.
        This command is an event (no query form).
        :param destination_data_name: The name of the data area to copy data into.
        :param source: The source of the data, which can be an existing data_name or a data_handle.
                       (e.g., ":DATA1" or "CALCulatel").
        """
        # <data_name> is <CHARACTER PROGRAM :DATA>
        # <data_handle> is also character data.
        # Ensure strings are properly quoted for SCPI.
        self.instrument.write(f":DATA:COPY '{destination_data_name}','{source}'")

    def set_data_data(self, data_name: str, data_source):
        """
        Sets the data values in the destination data area from information provided by the controller.
        The data_source can be:
        - A block of data (e.g., "#10123456789")
        - A DIF expression (string)
        - A single numeric_value (e.g., 0.22361) to set all elements to this constant.
        - A list of numeric_values to map into the data area.
        :param data_name: The name of the data area to set data for.
        :param data_source: The data to set. Can be a string (for block/DIF) or a numeric value/list.
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"

        if isinstance(data_source, (int, float)):
            # Single numeric value
            self.instrument.write(f":DATA::DATA {quoted_data_name},{data_source}")
        elif isinstance(data_source, str):
            # Block data or DIF expression (assumed to be properly formatted by caller)
            self.instrument.write(f":DATA::DATA {quoted_data_name},{data_source}")
        elif isinstance(data_source, (list, tuple)):
            # List of numeric values
            numeric_values_str = ",".join(map(str, data_source))
            self.instrument.write(f":DATA::DATA {quoted_data_name},({numeric_values_str})")
        else:
            raise ValueError(
                "Invalid data_source type. Must be numeric, string (block/DIF), or list of numerics."
            )

    def get_data_data(self, data_name: str) -> str:
        """
        Returns the data values for the specified data area, according to the format
        determined by commands in the FORMat subsystem.
        :param data_name: The name of the data area to query data from.
        :return: The data values as a string (format depends on instrument and FORMAT subsystem).
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA::DATA? {quoted_data_name}").strip()
        return response

    def data_data_line(
        self,
        data_name: str,
        start_index: int,
        start_value: float,
        end_index: int,
        end_value: float,
    ):
        """
        Defines a line segment (a series of points) within the boundaries of the data area.
        This command is an event (no query form). The index of the first point in a data area is 1.
        :param data_name: The name of the data area.
        :param start_index: The index of the starting point (numeric value).
        :param start_value: The value of the data area at the starting point (numeric value).
        :param end_index: The index of the ending point (numeric value).
        :param end_value: The value of the data area at the ending point (numeric value).
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        self.instrument.write(
            f":DATA::DATA:LINE {quoted_data_name},{start_index},{start_value},{end_index},{end_value}"
        )

    def get_data_data_preamble(self, data_name: str) -> str:
        """
        Returns the preamble information supporting the :DATA(CURVE(VALues)) for the specified data area.
        It omits DIF blocks of waveform, measurement, and delta, and curve block keywords VALues and CSUM.
        :param data_name: The name of the data area to query preamble from.
        :return: The preamble information as a string.
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA::DATA:PRE? {quoted_data_name}").strip()
        return response

    def set_data_data_value(self, data_name: str, index: int, value: float):
        """
        Sets the value of an individual point in a data area. The index of the first point in a data area is 1.
        :param data_name: The name of the data area.
        :param index: The index of the addressed point (numeric value).
        :param value: The value to be set for the point (numeric value).
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        self.instrument.write(f":DATA::DATA:VAL {quoted_data_name},{index},{value}")

    def get_data_data_value(self, data_name: str, index: int) -> float:
        """
        Returns the data value of the data area at the specified indexed point.
        The index of the first point in a data area is 1.
        :param data_name: The name of the data area.
        :param index: The index of the point to query (numeric value).
        :return: The data value of the point as a float.
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA::DATA:VAL? {quoted_data_name},{index}").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(
                f"Unexpected response for data data value (not numeric): '{response}'"
            )

    def data_define(self, data_name: str, size_or_source=None):
        """
        Allocates and initializes a new data area.
        :param data_name: The name of the new data area (string).
        :param size_or_source: Optional. Can be:
                               - A numeric_value: A new data area is allocated with this number of data elements.
                                 The data area is initialized to instrument-specified default values.
                               - A data_name (string): The new data area becomes a copy of this existing data area.
                               - None: The new data area has an instrument-specified default size and initial value.
        Notes: No query form for this command.
        """
        # <data_name> is CHARACTER :DATA, needs quoting
        quoted_data_name = f"'{data_name}'"

        if size_or_source is None:
            self.instrument.write(f":DATA:DEF {quoted_data_name}")
        elif isinstance(size_or_source, (int, float)):
            self.instrument.write(f":DATA:DEF {quoted_data_name},{size_or_source}")
        elif isinstance(size_or_source, str):
            # Source is another data name
            quoted_source_name = f"'{size_or_source}'"
            self.instrument.write(f":DATA:DEF {quoted_data_name},{quoted_source_name}")
        else:
            raise ValueError(
                "Invalid size_or_source. Must be numeric, a data name string, or None."
            )

    def data_delete_name(self, data_name: str):
        """
        Dissociates a user-created data_name from its data memory.
        If the instrument supports dynamic data memory allocation, the memory is freed.
        This command is an event (no query form). The NAME node is optional.
        :param data_name: The name of the data area to delete.
        """
        # <data_name> is character program data, needs quoting
        quoted_data_name = f"'{data_name}'"
        self.instrument.write(f":DATA:DEL:NAME {quoted_data_name}")

    def data_delete_all(self):
        """
        Dissociates all user-created data_names from their data memory units.
        If the instrument supports dynamic data memory allocation, all memory allocated
        for user-created data areas is freed. This command is an event (no query form).
        """
        self.instrument.write(":DATA:DEL:ALL")

    def set_data_feed(self, data_name, data_handle):
        """
        Sets which data flow is fed into the specified :DATA memory.
        :param data_name: The name of the :DATA memory.
        :param data_handle: The name of a point in the data flow (string), or None to stop feeding data.
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        if data_handle is None:
            self.instrument.write(f":DATA:FEED {quoted_data_name},NONE")
        else:
            # <data_handle> is also character data, needs quoting.
            quoted_data_handle = f"'{data_handle}'"
            self.instrument.write(f":DATA:FEED {quoted_data_name},{quoted_data_handle}")

    def get_data_feed(self, data_name: str) -> str:
        """
        Returns which data flow is fed into the specified :DATA memory.
        :param data_name: The name of the :DATA memory.
        :return: The data_handle string, or an empty string ("") if no feed is selected.
        :raises ValueError: If the data_name does not exist (-224 "Illegal parameter value").
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA:FEED? {quoted_data_name}").strip().strip("'")
        return response

    def set_data_feed_control(self, data_name: str, control_mode: str):
        """
        Sets how often the specified :DATA area accepts new data.
        This control has no effect if the FEED <data_handle> is set to null ("").
        :param data_name: The name of the :DATA area.
        :param control_mode: ALWays|OCONdition|NEXT|NEVer
        """
        valid_modes = {"ALW", "ALWAY", "ALWAYS", "OCON", "OCOND", "OCONDITION", "NEXT", "NEV", "NEVER"}
        mode_upper = control_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid control_mode: '{control_mode}'. Must be ALWays, OCONdition, NEXT, or NEVer.")

        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"

        if mode_upper.startswith("ALW"): scpi_mode = "ALW"
        elif mode_upper.startswith("OCON"): scpi_mode = "OCON"
        elif mode_upper.startswith("NEXT"): scpi_mode = "NEXT"
        elif mode_upper.startswith("NEV"): scpi_mode = "NEV"
        else: scpi_mode = mode_upper # Fallback for exact match of short or long form

        self.instrument.write(f":DATA:FEED:CONT {quoted_data_name},{scpi_mode}")

    def get_data_feed_control(self, data_name: str) -> str:
        """
        Returns how often the specified :DATA area accepts new data.
        :param data_name: The name of the :DATA area.
        :return: The control mode string (e.g., "ALWays", "OCONdition", "NEXT", "NEVer").
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA:FEED:CONT? {quoted_data_name}").strip().upper()
        if response.startswith("ALW"): return "ALWays"
        elif response.startswith("OCON"): return "OCONdition"
        elif response.startswith("NEXT"): return "NEXT"
        elif response.startswith("NEV"): return "NEVer"
        return response

    def set_data_feed_ocondition(self, data_name: str, condition_expr: str):
        """
        Sets the condition used to gate data flow into the specified :DATA area.
        :param data_name: The name of the :DATA area.
        :param condition_expr: EXPRESSION PROGRAM :DATA defining the condition.
                               e.g., "'(<operand_str> <equiv_op> <operand_str>')'" or "'(<event_handle>)'"
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        # <condition_expr> is expression program data, usually provided as a string that might need quoting.
        # The document shows it as quoted string literal.
        self.instrument.write(f":DATA:FEED:OCON {quoted_data_name},'{condition_expr}'")

    def get_data_free(self) -> tuple[int, int]:
        """
        Returns the amount of user memory space available for data areas and bytes in use.
        :return: A tuple (bytes_available, bytes_in_use).
        """
        response = self.instrument.query(":DATA:FREE?").strip()
        try:
            parts = [int(p) for p in response.split(',')]
            if len(parts) == 2:
                return (parts[0], parts[1])
            else:
                raise ValueError("Unexpected response format for :DATA:FREE? (not two integers).")
        except ValueError:
            raise ValueError(f"Failed to parse :DATA:FREE? response: '{response}'")

    def set_data_points(self, data_name: str, num_points: int = None):
        """
        Sets the number of measurement data points available in the specified data memory.
        :param data_name: The name of the data area to resize.
        :param num_points: Optional. The number of data points to accommodate. If omitted,
                           an instrument-specific default value will be used.
                           If more than one numeric value per point (e.g., real/imaginary pairs),
                           this specifies the number of N-tuples.
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        if num_points is None:
            self.instrument.write(f":DATA:POIN {quoted_data_name}")
        else:
            self.instrument.write(f":DATA:POIN {quoted_data_name},{num_points}")

    def get_data_points(self, data_name: str) -> int:
        """
        Returns the number of measurement data points in the specified data area.
        :param data_name: The name of the data area.
        :return: The number of data points as an integer.
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"
        response = self.instrument.query(f":DATA:POIN? {quoted_data_name}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for data POINts (not integer): '{response}'")

    def data_points_auto(self, data_name: str, auto_state):
        """
        Turns data autosizing ON/OFF. When enabled, the data area will automatically resize
        as necessary to accommodate new data.
        :param data_name: The name of the data area.
        :param auto_state: Boolean (True/False) or string ("ON", "OFF", "ONCE").
                           "ONCE" causes sizing to occur once on the next measurement, then reverts to OFF.
        Notes: This command is an event (no query form).
        """
        # <data_name> is character data, needs quoting.
        quoted_data_name = f"'{data_name}'"

        if isinstance(auto_state, bool):
            scpi_value = 1 if auto_state else 0
        elif isinstance(auto_state, str):
            normalized_state = auto_state.upper()
            if normalized_state in {1, "ON"}:
                scpi_value = "ON"
            elif normalized_state in {0, "OFF"}:
                scpi_value = "OFF"
            elif normalized_state == "ONCE":
                scpi_value = "ONCE"
            else:
                raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be True/False, 'ON', 'OFF', or 'ONCE'.")
        else:
            raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be True/False, 'ON', 'OFF', or 'ONCE'.")

        self.instrument.write(f":DATA:POIN:AUTO {quoted_data_name},{scpi_value}")
