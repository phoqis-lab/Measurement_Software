class Unit:
    """
    
    """
    def __init__(self, instrument):
        """
        
        """
        self.instrument = instrument

    
    def set_unit_angle(self, unit_type: str):
        """
        Specifies the fundamental unit of angle.
        :param unit_type: "DEG" (degrees) or "RAD" (radians).
        Notes: At *RST, the default unit is RAD.
        """
        valid_types = {"DEG", "RAD"}
        type_upper = unit_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid angle unit: '{unit_type}'. Must be 'DEG' or 'RAD'.")
        self.instrument.write(f"UNIT:ANG {type_upper}")

    def get_unit_angle(self) -> str:
        """
        Queries the fundamental unit of angle.
        :return: The angle unit ("DEG" or "RAD").
        """
        response = self.instrument.query("UNIT:ANG?").strip().upper()
        return response

    def set_unit_current(self, amplitude_unit: str):
        """
        Selects a default unit for commands which program absolute amplitude for current.
        :param amplitude_unit: The amplitude unit (e.g., "A", "DBA", "DBUW").
                                Refer to page 2 of the document for possible values.
        Notes: At *RST, this value is device-dependent.
        """
        # The document lists many possible values. Validation here would be extensive.
        # It's better to let the instrument itself validate the specific string.
        # However, a basic check for non-empty string is good.
        if not amplitude_unit:
            raise ValueError("Amplitude unit cannot be empty.")
        self.instrument.write(f"UNIT:CURR {amplitude_unit}")

    def get_unit_current(self) -> str:
        """
        Queries the default unit for commands which program absolute amplitude for current.
        :return: The amplitude unit string.
        """
        response = self.instrument.query("UNIT:CURR?").strip()
        return response

    def set_unit_power(self, amplitude_unit: str):
        """
        Selects a default unit for commands which program absolute amplitude for power.
        :param amplitude_unit: The amplitude unit (e.g., "W", "DBM").
                                Refer to page 2 of the document for possible values.
        Notes: At *RST, this value is device-dependent.
        """
        if not amplitude_unit:
            raise ValueError("Amplitude unit cannot be empty.")
        self.instrument.write(f"UNIT:POW {amplitude_unit}")

    def get_unit_power(self) -> str:
        """
        Queries the default unit for commands which program absolute amplitude for power.
        :return: The amplitude unit string.
        """
        response = self.instrument.query("UNIT:POW?").strip()
        return response

    
    def set_unit_temperature(self, unit_type: str):
        """
        Specifies the fundamental unit of temperature.
        :param unit_type: "C" (Celsius), "CEL" (Celsius), "F" (Fahrenheit),
                          "FAR" (Fahrenheit), or "K" (Kelvin).
        Notes: At *RST, this value is device-dependent.
               "CEL" and "FAR" are preferred forms for query return.
        """
        valid_types = {"C", "CEL", "F", "FAR", "K"}
        type_upper = unit_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid temperature unit: '{unit_type}'. Must be 'C', 'CEL', 'F', 'FAR', or 'K'.")

        if type_upper == "CEL": scpi_value = "CEL"
        elif type_upper == "FAR": scpi_value = "FAR"
        elif type_upper == "C": scpi_value = "C" # Explicitly keep C if that's the intention
        elif type_upper == "F": scpi_value = "F" # Explicitly keep F if that's the intention
        else: scpi_value = type_upper

        self.instrument.write(f"UNIT:TEMP {scpi_value}")

    def get_unit_temperature(self) -> str:
        """
        Queries the fundamental unit of temperature.
        :return: The temperature unit ("C", "CEL", "F", "FAR", or "K").
        """
        response = self.instrument.query("UNIT:TEMP?").strip().upper()
        return response

    def set_unit_time(self, unit_type: str):
        """
        Specifies the fundamental unit of time.
        :param unit_type: "HOUR", "MINute", or "SECond".
        Notes: At *RST, this value is SECond.
        """
        valid_types = {"HOUR", "MIN", "MINUTE", "SEC", "SECOND"}
        type_upper = unit_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid time unit: '{unit_type}'. Must be 'HOUR', 'MINute', or 'SECond'.")

        if type_upper.startswith("MIN"): scpi_value = "MIN"
        elif type_upper.startswith("SEC"): scpi_value = "SEC"
        else: scpi_value = type_upper

        self.instrument.write(f"UNIT:TIME {scpi_value}")

    def get_unit_time(self) -> str:
        """
        Queries the fundamental unit of time.
        :return: The time unit ("HOUR", "MINute", or "SECond").
        """
        response = self.instrument.query("UNIT:TIME?").strip().upper()
        if response.startswith("MIN"): return "MINute"
        if response.startswith("SEC"): return "SECond"
        return response

    def set_unit_voltage(self, amplitude_unit: str):
        """
        Selects a default unit for commands which program absolute amplitude for voltage.
        :param amplitude_unit: The amplitude unit (e.g., "V", "DBV", "DBUV").
                                Refer to page 2 of the document for possible values.
        Notes: At *RST, this value is device-dependent.
        """
        if not amplitude_unit:
            raise ValueError("Amplitude unit cannot be empty.")
        self.instrument.write(f"UNIT:VOLT {amplitude_unit}")

    def get_unit_voltage(self) -> str:
        """
        Queries the default unit for commands which program absolute amplitude for voltage.
        :return: The amplitude unit string.
        """
        response = self.instrument.query("UNIT:VOLT?").strip()
        return response
