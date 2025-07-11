"""For commands that give status reporting"""
class Status:
    """
    A class to encapsulate SCPI commands for instrument control.
    Assumes 'self.instrument' is an object with 'write' and 'query' methods
    that handle communication with the physical instrument.
    """
    def __init__(self,instrument):

        self.instrument = instrument

    # --- Functions for general STATUS commands (Applicable to OPERation, QUEStionable, etc.) ---
    # These functions are designed to be generic and can be called with a specific register path.

    def _get_status_condition(self, register_path: str) -> int:
        """
        Returns the contents of the condition register for the specified status structure.
        Reading the condition register is nondestructive.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :return: The integer value of the condition register (range: 0 through 32767).
        """
        response = self.instrument.query(f"STAT:{register_path}:COND?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {register_path} condition register (not integer): '{response}'")

    def _set_status_enable(self, register_path: str, value: int):
        """
        Sets the enable mask which allows true conditions in the event register to be
        reported in the summary bit for the specified status structure.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :param value: The integer value of the enable mask (range: 0 through 65535).
        """
        if not (0 <= value <= 65535):
            raise ValueError("Enable mask value must be between 0 and 65535.")
        self.instrument.write(f"STAT:{register_path}:ENAB {value}")

    def _get_status_enable(self, register_path: str) -> int:
        """
        Returns the contents of the enable mask for the specified status structure.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :return: The integer value of the enable mask (range: 0 through 32767).
        """
        response = self.instrument.query(f"STAT:{register_path}:ENAB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {register_path} enable register (not integer): '{response}'")

    def _get_status_event(self, register_path: str) -> int:
        """
        Returns the contents of the event register for the specified status structure.
        Reading the event register clears it.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :return: The integer value of the event register (range: 0 through 32767).
        """
        response = self.instrument.query(f"STAT:{register_path}:EVEN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {register_path} event register (not integer): '{response}'")

    def _set_status_map(self, register_path: str, bit_location: int, event_number: int):
        """
        Maps an error from the list of possible events the instrument can generate into a specified bit
        in the register.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :param bit_location: The specified bit location in the register (numeric value).
        :param event_number: The event number to map (numeric value).
        """
        self.instrument.write(f"STAT:{register_path}:MAP {bit_location},{event_number}")

    def _set_status_ntransition(self, register_path: str, value: int):
        """
        Sets the negative transition filter for the specified status structure.
        Setting a bit causes a 1->0 transition in the condition register to set a 1 in the event register.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :param value: The integer value of the negative transition filter (range: 0 through 65535).
        """
        if not (0 <= value <= 65535):
            raise ValueError("Negative transition filter value must be between 0 and 65535.")
        self.instrument.write(f"STAT:{register_path}:NTR {value}")

    def _get_status_ntransition(self, register_path: str) -> int:
        """
        Returns the contents of the negative transition filter for the specified status structure.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :return: The integer value of the negative transition filter (range: 0 through 32767).
        """
        response = self.instrument.query(f"STAT:{register_path}:NTR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {register_path} NTRansition register (not integer): '{response}'")

    def _set_status_ptransition(self, register_path: str, value: int):
        """
        Sets the positive transition filter for the specified status structure.
        Setting a bit causes a 0->1 transition in the condition register to set a 1 in the event register.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :param value: The integer value of the positive transition filter (range: 0 through 65535).
        """
        if not (0 <= value <= 65535):
            raise ValueError("Positive transition filter value must be between 0 and 65535.")
        self.instrument.write(f"STAT:{register_path}:PTR {value}")

    def _get_status_ptransition(self, register_path: str) -> int:
        """
        Returns the contents of the positive transition filter for the specified status structure.
        :param register_path: The SCPI path to the status register (e.g., "OPERation", "QUEStionable").
        :return: The integer value of the positive transition filter (range: 0 through 32767).
        """
        response = self.instrument.query(f"STAT:{register_path}:PTR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {register_path} PTRansition register (not integer): '{response}'")

    # --- STATUS:OPERation Subsystem (Page 1) ---

    def set_status_operation_bit_n(self, bit_n: int, value: int):
        """
        Accesses the user-definable bits in the OPERation register set.
        :param bit_n: The bit number (n) restricted from 8 to 12.
        :param value: The numeric value (0 or 1) to set the bit.
        """
        if not (8 <= bit_n <= 12):
            raise ValueError("Bit number for OPERation must be between 8 and 12.")
        self.instrument.write(f"STAT:OPER:BIT{bit_n} {value}")

    def get_status_operation_bit_n(self, bit_n: int) -> int:
        """
        Queries the user-definable bits in the OPERation register set.
        :param bit_n: The bit number (n) restricted from 8 to 12.
        :return: The numeric value (0 or 1) of the bit.
        """
        if not (8 <= bit_n <= 12):
            raise ValueError("Bit number for OPERation must be between 8 and 12.")
        response = self.instrument.query(f"STAT:OPER:BIT{bit_n}?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for OPERation BIT{bit_n} (not integer): '{response}'")

    def get_status_operation_condition(self) -> int:
        """
        Returns the contents of the OPERation condition register.
        Notes: Query only. See Section 20.1.2 for details.
        """
        return self._get_status_condition(":STAT:OPER")



    def get_status_operation_event(self) -> int:
        """
        Returns the contents of the OPERation event register. Reading clears it.
        Notes: Query only. See Section 20.1.4 for details.
        """
        return self._get_status_event(":STAT:OPER")

    def set_status_operation_map(self, bit_location: int, event_number: int):
        """
        Maps an error event into a specified bit in the OPERation register.
        :param bit_location: The specified bit location in the OPERation register.
        :param event_number: The event number to map.
        Notes: See Section 20.1.5 for details.
        """
        self._set_status_map(":STAT:OPER", bit_location, event_number)

    def set_status_operation_ntransition(self, value: int):
        """
        Sets the negative transition filter for the OPERation register.
        :param value: The integer value (range: 0 through 65535).
        Notes: See Section 20.1.6 for details.
        """
        self._set_status_ntransition(":STAT:OPER", value)

    def get_status_operation_ntransition(self) -> int:
        """
        Returns the contents of the negative transition filter for the OPERation register.
        Notes: See Section 20.1.6 for details.
        """
        return self._get_status_ntransition(":STAT:OPER")

    def set_status_operation_ptransition(self, value: int):
        """
        Sets the positive transition filter for the OPERation register.
        :param value: The integer value (range: 0 through 65535).
        Notes: See Section 20.1.7 for details.
        """
        self._set_status_ptransition(":STAT:OPER", value)

    def get_status_operation_ptransition(self) -> int:
        """
        Returns the contents of the positive transition filter for the OPERation register.
        Notes: See Section 20.1.7 for details.
        """
        return self._get_status_ptransition(":STAT:OPER")

    # --- STATUS:PRESet (Page 4) ---

    def status_preset(self):
        """
        Configures the SCPI and device-dependent status data structures such that
        device-dependent events are reported at a higher level through the
        mandatory part of the status-reporting mechanism.
        Notes: This command is an event and has no query form. See Section 20.2 for details.
        """
        self.instrument.write(":STAT:PRES")

    # --- STATUS:QUEStionable Subsystem (Page 7) ---

    def set_status_questionable_bit_n(self, bit_n: int, value: int):
        """
        Accesses the user-definable bits in the QUEStionable register set.
        :param bit_n: The bit number (n) restricted from 9 to 12.
        :param value: The numeric value (0 or 1) to set the bit.
        """
        if not (9 <= bit_n <= 12):
            raise ValueError("Bit number for QUEStionable must be between 9 and 12.")
        self.instrument.write(f"STAT:QUES:BIT{bit_n} {value}")

    def get_status_questionable_bit_n(self, bit_n: int) -> int:
        """
        Queries the user-definable bits in the QUEStionable register set.
        :param bit_n: The bit number (n) restricted from 9 to 12.
        :return: The numeric value (0 or 1) of the bit.
        """
        if not (9 <= bit_n <= 12):
            raise ValueError("Bit number for QUEStionable must be between 9 and 12.")
        response = self.instrument.query(f"STAT:QUES:BIT{bit_n}?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for QUEStionable BIT{bit_n} (not integer): '{response}'")

    def get_status_questionable_condition(self) -> int:
        """
        Returns the contents of the QUEStionable condition register.
        Notes: Query only. Defined the same as STATus:OPERation:CONDition.
        """
        return self._get_status_condition("QUES")

    def set_status_questionable_enable(self, value: int):
        """
        Sets the enable mask for the QUEStionable register.
        :param value: The integer value of the enable mask (range: 0 through 65535).
        Notes: Defined the same as STATUS:OPERation:ENABle.
        """
        self._set_status_enable("QUES", value)

    def get_status_questionable_enable(self) -> int:
        """
        Returns the contents of the enable mask for the QUEStionable register.
        Notes: Defined the same as STATUS:OPERation:ENABle.
        """
        return self._get_status_enable("QUES")

    def get_status_questionable_event(self) -> int:
        """
        Returns the contents of the QUEStionable event register. Reading clears it.
        Notes: Query only. Defined the same as STATus:OPERation:EVENt.
        """
        return self._get_status_event("QUES")

    def set_status_questionable_map(self, bit_location: int, event_number: int):
        """
        Maps an error event into a specified bit in the QUEStionable register.
        :param bit_location: The specified bit location in the QUEStionable register.
        :param event_number: The event number to map.
        Notes: Defined the same as STATUS:OPERation:MAP.
        """
        self._set_status_map("QUES", bit_location, event_number)

    def set_status_questionable_ntransition(self, value: int):
        """
        Sets the negative transition filter for the QUEStionable register.
        :param value: The integer value (range: 0 through 65535).
        Notes: Defined the same as STATus:OPERation:NTRansition.
        """
        self._set_status_ntransition("QUES", value)

    def get_status_questionable_ntransition(self) -> int:
        """
        Returns the contents of the negative transition filter for the QUEStionable register.
        Notes: Defined the same as STATus:OPERation:NTRansition.
        """
        return self._get_status_ntransition("QUES")

    def set_status_questionable_ptransition(self, value: int):
        """
        Sets the positive transition filter for the QUEStionable register.
        :param value: The integer value (range: 0 through 65535).
        Notes: Defined the same as STATus:OPERation:PTRansition.
        """
        self._set_status_ptransition("QUES", value)

    def get_status_questionable_ptransition(self) -> int:
        """
        Returns the contents of the positive transition filter for the QUEStionable register.
        Notes: Defined the same as STATus:OPERation:PTRansition.
        """
        return self._get_status_ptransition("QUES")

    # --- Additional specific status registers mentioned in the PARAMETER FORM tables ---
    # These typically reuse the generic _get_status_condition, _set_status_enable, etc.

    def get_status_instrument_condition(self) -> int:
        """
        Returns the contents of the INSTrument condition register.
        Notes: Query only.
        """
        return self._get_status_condition("INST")

    def set_status_instrument_enable(self, value: int):
        """
        Sets the enable mask for the INSTrument register.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_enable("INST", value)

    def get_status_instrument_enable(self) -> int:
        """
        Returns the contents of the enable mask for the INSTrument register.
        """
        return self._get_status_enable("INST")

    def get_status_instrument_event(self) -> int:
        """
        Returns the contents of the INSTrument event register. Reading clears it.
        Notes: Query only.
        """
        return self._get_status_event("INST")

    def set_status_instrument_ntransition(self, value: int):
        """
        Sets the negative transition filter for the INSTrument register.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_ntransition("INST", value)

    def get_status_instrument_ntransition(self) -> int:
        """
        Returns the contents of the negative transition filter for the INSTrument register.
        """
        return self._get_status_ntransition("INST")

    def set_status_instrument_ptransition(self, value: int):
        """
        Sets the positive transition filter for the INSTrument register.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_ptransition("INST", value)

    def get_status_instrument_ptransition(self) -> int:
        """
        Returns the contents of the positive transition filter for the INSTrument register.
        """
        return self._get_status_ptransition("INST")

    # ISUMmary<n>
    def get_status_isummary_condition(self, n: int) -> int:
        """
        Returns the contents of the ISUMmary<n> condition register.
        :param n: The summary number.
        Notes: Query only.
        """
        return self._get_status_condition(f"ISUM{n}")

    def set_status_isummary_enable(self, n: int, value: int):
        """
        Sets the enable mask for the ISUMmary<n> register.
        :param n: The summary number.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_enable(f"ISUM{n}", value)

    def get_status_isummary_enable(self, n: int) -> int:
        """
        Returns the contents of the enable mask for the ISUMmary<n> register.
        :param n: The summary number.
        """
        return self._get_status_enable(f"ISUM{n}")

    def get_status_isummary_event(self, n: int) -> int:
        """
        Returns the contents of the ISUMmary<n> event register. Reading clears it.
        :param n: The summary number.
        Notes: Query only.
        """
        return self._get_status_event(f"ISUM{n}")

    def set_status_isummary_ntransition(self, n: int, value: int):
        """
        Sets the negative transition filter for the ISUMmary<n> register.
        :param n: The summary number.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_ntransition(f"ISUM{n}", value)

    def get_status_isummary_ntransition(self, n: int) -> int:
        """
        Returns the contents of the negative transition filter for the ISUMmary<n> register.
        :param n: The summary number.
        """
        return self._get_status_ntransition(f"ISUM{n}")

    def set_status_isummary_ptransition(self, n: int, value: int):
        """
        Sets the positive transition filter for the ISUMmary<n> register.
        :param n: The summary number.
        :param value: The integer value (range: 0 through 65535).
        """
        self._set_status_ptransition(f"ISUM{n}", value)

    def get_status_isummary_ptransition(self, n: int) -> int:
        """
        Returns the contents of the positive transition filter for the ISUMmary<n> register.
        :param n: The summary number.
        """
        return self._get_status_ptransition(f"ISUM{n}")

    # Specific status registers listed with individual commands at the end of the PARAMETER FORM table
    def get_status_voltage_condition(self) -> int:
        """Returns the condition register for Voltage status."""
        return self._get_status_condition("VOLT")

    def set_status_voltage_enable(self, value: int):
        """Sets the enable mask for Voltage status."""
        self._set_status_enable("VOLT", value)

    def get_status_voltage_enable(self) -> int:
        """Returns the enable mask for Voltage status."""
        return self._get_status_enable("VOLT")

    def get_status_voltage_event(self) -> int:
        """Returns the event register for Voltage status. Reading clears it."""
        return self._get_status_event("VOLT")

    def set_status_voltage_ntransition(self, value: int):
        """Sets the negative transition filter for Voltage status."""
        self._set_status_ntransition("VOLT", value)

    def get_status_voltage_ntransition(self) -> int:
        """Returns the negative transition filter for Voltage status."""
        return self._get_status_ntransition("VOLT")

    def set_status_voltage_ptransition(self, value: int):
        """Sets the positive transition filter for Voltage status."""
        self._set_status_ptransition("VOLT", value)

    def get_status_voltage_ptransition(self) -> int:
        """Returns the positive transition filter for Voltage status."""
        return self._get_status_ptransition("VOLT")

    def get_status_current_condition(self) -> int:
        """Returns the condition register for Current status."""
        return self._get_status_condition("CURR")

    def set_status_current_enable(self, value: int):
        """Sets the enable mask for Current status."""
        self._set_status_enable("CURR", value)

    def get_status_current_enable(self) -> int:
        """Returns the enable mask for Current status."""
        return self._get_status_enable("CURR")

    def get_status_current_event(self) -> int:
        """Returns the event register for Current status. Reading clears it."""
        return self._get_status_event("CURR")

    def set_status_current_ntransition(self, value: int):
        """Sets the negative transition filter for Current status."""
        self._set_status_ntransition("CURR", value)

    def get_status_current_ntransition(self) -> int:
        """Returns the negative transition filter for Current status."""
        return self._get_status_ntransition("CURR")

    def set_status_current_ptransition(self, value: int):
        """Sets the positive transition filter for Current status."""
        self._set_status_ptransition("CURR", value)

    def get_status_current_ptransition(self) -> int:
        """Returns the positive transition filter for Current status."""
        return self._get_status_ptransition("CURR")

    def get_status_time_condition(self) -> int:
        """Returns the condition register for Time status."""
        return self._get_status_condition("TIM")

    def set_status_time_enable(self, value: int):
        """Sets the enable mask for Time status."""
        self._set_status_enable("TIM", value)

    def get_status_time_enable(self) -> int:
        """Returns the enable mask for Time status."""
        return self._get_status_enable("TIM")

    def get_status_time_event(self) -> int:
        """Returns the event register for Time status. Reading clears it."""
        return self._get_status_event("TIM")

    def set_status_time_ntransition(self, value: int):
        """Sets the negative transition filter for Time status."""
        self._set_status_ntransition("TIM", value)

    def get_status_time_ntransition(self) -> int:
        """Returns the negative transition filter for Time status."""
        return self._get_status_ntransition("TIM")

    def set_status_time_ptransition(self, value: int):
        """Sets the positive transition filter for Time status."""
        self._set_status_ptransition("TIM", value)

    def get_status_time_ptransition(self) -> int:
        """Returns the positive transition filter for Time status."""
        return self._get_status_ptransition("TIM")

    def get_status_power_condition(self) -> int:
        """Returns the condition register for Power status."""
        return self._get_status_condition("POW")

    def set_status_power_enable(self, value: int):
        """Sets the enable mask for Power status."""
        self._set_status_enable("POW", value)

    def get_status_power_enable(self) -> int:
        """Returns the enable mask for Power status."""
        return self._get_status_enable("POW")

    def get_status_power_event(self) -> int:
        """Returns the event register for Power status. Reading clears it."""
        return self._get_status_event("POW")

    def set_status_power_ntransition(self, value: int):
        """Sets the negative transition filter for Power status."""
        self._set_status_ntransition("POW", value)

    def get_status_power_ntransition(self) -> int:
        """Returns the negative transition filter for Power status."""
        return self._get_status_ntransition("POW")

    def set_status_power_ptransition(self, value: int):
        """Sets the positive transition filter for Power status."""
        self._set_status_ptransition("POW", value)

    def get_status_power_ptransition(self) -> int:
        """Returns the positive transition filter for Power status."""
        return self._get_status_ptransition("POW")

    def get_status_temperature_condition(self) -> int:
        """Returns the condition register for Temperature status."""
        return self._get_status_condition("TEMP")

    def set_status_temperature_enable(self, value: int):
        """Sets the enable mask for Temperature status."""
        self._set_status_enable("TEMP", value)

    def get_status_temperature_enable(self) -> int:
        """Returns the enable mask for Temperature status."""
        return self._get_status_enable("TEMP")

    def get_status_temperature_event(self) -> int:
        """Returns the event register for Temperature status. Reading clears it."""
        return self._get_status_event("TEMP")

    def set_status_temperature_ntransition(self, value: int):
        """Sets the negative transition filter for Temperature status."""
        self._set_status_ntransition("TEMP", value)

    def get_status_temperature_ntransition(self) -> int:
        """Returns the negative transition filter for Temperature status."""
        return self._get_status_ntransition("TEMP")

    def set_status_temperature_ptransition(self, value: int):
        """Sets the positive transition filter for Temperature status."""
        self._set_status_ptransition("TEMP", value)

    def get_status_temperature_ptransition(self) -> int:
        """Returns the positive transition filter for Temperature status."""
        return self._get_status_ptransition("TEMP")

    def get_status_frequency_condition(self) -> int:
        """Returns the condition register for Frequency status."""
        return self._get_status_condition("FREQ")

    def set_status_frequency_enable(self, value: int):
        """Sets the enable mask for Frequency status."""
        self._set_status_enable("FREQ", value)

    def get_status_frequency_enable(self) -> int:
        """Returns the enable mask for Frequency status."""
        return self._get_status_enable("FREQ")

    def get_status_frequency_event(self) -> int:
        """Returns the event register for Frequency status. Reading clears it."""
        return self._get_status_event("FREQ")

    def set_status_frequency_ntransition(self, value: int):
        """Sets the negative transition filter for Frequency status."""
        self._set_status_ntransition("FREQ", value)

    def get_status_frequency_ntransition(self) -> int:
        """Returns the negative transition filter for Frequency status."""
        return self._get_status_ntransition("FREQ")

    def set_status_frequency_ptransition(self, value: int):
        """Sets the positive transition filter for Frequency status."""
        self._set_status_ptransition("FREQ", value)

    def get_status_frequency_ptransition(self) -> int:
        """Returns the positive transition filter for Frequency status."""
        return self._get_status_ptransition("FREQ")

    def get_status_phase_condition(self) -> int:
        """Returns the condition register for Phase status."""
        return self._get_status_condition("PHAS")

    def set_status_phase_enable(self, value: int):
        """Sets the enable mask for Phase status."""
        self._set_status_enable("PHAS", value)

    def get_status_phase_enable(self) -> int:
        """Returns the enable mask for Phase status."""
        return self._get_status_enable("PHAS")

    def get_status_phase_event(self) -> int:
        """Returns the event register for Phase status. Reading clears it."""
        return self._get_status_event("PHAS")

    def set_status_phase_ntransition(self, value: int):
        """Sets the negative transition filter for Phase status."""
        self._set_status_ntransition("PHAS", value)

    def get_status_phase_ntransition(self) -> int:
        """Returns the negative transition filter for Phase status."""
        return self._get_status_ntransition("PHAS")

    def set_status_phase_ptransition(self, value: int):
        """Sets the positive transition filter for Phase status."""
        self._set_status_ptransition("PHAS", value)

    def get_status_phase_ptransition(self) -> int:
        """Returns the positive transition filter for Phase status."""
        return self._get_status_ptransition("PHAS")

    def get_status_modulation_condition(self) -> int:
        """Returns the condition register for Modulation status."""
        return self._get_status_condition("MOD")

    def set_status_modulation_enable(self, value: int):
        """Sets the enable mask for Modulation status."""
        self._set_status_enable("MOD", value)

    def get_status_modulation_enable(self) -> int:
        """Returns the enable mask for Modulation status."""
        return self._get_status_enable("MOD")

    def get_status_modulation_event(self) -> int:
        """Returns the event register for Modulation status. Reading clears it."""
        return self._get_status_event("MOD")

    def set_status_modulation_ntransition(self, value: int):
        """Sets the negative transition filter for Modulation status."""
        self._set_status_ntransition("MOD", value)

    def get_status_modulation_ntransition(self) -> int:
        """Returns the negative transition filter for Modulation status."""
        return self._get_status_ntransition("MOD")

    def set_status_modulation_ptransition(self, value: int):
        """Sets the positive transition filter for Modulation status."""
        self._set_status_ptransition("MOD", value)

    def get_status_modulation_ptransition(self) -> int:
        """Returns the positive transition filter for Modulation status."""
        return self._get_status_ptransition("MOD")

    def get_status_calibration_condition(self) -> int:
        """Returns the condition register for CALibration status."""
        return self._get_status_condition("CAL")

    def set_status_calibration_enable(self, value: int):
        """Sets the enable mask for CALibration status."""
        self._set_status_enable("CAL", value)

    def get_status_calibration_enable(self) -> int:
        """Returns the enable mask for CALibration status."""
        return self._get_status_enable("CAL")

    def get_status_calibration_event(self) -> int:
        """Returns the event register for CALibration status. Reading clears it."""
        return self._get_status_event("CAL")

    def set_status_calibration_ntransition(self, value: int):
        """Sets the negative transition filter for CALibration status."""
        self._set_status_ntransition("CAL", value)

    def get_status_calibration_ntransition(self) -> int:
        """Returns the negative transition filter for CALibration status."""
        return self._get_status_ntransition("CAL")

    def set_status_calibration_ptransition(self, value: int):
        """Sets the positive transition filter for CALibration status."""
        self._set_status_ptransition("CAL", value)

    def get_status_calibration_ptransition(self) -> int:
        """Returns the positive transition filter for CALibration status."""
        return self._get_status_ptransition("CAL")
