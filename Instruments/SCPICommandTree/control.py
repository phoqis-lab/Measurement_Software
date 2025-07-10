class Control():
    def __init__(self, instrument):
        self.instrument = instrument
    
    def set_apower_state(self, enable: bool):
        """Turns the Auxiliary Power ON and OFF.
        Parameters:
        enable: True to turn APOWer ON, False to turn APOWer OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:APOW:STATE {scpi_value}")

    def get_apower_state(self) -> bool:
        """Returns True if Auxiliary Power is ON, False if OFF."""
        response = self.instrument.query("CONT:APOW:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Auxiliary Power state: '{response}'")

    
    def set_blower_state(self, enable: bool):
        """Turns the Blower ON and OFF.
        Parameters:
        enable: True to turn BLOWer ON, False to turn BLOWer OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:BLOW:STATE {scpi_value}")

    def get_blower_state(self) -> bool:
        """Returns True if Blower is ON, False if OFF."""
        response = self.instrument.query("CONT:BLOW:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Blower state: '{response}'")

    def set_brake_state(self, enable: bool):
        """Sets or queries the state of the brake.
        Parameters:
        enable: True to set BRAKE ON, False to set BRAKE OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:BRAK:STATE {scpi_value}")

    def get_brake_state(self) -> bool:
        """Returns True if the brake is ON, False if OFF."""
        response = self.instrument.query("CONT:BRAK:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Brake state: '{response}'")

    def set_compressor_state(self, enable: bool):
        """Turns the Compressor ON and OFF.
        Parameters:
        enable: True to turn COMPressor ON, False to turn COMPressor OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:COMP:STATE {scpi_value}")

    def get_compressor_state(self) -> bool:
        """Returns True if Compressor is ON, False if OFF."""
        response = self.instrument.query("CONT:COMP:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Compressor state: '{response}'")

    def adjust_cover(self, adjustment_type: str):
        """Controls the cover.
        Parameters:
        adjustment_type: OPEN|CLOSE|SOPen|SCLOse"""
        valid_adjustments = {"OPEN", "CLOSE", "SOPEN", "SCLOSE"}
        adj_type_upper = adjustment_type.upper()
        if adj_type_upper not in valid_adjustments:
            raise ValueError(f"Invalid cover adjustment type: '{adjustment_type}'. Must be one of {list(valid_adjustments)}")
        self.instrument.write(f"CONT:COV:ADJ {adj_type_upper}")

    
    def get_cover_position(self) -> str:
        """Returns the position of the cover.
        Returns: 'OPEN', 'CLOSE', or 'MID'."""
        response = self.instrument.query("CONT:COV:POS?").strip().upper()
        valid_positions = {"OPEN", "CLOSE", "MID"}
        if response not in valid_positions:
            # Handle potential abbreviations or unexpected responses if necessary
            if response.startswith("OP"): return "OPEN"
            elif response.startswith("CL"): return "CLOSE"
            elif response.startswith("MI"): return "MID"
            return response # Return raw if still unexpected
        return response

    def initiate_eben_clean(self):
        """Initiates the bench's internal procedure to clean out its gas lines ('purge' or 'backflush').
        Notes: This is an event command; no query."""
        self.instrument.write("CONT:EBEN:CLE:INIT")

    def set_eben_clean_duration(self, duration_seconds: float):
        """Sets the duration in seconds of the 'clean' procedure for the gas analyzer emissions bench.
        Parameters:
        duration_seconds: Duration in seconds (numeric value)."""
        self.instrument.write(f"CONT:EBEN:CLE:DUR {duration_seconds}")

    def get_eben_clean_duration(self) -> float:
        """Returns the duration in seconds of the 'clean' procedure for the gas analyzer emissions bench."""
        response = self.instrument.query("CONT:EBEN:CLE:DUR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for EBench clean duration (not numeric): '{response}'")

    def initiate_idle(self):
        """Returns the device to idle.
        Notes: This is an event command; no query."""
        self.instrument.write("CONT:IDLE:INIT")

    
    def adjust_lift(self, adjustment_type: str):
        """Controls the lift.
        Parameters:
        adjustment_type: UP|DOWN"""
        valid_adjustments = {"UP", "DOWN"}
        adj_type_upper = adjustment_type.upper()
        if adj_type_upper not in valid_adjustments:
            raise ValueError(f"Invalid lift adjustment type: '{adjustment_type}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f"CONT:LIFT:ADJ {adj_type_upper}")

    def get_lift_position(self) -> str:
        """Queries the position of the lift.
        Returns: 'UP', 'DOWN', or 'MID'."""
        response = self.instrument.query("CONT:LIFT:POS?").strip().upper()
        valid_positions = {"UP", "DOWN", "MID"}
        if response not in valid_positions:
            # Handle potential abbreviations or unexpected responses
            if response.startswith("UP"): return "UP"
            elif response.startswith("DO"): return "DOWN"
            elif response.startswith("MI"): return "MID"
            return response # Return raw if still unexpected
        return response

    def set_mcontrol_state(self, enable: bool):
        """Turns the power of motor ON or OFF.
        Parameters:
        enable: True to turn motor power ON, False to turn motor power OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:MCON:STATE {scpi_value}")

    def get_mcontrol_state(self) -> bool:
        """Returns True if motor power is ON, False if OFF."""
        response = self.instrument.query("CONT:MCON:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Motor Control state: '{response}'")

    def set_rotation_direction(self, direction: str):
        """Configures the dynamometer rotation direction.
        Parameters:
        direction: FORWard|REVerse"""
        valid_directions = {"FORWARD", "REVERSE"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid rotation direction: '{direction}'. Must be 'FORWARD' or 'REVERSE'.")
        self.instrument.write(f"CONT:ROT:DIR {direction_upper}")

    def get_rotation_direction(self) -> str:
        """Returns the dynamometer rotation direction ('FORWARD' or 'REVERSE')."""
        response = self.instrument.query("CONT:ROT:DIR?").strip().upper()
        if response.startswith("FOR"):
            return "FORWARD"
        elif response.startswith("REV"):
            return "REVERSE"
        return response

    def set_vcdevice_state(self, enable: bool):
        """When the state is ON, the dynamometer is performing the centering function. When the state is OFF, centering is not being performed.
        Parameters:
        enable: True to enable centering function, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CONT:VCDE:STATE {scpi_value}")

    def get_vcdevice_state(self) -> bool:
        """Returns True if the vehicle centering device is performing centering, False if not."""
        response = self.instrument.query("CONT:VCDE:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Vehicle Centering Device state: '{response}'")

    
    def set_vcdevice_tdiameter(self, tire_diameter_meters: float):
        """Sets the tire diameter (m) used by the centering device to center the vehicle on the dynamometer.
        Parameters:
        tire_diameter_meters: Tire Diameter in meters (numeric value)."""
        self.instrument.write(f"CONT:VCDE:TDI {tire_diameter_meters}")

    def get_vcdevice_tdiameter(self) -> float:
        """Returns the tire diameter (m) used by the centering device."""
        response = self.instrument.query("CONT:VCDE:TDI?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Vehicle Centering Device tire diameter (not numeric): '{response}'")

