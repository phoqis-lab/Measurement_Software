class Trace:
    """
    A class to encapsulate SCPI commands for instrument control related to TRACE | DATA.
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

    
    def get_trace_catalog(self) -> list[str]:
        """
        Queries and returns a comma-separated list of strings containing the names of all traces.
        If no traces are defined, a single empty string is returned.
        :return: A list of trace names (strings).
        """
        response = self.instrument.query("TRACE:CAT?").strip()
        if not response:
            return []
        # The document says "comma-separated list of strings".
        # Assuming the strings themselves might be quoted, and removing them.
        return [name.strip().strip('"') for name in response.split(',') if name.strip()]

    def trace_copy(self, destination_trace_name: str, source: str):
        """
        Sets the data values in the destination trace from internal data stores in the instrument.
        This command is an event (no query form).
        :param destination_trace_name: The name of the trace to copy data into.
        :param source: The source of the data, which can be an existing trace_name or a data_handle.
                       (e.g., "TRACE1" or "CALCulatel").
        """
        # <trace_name> is <CHARACTER PROGRAM DATA>
        # <data_handle> is also character data.
        # Ensure strings are properly quoted for SCPI.
        self.instrument.write(f"TRACE:COPY '{destination_trace_name}','{source}'")

    def set_trace_data(self, trace_name: str, data_source):
        """
        Sets the data values in the destination trace from information provided by the controller.
        The data_source can be:
        - A block of data (e.g., "#10123456789")
        - A DIF expression (string)
        - A single numeric_value (e.g., 0.22361) to set all elements to this constant.
        - A list of numeric_values to map into the trace.
        :param trace_name: The name of the trace to set data for.
        :param data_source: The data to set. Can be a string (for block/DIF) or a numeric value/list.
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"

        if isinstance(data_source, (int, float)):
            # Single numeric value
            self.instrument.write(f"TRACE:DATA {quoted_trace_name},{data_source}")
        elif isinstance(data_source, str):
            # Block data or DIF expression (assumed to be properly formatted by caller)
            # The document implies the block/DIF expression themselves are the parameter,
            # not a string containing the block/DIF expression that needs quoting.
            # Example: "TRACE:DATA REF,#10123456789" (no quotes around the block itself)
            # Or: "TRACE:DATA REF,DIF_EXPR" (no quotes around DIF_EXPR if it's treated as an identifier/keyword)
            # However, character data parameters for commands generally need quoting.
            # Let's assume for block/DIF expression, the input `data_source` string
            # is already in the correct format (e.g., "#10123456789" or "DIF_EXPRESSION_STRING")
            self.instrument.write(f"TRACE:DATA {quoted_trace_name},{data_source}")
        elif isinstance(data_source, (list, tuple)):
            # List of numeric values
            numeric_values_str = ",".join(map(str, data_source))
            self.instrument.write(f"TRACE:DATA {quoted_trace_name},({numeric_values_str})")
        else:
            raise ValueError(
                "Invalid data_source type. Must be numeric, string (block/DIF), or list of numerics."
            )

    def get_trace_data(self, trace_name: str) -> str:
        """
        Returns the data values for the specified trace, according to the format
        determined by commands in the FORMat subsystem.
        :param trace_name: The name of the trace to query data from.
        :return: The data values as a string (format depends on instrument and FORMAT subsystem).
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:DATA? {quoted_trace_name}").strip()
        return response

    def trace_data_line(
        self,
        trace_name: str,
        start_index: int,
        start_value: float,
        end_index: int,
        end_value: float,
    ):
        """
        Defines a line segment (a series of points) within the boundaries of the trace.
        This command is an event (no query form). The index of the first point in a trace is 1.
        :param trace_name: The name of the trace.
        :param start_index: The index of the starting point (numeric value).
        :param start_value: The value of the trace at the starting point (numeric value).
        :param end_index: The index of the ending point (numeric value).
        :param end_value: The value of the trace at the ending point (numeric value).
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        self.instrument.write(
            f"TRACE:DATA:LINE {quoted_trace_name},{start_index},{start_value},{end_index},{end_value}"
        )

    def get_trace_data_preamble(self, trace_name: str) -> str:
        """
        Returns the preamble information supporting the DATA(CURVE(VALues)) for the specified trace.
        It omits DIF blocks of waveform, measurement, and delta, and curve block keywords VALues and CSUM.
        :param trace_name: The name of the trace to query preamble from.
        :return: The preamble information as a string.
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:DATA:PRE? {quoted_trace_name}").strip()
        return response

    def set_trace_data_value(self, trace_name: str, index: int, value: float):
        """
        Sets the value of an individual point in a trace. The index of the first point in a trace is 1.
        :param trace_name: The name of the trace.
        :param index: The index of the addressed point (numeric value).
        :param value: The value to be set for the point (numeric value).
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        self.instrument.write(f"TRACE:DATA:VAL {quoted_trace_name},{index},{value}")

    def get_trace_data_value(self, trace_name: str, index: int) -> float:
        """
        Returns the data value of the trace at the specified indexed point.
        The index of the first point in a trace is 1.
        :param trace_name: The name of the trace.
        :param index: The index of the point to query (numeric value).
        :return: The data value of the point as a float.
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:DATA:VAL? {quoted_trace_name},{index}").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(
                f"Unexpected response for trace data value (not numeric): '{response}'"
            )

    def trace_define(self, trace_name: str, size_or_source=None):
        """
        Allocates and initializes a new trace.
        :param trace_name: The name of the new trace (string).
        :param size_or_source: Optional. Can be:
                               - A numeric_value: A new trace is allocated with this number of data elements.
                                 The trace is initialized to instrument-specified default values.
                               - A trace_name (string): The new trace becomes a copy of this existing trace.
                               - None: The new trace has an instrument-specified default size and initial value.
        Notes: No query form for this command.
        """
        # <trace_name> is CHARACTER DATA, needs quoting
        quoted_trace_name = f"'{trace_name}'"

        if size_or_source is None:
            self.instrument.write(f"TRACE:DEF {quoted_trace_name}")
        elif isinstance(size_or_source, (int, float)):
            self.instrument.write(f"TRACE:DEF {quoted_trace_name},{size_or_source}")
        elif isinstance(size_or_source, str):
            # Source is another trace name
            quoted_source_name = f"'{size_or_source}'"
            self.instrument.write(f"TRACE:DEF {quoted_trace_name},{quoted_source_name}")
        else:
            raise ValueError(
                "Invalid size_or_source. Must be numeric, a trace name string, or None."
            )

    def trace_delete_name(self, trace_name: str):
        """
        Dissociates a user-created trace_name from its trace memory.
        If the instrument supports dynamic trace memory allocation, the memory is freed.
        This command is an event (no query form). The NAME node is optional.
        :param trace_name: The name of the trace to delete.
        """
        # <trace_name> is character program data, needs quoting
        quoted_trace_name = f"'{trace_name}'"
        self.instrument.write(f"TRACE:DEL:NAME {quoted_trace_name}")

    def trace_delete_all(self):
        """
        Dissociates all user-created trace_names from their trace memory units.
        If the instrument supports dynamic trace memory allocation, all memory allocated
        for user-created traces is freed. This command is an event (no query form).
        """
        self.instrument.write("TRACE:DEL:ALL")

    def set_trace_feed(self, trace_name: str, data_handle: str):
        """
        Sets which data flow is fed into the specified TRACE DATA memory.
        :param trace_name: The name of the TRACE DATA memory.
        :param data_handle: The name of a point in the data flow (string), or None to stop feeding data.
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        if data_handle is None:
            self.instrument.write(f"TRACE:FEED {quoted_trace_name},NONE")
        else:
            # <data_handle> is also character data, needs quoting.
            quoted_data_handle = f"'{data_handle}'"
            self.instrument.write(f"TRACE:FEED {quoted_trace_name},{quoted_data_handle}")

    def get_trace_feed(self, trace_name: str) -> str:
        """
        Returns which data flow is fed into the specified TRACE DATA memory.
        :param trace_name: The name of the TRACE DATA memory.
        :return: The data_handle string, or an empty string ("") if no feed is selected.
        :raises ValueError: If the trace_name does not exist (-224 "Illegal parameter value").
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:FEED? {quoted_trace_name}").strip().strip("'")
        return response

    def set_trace_feed_control(self, trace_name: str, control_mode: str):
        """
        Sets how often the specified TRACE | DATA area accepts new data.
        This control has no effect if the FEED <data_handle> is set to null ("").
        :param trace_name: The name of the TRACE | DATA area.
        :param control_mode: ALWays|OCONdition|NEXT|NEVer
        """
        valid_modes = {"ALW", "ALWAY", "ALWAYS", "OCON", "OCOND", "OCONDITION", "NEXT", "NEV", "NEVER"}
        mode_upper = control_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid control_mode: '{control_mode}'. Must be ALWays, OCONdition, NEXT, or NEVer.")

        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"

        if mode_upper.startswith("ALW"): scpi_mode = "ALW"
        elif mode_upper.startswith("OCON"): scpi_mode = "OCON"
        elif mode_upper.startswith("NEXT"): scpi_mode = "NEXT"
        elif mode_upper.startswith("NEV"): scpi_mode = "NEV"
        else: scpi_mode = mode_upper # Fallback for exact match of short or long form

        self.instrument.write(f"TRACE:FEED:CONT {quoted_trace_name},{scpi_mode}")

    def get_trace_feed_control(self, trace_name: str) -> str:
        """
        Returns how often the specified TRACE | DATA area accepts new data.
        :param trace_name: The name of the TRACE | DATA area.
        :return: The control mode string (e.g., "ALWays", "OCONdition", "NEXT", "NEVer").
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:FEED:CONT? {quoted_trace_name}").strip().upper()
        if response.startswith("ALW"): return "ALWays"
        elif response.startswith("OCON"): return "OCONdition"
        elif response.startswith("NEXT"): return "NEXT"
        elif response.startswith("NEV"): return "NEVer"
        return response

    def set_trace_feed_ocondition(self, trace_name: str, condition_expr: str):
        """
        Sets the condition used to gate data flow into the specified TRACE | DATA area.
        :param trace_name: The name of the TRACE | DATA area.
        :param condition_expr: EXPRESSION PROGRAM DATA defining the condition.
                               e.g., "'(<operand_str> <equiv_op> <operand_str>')'" or "'(<event_handle>)'"
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        # <condition_expr> is expression program data, usually provided as a string that might need quoting.
        # The document shows it as quoted string literal.
        self.instrument.write(f"TRACE:FEED:OCON {quoted_trace_name},'{condition_expr}'")

    def get_trace_free(self) -> tuple[int, int]:
        """
        Returns the amount of user memory space available for traces and bytes in use.
        :return: A tuple (bytes_available, bytes_in_use).
        """
        response = self.instrument.query("TRACE:FREE?").strip()
        try:
            parts = [int(p) for p in response.split(',')]
            if len(parts) == 2:
                return (parts[0], parts[1])
            else:
                raise ValueError("Unexpected response format for TRACE:FREE? (not two integers).")
        except ValueError:
            raise ValueError(f"Failed to parse TRACE:FREE? response: '{response}'")

    def set_trace_points(self, trace_name: str, num_points: int = None):
        """
        Sets the number of measurement data points available in the specified trace memory.
        :param trace_name: The name of the trace to resize.
        :param num_points: Optional. The number of data points to accommodate. If omitted,
                           an instrument-specific default value will be used.
                           If more than one numeric value per point (e.g., real/imaginary pairs),
                           this specifies the number of N-tuples.
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        if num_points is None:
            self.instrument.write(f"TRACE:POIN {quoted_trace_name}")
        else:
            self.instrument.write(f"TRACE:POIN {quoted_trace_name},{num_points}")

    def get_trace_points(self, trace_name: str) -> int:
        """
        Returns the number of measurement data points in the specified trace.
        :param trace_name: The name of the trace.
        :return: The number of data points as an integer.
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"
        response = self.instrument.query(f"TRACE:POIN? {quoted_trace_name}").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for trace POINts (not integer): '{response}'")

    def trace_points_auto(self, trace_name: str, auto_state):
        """
        Turns trace autosizing ON/OFF. When enabled, the trace will automatically resize
        as necessary to accommodate new data.
        :param trace_name: The name of the trace.
        :param auto_state: Boolean (True/False) or string ("ON", "OFF", "ONCE").
                           "ONCE" causes sizing to occur once on the next measurement, then reverts to OFF.
        Notes: This command is an event (no query form).
        """
        # <trace_name> is character data, needs quoting.
        quoted_trace_name = f"'{trace_name}'"

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

        self.instrument.write(f"TRACE:POIN:AUTO {quoted_trace_name},{scpi_value}")
