class Output():
    def __init__(self):
        self.instrument = None

    def set_output_attenuation(self, value: float):
        """Sets the output attenuation level.
        Parameters:
        value: The attenuation value (numeric value) in current relative amplitude units."""
        self.instrument.write(f"OUTP:ATT {value}")

    def get_output_attenuation(self) -> float:
        """Returns the output attenuation level."""
        response = self.instrument.query("OUTP:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output attenuation (not numeric): '{response}'")

    def set_output_coupling(self, coupling_type: str):
        """Controls whether the signal is AC or DC coupled to the output port.
        Parameters:
        coupling_type: AC|DC"""
        valid_types = {"AC", "DC"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC' or 'DC'.")
        self.instrument.write(f"OUTP:COUP {type_upper}")

    def get_output_coupling(self) -> str:
        """Returns whether the signal is AC or DC coupled to the output port."""
        response = self.instrument.query("OUTP:COUP?").strip().upper()
        return response

    def set_output_filter_auto(self, auto_state: str):
        """Allows the system to determine the best filter characteristic and cutoff frequency.
        Parameters:
        auto_state: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto filter state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"OUTP:FILT:AUTO {scpi_value}")

    def get_output_filter_auto(self) -> str:
        """Returns whether the system automatically determines the best filter characteristic ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query("OUTP:FILT:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()


    def set_output_filter_external_state(self, enable: bool):
        """Selects a user provided filter. When STATE is ON the filter is placed in the signal path.
        Parameters:
        enable: True to enable the external filter, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:FILT:EXT:STATE {scpi_value}")

    def get_output_filter_external_state(self) -> bool:
        """Returns True if the external filter is enabled, False if disabled."""
        response = self.instrument.query("OUTP:FILT:EXT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output filter external state: '{response}'")

    def set_output_filter_hpass_frequency(self, frequency: float):
        """Determines the cutoff frequency of the high pass filter.
        Parameters:
        frequency: The cutoff frequency (numeric value)."""
        self.instrument.write(f"OUTP:FILT:HPAS:FREQ {frequency}")

    def get_output_filter_hpass_frequency(self) -> float:
        """Returns the cutoff frequency of the high pass filter."""
        response = self.instrument.query("OUTP:FILT:HPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output filter high pass frequency (not numeric): '{response}'")

    def set_output_filter_hpass_state(self, enable: bool):
        """Turns the high pass filter ON and OFF.
        Parameters:
        enable: True to turn the filter ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:FILT:HPAS:STATE {scpi_value}")

    def get_output_filter_hpass_state(self) -> bool:
        """Returns True if the high pass filter is ON, False if OFF."""
        response = self.instrument.query("OUTP:FILT:HPAS:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output filter high pass state: '{response}'")

    def set_output_filter_hpass_type(self, filter_type: str):
        """Determines the characteristic of the high pass filter.
        Parameters:
        filter_type: BESSel|CHEByshev"""
        valid_types = {"BESSEL", "CHEBYSHEV", "BESS", "CHEB"}
        type_upper = filter_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be 'BESSEL' or 'CHEBYSHEV'.")

        if type_upper == "BESSEL": scpi_value = "BESS"
        elif type_upper == "CHEBYSHEV": scpi_value = "CHEB"
        else: scpi_value = type_upper

        self.instrument.write(f"OUTP:FILT:HPAS:TYPE {scpi_value}")

    def get_output_filter_hpass_type(self) -> str:
        """Returns the characteristic of the high pass filter ('BESSEL' or 'CHEBYSHEV')."""
        response = self.instrument.query("OUTP:FILT:HPAS:TYPE?").strip().upper()
        if response.startswith("BESS"):
            return "BESSEL"
        elif response.startswith("CHEB"):
            return "CHEBYSHEV"
        return response

    def set_output_filter_lpass_frequency(self, frequency: float):
        """Determines the cutoff frequency of the low pass filter.
        Parameters:
        frequency: The cutoff frequency (numeric value)."""
        self.instrument.write(f"OUTP:FILT:LPAS:FREQ {frequency}")

    def get_output_filter_lpass_frequency(self) -> float:
        """Returns the cutoff frequency of the low pass filter."""
        response = self.instrument.query("OUTP:FILT:LPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output filter low pass frequency (not numeric): '{response}'")

    def set_output_filter_lpass_state(self, enable: bool):
        """Turns the low pass filter ON and OFF.
        Parameters:
        enable: True to turn the filter ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:FILT:LPAS:STATE {scpi_value}")

    def get_output_filter_lpass_state(self) -> bool:
        """Returns True if the low pass filter is ON, False if OFF."""
        response = self.instrument.query("OUTP:FILT:LPAS:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output filter low pass state: '{response}'")

    def set_output_filter_lpass_type(self, filter_type: str):
        """Determines the characteristic of the low pass filter.
        Parameters:
        filter_type: BESSel|CHEByshev"""
        valid_types = {"BESSEL", "CHEBYSHEV", "BESS", "CHEB"}
        type_upper = filter_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be 'BESSEL' or 'CHEBYSHEV'.")

        if type_upper == "BESSEL": scpi_value = "BESS"
        elif type_upper == "CHEBYSHEV": scpi_value = "CHEB"
        else: scpi_value = type_upper

        self.instrument.write(f"OUTP:FILT:LPAS:TYPE {scpi_value}")

    def get_output_filter_lpass_type(self) -> str:
        """Returns the characteristic of the low pass filter ('BESSEL' or 'CHEBYSHEV')."""
        response = self.instrument.query("OUTP:FILT:LPAS:TYPE?").strip().upper()
        if response.startswith("BESS"):
            return "BESSEL"
        elif response.startswith("CHEB"):
            return "CHEBYSHEV"
        return response


    def set_output_impedance(self, impedance_ohms: float):
        """Sets the output source impedance for the signal in Ohms.
        Parameters:
        impedance_ohms: Impedance in Ohms (numeric value)."""
        self.instrument.write(f"OUTP:IMP {impedance_ohms}")

    def get_output_impedance(self) -> float:
        """Returns the output source impedance for the signal in Ohms."""
        response = self.instrument.query("OUTP:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output impedance (not numeric): '{response}'")

    def set_output_low(self, low_type: str):
        """Connects the low signal terminal to ground or allows it to float.
        Parameters:
        low_type: FLOat|GROund"""
        valid_types = {"FLOAT", "GROUND", "FLO", "GRO"}
        type_upper = low_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid low connection type: '{low_type}'. Must be 'FLOAT' or 'GROUND'.")

        if type_upper == "FLOAT": scpi_value = "FLO"
        elif type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f"OUTP:LOW {scpi_value}")

    def get_output_low(self) -> str:
        """Returns how the low signal terminal is connected ('FLOAT' or 'GROUND')."""
        response = self.instrument.query("OUTP:LOW?").strip().upper()
        if response.startswith("FLO"):
            return "FLOAT"
        elif response.startswith("GRO"):
            return "GROUND"
        return response

    def set_output_polarity(self, polarity_type: str):
        """Sets or queries the output polarity.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMAL' or 'INVERTED'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f"OUTP:POL {scpi_value}")

    def get_output_polarity(self) -> str:
        """Returns the output polarity ('NORMAL' or 'INVERTED')."""
        response = self.instrument.query("OUTP:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_output_polarization(self, value_radians: float):
        """Sets the polarization of the output in radians.
        Parameters:
        value_radians: Polarization value in radians (numeric value)."""
        self.instrument.write(f"OUTP:POLZ {value_radians}")

    def get_output_polarization(self) -> float:
        """Returns the polarization of the output in radians."""
        response = self.instrument.query("OUTP:POLZ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output polarization (not numeric): '{response}'")

    def set_output_polarization_horizontal(self):
        """Sets the polarization of the output to zero (horizontal).
        Notes: This is an event command; no query."""
        self.instrument.write(f"OUTP:POLZ:HOR")

    def set_output_polarization_vertical(self):
        """Sets the polarization of the output to PI/2 radians (vertical).
        Notes: This is an event command; no query."""
        self.instrument.write(f"OUTP:POLZ:VERT")


    def set_output_position_x_angle_direction(self, direction: str):
        """Controls the direction of the movement for X-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:X:ANG:DIR {direction_upper}")

    def get_output_position_x_angle_direction(self) -> str:
        """Returns the direction of the movement for X-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:X:ANG:DIR?").strip().upper()
        return response

    def set_output_position_x_angle_immediate(self, value: float):
        """Indicates that the output is moved to the specified X-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:ANG:IMM {value}")

    def get_output_position_x_angle_immediate(self) -> float:
        """Returns the immediate position value for X-axis angle."""
        response = self.instrument.query("OUTP:POS:X:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle immediate position (not numeric): '{response}'")

    def set_output_position_x_angle_limit_high(self, value: float):
        """Sets the maximum for the X-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:ANG:LIM:HIGH {value}")

    def get_output_position_x_angle_limit_high(self) -> float:
        """Returns the maximum for the X-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:X:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle limit high (not numeric): '{response}'")

    def set_output_position_x_angle_limit_low(self, value: float):
        """Sets the minimum for the X-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:ANG:LIM:LOW {value}")

    def get_output_position_x_angle_limit_low(self) -> float:
        """Returns the minimum for the X-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:X:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle limit low (not numeric): '{response}'")

    def set_output_position_x_angle_limit_state(self, enable: bool):
        """Controls whether the X-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:X:ANG:LIM:STATE {scpi_value}")

    def get_output_position_x_angle_limit_state(self) -> bool:
        """Returns True if the X-axis angle limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:X:ANG:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for X-axis angle limit state: '{response}'")

    def set_output_position_x_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical X-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:ANG:OFFS {value}")

    def get_output_position_x_angle_offset(self) -> float:
        """Returns the offset value for the X-axis angle position."""
        response = self.instrument.query("OUTP:POS:X:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle offset (not numeric): '{response}'")

    def set_output_position_x_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the x-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:ANG:VEL {value}")

    def get_output_position_x_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the x-axis."""
        response = self.instrument.query("OUTP:POS:X:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle velocity (not numeric): '{response}'")

    def set_output_position_x_distance_direction(self, direction: str):
        """Controls the direction of the movement for X-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:X:DIST:DIR {direction_upper}")

    def get_output_position_x_distance_direction(self) -> str:
        """Returns the direction of the movement for X-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:X:DIST:DIR?").strip().upper()
        return response

    def set_output_position_x_distance_immediate(self, value: float):
        """Indicates that the output is moved to the specified X-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:DIST:IMM {value}")

    def get_output_position_x_distance_immediate(self) -> float:
        """Returns the immediate position value for X-axis linear distance."""
        response = self.instrument.query("OUTP:POS:X:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance immediate position (not numeric): '{response}'")

    def set_output_position_x_distance_limit_high(self, value: float):
        """Sets the maximum for the X-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:DIST:LIM:HIGH {value}")

    def get_output_position_x_distance_limit_high(self) -> float:
        """Returns the maximum for the X-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:X:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance limit high (not numeric): '{response}'")

    def set_output_position_x_distance_limit_low(self, value: float):
        """Sets the minimum for the X-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:DIST:LIM:LOW {value}")

    def get_output_position_x_distance_limit_low(self) -> float:
        """Returns the minimum for the X-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:X:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance limit low (not numeric): '{response}'")

    def set_output_position_x_distance_limit_state(self, enable: bool):
        """Controls whether the X-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:X:DIST:LIM:STATE {scpi_value}")

    def get_output_position_x_distance_limit_state(self) -> bool:
        """Returns True if the X-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:X:DIST:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for X-axis distance limit state: '{response}'")

    def set_output_position_x_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical X-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:DIST:OFFS {value}")

    def get_output_position_x_distance_offset(self) -> float:
        """Returns the offset value for the X-axis linear distance position."""
        response = self.instrument.query("OUTP:POS:X:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance offset (not numeric): '{response}'")

    def set_output_position_x_distance_velocity(self, value: float):
        """Controls the velocity of the displacement on the x-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:X:DIST:VEL {value}")

    def get_output_position_x_distance_velocity(self) -> float:
        """Returns the velocity of the displacement on the x-axis."""
        response = self.instrument.query("OUTP:POS:X:DIST:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance velocity (not numeric): '{response}'")


    def set_output_position_y_angle_direction(self, direction: str):
        """Controls the direction of the movement for Y-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:Y:ANG:DIR {direction_upper}")

    def get_output_position_y_angle_direction(self) -> str:
        """Returns the direction of the movement for Y-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:Y:ANG:DIR?").strip().upper()
        return response

    def set_output_position_y_angle_immediate(self, value: float):
        """Indicates that the output is moved to the specified Y-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:ANG:IMM {value}")

    def get_output_position_y_angle_immediate(self) -> float:
        """Returns the immediate position value for Y-axis angle."""
        response = self.instrument.query("OUTP:POS:Y:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle immediate position (not numeric): '{response}'")

    def set_output_position_y_angle_limit_high(self, value: float):
        """Sets the maximum for the Y-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:ANG:LIM:HIGH {value}")

    def get_output_position_y_angle_limit_high(self) -> float:
        """Returns the maximum for the Y-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:Y:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle limit high (not numeric): '{response}'")

    def set_output_position_y_angle_limit_low(self, value: float):
        """Sets the minimum for the Y-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:ANG:LIM:LOW {value}")

    def get_output_position_y_angle_limit_low(self) -> float:
        """Returns the minimum for the Y-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:Y:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle limit low (not numeric): '{response}'")

    def set_output_position_y_angle_limit_state(self, enable: bool):
        """Controls whether the Y-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:Y:ANG:LIM:STATE {scpi_value}")

    def get_output_position_y_angle_limit_state(self) -> bool:
        """Returns True if the Y-axis angle limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:Y:ANG:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis angle limit state: '{response}'")

    def set_output_position_y_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Y-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:ANG:OFFS {value}")

    def get_output_position_y_angle_offset(self) -> float:
        """Returns the offset value for the Y-axis angle position."""
        response = self.instrument.query("OUTP:POS:Y:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle offset (not numeric): '{response}'")

    def set_output_position_y_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the y-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:ANG:VEL {value}")

    def get_output_position_y_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the y-axis."""
        response = self.instrument.query("OUTP:POS:Y:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle velocity (not numeric): '{response}'")

    def set_output_position_y_distance_direction(self, direction: str):
        """Controls the direction of the movement for Y-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:Y:DIST:DIR {direction_upper}")

    def get_output_position_y_distance_direction(self) -> str:
        """Returns the direction of the movement for Y-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:Y:DIST:DIR?").strip().upper()
        return response

    def set_output_position_y_distance_immediate(self, value: float):
        """Indicates that the output is moved to the specified Y-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:DIST:IMM {value}")

    def get_output_position_y_distance_immediate(self) -> float:
        """Returns the immediate position value for Y-axis linear distance."""
        response = self.instrument.query("OUTP:POS:Y:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance immediate position (not numeric): '{response}'")

    def set_output_position_y_distance_limit_high(self, value: float):
        """Sets the maximum for the Y-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:DIST:LIM:HIGH {value}")

    def get_output_position_y_distance_limit_high(self) -> float:
        """Returns the maximum for the Y-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:Y:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance limit high (not numeric): '{response}'")

    def set_output_position_y_distance_limit_low(self, value: float):
        """Sets the minimum for the Y-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:DIST:LIM:LOW {value}")

    def get_output_position_y_distance_limit_low(self) -> float:
        """Returns the minimum for the Y-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:Y:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance limit low (not numeric): '{response}'")

    def set_output_position_y_distance_limit_state(self, enable: bool):
        """Controls whether the Y-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:Y:DIST:LIM:STATE {scpi_value}")

    def get_output_position_y_distance_limit_state(self) -> bool:
        """Returns True if the Y-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:Y:DIST:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis distance limit state: '{response}'")

    def set_output_position_y_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Y-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:DIST:OFFS {value}")

    def get_output_position_y_distance_offset(self) -> float:
        """Returns the offset value for the Y-axis linear distance position."""
        response = self.instrument.query("OUTP:POS:Y:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance offset (not numeric): '{response}'")

    def set_output_position_y_distance_velocity(self, value: float):
        """Controls the velocity of the displacement on the y-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Y:DIST:VEL {value}")

    def get_output_position_y_distance_velocity(self) -> float:
        """Returns the velocity of the displacement on the y-axis."""
        response = self.instrument.query("OUTP:POS:Y:DIST:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance velocity (not numeric): '{response}'")

    def set_output_position_z_angle_direction(self, direction: str):
        """Controls the direction of the movement for Z-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:Z:ANG:DIR {direction_upper}")

    def get_output_position_z_angle_direction(self) -> str:
        """Returns the direction of the movement for Z-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:Z:ANG:DIR?").strip().upper()
        return response

    def set_output_position_z_angle_immediate(self, value: float):
        """Indicates that the output is moved to the specified Z-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:ANG:IMM {value}")

    def get_output_position_z_angle_immediate(self) -> float:
        """Returns the immediate position value for Z-axis angle."""
        response = self.instrument.query("OUTP:POS:Z:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle immediate position (not numeric): '{response}'")

    def set_output_position_z_angle_limit_high(self, value: float):
        """Sets the maximum for the Z-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:ANG:LIM:HIGH {value}")

    def get_output_position_z_angle_limit_high(self) -> float:
        """Returns the maximum for the Z-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:Z:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle limit high (not numeric): '{response}'")

    def set_output_position_z_angle_limit_low(self, value: float):
        """Sets the minimum for the Z-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:ANG:LIM:LOW {value}")

    def get_output_position_z_angle_limit_low(self) -> float:
        """Returns the minimum for the Z-axis angle position limit."""
        response = self.instrument.query("OUTP:POS:Z:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle limit low (not numeric): '{response}'")

    def set_output_position_z_angle_limit_state(self, enable: bool):
        """Controls whether the Z-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:Z:ANG:LIM:STATE {scpi_value}")

    def get_output_position_z_angle_limit_state(self) -> bool:
        """Returns True if the Z-axis angle limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:Z:ANG:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Z-axis angle limit state: '{response}'")

    def set_output_position_z_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Z-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:ANG:OFFS {value}")

    def get_output_position_z_angle_offset(self) -> float:
        """Returns the offset value for the Z-axis angle position."""
        response = self.instrument.query("OUTP:POS:Z:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle offset (not numeric): '{response}'")

    def set_output_position_z_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the z-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:ANG:VEL {value}")

    def get_output_position_z_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the z-axis."""
        response = self.instrument.query("OUTP:POS:Z:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle velocity (not numeric): '{response}'")

    def set_output_position_z_distance_direction(self, direction: str):
        """Controls the direction of the movement for Z-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"OUTP:POS:Z:DIST:DIR {direction_upper}")

    def get_output_position_z_distance_direction(self) -> str:
        """Returns the direction of the movement for Z-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query("OUTP:POS:Z:DIST:DIR?").strip().upper()
        return response

    def set_output_position_z_distance_immediate(self, value: float):
        """Indicates that the output is moved to the specified Z-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:DIST:IMM {value}")

    def get_output_position_z_distance_immediate(self) -> float:
        """Returns the immediate position value for Z-axis linear distance."""
        response = self.instrument.query("OUTP:POS:Z:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance immediate position (not numeric): '{response}'")

    def set_output_position_z_distance_limit_high(self, value: float):
        """Sets the maximum for the Z-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:DIST:LIM:HIGH {value}")

    def get_output_position_z_distance_limit_high(self) -> float:
        """Returns the maximum for the Z-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:Z:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance limit high (not numeric): '{response}'")

    def set_output_position_z_distance_limit_low(self, value: float):
        """Sets the minimum for the Z-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:DIST:LIM:LOW {value}")

    def get_output_position_z_distance_limit_low(self) -> float:
        """Returns the minimum for the Z-axis linear distance position limit."""
        response = self.instrument.query("OUTP:POS:Z:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance limit low (not numeric): '{response}'")

    def set_output_position_z_distance_limit_state(self, enable: bool):
        """Controls whether the Z-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:POS:Z:DIST:LIM:STATE {scpi_value}")

    def get_output_position_z_distance_limit_state(self) -> bool:
        """Returns True if the Z-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query("OUTP:POS:Z:DIST:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Z-axis distance limit state: '{response}'")

    def set_output_position_z_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Z-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:DIST:OFFS {value}")

    def get_output_position_z_distance_offset(self) -> float:
        """Returns the offset value for the Z-axis linear distance position."""
        response = self.instrument.query("OUTP:POS:Z:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance offset (not numeric): '{response}'")

    def set_output_position_z_distance_velocity(self, value: float):
        """Controls the velocity of the displacement on the z-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f"OUTP:POS:Z:DIST:VEL {value}")

    def get_output_position_z_distance_velocity(self) -> float:
        """Returns the velocity of the displacement on the z-axis."""
        response = self.instrument.query("OUTP:POS:Z:DIST:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance velocity (not numeric): '{response}'")

    def set_output_protection_delay(self, delay_seconds: float):
        """Controls the amount of time the protection trip condition must be true before the subsequent protection is taken.
        Parameters:
        delay_seconds: The delay time in seconds (numeric value)."""
        self.instrument.write(f"OUTP:PROT:DEL {delay_seconds}")

    def get_output_protection_delay(self) -> float:
        """Returns the delay time for output protection in seconds."""
        response = self.instrument.query("OUTP:PROT:DEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for output protection delay (not numeric): '{response}'")

    def set_output_protection_state(self, enable: bool):
        """Controls whether the output protection circuit is enabled.
        Parameters:
        enable: True to enable protection, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:PROT:STATE {scpi_value}")

    def get_output_protection_state(self) -> bool:
        """Returns True if the output protection circuit is enabled, False if not."""
        response = self.instrument.query("OUTP:PROT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output protection state: '{response}'")

    def get_output_protection_tripped(self) -> bool:
        """Returns True if the protection circuit is tripped, False if untripped.
        Notes: Query only."""
        response = self.instrument.query("OUTP:PROT:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for output protection tripped status: '{response}'")

    def clear_output_protection(self):
        """Causes the protection circuit to be cleared.
        Notes: This is an event command; no query."""
        self.instrument.write("OUTP:PROT:CLE")

    def set_output_roscillator_state(self, enable: bool):
        """Selects whether or not the device outputs a signal on its ROSCillator port.
        Parameters:
        enable: True to output a signal, False to not output."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:ROSC:STATE {scpi_value}")

    def get_output_roscillator_state(self) -> bool:
        """Returns True if the device outputs a signal on its ROSCillator port, False if not."""
        response = self.instrument.query("OUTP:ROSC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output roscillator state: '{response}'")

    def set_output_ttl_ecl_trigger_immediate(self, trigger_line: str):
        """Causes a pulse to appear on the specified TTLTrg or ECLTrg trigger line.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1')."""
        self.instrument.write(f"OUTP:{trigger_line}:IMM")

    def set_output_ttl_ecl_trigger_level(self, trigger_line: str, level: bool):
        """Sets the selected TTLTrg or ECLTrg line to a logical level (0 or 1).
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        level: True for logical level 1, False for logical level 0."""
        scpi_value = "1" if level else "0"
        self.instrument.write(f"OUTP:{trigger_line}:LEVel {scpi_value}")

    def get_output_ttl_ecl_trigger_level(self, trigger_line: str) -> bool:
        """Returns the logical level of the selected TTLTrg or ECLTrg line (True for 1, False for 0)."""
        response = self.instrument.query(f"OUTP:{trigger_line}:LEVel?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for {trigger_line} level: '{response}'")

    def set_output_ttl_ecl_trigger_polarity(self, trigger_line: str, polarity: str):
        """Sets the polarity of the specified VXI TTL or ECL trigger line.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        polarity: NORMal|INVerted"""
        valid_polarities = {"NORMAL", "INVERTED", "NORM", "INV"}
        polarity_upper = polarity.upper()
        if polarity_upper not in valid_polarities:
            raise ValueError(f"Invalid polarity: '{polarity}'. Must be 'NORMAL' or 'INVERTED'.")

        if polarity_upper == "NORMAL": scpi_value = "NORM"
        elif polarity_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = polarity_upper

        self.instrument.write(f"OUTP:{trigger_line}:POL {scpi_value}")

    def get_output_ttl_ecl_trigger_polarity(self, trigger_line: str) -> str:
        """Returns the polarity of the specified VXI TTL or ECL trigger line ('NORMAL' or 'INVERTED')."""
        response = self.instrument.query(f"OUTP:{trigger_line}:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_output_ttl_ecl_trigger_protocol(self, trigger_line: str, protocol: str):
        """Selects the trigger protocol for the VXI TTLTrg or ECLTrg trigger lines.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        protocol: SYNChronous|SSYNchronous|ASYNchronous"""
        valid_protocols = {"SYNCHRONOUS", "SEMISYNCHRONOUS", "ASYNCHRONOUS", "SYCN", "SSYN", "ASYN"}
        protocol_upper = protocol.upper()
        if protocol_upper not in valid_protocols:
            raise ValueError(f"Invalid protocol: '{protocol}'. Must be 'SYNCHRONOUS', 'SEMISYNCHRONOUS', or 'ASYNCHRONOUS'.")

        if protocol_upper == "SYNCHRONOUS": scpi_value = "SYCN"
        elif protocol_upper == "SEMISYNCHRONOUS": scpi_value = "SSYN"
        elif protocol_upper == "ASYNCHRONOUS": scpi_value = "ASYN"
        else: scpi_value = protocol_upper

        self.instrument.write(f"OUTP:{trigger_line}:PROT {scpi_value}")

    def get_output_ttl_ecl_trigger_protocol(self, trigger_line: str) -> str:
        """Returns the trigger protocol for the VXI TTLTrg or ECLTrg trigger lines ('SYNCHRONOUS', 'SEMISYNCHRONOUS', or 'ASYNCHRONOUS')."""
        response = self.instrument.query(f"OUTP:{trigger_line}:PROT?").strip().upper()
        if response.startswith("SYCN"):
            return "SYNCHRONOUS"
        elif response.startswith("SSYN"):
            return "SEMISYNCHRONOUS"
        elif response.startswith("ASYN"):
            return "ASYNCHRONOUS"
        return response

    def set_output_ttl_ecl_trigger_width(self, trigger_line: str, width_seconds: float):
        """Selects width of the pulse being generated by the immediate command.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        width_seconds: The width of the pulse in seconds (numeric value)."""
        self.instrument.write(f"OUTP:{trigger_line}:WIDT {width_seconds}")

    def get_output_ttl_ecl_trigger_width(self, trigger_line: str) -> float:
        """Returns the width of the pulse being generated by the immediate command in seconds."""
        response = self.instrument.query(f"OUTP:{trigger_line}:WIDT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {trigger_line} width (not numeric): '{response}'")

    def set_output_ttl_ecl_trigger_state(self, trigger_line: str, enable: bool):
        """Selects whether or not the VXI module drives the VXI backplane trigger line.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        enable: True to drive the trigger line, False to not drive."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:{trigger_line}:STATE {scpi_value}")

    def get_output_ttl_ecl_trigger_state(self, trigger_line: str) -> bool:
        """Returns True if the VXI module drives the VXI backplane trigger line, False if not."""
        response = self.instrument.query(f"OUTP:{trigger_line}:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for {trigger_line} state: '{response}'")

    def set_output_ttl_ecl_trigger_source(self, trigger_line: str, source: str):
        """Controls which signal from the VXI module shall drive the VXI backplane trigger line.
        Parameters:
        trigger_line: The trigger line (e.g., 'TTLTrg0', 'ECLTrg1').
        source: The source name (character data, such as 'INTernal' or 'EXTernal')."""
        self.instrument.write(f"OUTP:{trigger_line}:SOUR '{source}'")

    def get_output_ttl_ecl_trigger_source(self, trigger_line: str) -> str:
        """Returns which signal from the VXI module drives the VXI backplane trigger line."""
        response = self.instrument.query(f"OUTP:{trigger_line}:SOUR?").strip().strip("'\"")
        return response

    def set_output_state(self, enable: bool):
        """Controls whether the output terminals are open or closed.
        Parameters:
        enable: True to close terminals, False for maximum isolation."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"OUTP:STATE {scpi_value}")

    def get_output_state(self) -> bool:
        """Returns True if the output terminals are closed, False if open."""
        response = self.instrument.query("OUTP:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for output state: '{response}'")

    def set_output_type(self, output_type_char: str):
        """Selects the output characteristic to be used if more than one is available.
        Parameters:
        output_type_char: BALanced|UNBalanced"""
        valid_types = {"BALANCED", "UNBALANCED", "BAL", "UNB"}
        type_upper = output_type_char.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid output type: '{output_type_char}'. Must be 'BALANCED' or 'UNBALANCED'.")

        if type_upper == "BALANCED": scpi_value = "BAL"
        elif type_upper == "UNBALANCED": scpi_value = "UNB"
        else: scpi_value = type_upper

        self.instrument.write(f"OUTP:TYPE {scpi_value}")

    def get_output_type(self) -> str:
        """Returns the output characteristic being used ('BALANCED' or 'UNBALANCED')."""
        response = self.instrument.query("OUTP:TYPE?").strip().upper()
        if response.startswith("BAL"):
            return "BALANCED"
        elif response.startswith("UNB"):
            return "UNBALANCED"
        return response

