"""Write down source formula pieces here. Page 394 in SCPI""" 
class Source:
    """
    A class to encapsulate SCPI commands for instrument control.
    Assumes 'self.instrument' is an object with 'write' and 'query' methods
    that handle communication with the physical instrument.
    """
    def __init__(self,instrument):
        """
        Initializes the InstrumentControl with an instrument connection.
        :param instrument_connection: An object capable of sending/receiving
                                      SCPI commands (e.g., pyvisa resource).
        """
        self.instrument = instrument

    
    def set_source_acceleration_level(self, value: float):
        """Sets the acceleration in m/s^2.
        Parameters:
        value: The acceleration value (numeric value)."""
        self.instrument.write(f":SOUR:ACC {value}")

    def get_source_acceleration_level(self) -> float:
        """Returns the acceleration in m/s^2."""
        response = self.instrument.query(":SOUR:ACC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for acceleration level (not numeric): '{response}'")

    
    def set_source_am_coupling(self, coupling_type: str):
        """Sets the coupling between the modulator and the modulating signal.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:COUP {scpi_value}")

    def get_source_am_coupling(self) -> str:
        """Returns the coupling between the modulator and the modulating signal ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(":SOUR:AM:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_am_depth(self, value: float):
        """Sets the modulation DEPTh of an AM signal in percent (%).
        Parameters:
        value: The modulation depth percentage (numeric value)."""
        self.instrument.write(f":SOUR:AM:DEP {value}")

    def get_source_am_depth(self) -> float:
        """Returns the modulation DEPTh of an AM signal in percent (%)."""
        response = self.instrument.query(":SOUR:AM:DEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for AM depth (not numeric): '{response}'")


    def set_source_am_external_coupling(self, external_source_number: int, coupling_type: str):
        """Sets the coupling for a specified external AM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:EXT{external_source_number}:COUP {scpi_value}")

    def get_source_am_external_coupling(self, external_source_number: int) -> str:
        """Returns the coupling for a specified external AM signal source ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(f":SOUR:AM:EXT{external_source_number}:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_am_external_impedance(self, external_source_number: int, value: float):
        """Sets the impedance of the specified external AM signal source in Ohms.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        value: The impedance in Ohms (numeric value)."""
        self.instrument.write(f":SOUR:AM:EXT{external_source_number}:IMP {value}")

    def get_source_am_external_impedance(self, external_source_number: int) -> float:
        """Returns the impedance of the specified external AM signal source in Ohms."""
        response = self.instrument.query(f":SOUR:AM:EXT{external_source_number}:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for external AM impedance (not numeric): '{response}'")

    def set_source_am_external_polarity(self, external_source_number: int, polarity_type: str):
        """Sets the polarity for a specified external AM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:EXT{external_source_number}:POL {scpi_value}")

    def get_source_am_external_polarity(self, external_source_number: int) -> str:
        """Returns the polarity for a specified external AM signal source ('NORMal' or 'INVerted')."""
        response = self.instrument.query(f":SOUR:AM:EXT{external_source_number}:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_am_internal_frequency(self, internal_source_number: int, value: float):
        """Sets the frequency of the specified internal AM signal source in Hz.
        Parameters:
        internal_source_number: The internal signal source number (e.g., 1).
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:AM:INT{internal_source_number}:FREQ {value}")

    def get_source_am_internal_frequency(self, internal_source_number: int) -> float:
        """Returns the frequency of the specified internal AM signal source in Hz."""
        response = self.instrument.query(f":SOUR:AM:INT{internal_source_number}:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for internal AM frequency (not numeric): '{response}'")

    def set_source_am_mode(self, mode_type: str):
        """Determines which set of commands currently control the AM subsystem.
        Parameters:
        mode_type: FIXed|LIST"""
        valid_types = {"FIXED", "LIST", "FIX"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid AM mode: '{mode_type}'. Must be 'FIXed' or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:MODE {scpi_value}")

    def get_source_am_mode(self) -> str:
        """Returns which set of commands currently control the AM subsystem ('FIXed' or 'LIST')."""
        response = self.instrument.query(":SOUR:AM:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        return response

    def set_source_am_polarity(self, polarity_type: str):
        """Sets the polarity between the modulator and the modulating signal.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:POL {scpi_value}")

    def get_source_am_polarity(self) -> str:
        """Returns the polarity between the modulator and the modulating signal ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:AM:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_am_sensitivity(self, value: float):
        """Controls the modulation depth by setting a sensitivity to the modulation signal voltage level. Unit is percent/Volt (%/V).
        Parameters:
        value: The sensitivity value (numeric value)."""
        self.instrument.write(f":SOUR:AM:SENS {value}")

    def get_source_am_sensitivity(self) -> float:
        """Returns the sensitivity in percent/Volt (%/V)."""
        response = self.instrument.query(":SOUR:AM:SENS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for AM sensitivity (not numeric): '{response}'")

    def set_source_am_source(self, sources: list[str]):
        """Selects the source(s) for the modulating signal.
        Parameters:
        sources: A list of strings, each being 'EXTernal' or 'INTernal', optionally followed by a number (e.g., ["INTernal1", "EXTernal"])."""
        formatted_sources = []
        for src in sources:
            src_upper = src.upper()
            if src_upper.startswith("INTERNAL"):
                formatted_sources.append(f"INT{src_upper[8:]}") # Handle INTernal1 -> INT1
            elif src_upper.startswith("EXTERNAL"):
                formatted_sources.append(f"EXT{src_upper[8:]}") # Handle EXTernal1 -> EXT1
            else:
                raise ValueError(f"Invalid source type: '{src}'. Must be 'INTernal' or 'EXTernal'.")
        source_str = ",".join(formatted_sources)
        self.instrument.write(f":SOUR:AM::SOUR {source_str}")

    def get_source_am_source(self) -> list[str]:
        """Returns the selected source(s) for the modulating signal.
        Returns: A list of source strings (e.g., ['INTernal', 'EXTernal1'])."""
        response = self.instrument.query(":SOUR:AM::SOUR?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., "INT,EXT1")
        return [s.replace("INT", "INTernal").replace("EXT", "EXTernal") for s in response.split(',')]


    def set_source_am_state(self, enable: bool):
        """Turns Amplitude Modulation ON or OFF.
        Parameters:
        enable: True to turn AM modulation ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:AM:STATE {scpi_value}")

    def get_source_am_state(self) -> bool:
        """Returns True if Amplitude Modulation is ON, False if OFF."""
        response = self.instrument.query(":SOUR:AM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for AM state: '{response}'")


    def set_source_am_type(self, am_type: str):
        """Controls the type of AM shaping.
        Parameters:
        am_type: LINear|LOGarithmic|EXPonential"""
        valid_types = {"LINEAR", "LOGARITHMIC", "EXPONENTIAL", "LIN", "LOG", "EXP"}
        type_upper = am_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid AM type: '{am_type}'. Must be 'LINear', 'LOGarithmic', or 'EXPonential'.")

        if type_upper == "LINEAR": scpi_value = "LIN"
        elif type_upper == "LOGARITHMIC": scpi_value = "LOG"
        elif type_upper == "EXPONENTIAL": scpi_value = "EXP"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:AM:TYPE {scpi_value}")

    def get_source_am_type(self) -> str:
        """Returns the type of AM shaping ('LINear', 'LOGarithmic', or 'EXPonential')."""
        response = self.instrument.query(":SOUR:AM:TYPE?").strip().upper()
        if response.startswith("LIN"):
            return "LINEAR"
        elif response.startswith("LOG"):
            return "LOGARITHMIC"
        elif response.startswith("EXP"):
            return "EXPONENTIAL"
        return response

    
    def set_source_combine_feed(self, data_handle: str):
        """Sets the data flow into the COMBine block.
        Parameters:
        data_handle: The data handle string (character data)."""
        self.instrument.write(f":SOUR:COMB:FEED '{data_handle}'")

    def get_source_combine_feed(self) -> str:
        """Returns the data flow into the COMBine block."""
        response = self.instrument.query(":SOUR:COMB:FEED?").strip().strip("'\"")
        return response

    
    def set_source_correction_state(self, enable: bool):
        """Determines whether the correction data defined in this section is applied to the signal.
        Parameters:
        enable: True to apply correction, False to not apply."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:STATE {scpi_value}")

    def get_source_correction_state(self) -> bool:
        """Returns True if the correction data is applied, False if not."""
        response = self.instrument.query(":SOUR:CORR:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for correction state: '{response}'")

    
    def source_correction_collect_acquire(self):
        """A signal will be generated, measured, and the results saved as data for the chosen correction method.
        Notes: This is an event command; no query."""
        self.instrument.write(":SOUR:CORR:COLL:ACQ")

    def set_source_correction_collect_method(self, method_type: str):
        """Selects the correction method to be used for the correction that is about to be performed.
        Parameters:
        method_type: PMETer"""
        valid_types = {"PMETER", "PMET"}
        type_upper = method_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid method type: '{method_type}'. Must be 'PMETer'.")
        self.instrument.write(f":SOUR:CORR:COLL:METH {type_upper}")

    def get_source_correction_collect_method(self) -> str:
        """Returns the correction method currently selected ('PMETer')."""
        response = self.instrument.query(":SOUR:CORR:COLL:METH?").strip().upper()
        if response.startswith("PMET"):
            return "PMETer"
        return response

    def source_correction_collect_save(self, name: str = None):
        """Calculates the correction data using the current method selection and then saves the correction data.
        Parameters:
        name: (Optional) The name (trace_name or table_name) where the correction data is saved."""
        if name:
            self.instrument.write(f":SOUR:CORR:COLL:SAVE '{name}'")
        else:
            self.instrument.write(":SOUR:CORR:COLL:SAVE")

    def set_source_correction_cset_select(self, name: str):
        """Specifies the active correction set.
        Parameters:
        name: The name of the trace or table (character data)."""
        self.instrument.write(f":SOUR:CORR:CSET:SEL '{name}'")

    def get_source_correction_cset_select(self) -> str:
        """Returns the name of the active correction set."""
        response = self.instrument.query(":SOUR:CORR:CSET:SEL?").strip().strip("'\"")
        return response

    def set_source_correction_cset_state(self, enable: bool):
        """Determines whether the correction data defined in the selected set is applied to the output.
        Parameters:
        enable: True to apply correction, False to not apply."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:CSET:STATE {scpi_value}")

    def get_source_correction_cset_state(self) -> bool:
        """Returns True if the correction data is applied, False if not."""
        response = self.instrument.query(":SOUR:CORR:CSET:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for correction CSET state: '{response}'")

    
    def set_source_correction_offset_magnitude(self, value: float):
        """Sets the magnitude value of the correction offset data.
        Parameters:
        value: The magnitude value (numeric value). Magnitude is always added linearly, as in volts."""
        self.instrument.write(f":SOUR:CORR:OFFS:MAGN {value}")

    def get_source_correction_offset_magnitude(self) -> float:
        """Returns the magnitude value of the correction offset data."""
        response = self.instrument.query(":SOUR:CORR:OFFS:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for offset magnitude (not numeric): '{response}'")

    def set_source_correction_offset_phase(self, value: float):
        """Sets the phase value of the correction offset data. Units are currently selected angle units.
        Parameters:
        value: The phase value (numeric value)."""
        self.instrument.write(f":SOUR:CORR:OFFS:PHAS {value}")

    def get_source_correction_offset_phase(self) -> float:
        """Returns the phase value of the correction offset data."""
        response = self.instrument.query(":SOUR:CORR:OFFS:PHAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for offset phase (not numeric): '{response}'")

    def set_source_correction_offset_state(self, enable: bool):
        """Enables or disables the offset correction.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:OFFS:STATE {scpi_value}")

    def get_source_correction_offset_state(self) -> bool:
        """Returns True if the offset correction is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:CORR:OFFS:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for offset state: '{response}'")

    # Grouping LOSS, GAIN, SLOPE as they share parameters and structure.
    def set_source_correction_loss_gain_slope_state(self, type_prefix: str, enable: bool):
        """Enables or disables the correction for LOSS, GAIN, or SLOPe.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        enable: True to enable, False to disable."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:{prefix_upper}:STATE {scpi_value}")

    def get_source_correction_loss_gain_slope_state(self, type_prefix: str) -> bool:
        """Returns True if the correction for LOSS, GAIN, or SLOPe is enabled, False if disabled."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SOUR:CORR:{prefix_upper}:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for {type_prefix} state: '{response}'")

    
    def set_source_correction_loss_gain_output_magnitude(self, type_prefix: str, value: float):
        """Sets the magnitude value of the correction for LOSS or GAIN for output measurements.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'
        value: The magnitude value (numeric value). Units are current relative amplitude units."""
        valid_prefixes = {"LOSS", "GAIN", "LOS", "GAI"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS' or 'GAIN'.")

        self.instrument.write(f":SOUR:CORR:{prefix_upper}:OUTP:MAGN {value}")

    def get_source_correction_loss_gain_output_magnitude(self, type_prefix: str) -> float:
        """Returns the magnitude value of the correction for LOSS or GAIN for output measurements."""
        valid_prefixes = {"LOSS", "GAIN", "LOS", "GAI"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS' or 'GAIN'.")

        response = self.instrument.query(f":SOUR:CORR:{prefix_upper}:OUTP:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} output magnitude (not numeric): '{response}'")

    def set_source_correction_loss_gain_output_phase(self, type_prefix: str, value: float):
        """Sets the phase value of the correction for LOSS or GAIN for output measurements.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'
        value: The phase value (numeric value). Units are currently selected angle units."""
        valid_prefixes = {"LOSS", "GAIN", "LOS", "GAI"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS' or 'GAIN'.")

        self.instrument.write(f":SOUR:CORR:{prefix_upper}:OUTP:PHAS {value}")

    def get_source_correction_loss_gain_output_phase(self, type_prefix: str) -> float:
        """Returns the phase value of the correction for LOSS or GAIN for output measurements."""
        valid_prefixes = {"LOSS", "GAIN", "LOS", "GAI"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS' or 'GAIN'.")

        response = self.instrument.query(f":SOUR:CORR:{prefix_upper}:OUTP:PHAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} output phase (not numeric): '{response}'")

    def set_source_correction_edelay_time(self, time_seconds: float):
        """Sets the electrical delay with the time parameter.
        Parameters:
        time_seconds: The time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:CORR:EDEL:TIME {time_seconds}")

    def get_source_correction_edelay_time(self) -> float:
        """Returns the electrical delay time in seconds."""
        response = self.instrument.query(":SOUR:CORR:EDEL:TIME?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for electrical delay time (not numeric): '{response}'")

    def set_source_correction_edelay_distance(self, distance_meters: float):
        """Sets the electrical delay with the distance parameter.
        Parameters:
        distance_meters: The distance in meters (numeric value)."""
        self.instrument.write(f":SOUR:CORR:EDEL:DIST {distance_meters}")

    def get_source_correction_edelay_distance(self) -> float:
        """Returns the electrical delay distance in meters."""
        response = self.instrument.query(":SOUR:CORR:EDEL:DIST?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for electrical delay distance (not numeric): '{response}'")

    
    def set_source_correction_edelay_state(self, enable: bool):
        """Enables or disables the correction for electrical delay.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:EDEL:STATE {scpi_value}")

    def get_source_correction_edelay_state(self) -> bool:
        """Returns True if electrical delay correction is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:CORR:EDEL:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for electrical delay state: '{response}'")

    def set_source_correction_rvelocity_medium(self, medium_type: str):
        """Selects the method of correction for any operation that uses relative velocity.
        Parameters:
        medium_type: COAX|WAVeguide"""
        valid_types = {"COAX", "WAVEGUIDE", "WAV"}
        type_upper = medium_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid medium type: '{medium_type}'. Must be 'COAX' or 'WAVeguide'.")

        if type_upper == "WAVEGUIDE": scpi_value = "WAV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:CORR:RVEL:MED {scpi_value}")

    def get_source_correction_rvelocity_medium(self) -> str:
        """Returns the method of correction for any operation that uses relative velocity ('COAX' or 'WAVeguide')."""
        response = self.instrument.query(":SOUR:CORR:RVEL:MED?").strip().upper()
        if response.startswith("WAV"):
            return "WAVEGUIDE"
        return response

    def set_source_correction_rvelocity_coax(self, value: float):
        """Sets the relative velocity for coaxial transmission lines. The parameter is unitless.
        Parameters:
        value: The relative velocity factor (numeric value)."""
        self.instrument.write(f":SOUR:CORR:RVEL:COAX {value}")

    def get_source_correction_rvelocity_coax(self) -> float:
        """Returns the relative velocity for coaxial transmission lines."""
        response = self.instrument.query(":SOUR:CORR:RVEL:COAX?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity coax (not numeric): '{response}'")

    def set_source_correction_rvelocity_waveguide(self, value: float):
        """Sets the relative velocity factor for waveguide. The parameter is unitless.
        Parameters:
        value: The relative velocity factor (numeric value)."""
        self.instrument.write(f":SOUR:CORR:RVEL:WAV {value}")

    def get_source_correction_rvelocity_waveguide(self) -> float:
        """Returns the relative velocity factor for waveguide."""
        response = self.instrument.query(":SOUR:CORR:RVEL:WAV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity waveguide (not numeric): '{response}'")

    def set_source_correction_rvelocity_waveguide_fcutoff(self, value: float):
        """Specifies the frequency cutoff of the waveguide medium in Hertz.
        Parameters:
        value: The cutoff frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:CORR:RVEL:WAV:FCUT {value}")

    def get_source_correction_rvelocity_waveguide_fcutoff(self) -> float:
        """Returns the frequency cutoff of the waveguide medium in Hertz."""
        response = self.instrument.query(":SOUR:CORR:RVEL:WAV:FCUT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity waveguide fcutoff (not numeric): '{response}'")

    def set_source_correction_rvelocity_state(self, enable: bool):
        """Enables or disables the relative velocity correction.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CORR:RVEL:STATE {scpi_value}")

    def get_source_correction_rvelocity_state(self) -> bool:
        """Returns True if the relative velocity correction is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:CORR:RVEL:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for relative velocity state: '{response}'")

    
    def set_source_current_attenuation(self, value: float):
        """Sets the ATTenuation level for Current.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNIT system."""
        self.instrument.write(f":SOUR:CURR:ATT {value}")

    def get_source_current_attenuation(self) -> float:
        """Returns the ATTenuation level for Current."""
        response = self.instrument.query(":SOUR:CURR:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current attenuation (not numeric): '{response}'")

    def set_source_current_attenuation_auto(self, enable: bool):
        """Couples the attenuator to LEVel for Current.
        Parameters:
        enable: True to enable auto-coupling, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:ATT:AUTO {scpi_value}")

    def get_source_current_attenuation_auto(self) -> bool:
        """Returns True if auto-coupling of attenuator to LEVel is enabled for Current, False if disabled."""
        response = self.instrument.query(":SOUR:CURR:ATT:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current attenuation auto state: '{response}'")

    def set_source_current_alc_state(self, enable: bool):
        """Controls whether the ALC loop controls the output level for Current.
        Parameters:
        enable: True to enable ALC, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:ALC:STATE {scpi_value}")

    def get_source_current_alc_state(self) -> bool:
        """Returns True if the ALC loop controls the output level for Current, False if not."""
        response = self.instrument.query(":SOUR:CURR:ALC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current ALC state: '{response}'")

    def set_source_current_alc_search(self, search_state: str):
        """Enables a form of leveling where the output level is calibrated by momentarily closing the leveling loop for Current.
        Parameters:
        search_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets SEARch to ON and then OFF."""
        normalized_state = search_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid search state: '{search_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:CURR:ALC:SEAR {scpi_value}")

    def get_source_current_alc_search(self) -> str:
        """Returns the search state for Current ALC ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:CURR:ALC:SEAR?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    
    def set_source_current_alc_source(self, source_type: str):
        """Selects the source of the feedback signal for ALC for Current.
        Parameters:
        source_type: INTernal|DIODe|PMETer|MMHead"""
        valid_types = {"INTERNAL", "DIODE", "PMETER", "MMHEAD", "INT", "DIOD", "PMET", "MMH"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid ALC source type: '{source_type}'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "DIODE": scpi_value = "DIOD"
        elif type_upper == "PMETER": scpi_value = "PMET"
        elif type_upper == "MMHEAD": scpi_value = "MMH"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:CURR:ALC::SOUR {scpi_value}")

    def get_source_current_alc_source(self) -> str:
        """Returns the source of the feedback signal for ALC for Current ('INTernal', 'DIODe', 'PMETer', or 'MMHead')."""
        response = self.instrument.query(":SOUR:CURR:ALC::SOUR?").strip().upper()
        if response.startswith("INT"): return "INTernal"
        elif response.startswith("DIOD"): return "DIODe"
        elif response.startswith("PMET"): return "PMETer"
        elif response.startswith("MMH"): return "MMHead"
        return response

    def set_source_current_alc_bandwidth(self, value: float):
        """Controls the bandwidth of the ALC feedback signal for Current in Hz.
        Parameters:
        value: The bandwidth in Hz (numeric value)."""
        self.instrument.write(f":SOUR:CURR:ALC:BAND {value}")

    def get_source_current_alc_bandwidth(self) -> float:
        """Returns the bandwidth of the ALC feedback signal for Current in Hz."""
        response = self.instrument.query(":SOUR:CURR:ALC:BAND?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current ALC bandwidth (not numeric): '{response}'")

    def set_source_current_alc_bandwidth_auto(self, auto_state: str):
        """Couples the bandwidth of the ALC feedback signal to instrument-dependent parameters for Current.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:CURR:ALC:BAND:AUTO {scpi_value}")

    def get_source_current_alc_bandwidth_auto(self) -> str:
        """Returns the auto state of the ALC bandwidth for Current ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:CURR:ALC:BAND:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_current_center(self, value: float):
        """Sets the center amplitude for Current.
        Parameters:
        value: The center amplitude (numeric value)."""
        self.instrument.write(f":SOUR:CURR:CENT {value}")

    def get_source_current_center(self) -> float:
        """Returns the center amplitude for Current."""
        response = self.instrument.query(":SOUR:CURR:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current center (not numeric): '{response}'")

    def set_source_current_level_immediate_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Current in terms of current operating units.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:IMM:AMPL {value}")

    def get_source_current_level_immediate_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LEV:IMM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level immediate amplitude (not numeric): '{response}'")

    
    def set_source_current_level_immediate_amplitude_auto(self, auto_state: str):
        """If AUTO ON is selected, the voltage setting will be adjusted automatically when a new current setting (with the existing voltage setting) exceeds the maximum power limit.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:CURR:LEV:IMM:AMPL:AUTO {scpi_value}")

    def get_source_current_level_immediate_amplitude_auto(self) -> str:
        """Returns the auto state of the current level immediate amplitude ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:CURR:LEV:IMM:AMPL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_current_level_immediate_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal specified in AMPLitude, in terms of current operating units for Current.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:IMM:OFFS {value}")

    def get_source_current_level_immediate_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LEV:IMM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level immediate offset (not numeric): '{response}'")

    def set_source_current_level_immediate_high(self, value: float):
        """Sets the more positive peak of a time varying signal for Current.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:IMM:HIGH {value}")

    def get_source_current_level_immediate_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LEV:IMM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level immediate high (not numeric): '{response}'")

    def set_source_current_level_immediate_low(self, value: float):
        """Sets the more negative peak of a time varying signal for Current.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:IMM:LOW {value}")

    def get_source_current_level_immediate_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LEV:IMM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level immediate low (not numeric): '{response}'")

    
    def set_source_current_level_triggered_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Current, to be transferred upon trigger.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:TRIG:AMPL {value}")

    def get_source_current_level_triggered_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Current (triggered)."""
        response = self.instrument.query(":SOUR:CURR:LEV:TRIG:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level triggered amplitude (not numeric): '{response}'")

    def set_source_current_level_triggered_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal for Current, to be transferred upon trigger.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:TRIG:OFFS {value}")

    def get_source_current_level_triggered_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Current (triggered)."""
        response = self.instrument.query(":SOUR:CURR:LEV:TRIG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level triggered offset (not numeric): '{response}'")

    def set_source_current_level_triggered_high(self, value: float):
        """Sets the more positive peak of a time varying signal for Current, to be transferred upon trigger.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:TRIG:HIGH {value}")

    def get_source_current_level_triggered_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Current (triggered)."""
        response = self.instrument.query(":SOUR:CURR:LEV:TRIG:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level triggered high (not numeric): '{response}'")

    def set_source_current_level_triggered_low(self, value: float):
        """Sets the more negative peak of a time varying signal for Current, to be transferred upon trigger.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LEV:TRIG:LOW {value}")

    def get_source_current_level_triggered_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Current (triggered)."""
        response = self.instrument.query(":SOUR:CURR:LEV:TRIG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current level triggered low (not numeric): '{response}'")

    def set_source_current_limit_amplitude(self, value: float):
        """Sets the limit on the actual magnitude of the unswept output signal for Current.
        Parameters:
        value: The amplitude limit (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LIM:AMPL {value}")

    def get_source_current_limit_amplitude(self) -> float:
        """Returns the limit on the actual magnitude of the unswept output signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LIM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current limit amplitude (not numeric): '{response}'")

    
    def set_source_current_limit_offset(self, value: float):
        """Sets a non-time varying component limit of signal that is added to the time varying signal for Current.
        Parameters:
        value: The offset limit (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LIM:OFFS {value}")

    def get_source_current_limit_offset(self) -> float:
        """Returns a non-time varying component limit of signal that is added to the time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LIM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current limit offset (not numeric): '{response}'")

    def set_source_current_limit_high(self, value: float):
        """Sets the more positive peak limit of a time varying signal for Current.
        Parameters:
        value: The high peak limit (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LIM:HIGH {value}")

    def get_source_current_limit_high(self) -> float:
        """Returns the more positive peak limit of a time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current limit high (not numeric): '{response}'")

    def set_source_current_limit_low(self, value: float):
        """Sets the more negative peak limit of a time varying signal for Current.
        Parameters:
        value: The low peak limit (numeric value)."""
        self.instrument.write(f":SOUR:CURR:LIM:LOW {value}")

    def get_source_current_limit_low(self) -> float:
        """Returns the more negative peak limit of a time varying signal for Current."""
        response = self.instrument.query(":SOUR:CURR:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current limit low (not numeric): '{response}'")

    def set_source_current_limit_state(self, enable: bool):
        """Controls whether the LIMit is enabled for Current.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:LIM:STATE {scpi_value}")

    def get_source_current_limit_state(self) -> bool:
        """Returns True if the LIMit is enabled for Current, False if disabled."""
        response = self.instrument.query(":SOUR:CURR:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current limit state: '{response}'")

    def set_source_current_manual(self, value: float):
        """Allows manual adjustment of the amplitude between the sweep limits for Current.
        Parameters:
        value: The manual amplitude value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:MAN {value}")

    def get_source_current_manual(self) -> float:
        """Returns the manual amplitude for Current."""
        response = self.instrument.query(":SOUR:CURR:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current manual (not numeric): '{response}'")

    def set_source_current_mode(self, mode_type: str):
        """Determines which set of commands control the amplitude subsystem for Current.
        Parameters:
        mode_type: FIXed|SWEep|LIST"""
        valid_types = {"FIXED", "SWEEP", "LIST", "FIX", "SWE"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid current mode: '{mode_type}'. Must be 'FIXed', 'SWEep', or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:CURR:MODE {scpi_value}")

    def get_source_current_mode(self) -> str:
        """Returns which set of commands control the amplitude subsystem for Current ('FIXed', 'SWEep', or 'LIST')."""
        response = self.instrument.query(":SOUR:CURR:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        elif response.startswith("SWE"):
            return "SWEEP"
        return response

    
    def set_source_current_protection_level(self, value: float):
        """Sets the output level at which the output protection circuit will trip for Current.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SOUR:CURR:PROT:LEV {value}")

    def get_source_current_protection_level(self) -> float:
        """Returns the output level at which the output protection circuit will trip for Current."""
        response = self.instrument.query(":SOUR:CURR:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current protection level (not numeric): '{response}'")

    def set_source_current_protection_state(self, enable: bool):
        """Controls whether the output protection circuit is enabled for Current.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:PROT:STATE {scpi_value}")

    def get_source_current_protection_state(self) -> bool:
        """Returns True if the output protection circuit is enabled for Current, False if disabled."""
        response = self.instrument.query(":SOUR:CURR:PROT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current protection state: '{response}'")

    def get_source_current_protection_tripped(self) -> bool:
        """Returns a 1 if the protection circuit is tripped for Current and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:CURR:PROT:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for current protection tripped status: '{response}'")

    def clear_source_current_protection(self):
        """Causes the protection circuit to be cleared for Current.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:CURR:PROT:CLE")

    def set_source_current_range(self, value: float):
        """Sets a range for the output amplitude for Current.
        Parameters:
        value: The range value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:RANG {value}")

    def get_source_current_range(self) -> float:
        """Returns the range for the output amplitude for Current."""
        response = self.instrument.query(":SOUR:CURR:RANG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current range (not numeric): '{response}'")

    def set_source_current_range_auto(self, auto_state: str):
        """Couples the RANGe to an instrument-determined value for Current.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:CURR:RANG:AUTO {scpi_value}")

    def get_source_current_range_auto(self) -> str:
        """Returns the auto state of the Current range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:CURR:RANG:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_current_reference(self, value: float):
        """Sets a reference value for Current which, if STATe is ON, allows all amplitude parameters to be queried/set as relative to the reference value.
        Parameters:
        value: The reference value (numeric value)."""
        self.instrument.write(f":SOUR:CURR:REF {value}")

    def get_source_current_reference(self) -> float:
        """Returns the reference value for Current."""
        response = self.instrument.query(":SOUR:CURR:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current reference (not numeric): '{response}'")

    
    def set_source_current_reference_state(self, enable: bool):
        """Determines whether amplitude is measured/output in absolute or relative mode for Current.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:REF:STATE {scpi_value}")

    def get_source_current_reference_state(self) -> bool:
        """Returns True if amplitude is measured/output in relative mode for Current, False for absolute mode."""
        response = self.instrument.query(":SOUR:CURR:REF:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current reference state: '{response}'")

    def set_source_current_slew(self, value: float):
        """Sets the slew rate of the output change when a new output level is programmed for Current. Units are (currently active) amplitude unit/sec.
        Parameters:
        value: The slew rate (numeric value)."""
        self.instrument.write(f":SOUR:CURR:SLEW {value}")

    def get_source_current_slew(self) -> float:
        """Returns the slew rate of the output change for Current."""
        response = self.instrument.query(":SOUR:CURR:SLEW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current slew (not numeric): '{response}'")

    def set_source_current_span(self, value: float):
        """Sets the amplitude span for Current. If current amplitude unit is logarithmic (dBm, dBuV, etc), then unit of SPAN is dB. Otherwise SPAN is programmed in current amplitude unit.
        Parameters:
        value: The amplitude span (numeric value)."""
        self.instrument.write(f":SOUR:CURR:SPAN {value}")

    def get_source_current_span(self) -> float:
        """Returns the amplitude span for Current."""
        response = self.instrument.query(":SOUR:CURR:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current span (not numeric): '{response}'")

    def source_current_span_full(self):
        """Sets STARt amplitude to its minimum value and STOP amplitude to its maximum value for Current. CENTer amplitude and SPAN are set to their coupled values.
        Notes: This command is an event rather than a state."""
        self.instrument.write(":SOUR:CURR:SPAN:FULL")

    def set_source_current_span_hold(self, enable: bool):
        """Provides a mechanism to prevent the SPAN from being changed implicitly by the defined coupling between STARt, STOP, CENTer and SPAN for Current.
        Parameters:
        enable: True to hold SPAN, False to allow changes."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:CURR:SPAN:HOLD {scpi_value}")

    def get_source_current_span_hold(self) -> bool:
        """Returns True if SPAN is held for Current, False if not."""
        response = self.instrument.query(":SOUR:CURR:SPAN:HOLD?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current span hold state: '{response}'")

    def set_source_current_span_link(self, link_parameter: str):
        """Allows the default couplings for SPAN to be overridden for Current. LINK selects the parameter, either CENTer, STARt or STOP, that shall not be changed when SPAN’s value is changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:CURR:SPAN:LINK {scpi_value}")

    def get_source_current_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN’s value is changed for Current ('CENTer', 'STARt', or 'STOP')."""
        response = self.instrument.query(":SOUR:CURR:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        return response

    def set_source_current_start(self, value: float):
        """Sets STARt amplitude for Current.
        Parameters:
        value: The start amplitude (numeric value)."""
        self.instrument.write(f":SOUR:CURR:STAR {value}")

    def get_source_current_start(self) -> float:
        """Returns STARt amplitude for Current."""
        response = self.instrument.query(":SOUR:CURR:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current start (not numeric): '{response}'")

    
    def set_source_current_stop(self, value: float):
        """Sets STOP amplitude for Current.
        Parameters:
        value: The stop amplitude (numeric value)."""
        self.instrument.write(f":SOUR:CURR:STOP {value}")

    def get_source_current_stop(self) -> float:
        """Returns STOP amplitude for Current."""
        response = self.instrument.query(":SOUR:CURR:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current stop (not numeric): '{response}'")

    
    def set_source_dm_format(self, format_type: str):
        """Sets the format type to be employed for Digital Modulation.
        Parameters:
        format_type: BPSK|PSK2|QPSK|PSK4|PSK8|QAM16|QAM64|QAM256|QAM1024|PRS9|PRS25|PRS49|PRS81"""
        valid_types = {
            "BPSK", "PSK2", "QPSK", "PSK4", "PSK8", "QAM16", "QAM64", "QAM256", "QAM1024",
            "PRS9", "PRS25", "PRS49", "PRS81"
        }
        type_upper = format_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid DM format type: '{format_type}'.")
        self.instrument.write(f":SOUR:DM:FORM {type_upper}")

    def get_source_dm_format(self) -> str:
        """Returns the format type employed for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:FORM?").strip().upper()
        return response

    def set_source_dm_state(self, enable: bool):
        """Turns the digital modulation subsystem ON or OFF.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:DM:STATE {scpi_value}")

    def get_source_dm_state(self) -> bool:
        """Returns True if the digital modulation subsystem is ON, False if OFF."""
        response = self.instrument.query(":SOUR:DM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for DM state: '{response}'")

    def set_source_dm_source(self, source_type: str):
        """Sets the source of digital modulation data.
        Parameters:
        source_type: EXTernal|PRBS|CALibrate"""
        valid_types = {"EXTERNAL", "PRBS", "CALIBRATE", "EXT", "CAL"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid DM source type: '{source_type}'. Must be 'EXTernal', 'PRBS', or 'CALibrate'.")

        if type_upper == "EXTERNAL": scpi_value = "EXT"
        elif type_upper == "CALIBRATE": scpi_value = "CAL"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM::SOUR {scpi_value}")

    def get_source_dm_source(self) -> str:
        """Returns the source of digital modulation data ('EXTernal', 'PRBS', or 'CALibrate')."""
        response = self.instrument.query(":SOUR:DM::SOUR?").strip().upper()
        if response.startswith("EXT"):
            return "EXTERNAL"
        elif response.startswith("CAL"):
            return "CALIBRATE"
        return response

    def set_source_dm_filter_source(self, source_type: str):
        """Allows a choice between INTernal or EXTernal I and Q filters for Digital Modulation.
        Parameters:
        source_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid filter source type: '{source_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:FILT::SOUR {scpi_value}")

    def get_source_dm_filter_source(self) -> str:
        """Returns the choice between INTernal or EXTernal I and Q filters for Digital Modulation ('INTernal' or 'EXTernal')."""
        response = self.instrument.query(":SOUR:DM:FILT::SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    def set_source_dm_filter_icorrection(self, value: float):
        """Allows the entry of gain information about the EXTernal I filter.
        Parameters:
        value: The gain value (numeric value) in dB."""
        self.instrument.write(f":SOUR:DM:FILT:ICOR {value}")

    def get_source_dm_filter_icorrection(self) -> float:
        """Returns the gain information about the EXTernal I filter."""
        response = self.instrument.query(":SOUR:DM:FILT:ICOR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM filter I correction (not numeric): '{response}'")

    def set_source_dm_filter_qcorrection(self, value: float):
        """Allows the entry of gain information about the EXTernal Q filter.
        Parameters:
        value: The gain value (numeric value) in dB."""
        self.instrument.write(f":SOUR:DM:FILT:QCOR {value}")

    def get_source_dm_filter_qcorrection(self) -> float:
        """Returns the gain information about the EXTernal Q filter."""
        response = self.instrument.query(":SOUR:DM:FILT:QCOR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM filter Q correction (not numeric): '{response}'")

    
    def set_source_dm_iqratio_state(self, enable: bool):
        """Turns ON and OFF the gain imbalance correction between the I and Q channels for Digital Modulation.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:DM:IQR:STATE {scpi_value}")

    def get_source_dm_iqratio_state(self) -> bool:
        """Returns True if the gain imbalance correction is ON, False if OFF for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:IQR:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for DM IQ Ratio state: '{response}'")

    def set_source_dm_iqratio_magnitude(self, value: float):
        """Specifies the correction for the gain imbalance between the I and Q channels for Digital Modulation. This value is equal to I/Q.
        Parameters:
        value: The magnitude value (numeric value) in dB."""
        self.instrument.write(f":SOUR:DM:IQR:MAGN {value}")

    def get_source_dm_iqratio_magnitude(self) -> float:
        """Returns the correction for the gain imbalance between the I and Q channels for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:IQR:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM IQ Ratio magnitude (not numeric): '{response}'")

    def set_source_dm_leakage_state(self, enable: bool):
        """Turns carrier leakage ON and OFF for Digital Modulation.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:DM:LEAK:STATE {scpi_value}")

    def get_source_dm_leakage_state(self) -> bool:
        """Returns True if carrier leakage is ON, False if OFF for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:LEAK:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for DM Leakage state: '{response}'")

    def set_source_dm_leakage_magnitude(self, value: float):
        """Specifies the magnitude of carrier leakage relative to the full scale of the signal for Digital Modulation.
        Parameters:
        value: The magnitude value (numeric value) in dB."""
        self.instrument.write(f":SOUR:DM:LEAK:MAGN {value}")

    def get_source_dm_leakage_magnitude(self) -> float:
        """Returns the magnitude of carrier leakage relative to the full scale of the signal for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:LEAK:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM Leakage magnitude (not numeric): '{response}'")

    def set_source_dm_leakage_angle(self, value: float):
        """Specifies the angle of carrier leakage for Digital Modulation.
        Parameters:
        value: The angle value (numeric value)."""
        self.instrument.write(f":SOUR:DM:LEAK:ANGLe {value}")

    def get_source_dm_leakage_angle(self) -> float:
        """Returns the angle of carrier leakage for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:LEAK:ANGLe?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM Leakage angle (not numeric): '{response}'")

    def set_source_dm_quadrature_state(self, enable: bool):
        """Turns ON or OFF the quadrature angle correction for Digital Modulation.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:DM:QUAD:STATE {scpi_value}")

    def get_source_dm_quadrature_state(self) -> bool:
        """Returns True if the quadrature angle correction is ON, False if OFF for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:QUAD:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for DM Quadrature state: '{response}'")

    
    def set_source_dm_quadrature_angle(self, value: float):
        """Specifies the angle of quadrature correction for Digital Modulation.
        Parameters:
        value: The angle value (numeric value)."""
        self.instrument.write(f":SOUR:DM:QUAD:ANGLe {value}")

    def get_source_dm_quadrature_angle(self) -> float:
        """Returns the angle of quadrature correction for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:QUAD:ANGLe?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM Quadrature angle (not numeric): '{response}'")

    def set_source_dm_coupling_all(self, coupling_type: str):
        """Sets the coupling of both the clock and data inputs to the instrument for Digital Modulation.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:COUP:ALL {scpi_value}")

    def set_source_dm_coupling_data(self, coupling_type: str):
        """Sets the coupling of the data inputs to the instrument for Digital Modulation.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:COUP:DATA {scpi_value}")

    def get_source_dm_coupling_data(self) -> str:
        """Returns the coupling of the data inputs to the instrument for Digital Modulation ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(":SOUR:DM:COUP:DATA?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_dm_coupling_clock(self, coupling_type: str):
        """Sets the coupling of the clock inputs to the instrument for Digital Modulation.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:COUP:CLOC {scpi_value}")

    def get_source_dm_coupling_clock(self) -> str:
        """Returns the coupling of the clock inputs to the instrument for Digital Modulation ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(":SOUR:DM:COUP:CLOC?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_dm_threshold_all(self, value: float):
        """Sets the threshold of both the clock and data inputs to the instrument for Digital Modulation.
        Parameters:
        value: The threshold value (numeric value)."""
        self.instrument.write(f":SOUR:DM:THRES:ALL {value}")

    def set_source_dm_threshold_data(self, value: float):
        """Sets the threshold of the data inputs to the instrument for Digital Modulation.
        Parameters:
        value: The threshold value (numeric value)."""
        self.instrument.write(f":SOUR:DM:THRES:DATA {value}")

    def get_source_dm_threshold_data(self) -> float:
        """Returns the threshold of the data inputs to the instrument for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:THRES:DATA?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM Threshold Data (not numeric): '{response}'")

    def set_source_dm_threshold_clock(self, value: float):
        """Sets the threshold of the clock inputs to the instrument for Digital Modulation.
        Parameters:
        value: The threshold value (numeric value)."""
        self.instrument.write(f":SOUR:DM:THRES:CLOC {value}")

    def get_source_dm_threshold_clock(self) -> float:
        """Returns the threshold of the clock inputs to the instrument for Digital Modulation."""
        response = self.instrument.query(":SOUR:DM:THRES:CLOC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for DM Threshold Clock (not numeric): '{response}'")

    
    def set_source_dm_dmode(self, dmode_type: str):
        """Sets the data transfer mode for Digital Modulation.
        Parameters:
        dmode_type: SERial|PARallel"""
        valid_types = {"SERIAL", "PARALLEL", "SER", "PAR"}
        type_upper = dmode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid DM DMODe type: '{dmode_type}'. Must be 'SERial' or 'PARallel'.")

        if type_upper == "SERIAL": scpi_value = "SER"
        elif type_upper == "PARALLEL": scpi_value = "PAR"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:DMOD {scpi_value}")

    def get_source_dm_dmode(self) -> str:
        """Returns the data transfer mode for Digital Modulation ('SERial' or 'PARallel')."""
        response = self.instrument.query(":SOUR:DM:DMOD?").strip().upper()
        if response.startswith("SER"):
            return "SERIAL"
        elif response.startswith("PAR"):
            return "PARALLEL"
        return response

    def set_source_dm_frame_source(self, source_type: str):
        """Selects the source frame when data is transferred serially for Digital Modulation.
        Parameters:
        source_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid frame source type: '{source_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:FRAM::SOUR {scpi_value}")

    def get_source_dm_frame_source(self) -> str:
        """Returns the source frame when data is transferred serially for Digital Modulation ('INTernal' or 'EXTernal')."""
        response = self.instrument.query(":SOUR:DM:FRAM::SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    def set_source_dm_polarity_all(self, polarity_type: str):
        """Sets the polarity of all the clock and data inputs to the instrument for Digital Modulation.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:POL:ALL {scpi_value}")

    def set_source_dm_polarity_ich_n(self, channel_number: int, polarity_type: str):
        """Selects the polarity of data inputs for the I channel for Digital Modulation.
        Parameters:
        channel_number: The data input number (0-1 for log4, 0-4 for QAM1024).
        polarity_type: NORMal|INVerted"""
        if not (0 <= channel_number <= 4): # Based on example, 0-1 for log4 implies up to 4 for QAM1024
            raise ValueError("Channel number must be between 0 and 4.")
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:POL:I{channel_number} {scpi_value}")

    def get_source_dm_polarity_ich_n(self, channel_number: int) -> str:
        """Returns the polarity of data inputs for the I channel for Digital Modulation ('NORMal' or 'INVerted')."""
        if not (0 <= channel_number <= 4):
            raise ValueError("Channel number must be between 0 and 4.")
        response = self.instrument.query(f":SOUR:DM:POL:I{channel_number}?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_dm_polarity_qch_n(self, channel_number: int, polarity_type: str):
        """Selects the polarity of data inputs for the Q channel for Digital Modulation.
        Parameters:
        channel_number: The data input number (0-1 for log4, 0-4 for QAM1024).
        polarity_type: NORMal|INVerted"""
        if not (0 <= channel_number <= 4):
            raise ValueError("Channel number must be between 0 and 4.")
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:POL:Q{channel_number} {scpi_value}")

    def get_source_dm_polarity_qch_n(self, channel_number: int) -> str:
        """Returns the polarity of data inputs for the Q channel for Digital Modulation ('NORMal' or 'INVerted')."""
        if not (0 <= channel_number <= 4):
            raise ValueError("Channel number must be between 0 and 4.")
        response = self.instrument.query(f":SOUR:DM:POL:Q{channel_number}?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_dm_polarity_iclock(self, polarity_type: str):
        """Selects the polarity of the I channel clock input for Digital Modulation.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:POL:ICLOC {scpi_value}")

    def get_source_dm_polarity_iclock(self) -> str:
        """Returns the polarity of the I channel clock input for Digital Modulation ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:DM:POL:ICLOC?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_dm_polarity_qclock(self, polarity_type: str):
        """Selects the polarity of the Q channel clock input for Digital Modulation.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:POL:QCLOC {scpi_value}")

    def get_source_dm_polarity_qclock(self) -> str:
        """Returns the polarity of the Q channel clock input for Digital Modulation ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:DM:POL:QCLOC?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    
    def set_source_dm_clock_source(self, source_type: str):
        """Selects either no clock (asynchronous operation) or external clocking for Digital Modulation.
        Parameters:
        source_type: NONE|INTernal|EXTernal"""
        valid_types = {"NONE", "INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid clock source type: '{source_type}'. Must be 'NONE', 'INTernal', or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:DM:CLOC::SOUR {scpi_value}")

    def get_source_dm_clock_source(self) -> str:
        """Returns the clock source for Digital Modulation ('NONE', 'INTernal', or 'EXTernal')."""
        response = self.instrument.query(":SOUR:DM:CLOC::SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    
    def set_source_fm_coupling(self, coupling_type: str):
        """Sets the coupling between the modulator and the modulating signal for FM.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FM:COUP {scpi_value}")

    def get_source_fm_coupling(self) -> str:
        """Returns the coupling between the modulator and the modulating signal for FM ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(":SOUR:FM:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_fm_deviation(self, value: float):
        """Sets the modulation DEViation of an FM signal in Hertz (Hz).
        Parameters:
        value: The modulation deviation value (numeric value)."""
        self.instrument.write(f":SOUR:FM:DEV {value}")

    def get_source_fm_deviation(self) -> float:
        """Returns the modulation DEViation of an FM signal in Hertz (Hz)."""
        response = self.instrument.query(":SOUR:FM:DEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for FM deviation (not numeric): '{response}'")

    
    def set_source_fm_external_coupling(self, external_source_number: int, coupling_type: str):
        """Sets the coupling for a specified external FM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FM:EXT{external_source_number}:COUP {scpi_value}")

    def get_source_fm_external_coupling(self, external_source_number: int) -> str:
        """Returns the coupling for a specified external FM signal source ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(f":SOUR:FM:EXT{external_source_number}:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_fm_external_impedance(self, external_source_number: int, value: float):
        """Sets the impedance of the specified external FM signal source in Ohms.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        value: The impedance in Ohms (numeric value)."""
        self.instrument.write(f":SOUR:FM:EXT{external_source_number}:IMP {value}")

    def get_source_fm_external_impedance(self, external_source_number: int) -> float:
        """Returns the impedance of the specified external FM signal source in Ohms."""
        response = self.instrument.query(f":SOUR:FM:EXT{external_source_number}:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for external FM impedance (not numeric): '{response}'")

    def set_source_fm_external_polarity(self, external_source_number: int, polarity_type: str):
        """Sets the polarity for a specified external FM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FM:EXT{external_source_number}:POL {scpi_value}")

    def get_source_fm_external_polarity(self, external_source_number: int) -> str:
        """Returns the polarity for a specified external FM signal source ('NORMal' or 'INVerted')."""
        response = self.instrument.query(f":SOUR:FM:EXT{external_source_number}:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_fm_internal_frequency(self, internal_source_number: int, value: float):
        """Sets the frequency of the specified internal FM signal source in Hertz (Hz).
        Parameters:
        internal_source_number: The internal signal source number (e.g., 1).
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:FM:INT{internal_source_number}:FREQ {value}")

    def get_source_fm_internal_frequency(self, internal_source_number: int) -> float:
        """Returns the frequency of the specified internal FM signal source in Hertz (Hz)."""
        response = self.instrument.query(f":SOUR:FM:INT{internal_source_number}:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for internal FM frequency (not numeric): '{response}'")

    def set_source_fm_mode(self, mode_type: str):
        """Sets the synthesis mode employed in generating the FM signal.
        Parameters:
        mode_type: LOCKed|UNLocked"""
        valid_types = {"LOCKED", "UNLOCKED", "LOCK", "UNL"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid FM mode: '{mode_type}'. Must be 'LOCKed' or 'UNLocked'.")

        if type_upper == "LOCKED": scpi_value = "LOCK"
        elif type_upper == "UNLOCKED": scpi_value = "UNL"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FM:MODE {scpi_value}")

    def get_source_fm_mode(self) -> str:
        """Returns the synthesis mode employed in generating the FM signal ('LOCKed' or 'UNLocked')."""
        response = self.instrument.query(":SOUR:FM:MODE?").strip().upper()
        if response.startswith("LOCK"):
            return "LOCKED"
        elif response.startswith("UNL"):
            return "UNLOCKED"
        return response

    
    def set_source_fm_polarity(self, polarity_type: str):
        """Sets the polarity between the modulator and the modulating signal for FM.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FM:POL {scpi_value}")

    def get_source_fm_polarity(self) -> str:
        """Returns the polarity between the modulator and the modulating signal for FM ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:FM:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_fm_sensitivity(self, value: float):
        """Controls the modulation deviation by setting a sensitivity to the modulation signal voltage level for FM. Unit is Hertz/Volt (Hz/V).
        Parameters:
        value: The sensitivity value (numeric value)."""
        self.instrument.write(f":SOUR:FM:SENS {value}")

    def get_source_fm_sensitivity(self) -> float:
        """Returns the sensitivity in Hertz/Volt (Hz/V) for FM."""
        response = self.instrument.query(":SOUR:FM:SENS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for FM sensitivity (not numeric): '{response}'")

    def set_source_fm_source(self, sources: list[str]):
        """Selects the source(s) for the modulating signal for FM.
        Parameters:
        sources: A list of strings, each being 'EXTernal' or 'INTernal', optionally followed by a number (e.g., ["INTernal1", "EXTernal"])."""
        formatted_sources = []
        for src in sources:
            src_upper = src.upper()
            if src_upper.startswith("INTERNAL"):
                formatted_sources.append(f"INT{src_upper[8:]}") # Handle INTernal1 -> INT1
            elif src_upper.startswith("EXTERNAL"):
                formatted_sources.append(f"EXT{src_upper[8:]}") # Handle EXTernal1 -> EXT1
            else:
                raise ValueError(f"Invalid source type: '{src}'. Must be 'INTernal' or 'EXTernal'.")
        source_str = ",".join(formatted_sources)
        self.instrument.write(f":SOUR:FM::SOUR {source_str}")

    def get_source_fm_source(self) -> list[str]:
        """Returns the selected source(s) for the modulating signal for FM.
        Returns: A list of source strings (e.g., ['INTernal', 'EXTernal1'])."""
        response = self.instrument.query(":SOUR:FM::SOUR?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., "INT,EXT1")
        return [s.replace("INT", "INTernal").replace("EXT", "EXTernal") for s in response.split(',')]

    def set_source_fm_state(self, enable: bool):
        """Turns frequency modulation ON or OFF.
        Parameters:
        enable: True to turn FM modulation ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:FM:STATE {scpi_value}")

    def get_source_fm_state(self) -> bool:
        """Returns True if frequency modulation is ON, False if OFF."""
        response = self.instrument.query(":SOUR:FM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for FM state: '{response}'")

    
    def source_force_cndown_initiate(self):
        """Initiates the coast down procedure.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:FORC:CDOW:INIT")

    def set_source_force_cndown_soffset(self, value: float):
        """Sets how much speed offset above the top speed in the CDownSpeed Table to which the dynamometer should be accelerated before beginning the coast down.
        Parameters:
        value: Speed Offset in m/s (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CDOW:SOFF {value}")

    def get_source_force_cndown_soffset(self) -> float:
        """Returns the speed offset for the coast down procedure in m/s."""
        response = self.instrument.query(":SOUR:FORC:CDOW:SOFF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force coast down speed offset (not numeric): '{response}'")

    
    def set_source_force_cndown_nruns(self, value: int):
        """Sets the number of coast downs to run.
        Parameters:
        value: Number of runs (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CDOW:NRUN {value}")

    def get_source_force_cndown_nruns(self) -> int:
        """Returns the number of coast downs to run."""
        response = self.instrument.query(":SOUR:FORC:CDOW:NRUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force coast down number of runs (not integer): '{response}'")

    def set_source_force_cndown_rlderivation_facceptance(self, value: float):
        """Sets the maximum acceptable force difference between the force vs. speed curve derived from the dynamometer target and measured coefficients for Road Load Derivation.
        Parameters:
        value: Force Acceptance in N (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CDOW:RLD:FACC {value}")

    def get_source_force_cndown_rlderivation_facceptance(self) -> float:
        """Returns the maximum acceptable force difference for Road Load Derivation in N."""
        response = self.instrument.query(":SOUR:FORC:CDOW:RLD:FACC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force coast down RL derivation force acceptance (not numeric): '{response}'")

    def source_force_cndown_rlderivation_initiate(self):
        """Initiates the Road Load Derivation simulation.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:FORC:CDOW:RLD:INIT")

    
    def set_source_force_cndown_rlderivation_rmaximum(self, value: int):
        """Sets the maximum number of coast down runs the Road Load Derivation test will run without convergence.
        Parameters:
        value: Runs Maximum (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CDOW:RLD:RMAX {value}")

    def get_source_force_cndown_rlderivation_rmaximum(self) -> int:
        """Returns the maximum number of coast down runs the Road Load Derivation test will run without convergence."""
        response = self.instrument.query(":SOUR:FORC:CDOW:RLD:RMAX?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force coast down RL derivation runs maximum (not integer): '{response}'")

    def set_source_force_cndown_rlderivation_rverify(self, value: int):
        """Sets the maximum number of verification coast down runs after convergence of the Road Load Derivation procedure.
        Parameters:
        value: Runs to Verify (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CDOW:RLD:RVER {value}")

    def get_source_force_cndown_rlderivation_rverify(self) -> int:
        """Returns the maximum number of verification coast down runs after convergence of the Road Load Derivation procedure."""
        response = self.instrument.query(":SOUR:FORC:CDOW:RLD:RVER?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force coast down RL derivation runs to verify (not integer): '{response}'")

    
    def set_source_force_configure_abrake_gain(self, value: float):
        """Sets the augmented brake gain.
        Parameters:
        value: The gain value (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:ABR:GAIN {value}")

    def get_source_force_configure_abrake_gain(self) -> float:
        """Returns the augmented brake gain."""
        response = self.instrument.query(":SOUR:FORC:CONF:ABR:GAIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure abrake gain (not numeric): '{response}'")

    def set_source_force_configure_abrake_state(self, enable: bool):
        """Sets the augmented brake simulation state.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:FORC:CONF:ABR:STATE {scpi_value}")

    def get_source_force_configure_abrake_state(self) -> bool:
        """Returns True if the augmented brake simulation state is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:FORC:CONF:ABR:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for force configure abrake state: '{response}'")

    def set_source_force_configure_abrake_threshold(self, value: float):
        """Sets the vehicle force absorption level in N to initiate a simulated braking force for the non-rotating wheel brakes.
        Parameters:
        value: The threshold in N (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:ABR:THRES {value}")

    def get_source_force_configure_abrake_threshold(self) -> float:
        """Returns the vehicle force absorption level in N for augmented brake threshold."""
        response = self.instrument.query(":SOUR:FORC:CONF:ABR:THRES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure abrake threshold (not numeric): '{response}'")

    def set_source_force_configure_grade_level(self, value: float):
        """Sets the grade force in units of Percent Grade.
        Parameters:
        value: The grade level (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:GRAD:LEV {value}")

    def get_source_force_configure_grade_level(self) -> float:
        """Returns the grade force in units of Percent Grade."""
        response = self.instrument.query(":SOUR:FORC:CONF:GRAD:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure grade level (not numeric): '{response}'")

    def set_source_force_configure_grade_source(self, source_type: str):
        """Sets the source for grade.
        Parameters:
        source_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid grade source type: '{source_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FORC:CONF:GRAD::SOUR {scpi_value}")

    def get_source_force_configure_grade_source(self) -> str:
        """Returns the source for grade ('INTernal' or 'EXTernal')."""
        response = self.instrument.query(":SOUR:FORC:CONF:GRAD::SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    
    def set_source_force_configure_grade_state(self, enable: bool):
        """Sets the grade simulation state.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:FORC:CONF:GRAD:STATE {scpi_value}")

    def get_source_force_configure_grade_state(self) -> bool:
        """Returns True if the grade simulation state is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:FORC:CONF:GRAD:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for force configure grade state: '{response}'")

    def set_source_force_configure_vehicle_dcoefficient(self, coefficients: list[float]):
        """Sets the coefficients of the road-load polynomial for the force to be simulated.
        Parameters:
        coefficients: A list of 3 or 4 numeric values [N, N/(m/s), N/((m/s)^2), N/((m/s)^3)]."""
        if not (3 <= len(coefficients) <= 4):
            raise ValueError("Coefficients list must contain 3 or 4 numeric values.")
        coeff_str = ",".join(map(str, coefficients))
        self.instrument.write(f":SOUR:FORC:CONF:VEH:DCO {coeff_str}")

    def get_source_force_configure_vehicle_dcoefficient(self) -> list[float]:
        """Returns the active dynamometer coefficients of the road-load polynomial."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:DCO?").strip()
        try:
            return [float(c) for c in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for force configure vehicle DCoeff (not numeric list): '{response}'")

    def set_source_force_configure_vehicle_dinertia(self, value: float):
        """Sets the "Inertia" (in kg) to be simulated by the dynamometer.
        Parameters:
        value: Dynamometer-setting Inertia in kg (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:VEH:DIN {value}")

    def get_source_force_configure_vehicle_dinertia(self) -> float:
        """Returns the "Inertia" (in kg) to be simulated by the dynamometer."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:DIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure vehicle DINertia (not numeric): '{response}'")

    def set_source_force_configure_vehicle_state(self, enable: bool):
        """Tells the dynamometer that a vehicle is on the rolls.
        Parameters:
        enable: True if vehicle is on rolls, False otherwise."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:FORC:CONF:VEH:STATE {scpi_value}")

    def get_source_force_configure_vehicle_state(self) -> bool:
        """Returns True if the dynamometer is configured for a vehicle on rolls, False otherwise."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for force configure vehicle state: '{response}'")

    
    def set_source_force_configure_vehicle_tcoefficient(self, coefficients: list[float]):
        """Sets the Target Road-Load Coefficients for the road load derivation or coast down procedure.
        Parameters:
        coefficients: A list of 3 or 4 numeric values [N, N/(m/s), N/((m/s)^2), N/((m/s)^3)]."""
        if not (3 <= len(coefficients) <= 4):
            raise ValueError("Coefficients list must contain 3 or 4 numeric values.")
        coeff_str = ",".join(map(str, coefficients))
        self.instrument.write(f":SOUR:FORC:CONF:VEH:TCO {coeff_str}")

    def get_source_force_configure_vehicle_tcoefficient(self) -> list[float]:
        """Returns the Target Road-Load Coefficients."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:TCO?").strip()
        try:
            return [float(c) for c in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for force configure vehicle TCoeff (not numeric list): '{response}'")

    def set_source_force_configure_vehicle_tinertia(self, value: float):
        """Sets the target inertia (kg) for a road load derivation procedure.
        Parameters:
        value: Target-setting Inertia in kg (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:VEH:TIN {value}")

    def get_source_force_configure_vehicle_tinertia(self) -> float:
        """Returns the target inertia (kg) for a road load derivation procedure."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:TIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure vehicle TINertia (not numeric): '{response}'")

    def set_source_force_configure_vehicle_weight(self, value: float):
        """Sets the (kg) weight of vehicle, not including the "inertia weight" of the wheels and drive-train.
        Parameters:
        value: Weight in kg (numeric value)."""
        self.instrument.write(f":SOUR:FORC:CONF:VEH:WEIG {value}")

    def get_source_force_configure_vehicle_weight(self) -> float:
        """Returns the (kg) weight of vehicle."""
        response = self.instrument.query(":SOUR:FORC:CONF:VEH:WEIG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force configure vehicle weight (not numeric): '{response}'")

    def source_force_initiate(self):
        """Initiates force.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:FORC:INIT")

    
    def set_source_force_level(self, value: float):
        """Sets the force set-point in N.
        Parameters:
        value: The force set-point in N (numeric value)."""
        self.instrument.write(f":SOUR:FORC:LEV {value}")

    def get_source_force_level(self) -> float:
        """Returns the force set-point in N."""
        response = self.instrument.query(":SOUR:FORC:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force level (not numeric): '{response}'")

    def source_force_rlsimulation_initiate(self):
        """Initiates the Road Load Simulation.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:FORC:RLS:INIT")

    
    def set_source_frequency_center(self, value: float):
        """Sets the CENTer frequency.
        Parameters:
        value: The center frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:CENT {value}")

    def get_source_frequency_center(self) -> float:
        """Returns the CENTer frequency."""
        response = self.instrument.query(":SOUR:FREQ:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency center (not numeric): '{response}'")

    def set_source_frequency_cw(self, value: float):
        """Selects a frequency of a non-swept signal (Continuous Wave or FIXed).
        Parameters:
        value: The frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:CW {value}")

    def get_source_frequency_cw(self) -> float:
        """Returns the frequency of a non-swept signal (Continuous Wave or FIXed)."""
        response = self.instrument.query(":SOUR:FREQ:CW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency CW (not numeric): '{response}'")

    def set_source_frequency_fixed(self, value: float):
        """Selects a frequency of a non-swept signal (Continuous Wave or FIXed). Alias for set_source_frequency_cw.
        Parameters:
        value: The frequency (numeric value)."""
        self.set_source_frequency_cw(value)

    def get_source_frequency_fixed(self) -> float:
        """Returns the frequency of a non-swept signal (Continuous Wave or FIXed). Alias for get_source_frequency_cw."""
        return self.get_source_frequency_cw()

    def set_source_frequency_cw_auto(self, auto_state: str):
        """Couples the CW frequency to center frequency.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:FREQ:CW:AUTO {scpi_value}")

    def get_source_frequency_cw_auto(self) -> str:
        """Returns the auto state of the CW frequency coupling to center frequency ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:FREQ:CW:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    
    def set_source_frequency_manual(self, value: float):
        """Sets the manual frequency adjustment.
        Parameters:
        value: The manual frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:MAN {value}")

    def get_source_frequency_manual(self) -> float:
        """Returns the manual frequency adjustment."""
        response = self.instrument.query(":SOUR:FREQ:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency manual (not numeric): '{response}'")

    def set_source_frequency_mode(self, mode_type: str):
        """Determines which set of commands control the frequency subsystem.
        Parameters:
        mode_type: CW|FIXed|SWEep|LIST|SENSe"""
        valid_types = {"CW", "FIXED", "SWEEP", "LIST", "SENSE", "FIX", "SWE", "SEN"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid frequency mode: '{mode_type}'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        elif type_upper == "SENSE": scpi_value = "SEN"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:FREQ:MODE {scpi_value}")

    def get_source_frequency_mode(self) -> str:
        """Returns which set of commands control the frequency subsystem ('CW', 'FIXed', 'SWEep', 'LIST', or 'SENSe')."""
        response = self.instrument.query(":SOUR:FREQ:MODE?").strip().upper()
        if response == "CW": return "CW"
        elif response.startswith("FIX"): return "FIXED"
        elif response.startswith("SWE"): return "SWEEP"
        elif response.startswith("LIST"): return "LIST"
        elif response.startswith("SEN"): return "SENSE"
        return response

    def set_source_frequency_multiplier(self, value: float):
        """Sets a reference multiplier for all other frequency settings in the instrument.
        Parameters:
        value: The multiplier value (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:MULT {value}")

    def get_source_frequency_multiplier(self) -> float:
        """Returns the reference multiplier for all other frequency settings in the instrument."""
        response = self.instrument.query(":SOUR:FREQ:MULT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency multiplier (not numeric): '{response}'")

    def set_source_frequency_offset(self, value: float):
        """Sets a reference frequency for all other absolute frequency settings in the instrument.
        Parameters:
        value: The offset frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:OFFS {value}")

    def get_source_frequency_offset(self) -> float:
        """Returns the reference frequency for all other absolute frequency settings in the instrument."""
        response = self.instrument.query(":SOUR:FREQ:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency offset (not numeric): '{response}'")

    
    def set_source_frequency_resolution(self, value: float):
        """Sets the absolute increment/decrement, at which the frequency of the output signal can be changed.
        Parameters:
        value: The resolution in Hertz (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:RES {value}")

    def get_source_frequency_resolution(self) -> float:
        """Returns the absolute increment/decrement, at which the frequency of the output signal can be changed in Hertz."""
        response = self.instrument.query(":SOUR:FREQ:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency resolution (not numeric): '{response}'")

    def set_source_frequency_resolution_auto(self, auto_state: str):
        """Couples the RESolution to an instrument-determined value.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:FREQ:RES:AUTO {scpi_value}")

    def get_source_frequency_resolution_auto(self) -> str:
        """Returns the auto state of the frequency resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:FREQ:RES:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_frequency_span(self, value: float):
        """Sets the frequency SPAN.
        Parameters:
        value: The frequency span (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:SPAN {value}")

    def get_source_frequency_span(self) -> float:
        """Returns the frequency SPAN."""
        response = self.instrument.query(":SOUR:FREQ:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency span (not numeric): '{response}'")

    def source_frequency_span_full(self):
        """Sets STARt frequency to its minimum value, and STOP frequency to its maximum value. CENTer frequency and SPAN are set to their coupled values.
        Notes: This command is an event, rather than a state."""
        self.instrument.write(":SOUR:FREQ:SPAN:FULL")

    def set_source_frequency_span_hold(self, enable: bool):
        """Provides a mechanism to prevent the SPAN from being changed implicitly by the defined coupling between STARt, STOP, CENTer, and SPAN.
        Parameters:
        enable: True to hold SPAN, False to allow changes."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:FREQ:SPAN:HOLD {scpi_value}")

    def get_source_frequency_span_hold(self) -> bool:
        """Returns True if SPAN is held, False if not."""
        response = self.instrument.query(":SOUR:FREQ:SPAN:HOLD?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for frequency span hold state: '{response}'")

    def set_source_frequency_span_link(self, link_parameter: str):
        """Allows the default couplings for SPAN to be overridden. LINK selects the parameter, either CENTer subsystem, STARt or STOP, that shall not be changed when SPAN’s value is changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:FREQ:SPAN:LINK {scpi_value}")

    def get_source_frequency_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN’s value is changed ('CENTer', 'STARt', or 'STOP')."""
        response = self.instrument.query(":SOUR:FREQ:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        return response

    
    def set_source_frequency_start(self, value: float):
        """Sets the STARting frequency.
        Parameters:
        value: The starting frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:STAR {value}")

    def get_source_frequency_start(self) -> float:
        """Returns the STARting frequency."""
        response = self.instrument.query(":SOUR:FREQ:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency start (not numeric): '{response}'")

    def set_source_frequency_stop(self, value: float):
        """Sets the STOP frequency.
        Parameters:
        value: The stop frequency (numeric value)."""
        self.instrument.write(f":SOUR:FREQ:STOP {value}")

    def get_source_frequency_stop(self) -> float:
        """Returns the STOP frequency."""
        response = self.instrument.query(":SOUR:FREQ:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency stop (not numeric): '{response}'")

    
    def set_source_function_shape(self, source_shape: str):
        """Selects the shape of the output signal.
        Parameters:
        source_shape: DC|IMPulse|PCHirp|PRNoise|PULSe|RANDom|SINusoid|SQUare|TRIangle|USER"""
        valid_shapes = {
            "DC", "IMPULSE", "PCHIRP", "PRNOISE", "PULSE", "RANDOM", "SINUSOID", "SQUARE", "TRIANGLE", "USER",
            "IMP", "PCH", "PRN", "PUL", "RAN", "SIN", "SQU", "TRI"
        }
        shape_upper = source_shape.upper()
        if shape_upper not in valid_shapes:
            raise ValueError(f"Invalid source shape: '{source_shape}'.")

        if shape_upper == "IMPULSE": scpi_value = "IMP"
        elif shape_upper == "PCHIRP": scpi_value = "PCH"
        elif shape_upper == "PRNOISE": scpi_value = "PRN"
        elif shape_upper == "PULSE": scpi_value = "PUL"
        elif shape_upper == "RANDOM": scpi_value = "RAN"
        elif shape_upper == "SINUSOID": scpi_value = "SIN"
        elif shape_upper == "SQUARE": scpi_value = "SQU"
        elif shape_upper == "TRIANGLE": scpi_value = "TRI"
        else: scpi_value = shape_upper

        self.instrument.write(f":SOUR:FUNC:SHAP {scpi_value}")

    def get_source_function_shape(self) -> str:
        """Returns the shape of the output signal ('DC', 'IMPulse', 'PCHirp', 'PRNoise', 'PULSe', 'RANDom', 'SINusoid', 'SQUare', 'TRIangle', or 'USER')."""
        response = self.instrument.query(":SOUR:FUNC:SHAP?").strip().upper()
        if response.startswith("IMP"): return "IMPULSE"
        elif response.startswith("PCH"): return "PCHIRP"
        elif response.startswith("PRN"): return "PRNOISE"
        elif response.startswith("PUL"): return "PULSE"
        elif response.startswith("RAN"): return "RANDOM"
        elif response.startswith("SIN"): return "SINUSOID"
        elif response.startswith("SQU"): return "SQUARE"
        elif response.startswith("TRI"): return "TRIANGLE"
        return response

    def set_source_function_mode(self, source_mode: str):
        """Determines which signal characteristic is being controlled.
        Parameters:
        source_mode: VOLTage|CURRent|POWer"""
        valid_modes = {"VOLTAGE", "CURRENT", "POWER", "VOLT", "CURR", "POW"}
        mode_upper = source_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid source mode: '{source_mode}'. Must be 'VOLTage', 'CURRent', or 'POWer'.")

        if mode_upper == "VOLTAGE": scpi_value = "VOLT"
        elif mode_upper == "CURRENT": scpi_value = "CURR"
        elif mode_upper == "POWER": scpi_value = "POW"
        else: scpi_value = mode_upper

        self.instrument.write(f":SOUR:FUNC:MODE {scpi_value}")

    def get_source_function_mode(self) -> str:
        """Returns which signal characteristic is being controlled ('VOLTage', 'CURRent', or 'POWer')."""
        response = self.instrument.query(":SOUR:FUNC:MODE?").strip().upper()
        if response.startswith("VOLT"): return "VOLTAGE"
        elif response.startswith("CURR"): return "CURRENT"
        elif response.startswith("POW"): return "POWER"
        return response

    
    def set_source_list_am_depth(self, values: list[float]):
        """Specifies the AM DEPTh points of the list.
        Parameters:
        values: A list of numeric values for AM Depth."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:AM:DEP {value_str}")

    def get_source_list_am_depth_points(self) -> int:
        """Returns the number of points currently in the AM DEPth list."""
        response = self.instrument.query(":SOUR:LIST:AM:DEP:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list AM depth points (not integer): '{response}'")

    def set_source_list_aprobe(self, values: list[float]):
        """APRobe selects the specified probe/s to control the temperature.
        Parameters:
        values: A list of numeric values for APRobe."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:APRO {value_str}")

    def get_source_list_aprobe_points(self) -> int:
        """Returns the number of points currently in the APRobe list."""
        response = self.instrument.query(":SOUR:LIST:APRO:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list APRobe points (not integer): '{response}'")

    def set_source_list_concurrent(self, values: list[float]):
        """Defines a list which indicates those elements of the signal list which shall be active, when CONCurrent operation is selected.
        Parameters:
        values: A list of numeric values (indexes into the lists)."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:CONC {value_str}")

    
    def set_source_list_concurrent_auto(self, auto_state: str):
        """When on, the CONCurrent list is set to 1-N, where N is the longest list.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:LIST:CONC:AUTO {scpi_value}")

    def get_source_list_concurrent_auto(self) -> str:
        """Returns the auto state of the CONCurrent list ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:LIST:CONC:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def get_source_list_concurrent_points(self) -> int:
        """Returns the number of points currently in the CONCurrent list."""
        response = self.instrument.query(":SOUR:LIST:CONC:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list CONCurrent points (not integer): '{response}'")

    def set_source_list_control_apower(self, states: list[bool]):
        """Turns the APOWer on or off.
        Parameters:
        states: A list of boolean values (True for ON, False for OFF)."""
        value_str = ",".join(["1" if s else "0" for s in states])
        self.instrument.write(f":SOUR:LIST:CONT:APOW {value_str}")

    def get_source_list_control_apower_points(self) -> int:
        """Returns the number of points currently in the APOWer list."""
        response = self.instrument.query(":SOUR:LIST:CONT:APOW:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list control APOWer points (not integer): '{response}'")

    def set_source_list_control_blower(self, states: list[bool]):
        """Turns the BLOWer on or off.
        Parameters:
        states: A list of boolean values (True for ON, False for OFF)."""
        value_str = ",".join(["1" if s else "0" for s in states])
        self.instrument.write(f":SOUR:LIST:CONT:BLOW {value_str}")

    def get_source_list_control_blower_points(self) -> int:
        """Returns the number of points currently in the BLOWer list."""
        response = self.instrument.query(":SOUR:LIST:CONT:BLOW:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list control BLOWer points (not integer): '{response}'")

    def set_source_list_control_compressor(self, states: list[bool]):
        """Turns the COMPressor on or off.
        Parameters:
        states: A list of boolean values (True for ON, False for OFF)."""
        value_str = ",".join(["1" if s else "0" for s in states])
        self.instrument.write(f":SOUR:LIST:CONT:COMP {value_str}")

    def get_source_list_control_compressor_points(self) -> int:
        """Returns the number of points currently in the COMPressor list."""
        response = self.instrument.query(":SOUR:LIST:CONT:COMP:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list control COMPressor points (not integer): '{response}'")

    def set_source_list_count(self, value: int):
        """Controls the number of times the list is sequenced when a trigger is received.
        Parameters:
        value: The count (numeric value)."""
        self.instrument.write(f":SOUR:LIST:COUN {value}")

    def get_source_list_count(self) -> int:
        """Returns the number of times the list is sequenced."""
        response = self.instrument.query(":SOUR:LIST:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list count (not integer): '{response}'")

    def set_source_list_current(self, values: list[float]):
        """Specifies the current points of the lists.
        Parameters:
        values: A list of numeric values for Current."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:CURR {value_str}")

    def get_source_list_current_points(self) -> int:
        """Returns the number of points currently in the CURRent list."""
        response = self.instrument.query(":SOUR:LIST:CURR:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list CURRent points (not integer): '{response}'")

    
    def set_source_list_direction(self, direction_type: str):
        """Specifies the direction that the sequence list is scanned.
        Parameters:
        direction_type: UP|DOWN"""
        valid_types = {"UP", "DOWN"}
        type_upper = direction_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid direction type: '{direction_type}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":SOUR:LIST:DIR {type_upper}")

    def get_source_list_direction(self) -> str:
        """Returns the direction that the sequence list is scanned ('UP' or 'DOWN')."""
        response = self.instrument.query(":SOUR:LIST:DIR?").strip().upper()
        return response

    def set_source_list_dwell(self, values: list[float]):
        """Specifies the dwell time points of the lists.
        Parameters:
        values: A list of numeric values for Dwell time."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:DWEL {value_str}")

    def get_source_list_dwell_points(self) -> int:
        """Returns the number of points currently in the DWELl list."""
        response = self.instrument.query(":SOUR:LIST:DWEL:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list DWELl points (not integer): '{response}'")

    def set_source_list_frequency(self, values: list[float]):
        """Specifies the frequency points of the list set.
        Parameters:
        values: A list of numeric values for Frequency."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:FREQ {value_str}")

    def get_source_list_frequency_points(self) -> int:
        """Returns the number of points currently in the FREQuency list."""
        response = self.instrument.query(":SOUR:LIST:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list FREQuency points (not integer): '{response}'")

    def set_source_list_generation(self, generation_mode: str):
        """Selects how the defined lists are applied in a particular instrument.
        Parameters:
        generation_mode: DSEQuence|SEQuence|DCONcurrent|CONCurrent"""
        valid_modes = {
            "DSEQUENCE", "SEQUENCE", "DCONCURRENT", "CONCURRENT",
            "DSEQ", "SEQ", "DCONC", "CONC"
        }
        mode_upper = generation_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid generation mode: '{generation_mode}'.")

        if mode_upper == "DSEQUENCE": scpi_value = "DSEQ"
        elif mode_upper == "SEQUENCE": scpi_value = "SEQ"
        elif mode_upper == "DCONCURRENT": scpi_value = "DCONC"
        elif mode_upper == "CONCURRENT": scpi_value = "CONC"
        else: scpi_value = mode_upper

        self.instrument.write(f":SOUR:LIST:GEN {scpi_value}")

    def get_source_list_generation(self) -> str:
        """Returns how the defined lists are applied in a particular instrument ('DSEQuence', 'SEQuence', 'DCONcurrent', or 'CONCurrent')."""
        response = self.instrument.query(":SOUR:LIST:GEN?").strip().upper()
        if response.startswith("DSEQ"): return "DSEQUENCE"
        elif response.startswith("SEQ"): return "SEQUENCE"
        elif response.startswith("DCONC"): return "DCONCURRENT"
        elif response.startswith("CONC"): return "CONCURRENT"
        return response

    def set_source_list_pulm_state(self, states: list[bool]):
        """Specifies the PULM STATe points of the list.
        Parameters:
        states: A list of boolean values (True for ON, False for OFF)."""
        value_str = ",".join(["1" if s else "0" for s in states])
        self.instrument.write(f":SOUR:LIST:PULM:STATE {value_str}")

    def get_source_list_pulm_state_points(self) -> int:
        """Returns the number of points currently in the PULM STATe list."""
        response = self.instrument.query(":SOUR:LIST:PULM:STATE:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list PULM state points (not integer): '{response}'")

    
    def set_source_list_power(self, values: list[float]):
        """Specifies the power/amplitude points of the lists.
        Parameters:
        values: A list of numeric values for Power/Amplitude."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:POW {value_str}")

    def get_source_list_power_points(self) -> int:
        """Returns the number of points currently in the POWer list."""
        response = self.instrument.query(":SOUR:LIST:POW:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list POWer points (not integer): '{response}'")

    def set_source_list_resistance(self, values: list[float]):
        """Specifies the resistance points of the lists.
        Parameters:
        values: A list of numeric values for Resistance."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:RES {value_str}")

    def get_source_list_resistance_points(self) -> int:
        """Returns the number of points currently in the RESistance list."""
        response = self.instrument.query(":SOUR:LIST:RES:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list RESistance points (not integer): '{response}'")

    def set_source_list_rtime(self, values: list[float]):
        """Ramp TIMe controls the time required to reach the target temperature.
        Parameters:
        values: A list of numeric values for Ramp Time."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:RTIM {value_str}")

    def get_source_list_rtime_points(self) -> int:
        """Returns the number of points currently in the RTIMe list."""
        response = self.instrument.query(":SOUR:LIST:RTIM:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list RTIMe points (not integer): '{response}'")

    def set_source_list_sequence(self, values: list[float]):
        """Defines a sequence for stepping through the list, when SEQuence operation is selected.
        Parameters:
        values: A list of numeric values (indexes into the lists)."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:SEQ {value_str}")

    
    def set_source_list_sequence_auto(self, auto_state: str):
        """When on, the sequence list is set to 1 through N, where N is the longest list.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:LIST:SEQ:AUTO {scpi_value}")

    def get_source_list_sequence_auto(self) -> str:
        """Returns the auto state of the sequence list ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:LIST:SEQ:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def get_source_list_sequence_points(self) -> int:
        """Returns the number of points currently in the SEQuence list."""
        response = self.instrument.query(":SOUR:LIST:SEQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list SEQuence points (not integer): '{response}'")

    def set_source_list_temperature(self, values: list[float]):
        """TEMPerature is the target temperature.
        Parameters:
        values: A list of numeric values for Temperature."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:TEMP {value_str}")

    def get_source_list_temperature_points(self) -> int:
        """Returns the number of points currently in the TEMPerature list."""
        response = self.instrument.query(":SOUR:LIST:TEMP:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list TEMPerature points (not integer): '{response}'")

    def set_source_list_voltage(self, values: list[float]):
        """Specifies the voltage points of the lists.
        Parameters:
        values: A list of numeric values for Voltage."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:LIST:VOLT {value_str}")

    def get_source_list_voltage_points(self) -> int:
        """Returns the number of points currently in the VOLT list."""
        response = self.instrument.query(":SOUR:LIST:VOLT:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list VOLTage points (not integer): '{response}'")

    
    def set_source_marker_amplitude(self, enable: bool):
        """Controls whether the marker affects the signal.
        Parameters:
        enable: True to modify signal, False to affect only marker output port."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:MARK:AMPL {scpi_value}")

    def get_source_marker_amplitude(self) -> bool:
        """Returns True if the marker affects the signal, False if not."""
        response = self.instrument.query(":SOUR:MARK:AMPL?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for marker amplitude state: '{response}'")

    def source_marker_aoff(self):
        """Turns OFF all markers.
        Notes: This command is an event, and therefore has no query form."""
        self.instrument.write(":SOUR:MARK:AOFF")

    def set_source_marker_frequency(self, value: float):
        """Controls the absolute frequency of the specified marker when MARKer:MODE is FREQuency. When MARKer:MODE is DELTa, this command controls relative frequency.
        Parameters:
        value: The frequency (numeric value)."""
        self.instrument.write(f":SOUR:MARK:FREQ {value}")

    def get_source_marker_frequency(self) -> float:
        """Returns the frequency of the specified marker."""
        response = self.instrument.query(":SOUR:MARK:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for marker frequency (not numeric): '{response}'")

    def set_source_marker_mode(self, mode_type: str):
        """Controls whether the marker is tied to a frequency, referenced to an absolute trace point (position), or referenced to another marker (delta).
        Parameters:
        mode_type: FREQuency|POSition|DELTa"""
        valid_modes = {"FREQUENCY", "POSITION", "DELTA", "FREQ", "POS", "DEL"}
        mode_upper = mode_type.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid marker mode: '{mode_type}'. Must be 'FREQuency', 'POSition', or 'DELTa'.")

        if mode_upper == "FREQUENCY": scpi_value = "FREQ"
        elif mode_upper == "POSITION": scpi_value = "POS"
        elif mode_upper == "DELTA": scpi_value = "DEL"
        else: scpi_value = mode_upper

        self.instrument.write(f":SOUR:MARK:MODE {scpi_value}")

    def get_source_marker_mode(self) -> str:
        """Returns whether the marker is tied to a frequency, referenced to an absolute trace point (position), or referenced to another marker (delta) ('FREQuency', 'POSition', or 'DELTa')."""
        response = self.instrument.query(":SOUR:MARK:MODE?").strip().upper()
        if response.startswith("FREQ"): return "FREQUENCY"
        elif response.startswith("POS"): return "POSITION"
        elif response.startswith("DEL"): return "DELTA"
        return response

    def set_source_marker_point(self, value: float):
        """Sets the marker to the specified sweep point.
        Parameters:
        value: The sweep point (numeric value)."""
        self.instrument.write(f":SOUR:MARK:POIN {value}")

    def get_source_marker_point(self) -> float:
        """Returns the sweep point of the marker."""
        response = self.instrument.query(":SOUR:MARK:POIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for marker point (not numeric): '{response}'")

    
    def set_source_marker_reference(self, value: float):
        """Establishes a reference marker for delta markers.
        Parameters:
        value: The reference marker number (numeric value)."""
        self.instrument.write(f":SOUR:MARK:REF {value}")

    def get_source_marker_reference(self) -> float:
        """Returns the reference marker for delta markers."""
        response = self.instrument.query(":SOUR:MARK:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for marker reference (not numeric): '{response}'")

    def set_source_marker_state(self, enable: bool):
        """Turns ON and OFF the marker specified by the MARKer command header suffix.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:MARK:STATE {scpi_value}")

    def get_source_marker_state(self) -> bool:
        """Returns True if the marker is ON, False if OFF."""
        response = self.instrument.query(":SOUR:MARK:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for marker state: '{response}'")

    
    def set_source_phase_adjust(self, value: float):
        """Controls the phase offset value relative to the reference.
        Parameters:
        value: The phase offset value (numeric value). Units are radians, accepts DEGree suffix."""
        self.instrument.write(f":SOUR:PHAS:ADJ {value}")

    def get_source_phase_adjust(self) -> float:
        """Returns the phase offset value relative to the reference."""
        response = self.instrument.query(":SOUR:PHAS:ADJ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for phase adjust (not numeric): '{response}'")

    def set_source_phase_adjust_step(self, value: float):
        """Controls the step size in radians.
        Parameters:
        value: The step size (numeric value). Accepts DEGree suffix."""
        self.instrument.write(f":SOUR:PHAS:ADJ:STEP {value}")

    def get_source_phase_adjust_step(self) -> float:
        """Returns the step size in radians."""
        response = self.instrument.query(":SOUR:PHAS:ADJ:STEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for phase adjust step (not numeric): '{response}'")

    def set_source_phase_source(self, source_type: str, source_number: int = None):
        """Determines whether the reference source is an external signal or if it is the internal signal itself marked at some reference time.
        Parameters:
        source_type: INTernal|EXTernal
        source_number: Optional numeric suffix for internal/external source."""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid phase source type: '{source_type}'. Must be 'INTernal' or 'EXTernal'.")

        scpi_value = ""
        if type_upper == "INTERNAL":
            scpi_value = "INT"
        elif type_upper == "EXTERNAL":
            scpi_value = "EXT"

        if source_number is not None:
            scpi_value += str(source_number)

        self.instrument.write(f":SOUR:PHAS::SOUR {scpi_value}")

    def get_source_phase_source(self) -> str:
        """Returns whether the reference source is an external signal or if it is the internal signal itself ('INTernal' or 'EXTernal', potentially with a number suffix)."""
        response = self.instrument.query(":SOUR:PHAS::SOUR?").strip().upper()
        # Parse for potential numeric suffix
        import re
        match = re.match(r"(INT|EXT)(\d*)", response)
        if match:
            prefix = match.group(1)
            num = match.group(2)
            if prefix == "INT":
                return f"INTernal{num}"
            elif prefix == "EXT":
                return f"EXTernal{num}"
        return response # Return raw if unable to parse

    def source_phase_reference(self):
        """This is an event which sets the current phase to be the reference for future phase adjustments.
        Notes: This function is nonqueryable."""
        self.instrument.write(":SOUR:PHAS:REF")

    
    def set_source_pm_deviation(self, value: float):
        """Sets the modulation DEViation of a PM signal. The unit for DEViation is radians.
        Parameters:
        value: The modulation deviation value (numeric value)."""
        self.instrument.write(f":SOUR:PM:DEV {value}")

    def get_source_pm_deviation(self) -> float:
        """Returns the modulation DEViation of a PM signal in radians."""
        response = self.instrument.query(":SOUR:PM:DEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PM deviation (not numeric): '{response}'")

    def set_source_pm_sensitivity(self, value: float):
        """Controls the modulation deviation by setting a sensitivity to the modulation signal voltage level for PM. The unit for SENSitivity is radians/Volt (radians/V).
        Parameters:
        value: The sensitivity value (numeric value)."""
        self.instrument.write(f":SOUR:PM:SENS {value}")

    def get_source_pm_sensitivity(self) -> float:
        """Returns the sensitivity in radians/Volt (radians/V) for PM."""
        response = self.instrument.query(":SOUR:PM:SENS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PM sensitivity (not numeric): '{response}'")

    def set_source_pm_mode(self, mode_type: str):
        """Sets the synthesis mode employed in generating the PM signal.
        Parameters:
        mode_type: LOCKed|UNLocked"""
        valid_types = {"LOCKED", "UNLOCKED", "LOCK", "UNL"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid PM mode: '{mode_type}'. Must be 'LOCKed' or 'UNLocked'.")

        if type_upper == "LOCKED": scpi_value = "LOCK"
        elif type_upper == "UNLOCKED": scpi_value = "UNL"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PM:MODE {scpi_value}")

    def get_source_pm_mode(self) -> str:
        """Returns the synthesis mode employed in generating the PM signal ('LOCKed' or 'UNLocked')."""
        response = self.instrument.query(":SOUR:PM:MODE?").strip().upper()
        if response.startswith("LOCK"):
            return "LOCKED"
        elif response.startswith("UNL"):
            return "UNLOCKED"
        return response

    
    def set_source_pm_state(self, enable: bool):
        """Turns phase modulation ON or OFF.
        Parameters:
        enable: True to turn PM modulation ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:PM:STATE {scpi_value}")

    def get_source_pm_state(self) -> bool:
        """Returns True if phase modulation is ON, False if OFF."""
        response = self.instrument.query(":SOUR:PM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for PM state: '{response}'")

    def set_source_pm_source(self, sources: list[str]):
        """Selects the source(s) for the modulating signal for PM.
        Parameters:
        sources: A list of strings, each being 'EXTernal' or 'INTernal', optionally followed by a number (e.g., ["INTernal1", "EXTernal"])."""
        formatted_sources = []
        for src in sources:
            src_upper = src.upper()
            if src_upper.startswith("INTERNAL"):
                formatted_sources.append(f"INT{src_upper[8:]}") # Handle INTernal1 -> INT1
            elif src_upper.startswith("EXTERNAL"):
                formatted_sources.append(f"EXT{src_upper[8:]}") # Handle EXTernal1 -> EXT1
            else:
                raise ValueError(f"Invalid source type: '{src}'. Must be 'INTernal' or 'EXTernal'.")
        source_str = ",".join(formatted_sources)
        self.instrument.write(f":SOUR:PM::SOUR {source_str}")

    def get_source_pm_source(self) -> list[str]:
        """Returns the selected source(s) for the modulating signal for PM.
        Returns: A list of source strings (e.g., ['INTernal', 'EXTernal1'])."""
        response = self.instrument.query(":SOUR:PM::SOUR?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., "INT,EXT1")
        return [s.replace("INT", "INTernal").replace("EXT", "EXTernal") for s in response.split(',')]

    def set_source_pm_coupling(self, coupling_type: str):
        """Sets the coupling between the modulator and the modulating signal for PM.
        Parameters:
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PM:COUP {scpi_value}")

    def get_source_pm_coupling(self) -> str:
        """Returns the coupling between the modulator and the modulating signal for PM ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(":SOUR:PM:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_pm_polarity(self, polarity_type: str):
        """Sets the polarity between the modulator and the modulating signal for PM.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PM:POL {scpi_value}")

    def get_source_pm_polarity(self) -> str:
        """Returns the polarity between the modulator and the modulating signal for PM ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:PM:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    
    def set_source_pm_internal_frequency(self, internal_source_number: int, value: float):
        """Sets the frequency of the specified internal PM signal source in Hertz (Hz).
        Parameters:
        internal_source_number: The internal signal source number (e.g., 1).
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:PM:INT{internal_source_number}:FREQ {value}")

    def get_source_pm_internal_frequency(self, internal_source_number: int) -> float:
        """Returns the frequency of the specified internal PM signal source in Hertz (Hz)."""
        response = self.instrument.query(f":SOUR:PM:INT{internal_source_number}:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for internal PM frequency (not numeric): '{response}'")

    def set_source_pm_external_impedance(self, external_source_number: int, value: float):
        """Sets the impedance of the specified external PM signal source in Ohms.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        value: The impedance in Ohms (numeric value)."""
        self.instrument.write(f":SOUR:PM:EXT{external_source_number}:IMP {value}")

    def get_source_pm_external_impedance(self, external_source_number: int) -> float:
        """Returns the impedance of the specified external PM signal source in Ohms."""
        response = self.instrument.query(f":SOUR:PM:EXT{external_source_number}:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for external PM impedance (not numeric): '{response}'")

    def set_source_pm_external_coupling(self, external_source_number: int, coupling_type: str):
        """Sets the coupling for a specified external PM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        coupling_type: AC|DC|GROund"""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROund'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PM:EXT{external_source_number}:COUP {scpi_value}")

    def get_source_pm_external_coupling(self, external_source_number: int) -> str:
        """Returns the coupling for a specified external PM signal source ('AC', 'DC', or 'GROund')."""
        response = self.instrument.query(f":SOUR:PM:EXT{external_source_number}:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    def set_source_pm_external_polarity(self, external_source_number: int, polarity_type: str):
        """Sets the polarity for a specified external PM signal source.
        Parameters:
        external_source_number: The external signal source number (e.g., 1).
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PM:EXT{external_source_number}:POL {scpi_value}")

    def get_source_pm_external_polarity(self, external_source_number: int) -> str:
        """Returns the polarity for a specified external PM signal source ('NORMal' or 'INVerted')."""
        response = self.instrument.query(f":SOUR:PM:EXT{external_source_number}:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    
    def set_source_power_attenuation(self, value: float):
        """Sets the ATTenuation level for Power.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNIT system."""
        self.instrument.write(f":SOUR:POW:ATT {value}")

    def get_source_power_attenuation(self) -> float:
        """Returns the ATTenuation level for Power."""
        response = self.instrument.query(":SOUR:POW:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power attenuation (not numeric): '{response}'")

    def set_source_power_attenuation_auto(self, enable: bool):
        """Couples the attenuator to LEVel for Power.
        Parameters:
        enable: True to enable auto-coupling, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:ATT:AUTO {scpi_value}")

    def get_source_power_attenuation_auto(self) -> bool:
        """Returns True if auto-coupling of attenuator to LEVel is enabled for Power, False if disabled."""
        response = self.instrument.query(":SOUR:POW:ATT:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power attenuation auto state: '{response}'")

    def set_source_power_alc_state(self, enable: bool):
        """Controls whether the ALC loop controls the output level for Power.
        Parameters:
        enable: True to enable ALC, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:ALC:STATE {scpi_value}")

    def get_source_power_alc_state(self) -> bool:
        """Returns True if the ALC loop controls the output level for Power, False if not."""
        response = self.instrument.query(":SOUR:POW:ALC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power ALC state: '{response}'")

    def set_source_power_alc_search(self, search_state: str):
        """Enables a form of leveling where the output level is calibrated by momentarily closing the leveling loop for Power.
        Parameters:
        search_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets SEARch to ON and then OFF."""
        normalized_state = search_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid search state: '{search_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:POW:ALC:SEAR {scpi_value}")

    def get_source_power_alc_search(self) -> str:
        """Returns the search state for Power ALC ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:POW:ALC:SEAR?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    
    def set_source_power_alc_source(self, source_type: str):
        """Selects the source of the feedback signal for ALC for Power.
        Parameters:
        source_type: INTernal|DIODe|PMETer|MMHead"""
        valid_types = {"INTERNAL", "DIODE", "PMETER", "MMHEAD", "INT", "DIOD", "PMET", "MMH"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid ALC source type: '{source_type}'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "DIODE": scpi_value = "DIOD"
        elif type_upper == "PMETER": scpi_value = "PMET"
        elif type_upper == "MMHEAD": scpi_value = "MMH"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:POW:ALC::SOUR {scpi_value}")

    def get_source_power_alc_source(self) -> str:
        """Returns the source of the feedback signal for ALC for Power ('INTernal', 'DIODe', 'PMETer', or 'MMHead')."""
        response = self.instrument.query(":SOUR:POW:ALC::SOUR?").strip().upper()
        if response.startswith("INT"): return "INTernal"
        elif response.startswith("DIOD"): return "DIODe"
        elif response.startswith("PMET"): return "PMETer"
        elif response.startswith("MMH"): return "MMHead"
        return response

    def set_source_power_alc_bandwidth(self, value: float):
        """Controls the bandwidth of the ALC feedback signal for Power in Hz.
        Parameters:
        value: The bandwidth in Hz (numeric value)."""
        self.instrument.write(f":SOUR:POW:ALC:BAND {value}")

    def get_source_power_alc_bandwidth(self) -> float:
        """Returns the bandwidth of the ALC feedback signal for Power in Hz."""
        response = self.instrument.query(":SOUR:POW:ALC:BAND?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power ALC bandwidth (not numeric): '{response}'")

    def set_source_power_alc_bandwidth_auto(self, auto_state: str):
        """Couples the bandwidth of the ALC feedback signal to instrument-dependent parameters for Power.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:POW:ALC:BAND:AUTO {scpi_value}")

    def get_source_power_alc_bandwidth_auto(self) -> str:
        """Returns the auto state of the ALC bandwidth for Power ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:POW:ALC:BAND:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_power_center(self, value: float):
        """Sets the center amplitude for Power.
        Parameters:
        value: The center amplitude (numeric value)."""
        self.instrument.write(f":SOUR:POW:CENT {value}")

    def get_source_power_center(self) -> float:
        """Returns the center amplitude for Power."""
        response = self.instrument.query(":SOUR:POW:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power center (not numeric): '{response}'")

    
    def set_source_power_level_immediate_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Power in terms of current operating units.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:IMM:AMPL {value}")

    def get_source_power_level_immediate_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Power."""
        response = self.instrument.query(":SOUR:POW:LEV:IMM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level immediate amplitude (not numeric): '{response}'")

    def set_source_power_level_immediate_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal specified in AMPLitude, in terms of current operating units for Power.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:IMM:OFFS {value}")

    def get_source_power_level_immediate_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LEV:IMM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level immediate offset (not numeric): '{response}'")

    def set_source_power_level_immediate_high(self, value: float):
        """Sets the more positive peak of a time varying signal for Power.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:IMM:HIGH {value}")

    def get_source_power_level_immediate_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LEV:IMM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level immediate high (not numeric): '{response}'")

    def set_source_power_level_immediate_low(self, value: float):
        """Sets the more negative peak of a time varying signal for Power.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:IMM:LOW {value}")

    def get_source_power_level_immediate_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LEV:IMM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level immediate low (not numeric): '{response}'")

    
    def set_source_power_level_triggered_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Power, to be transferred upon trigger.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:TRIG:AMPL {value}")

    def get_source_power_level_triggered_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Power (triggered)."""
        response = self.instrument.query(":SOUR:POW:LEV:TRIG:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level triggered amplitude (not numeric): '{response}'")

    def set_source_power_level_triggered_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal for Power, to be transferred upon trigger.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:TRIG:OFFS {value}")

    def get_source_power_level_triggered_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Power (triggered)."""
        response = self.instrument.query(":SOUR:POW:LEV:TRIG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level triggered offset (not numeric): '{response}'")

    def set_source_power_level_triggered_high(self, value: float):
        """Sets the more positive peak of a time varying signal for Power, to be transferred upon trigger.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:TRIG:HIGH {value}")

    def get_source_power_level_triggered_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Power (triggered)."""
        response = self.instrument.query(":SOUR:POW:LEV:TRIG:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level triggered high (not numeric): '{response}'")

    def set_source_power_level_triggered_low(self, value: float):
        """Sets the more negative peak of a time varying signal for Power, to be transferred upon trigger.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:POW:LEV:TRIG:LOW {value}")

    def get_source_power_level_triggered_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Power (triggered)."""
        response = self.instrument.query(":SOUR:POW:LEV:TRIG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power level triggered low (not numeric): '{response}'")

    def set_source_power_limit_amplitude(self, value: float):
        """Sets the limit on the actual magnitude of the unswept output signal for Power.
        Parameters:
        value: The amplitude limit (numeric value)."""
        self.instrument.write(f":SOUR:POW:LIM:AMPL {value}")

    def get_source_power_limit_amplitude(self) -> float:
        """Returns the limit on the actual magnitude of the unswept output signal for Power."""
        response = self.instrument.query(":SOUR:POW:LIM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power limit amplitude (not numeric): '{response}'")

    
    def set_source_power_limit_offset(self, value: float):
        """Sets a non-time varying component limit of signal that is added to the time varying signal for Power.
        Parameters:
        value: The offset limit (numeric value)."""
        self.instrument.write(f":SOUR:POW:LIM:OFFS {value}")

    def get_source_power_limit_offset(self) -> float:
        """Returns a non-time varying component limit of signal that is added to the time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LIM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power limit offset (not numeric): '{response}'")

    def set_source_power_limit_high(self, value: float):
        """Sets the more positive peak limit of a time varying signal for Power.
        Parameters:
        value: The high peak limit (numeric value)."""
        self.instrument.write(f":SOUR:POW:LIM:HIGH {value}")

    def get_source_power_limit_high(self) -> float:
        """Returns the more positive peak limit of a time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power limit high (not numeric): '{response}'")

    def set_source_power_limit_low(self, value: float):
        """Sets the more negative peak limit of a time varying signal for Power.
        Parameters:
        value: The low peak limit (numeric value)."""
        self.instrument.write(f":SOUR:POW:LIM:LOW {value}")

    def get_source_power_limit_low(self) -> float:
        """Returns the more negative peak limit of a time varying signal for Power."""
        response = self.instrument.query(":SOUR:POW:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power limit low (not numeric): '{response}'")

    def set_source_power_limit_state(self, enable: bool):
        """Controls whether the LIMit is enabled for Power.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:LIM:STATE {scpi_value}")

    def get_source_power_limit_state(self) -> bool:
        """Returns True if the LIMit is enabled for Power, False if disabled."""
        response = self.instrument.query(":SOUR:POW:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power limit state: '{response}'")

    def set_source_power_manual(self, value: float):
        """Allows manual adjustment of the amplitude between the sweep limits for Power.
        Parameters:
        value: The manual amplitude value (numeric value)."""
        self.instrument.write(f":SOUR:POW:MAN {value}")

    def get_source_power_manual(self) -> float:
        """Returns the manual amplitude for Power."""
        response = self.instrument.query(":SOUR:POW:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power manual (not numeric): '{response}'")

    def set_source_power_mode(self, mode_type: str):
        """Determines which set of commands control the amplitude subsystem for Power.
        Parameters:
        mode_type: FIXed|SWEep|LIST"""
        valid_types = {"FIXED", "SWEEP", "LIST", "FIX", "SWE"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid power mode: '{mode_type}'. Must be 'FIXed', 'SWEep', or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:POW:MODE {scpi_value}")

    def get_source_power_mode(self) -> str:
        """Returns which set of commands control the amplitude subsystem for Power ('FIXed', 'SWEep', or 'LIST')."""
        response = self.instrument.query(":SOUR:POW:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        elif response.startswith("SWE"):
            return "SWEEP"
        return response

    def set_source_power_protection_level(self, value: float):
        """Sets the output level at which the output protection circuit will trip for Power.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SOUR:POW:PROT:LEV {value}")

    def get_source_power_protection_level(self) -> float:
        """Returns the output level at which the output protection circuit will trip for Power."""
        response = self.instrument.query(":SOUR:POW:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power protection level (not numeric): '{response}'")

    
    def set_source_power_protection_state(self, enable: bool):
        """Controls whether the output protection circuit is enabled for Power.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:PROT:STATE {scpi_value}")

    def get_source_power_protection_state(self) -> bool:
        """Returns True if the output protection circuit is enabled for Power, False if disabled."""
        response = self.instrument.query(":SOUR:POW:PROT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power protection state: '{response}'")

    def get_source_power_protection_tripped(self) -> bool:
        """Returns a 1 if the protection circuit is tripped for Power and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:POW:PROT:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for power protection tripped status: '{response}'")

    def clear_source_power_protection(self):
        """Causes the protection circuit to be cleared for Power.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:POW:PROT:CLE")

    def set_source_power_range(self, value: float):
        """Sets a range for the output amplitude for Power.
        Parameters:
        value: The range value (numeric value)."""
        self.instrument.write(f":SOUR:POW:RANG {value}")

    def get_source_power_range(self) -> float:
        """Returns the range for the output amplitude for Power."""
        response = self.instrument.query(":SOUR:POW:RANG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power range (not numeric): '{response}'")

    def set_source_power_range_auto(self, auto_state: str):
        """Couples the RANGe to an instrument-determined value for Power.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:POW:RANG:AUTO {scpi_value}")

    def get_source_power_range_auto(self) -> str:
        """Returns the auto state of the Power range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:POW:RANG:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_power_reference(self, value: float):
        """Sets a reference value for Power which, if STATe is ON, allows all amplitude parameters to be queried/set as relative to the reference value.
        Parameters:
        value: The reference value (numeric value)."""
        self.instrument.write(f":SOUR:POW:REF {value}")

    def get_source_power_reference(self) -> float:
        """Returns the reference value for Power."""
        response = self.instrument.query(":SOUR:POW:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power reference (not numeric): '{response}'")

    def set_source_power_reference_state(self, enable: bool):
        """Determines whether amplitude is measured/output in absolute or relative mode for Power.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:REF:STATE {scpi_value}")

    def get_source_power_reference_state(self) -> bool:
        """Returns True if amplitude is measured/output in relative mode for Power, False for absolute mode."""
        response = self.instrument.query(":SOUR:POW:REF:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power reference state: '{response}'")

    def set_source_power_slew(self, value: float):
        """Sets the slew rate of the output change when a new output level is programmed for Power. The units are in (the currently active) amplitude unit/sec.
        Parameters:
        value: The slew rate (numeric value)."""
        self.instrument.write(f":SOUR:POW:SLEW {value}")

    def get_source_power_slew(self) -> float:
        """Returns the slew rate of the output change for Power."""
        response = self.instrument.query(":SOUR:POW:SLEW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power slew (not numeric): '{response}'")

    
    def set_source_power_span(self, value: float):
        """Sets the amplitude span for Power. If current amplitude unit is logarithmic (dBm, dBuV, etc), then unit of SPAN is dB. Otherwise SPAN is programmed in current amplitude unit.
        Parameters:
        value: The amplitude span (numeric value)."""
        self.instrument.write(f":SOUR:POW:SPAN {value}")

    def get_source_power_span(self) -> float:
        """Returns the amplitude span for Power."""
        response = self.instrument.query(":SOUR:POW:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power span (not numeric): '{response}'")

    def set_source_power_span_hold(self, enable: bool):
        """Provides a mechanism to prevent the SPAN from being changed implicitly by the defined coupling between STARt, STOP, CENTer and SPAN for Power.
        Parameters:
        enable: True to hold SPAN, False to allow changes."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:POW:SPAN:HOLD {scpi_value}")

    def get_source_power_span_hold(self) -> bool:
        """Returns True if SPAN is held for Power, False if not."""
        response = self.instrument.query(":SOUR:POW:SPAN:HOLD?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power span hold state: '{response}'")

    def set_source_power_span_link(self, link_parameter: str):
        """Allows the default couplings for SPAN to be overridden for Power. LINK selects the parameter, either CENTer, STARt or STOP, that shall not be changed when SPAN’s value is changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:POW:SPAN:LINK {scpi_value}")

    def get_source_power_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN’s value is changed for Power ('CENTer', 'STARt', or 'STOP')."""
        response = self.instrument.query(":SOUR:POW:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        return response

    def source_power_span_full(self):
        """Sets STARt amplitude to its minimum value and STOP amplitude to its maximum value for Power. CENTer amplitude and SPAN are set to their coupled values.
        Notes: This command is an event rather than a state."""
        self.instrument.write(":SOUR:POW:SPAN:FULL")

    def set_source_power_start(self, value: float):
        """Sets STARt amplitude for Power.
        Parameters:
        value: The start amplitude (numeric value)."""
        self.instrument.write(f":SOUR:POW:STAR {value}")

    def get_source_power_start(self) -> float:
        """Returns STARt amplitude for Power."""
        response = self.instrument.query(":SOUR:POW:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power start (not numeric): '{response}'")

    def set_source_power_stop(self, value: float):
        """Sets STOP amplitude for Power.
        Parameters:
        value: The stop amplitude (numeric value)."""
        self.instrument.write(f":SOUR:POW:STOP {value}")

    def get_source_power_stop(self) -> float:
        """Returns STOP amplitude for Power."""
        response = self.instrument.query(":SOUR:POW:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power stop (not numeric): '{response}'")

    
    def set_source_pulm_external_hysteresis(self, value: float):
        """Sets, for the specified signal source, how far the signal voltage must rise above (alternatively, fall below) the threshold LEVel before the carrier is turned ON from the OFF state (or turned OFF from the ON state). The unit for HYSTeresis is Volts.
        Parameters:
        value: The hysteresis value (numeric value)."""
        self.instrument.write(f":SOUR:PULM:EXT:HYST {value}")

    def get_source_pulm_external_hysteresis(self) -> float:
        """Returns the hysteresis value for the external PULM signal source in Volts."""
        response = self.instrument.query(":SOUR:PULM:EXT:HYST?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PULM external hysteresis (not numeric): '{response}'")

    def set_source_pulm_external_impedance(self, value: float):
        """Sets the impedance of the specified external signal source for PULM. The unit for IMPedance is Ohms.
        Parameters:
        value: The impedance in Ohms (numeric value)."""
        self.instrument.write(f":SOUR:PULM:EXT:IMP {value}")

    def get_source_pulm_external_impedance(self) -> float:
        """Returns the impedance of the specified external signal source for PULM in Ohms."""
        response = self.instrument.query(":SOUR:PULM:EXT:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PULM external impedance (not numeric): '{response}'")

    def set_source_pulm_external_level(self, value: float):
        """For the specified signal source, this sets the threshold voltage level used to turn ON the carrier for PULM. The unit for LEVel is Volts.
        Parameters:
        value: The level in Volts (numeric value)."""
        self.instrument.write(f":SOUR:PULM:EXT:LEV {value}")

    def get_source_pulm_external_level(self) -> float:
        """Returns the threshold voltage level used to turn ON the carrier for PULM in Volts."""
        response = self.instrument.query(":SOUR:PULM:EXT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PULM external level (not numeric): '{response}'")

    
    def set_source_pulm_external_polarity(self, polarity_type: str):
        """Sets the POLarity for only the specified external signal source for PULM.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PULM:EXT:POL {scpi_value}")

    def get_source_pulm_external_polarity(self) -> str:
        """Returns the POLarity for the specified external PULM signal source ('NORMal' or 'INVerted')."""
        response = self.instrument.query(f":SOUR:PULM:EXT:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_source_pulm_internal_frequency(self, internal_source_number: int, value: float):
        """Sets the frequency of the specified internal signal source for PULM. The unit of FREQuency is Hertz (Hz).
        Parameters:
        internal_source_number: The internal signal source number (e.g., 1).
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:PULM:INT{internal_source_number}:FREQ {value}")

    def get_source_pulm_internal_frequency(self, internal_source_number: int) -> float:
        """Returns the frequency of the specified internal signal source for PULM in Hertz (Hz)."""
        response = self.instrument.query(f":SOUR:PULM:INT{internal_source_number}:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PULM internal frequency (not numeric): '{response}'")

    def set_source_pulm_mode(self, mode_type: str):
        """Determines which set of commands currently control the PULM subsystem.
        Parameters:
        mode_type: FIXed|LIST"""
        valid_types = {"FIXED", "LIST", "FIX"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid PULM mode: '{mode_type}'. Must be 'FIXed' or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PULM:MODE {scpi_value}")

    def get_source_pulm_mode(self) -> str:
        """Returns which set of commands currently control the PULM subsystem ('FIXed' or 'LIST')."""
        response = self.instrument.query(":SOUR:PULM:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        return response

    def set_source_pulm_polarity(self, polarity_type: str):
        """Sets the polarity between the modulator and the modulating signal for PULM.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal' or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PULM:POL {scpi_value}")

    def get_source_pulm_polarity(self) -> str:
        """Returns the polarity between the modulator and the modulating signal for PULM ('NORMal' or 'INVerted')."""
        response = self.instrument.query(":SOUR:PULM:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    
    def set_source_pulm_source(self, sources: list[str]):
        """Selects the source for the modulating signal for PULM.
        Parameters:
        sources: A list of strings, each being 'EXTernal' or 'INTernal', optionally followed by a number (e.g., ["INTernal1", "EXTernal"])."""
        formatted_sources = []
        for src in sources:
            src_upper = src.upper()
            if src_upper.startswith("INTERNAL"):
                formatted_sources.append(f"INT{src_upper[8:]}") # Handle INTernal1 -> INT1
            elif src_upper.startswith("EXTERNAL"):
                formatted_sources.append(f"EXT{src_upper[8:]}") # Handle EXTernal1 -> EXT1
            else:
                raise ValueError(f"Invalid source type: '{src}'. Must be 'INTernal' or 'EXTernal'.")
        source_str = ",".join(formatted_sources)
        self.instrument.write(f":SOUR:PULM::SOUR {source_str}")

    def get_source_pulm_source(self) -> list[str]:
        """Returns the selected source(s) for the modulating signal for PULM.
        Returns: A list of source strings (e.g., ['INTernal', 'EXTernal1'])."""
        response = self.instrument.query(":SOUR:PULM::SOUR?").strip()
        if not response:
            return []
        # Response is comma-separated strings (e.g., "INT,EXT1")
        return [s.replace("INT", "INTernal").replace("EXT", "EXTernal") for s in response.split(',')]

    def set_source_pulm_state(self, enable: bool):
        """Turns Pulse Modulation ON or OFF.
        Parameters:
        enable: True to turn PULse Modulation ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:PULM:STATE {scpi_value}")

    def get_source_pulm_state(self) -> bool:
        """Returns True if Pulse Modulation is ON, False if OFF."""
        response = self.instrument.query(":SOUR:PULM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for PULM state: '{response}'")

    
    def set_source_pulse_period(self, value: float):
        """Sets the period of a pulsed waveform. The fundamental units for PERiod is seconds.
        Parameters:
        value: The period in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:PER {value}")

    def get_source_pulse_period(self) -> float:
        """Returns the period of a pulsed waveform in seconds."""
        response = self.instrument.query(":SOUR:PULS:PER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse period (not numeric): '{response}'")

    def set_source_pulse_width(self, value: float):
        """Sets the width or duration of the pulse. The fundamental units for WIDTh is seconds.
        Parameters:
        value: The width in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:WIDT {value}")

    def get_source_pulse_width(self) -> float:
        """Returns the width or duration of the pulse in seconds."""
        response = self.instrument.query(":SOUR:PULS:WIDT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse width (not numeric): '{response}'")

    def set_source_pulse_duty_cycle(self, value: float):
        """Sets the duty cycle of a repetitive pulsed waveform. The fundamental units for DCYCle is percent (%).
        Parameters:
        value: The duty cycle in percent (numeric value)."""
        self.instrument.write(f":SOUR:PULS:DCYC {value}")

    def get_source_pulse_duty_cycle(self) -> float:
        """Returns the duty cycle of a repetitive pulsed waveform in percent (%)."""
        response = self.instrument.query(":SOUR:PULS:DCYC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse duty cycle (not numeric): '{response}'")

    def set_source_pulse_hold(self, hold_parameter: str):
        """Sets, for a pulsed waveform, the parameter to be held constant when the period changes.
        Parameters:
        hold_parameter: WIDTh|DCYCle"""
        valid_params = {"WIDTH", "DCYCLE", "WIDT", "DCYC"}
        param_upper = hold_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid hold parameter: '{hold_parameter}'. Must be 'WIDTh' or 'DCYCle'.")

        if param_upper == "WIDTH": scpi_value = "WIDT"
        elif param_upper == "DCYCLE": scpi_value = "DCYC"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:PULS:HOLD {scpi_value}")

    def get_source_pulse_hold(self) -> str:
        """Returns the parameter to be held constant when the period changes for a pulsed waveform ('WIDTh' or 'DCYCle')."""
        response = self.instrument.query(":SOUR:PULS:HOLD?").strip().upper()
        if response.startswith("WIDT"):
            return "WIDTH"
        elif response.startswith("DCYC"):
            return "DCYCLE"
        return response

    def set_source_pulse_delay(self, value: float):
        """Sets the time from the start of the period to the first edge of the pulse. The fundamental units for DELay is seconds.
        Parameters:
        value: The delay in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:DEL {value}")

    def get_source_pulse_delay(self) -> float:
        """Returns the time from the start of the period to the first edge of the pulse in seconds."""
        response = self.instrument.query(":SOUR:PULS:DEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse delay (not numeric): '{response}'")

    
    def set_source_pulse_double_state(self, enable: bool):
        """Sets the double pulse mode to ON or OFF.
        Parameters:
        enable: True to enable double pulse mode, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:PULS:DOUB:STATE {scpi_value}")

    def get_source_pulse_double_state(self) -> bool:
        """Returns True if the double pulse mode is ON, False if OFF."""
        response = self.instrument.query(":SOUR:PULS:DOUB:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for pulse double state: '{response}'")

    def set_source_pulse_double_delay(self, value: float):
        """Sets the time from the start of the period to the first edge of the second pulse. The fundamental units for DELay is seconds.
        Parameters:
        value: The delay in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:DOUB:DEL {value}")

    def get_source_pulse_double_delay(self) -> float:
        """Returns the time from the start of the period to the first edge of the second pulse in seconds."""
        response = self.instrument.query(":SOUR:PULS:DOUB:DEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse double delay (not numeric): '{response}'")

    def set_source_pulse_transition_state(self, enable: bool):
        """Sets the transition mode to ON or OFF.
        Parameters:
        enable: True to enable transition times, False to set to minimum."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:PULS:TRAN:STATE {scpi_value}")

    def get_source_pulse_transition_state(self) -> bool:
        """Returns True if the transition mode is ON, False if OFF."""
        response = self.instrument.query(":SOUR:PULS:TRAN:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for pulse transition state: '{response}'")

    def set_source_pulse_transition_leading(self, value: float):
        """Sets the transition time for the LEADing edge. The fundamental units for LEADing is seconds.
        Parameters:
        value: The leading edge transition time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:TRAN:LEAD {value}")

    def get_source_pulse_transition_leading(self) -> float:
        """Returns the transition time for the LEADing edge in seconds."""
        response = self.instrument.query(":SOUR:PULS:TRAN:LEAD?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse transition leading (not numeric): '{response}'")

    
    def set_source_pulse_transition_trailing(self, value: float):
        """Sets the transition time for the TRAiling edge. The fundamental units for TRAiling is seconds.
        Parameters:
        value: The trailing edge transition time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:PULS:TRAN:TRA {value}")

    def get_source_pulse_transition_trailing(self) -> float:
        """Returns the transition time for the TRAiling edge in seconds."""
        response = self.instrument.query(":SOUR:PULS:TRAN:TRA?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse transition trailing (not numeric): '{response}'")

    def set_source_pulse_transition_trailing_auto(self, auto_state: str):
        """Couples the value of TRAiling to LEADing, when AUTO is set to ON for Pulse Transition.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:PULS:TRAN:TRA:AUTO {scpi_value}")

    def get_source_pulse_transition_trailing_auto(self) -> str:
        """Returns the auto state of the trailing transition time for Pulse ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:PULS:TRAN:TRA:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_pulse_count(self, value: int):
        """Sets the number of times pulse (or double pulse) must be repeated for a single trigger event.
        Parameters:
        value: The count (numeric value)."""
        self.instrument.write(f":SOUR:PULS:COUN {value}")

    def get_source_pulse_count(self) -> int:
        """Returns the number of times pulse (or double pulse) must be repeated for a single trigger event."""
        response = self.instrument.query(":SOUR:PULS:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for pulse count (not integer): '{response}'")

    def set_source_pulse_polarity(self, polarity_type: str):
        """Sets the polarity of the pulse.
        Parameters:
        polarity_type: NORMal|COMPlement|INVerted"""
        valid_types = {"NORMAL", "COMPLEMENT", "INVERTED", "NORM", "COMP", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMal', 'COMPlement', or 'INVerted'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "COMPLEMENT": scpi_value = "COMP"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:PULS:POL {scpi_value}")

    def get_source_pulse_polarity(self) -> str:
        """Returns the polarity of the pulse ('NORMal', 'COMPlement', or 'INVerted')."""
        response = self.instrument.query(":SOUR:PULS:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("COMP"):
            return "COMPLEMENT"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    
    def set_source_resistance_level_immediate_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept resistance.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:IMM:AMPL {value}")

    def get_source_resistance_level_immediate_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept resistance."""
        response = self.instrument.query(":SOUR:RES:LEV:IMM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level immediate amplitude (not numeric): '{response}'")

    def set_source_resistance_level_immediate_offset(self, value: float):
        """Sets the non-time varying component of the resistance that is added to the time varying resistance signal specified in AMPLitude.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:IMM:OFFS {value}")

    def get_source_resistance_level_immediate_offset(self) -> float:
        """Returns the non-time varying component of the resistance that is added to the time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LEV:IMM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level immediate offset (not numeric): '{response}'")

    def set_source_resistance_level_immediate_high(self, value: float):
        """Sets the more positive peak of a time varying resistance signal.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:IMM:HIGH {value}")

    def get_source_resistance_level_immediate_high(self) -> float:
        """Returns the more positive peak of a time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LEV:IMM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level immediate high (not numeric): '{response}'")

    def set_source_resistance_level_immediate_low(self, value: float):
        """Sets the more negative peak of a time varying resistance signal.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:IMM:LOW {value}")

    def get_source_resistance_level_immediate_low(self) -> float:
        """Returns the more negative peak of a time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LEV:IMM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level immediate low (not numeric): '{response}'")

    
    def set_source_resistance_level_triggered_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Resistance, to be transferred upon trigger.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:TRIG:AMPL {value}")

    def get_source_resistance_level_triggered_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Resistance (triggered)."""
        response = self.instrument.query(":SOUR:RES:LEV:TRIG:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level triggered amplitude (not numeric): '{response}'")

    def set_source_resistance_level_triggered_offset(self, value: float):
        """Sets the non-time varying component of the resistance that is added to the time varying resistance signal for Resistance, to be transferred upon trigger.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:TRIG:OFFS {value}")

    def get_source_resistance_level_triggered_offset(self) -> float:
        """Returns the non-time varying component of the resistance that is added to the time varying resistance signal for Resistance (triggered)."""
        response = self.instrument.query(":SOUR:RES:LEV:TRIG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level triggered offset (not numeric): '{response}'")

    def set_source_resistance_level_triggered_high(self, value: float):
        """Sets the more positive peak of a time varying resistance signal for Resistance, to be transferred upon trigger.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:TRIG:HIGH {value}")

    def get_source_resistance_level_triggered_high(self) -> float:
        """Returns the more positive peak of a time varying resistance signal for Resistance (triggered)."""
        response = self.instrument.query(":SOUR:RES:LEV:TRIG:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level triggered high (not numeric): '{response}'")

    def set_source_resistance_level_triggered_low(self, value: float):
        """Sets the more negative peak of a time varying resistance signal for Resistance, to be transferred upon trigger.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:RES:LEV:TRIG:LOW {value}")

    def get_source_resistance_level_triggered_low(self) -> float:
        """Returns the more negative peak of a time varying resistance signal for Resistance (triggered)."""
        response = self.instrument.query(":SOUR:RES:LEV:TRIG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance level triggered low (not numeric): '{response}'")

    def set_source_resistance_limit_amplitude(self, value: float):
        """Sets the limit on the actual magnitude of the unswept resistance.
        Parameters:
        value: The amplitude limit (numeric value)."""
        self.instrument.write(f":SOUR:RES:LIM:AMPL {value}")

    def get_source_resistance_limit_amplitude(self) -> float:
        """Returns the limit on the actual magnitude of the unswept resistance."""
        response = self.instrument.query(":SOUR:RES:LIM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance limit amplitude (not numeric): '{response}'")

    def set_source_resistance_limit_offset(self, value: float):
        """Sets the limit for the non-time varying component of resistance that is added to the time varying resistance signal.
        Parameters:
        value: The offset limit (numeric value)."""
        self.instrument.write(f":SOUR:RES:LIM:OFFS {value}")

    def get_source_resistance_limit_offset(self) -> float:
        """Returns the limit for the non-time varying component of resistance that is added to the time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LIM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance limit offset (not numeric): '{response}'")

    def set_source_resistance_limit_high(self, value: float):
        """Sets the more positive peak limit of a time varying resistance signal.
        Parameters:
        value: The high peak limit (numeric value)."""
        self.instrument.write(f":SOUR:RES:LIM:HIGH {value}")

    def get_source_resistance_limit_high(self) -> float:
        """Returns the more positive peak limit of a time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance limit high (not numeric): '{response}'")

    
    def set_source_resistance_limit_low(self, value: float):
        """Sets the more negative peak limit of a time varying resistance signal.
        Parameters:
        value: The low peak limit (numeric value)."""
        self.instrument.write(f":SOUR:RES:LIM:LOW {value}")

    def get_source_resistance_limit_low(self) -> float:
        """Returns the more negative peak limit of a time varying resistance signal."""
        response = self.instrument.query(":SOUR:RES:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance limit low (not numeric): '{response}'")

    def set_source_resistance_protection_level(self, value: float):
        """Sets the output resistance level at which the output protection circuit will trip.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SOUR:RES:PROT:LEV {value}")

    def get_source_resistance_protection_level(self) -> float:
        """Returns the output resistance level at which the output protection circuit will trip."""
        response = self.instrument.query(":SOUR:RES:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance protection level (not numeric): '{response}'")

    def set_source_resistance_protection_state(self, enable: bool):
        """Controls whether the output protection circuit is enabled.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:RES:PROT:STATE {scpi_value}")

    def get_source_resistance_protection_state(self) -> bool:
        """Returns True if the output protection circuit is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:RES:PROT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance protection state: '{response}'")

    def get_source_resistance_protection_tripped(self) -> bool:
        """Returns a 1 if the protection circuit is tripped and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:RES:PROT:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance protection tripped status: '{response}'")

    def clear_source_resistance_protection(self):
        """Causes the protection circuit to be cleared.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:RES:PROT:CLE")

    def set_source_resistance_slew(self, value: float):
        """Sets the slew rate of the resistance change when a new resistance level is programmed. The units are in Ohm/sec.
        Parameters:
        value: The slew rate in Ohm/sec (numeric value)."""
        self.instrument.write(f":SOUR:RES:SLEW {value}")

    def get_source_resistance_slew(self) -> float:
        """Returns the slew rate of the resistance change in Ohm/sec."""
        response = self.instrument.query(":SOUR:RES:SLEW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance slew (not numeric): '{response}'")

    def set_source_resistance_center(self, value: float):
        """Sets the CENTer RESistance.
        Parameters:
        value: The center resistance (numeric value)."""
        self.instrument.write(f":SOUR:RES:CENT {value}")

    def get_source_resistance_center(self) -> float:
        """Returns the CENTer RESistance."""
        response = self.instrument.query(":SOUR:RES:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance center (not numeric): '{response}'")

    def set_source_resistance_span(self, value: float):
        """Sets the resistance SPAN.
        Parameters:
        value: The resistance span (numeric value)."""
        self.instrument.write(f":SOUR:RES:SPAN {value}")

    def get_source_resistance_span(self) -> float:
        """Returns the resistance SPAN."""
        response = self.instrument.query(":SOUR:RES:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance span (not numeric): '{response}'")

    
    def set_source_resistance_span_hold(self, enable: bool):
        """Provides a mechanism to prevent the SPAN from being changed implicitly by the defined coupling between STARt, STOP, CENTer and SPAN for Resistance.
        Parameters:
        enable: True to hold SPAN, False to allow changes."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:RES:SPAN:HOLD {scpi_value}")

    def get_source_resistance_span_hold(self) -> bool:
        """Returns True if SPAN is held for Resistance, False if not."""
        response = self.instrument.query(":SOUR:RES:SPAN:HOLD?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance span hold state: '{response}'")

    def set_source_resistance_span_link(self, link_parameter: str):
        """Allows the default couplings for SPAN to be overridden for Resistance. LINK selects the parameter, either CENTer, STARt or STOP, that shall not be changed when SPAN’s value is changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:RES:SPAN:LINK {scpi_value}")

    def get_source_resistance_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN’s value is changed for Resistance ('CENTer', 'STARt', or 'STOP')."""
        response = self.instrument.query(":SOUR:RES:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        return response

    def source_resistance_span_full(self):
        """Sets STARt RESistance to MINimum, and STOP RESistance to MAXimum. CENTer RESistance and SPAN are set to their coupled values.
        Notes: This command is an event, rather than a state."""
        self.instrument.write(":SOUR:RES:SPAN:FULL")

    def set_source_resistance_start(self, value: float):
        """Sets STARt resistance.
        Parameters:
        value: The start resistance (numeric value)."""
        self.instrument.write(f":SOUR:RES:STAR {value}")

    def get_source_resistance_start(self) -> float:
        """Returns STARt resistance."""
        response = self.instrument.query(":SOUR:RES:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance start (not numeric): '{response}'")

    def set_source_resistance_stop(self, value: float):
        """Sets STOP resistance.
        Parameters:
        value: The stop resistance (numeric value)."""
        self.instrument.write(f":SOUR:RES:STOP {value}")

    def get_source_resistance_stop(self) -> float:
        """Returns STOP resistance."""
        response = self.instrument.query(":SOUR:RES:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance stop (not numeric): '{response}'")

    def set_source_resistance_manual(self, value: float):
        """Allows manual adjustment of the RESistance between the sweep limits.
        Parameters:
        value: The manual resistance value (numeric value)."""
        self.instrument.write(f":SOUR:RES:MAN {value}")

    def get_source_resistance_manual(self) -> float:
        """Returns the manual adjustment of the RESistance."""
        response = self.instrument.query(":SOUR:RES:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance manual (not numeric): '{response}'")

    
    def set_source_resistance_mode(self, mode_type: str):
        """Determines which set of commands control the resistance subsystem.
        Parameters:
        mode_type: FIXed|SWEep|LIST"""
        valid_types = {"FIXED", "SWEEP", "LIST", "FIX", "SWE"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid resistance mode: '{mode_type}'. Must be 'FIXed', 'SWEep', or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:RES:MODE {scpi_value}")

    def get_source_resistance_mode(self) -> str:
        """Returns which set of commands control the resistance subsystem ('FIXed', 'SWEep', or 'LIST')."""
        response = self.instrument.query(":SOUR:RES:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        elif response.startswith("SWE"):
            return "SWEEP"
        return response

    def set_source_resistance_reference(self, value: float):
        """Sets a reference value which, if STATe is ON, allows all RESistance parameters to be queried/set as a relative to the reference value.
        Parameters:
        value: The reference value (numeric value)."""
        self.instrument.write(f":SOUR:RES:REF {value}")

    def get_source_resistance_reference(self) -> float:
        """Returns the reference value for Resistance."""
        response = self.instrument.query(":SOUR:RES:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance reference (not numeric): '{response}'")

    def set_source_resistance_reference_state(self, enable: bool):
        """Determines whether RESistance is in absolute or relative mode.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:RES:REF:STATE {scpi_value}")

    def get_source_resistance_reference_state(self) -> bool:
        """Returns True if Resistance is in relative mode, False for absolute mode."""
        response = self.instrument.query(":SOUR:RES:REF:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance reference state: '{response}'")

    def set_source_resistance_range(self, value: float):
        """Sets a range for the output RESistance.
        Parameters:
        value: The range value (numeric value)."""
        self.instrument.write(f":SOUR:RES:RANG {value}")

    def get_source_resistance_range(self) -> float:
        """Returns the range for the output RESistance."""
        response = self.instrument.query(":SOUR:RES:RANG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance range (not numeric): '{response}'")

    def set_source_resistance_range_auto(self, auto_state: str):
        """Couples the RANGe to an instrument-determined value for Resistance.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:RES:RANG:AUTO {scpi_value}")

    def get_source_resistance_range_auto(self) -> str:
        """Returns the auto state of the Resistance range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:RES:RANG:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    
    def set_source_rocsillator_internal_frequency(self, value: float):
        """Specifies the frequency of the internal reference oscillator. The default units are Hz.
        Parameters:
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:ROSC:INT:FREQ {value}")

    def get_source_rocsillator_internal_frequency(self) -> float:
        """Returns the frequency of the internal reference oscillator in Hz."""
        response = self.instrument.query(":SOUR:ROSC:INT:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for internal oscillator frequency (not numeric): '{response}'")

    def set_source_rocsillator_external_frequency(self, value: float):
        """Specifies the frequency of the external reference oscillator. The default units are Hz.
        Parameters:
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SOUR:ROSC:EXT:FREQ {value}")

    def get_source_rocsillator_external_frequency(self) -> float:
        """Returns the frequency of the external reference oscillator in Hz."""
        response = self.instrument.query(":SOUR:ROSC:EXT:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for external oscillator frequency (not numeric): '{response}'")

    def set_source_rocsillator_source(self, source_type: str):
        """Controls the selection of the reference oscillator source.
        Parameters:
        source_type: INTernal|EXTernal|NONE"""
        valid_types = {"INTERNAL", "EXTERNAL", "NONE", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid oscillator source type: '{source_type}'. Must be 'INTernal', 'EXTernal', or 'NONE'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:ROSC::SOUR {scpi_value}")

    def get_source_rocsillator_source(self) -> str:
        """Returns the selection of the reference oscillator source ('INTernal', 'EXTernal', or 'NONE')."""
        response = self.instrument.query(":SOUR:ROSC::SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    def set_source_rocsillator_source_auto(self, auto_state: str):
        """When AUTO is ON, the system automatically selects which oscillator will be used by the instrument.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:ROSC::SOUR:AUTO {scpi_value}")

    def get_source_rocsillator_source_auto(self) -> str:
        """Returns the auto state of the reference oscillator source ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:ROSC::SOUR:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()
  
    def source_speed_initiate(self):
        """Initiates speed for the device.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:SPE:INIT")

    def set_source_speed_level(self, value: float):
        """Sets the desired speed set-point in m/s.
        Parameters:
        value: The speed set-point in m/s (numeric value)."""
        self.instrument.write(f":SOUR:SPE:LEV {value}")

    def get_source_speed_level(self) -> float:
        """Returns the desired speed set-point in m/s."""
        response = self.instrument.query(":SOUR:SPE:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for speed level (not numeric): '{response}'")

    
    def source_speed_ssdloss_initiate(self):
        """Initiates the Steady State Driveline Loss procedure.
        Notes: This is an overlapped command and an event; no query."""
        self.instrument.write(":SOUR:SPE:SSDL:INIT")

    def set_source_speed_ssdloss_latime(self, value: float):
        """Sets the time after stabilization that the losses are to be averaged before moving to the next speed point.
        Parameters:
        value: Loss Averaging Time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:SPE:SSDL:LAT {value}")

    def get_source_speed_ssdloss_latime(self) -> float:
        """Returns the Loss Averaging Time in seconds."""
        response = self.instrument.query(":SOUR:SPE:SSDL:LAT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for speed SSDLoss LATime (not numeric): '{response}'")

    
    def set_source_speed_ssdloss_stime(self, value: float):
        """Sets the time for stabilization prior to LATime after a change in speed.
        Parameters:
        value: Stabilization Time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:SPE:SSDL:STIM {value}")

    def get_source_speed_ssdloss_stime(self) -> float:
        """Returns the Stabilization Time in seconds."""
        response = self.instrument.query(":SOUR:SPE:SSDL:STIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for speed SSDLoss STIMe (not numeric): '{response}'")

    
    def set_source_sweep_time(self, value: float):
        """Sets the duration of the sweep in seconds.
        Parameters:
        value: The duration in seconds (numeric value)."""
        self.instrument.write(f":SOUR:SWE:TIME {value}")

    def get_source_sweep_time(self) -> float:
        """Returns the duration of the sweep in seconds."""
        response = self.instrument.query(":SOUR:SWE:TIME?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep time (not numeric): '{response}'")

    def set_source_sweep_time_auto(self, auto_state: str):
        """When enabled, the sweep time is calculated internally and is dependent on the span of the sweep.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:SWE:TIME:AUTO {scpi_value}")

    def get_source_sweep_time_auto(self) -> str:
        """Returns the auto state of the sweep time ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:SWE:TIME:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_sweep_time_llimit(self, value: float):
        """Defines a lower limit for sweep time. This lower limit restricts the sweep time value set either explicitly or automatically.
        Parameters:
        value: The lower limit in seconds (numeric value)."""
        self.instrument.write(f":SOUR:SWE:TIME:LLIM {value}")

    def get_source_sweep_time_llimit(self) -> float:
        """Returns the lower limit for sweep time in seconds."""
        response = self.instrument.query(":SOUR:SWE:TIME:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep time LLIMit (not numeric): '{response}'")

    def set_source_sweep_dwell(self, value: float):
        """Controls the amount of time spent at each point during a sweep.
        Parameters:
        value: The dwell time in seconds (numeric value)."""
        self.instrument.write(f":SOUR:SWE:DWEL {value}")

    def get_source_sweep_dwell(self) -> float:
        """Returns the amount of time spent at each point during a sweep in seconds."""
        response = self.instrument.query(":SOUR:SWE:DWEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep dwell (not numeric): '{response}'")

    
    def set_source_sweep_dwell_auto(self, auto_state: str):
        """When AUTO ON is selected, the dwell time is coupled to the sweep time and number of points.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:SWE:DWEL:AUTO {scpi_value}")

    def get_source_sweep_dwell_auto(self) -> str:
        """Returns the auto state of the sweep dwell time ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:SWE:DWEL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_sweep_direction(self, direction_type: str):
        """Controls the direction of the sweep.
        Parameters:
        direction_type: UP|DOWN"""
        valid_types = {"UP", "DOWN"}
        type_upper = direction_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid direction type: '{direction_type}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":SOUR:SWE:DIR {type_upper}")

    def get_source_sweep_direction(self) -> str:
        """Returns the direction of the sweep ('UP' or 'DOWN')."""
        response = self.instrument.query(":SOUR:SWE:DIR?").strip().upper()
        return response

    def set_source_sweep_mode(self, mode_type: str):
        """Selects the sweep conditions for the sweep.
        Parameters:
        mode_type: AUTO|MANual"""
        valid_types = {"AUTO", "MANUAL", "MAN"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid sweep mode: '{mode_type}'. Must be 'AUTO' or 'MANual'.")

        if type_upper == "MANUAL": scpi_value = "MAN"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:SWE:MODE {scpi_value}")

    def get_source_sweep_mode(self) -> str:
        """Returns the sweep conditions for the sweep ('AUTO' or 'MANual')."""
        response = self.instrument.query(":SOUR:SWE:MODE?").strip().upper()
        if response.startswith("MAN"):
            return "MANUAL"
        return response

    def set_source_sweep_spacing(self, spacing_type: str):
        """Determines the swept entity versus time characteristics of the sweep.
        Parameters:
        spacing_type: LINear|LOGarithmic"""
        valid_types = {"LINEAR", "LOGARITHMIC", "LIN", "LOG"}
        type_upper = spacing_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid spacing type: '{spacing_type}'. Must be 'LINear' or 'LOGarithmic'.")

        if type_upper == "LINEAR": scpi_value = "LIN"
        elif type_upper == "LOGARITHMIC": scpi_value = "LOG"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:SWE:SPAC {scpi_value}")

    def get_source_sweep_spacing(self) -> str:
        """Returns the swept entity versus time characteristics of the sweep ('LINear' or 'LOGarithmic')."""
        response = self.instrument.query(":SOUR:SWE:SPAC?").strip().upper()
        if response.startswith("LIN"):
            return "LINEAR"
        elif response.startswith("LOG"):
            return "LOGARITHMIC"
        return response

    def set_source_sweep_generation(self, generation_type: str):
        """Selects between an analog or stepped sweep.
        Parameters:
        generation_type: STEPped|ANALog"""
        valid_types = {"STEPPED", "ANALOG", "STEP", "ANAL"}
        type_upper = generation_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid generation type: '{generation_type}'. Must be 'STEPped' or 'ANALog'.")

        if type_upper == "STEPPED": scpi_value = "STEP"
        elif type_upper == "ANALOG": scpi_value = "ANAL"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:SWE:GEN {scpi_value}")

    def get_source_sweep_generation(self) -> str:
        """Returns whether the sweep is analog or stepped ('STEPped' or 'ANALog')."""
        response = self.instrument.query(":SOUR:SWE:GEN?").strip().upper()
        if response.startswith("STEP"):
            return "STEPPED"
        elif response.startswith("ANAL"):
            return "ANALOG"
        return response

    
    def set_source_sweep_step(self, value: float):
        """Controls the swept entity step size for a stepped linear sweep. This parameter is not used if GENeration is ANALog or if SPACing is LOGarithmic.
        Parameters:
        value: The step size (numeric value)."""
        self.instrument.write(f":SOUR:SWE:STEP {value}")

    def get_source_sweep_step(self) -> float:
        """Returns the swept entity step size for a stepped linear sweep."""
        response = self.instrument.query(":SOUR:SWE:STEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep step (not numeric): '{response}'")

    def set_source_sweep_points(self, value: int):
        """Sets the number of points in a stepped sweep. This parameter is not used if GENeration is ANALog.
        Parameters:
        value: The number of points (numeric value)."""
        self.instrument.write(f":SOUR:SWE:POIN {value}")

    def get_source_sweep_points(self) -> int:
        """Returns the number of points in a stepped sweep."""
        response = self.instrument.query(":SOUR:SWE:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep points (not integer): '{response}'")

    def set_source_sweep_count(self, value: int):
        """Determines the number of sweeps which are enabled by a single trigger event.
        Parameters:
        value: The count (numeric value)."""
        self.instrument.write(f":SOUR:SWE:COUN {value}")

    def get_source_sweep_count(self) -> int:
        """Returns the number of sweeps which are enabled by a single trigger event."""
        response = self.instrument.query(":SOUR:SWE:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep count (not integer): '{response}'")

    
    def set_source_temperature_aprobe(self, values: list[int]):
        """Active PRobe selects one or more probes to become part of the feedback loop to control the temperature.
        Parameters:
        values: A list of numeric values (probe numbers)."""
        value_str = ",".join(map(str, values))
        self.instrument.write(f":SOUR:TEMP:APRO {value_str}")

    def set_source_temperature_dwell(self, value: float):
        """Specifies the amount of time the temperature chamber will stay at the target temperature.
        Parameters:
        value: The dwell time (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:DWEL {value}")

    def get_source_temperature_dwell(self) -> float:
        """Returns the amount of time the temperature chamber will stay at the target temperature."""
        response = self.instrument.query(":SOUR:TEMP:DWEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature dwell (not numeric): '{response}'")

    
    def set_source_temperature_lconstants_derivative(self, value: float):
        """Sets the DERivative (lead compensator) value for the temperature control loop.
        Parameters:
        value: The derivative value (numeric value). Units are (currently selected units) degrees per second."""
        self.instrument.write(f":SOUR:TEMP:LCON:DER {value}")

    def get_source_temperature_lconstants_derivative(self) -> float:
        """Returns the DERivative (lead compensator) value for the temperature control loop."""
        response = self.instrument.query(":SOUR:TEMP:LCON:DER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature LCONstants derivative (not numeric): '{response}'")

    def set_source_temperature_lconstants_gain(self, value: float):
        """Sets the GAIN (proportional control) value for the temperature control loop. This is a unitless quantity.
        Parameters:
        value: The gain value (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:LCON:GAIN {value}")

    def get_source_temperature_lconstants_gain(self) -> float:
        """Returns the GAIN (proportional control) value for the temperature control loop."""
        response = self.instrument.query(":SOUR:TEMP:LCON:GAIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature LCONstants gain (not numeric): '{response}'")

    def set_source_temperature_lconstants_integral(self, value: float):
        """Sets the INTegral (lag compensator) value for the temperature control loop. The units for INTegral are degree*seconds.
        Parameters:
        value: The integral value (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:LCON:INT {value}")

    def get_source_temperature_lconstants_integral(self) -> float:
        """Returns the INTegral (lag compensator) value for the temperature control loop."""
        response = self.instrument.query(":SOUR:TEMP:LCON:INT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature LCONstants integral (not numeric): '{response}'")

    
    def set_source_temperature_mode(self, mode_type: str):
        """Determines which set of commands control the temperature subsystem.
        Parameters:
        mode_type: FIXed|LIST|PROGram"""
        valid_types = {"FIXED", "LIST", "PROGRAM", "FIX", "PROG"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid temperature mode: '{mode_type}'. Must be 'FIXed', 'LIST', or 'PROGram'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "PROGRAM": scpi_value = "PROG"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:TEMP:MODE {scpi_value}")

    def get_source_temperature_mode(self) -> str:
        """Returns which set of commands control the temperature subsystem ('FIXed', 'LIST', or 'PROGram')."""
        response = self.instrument.query(":SOUR:TEMP:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        elif response.startswith("PROG"):
            return "PROGRAM"
        return response

    def clear_source_temperature_protection_high(self):
        """Causes the high temperature protection circuit to be cleared.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:TEMP:PROT:HIGH:CLE")

    def set_source_temperature_protection_high_level(self, value: float):
        """Specifies the high temperature trip level.
        Parameters:
        value: The high temperature trip level (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:PROT:HIGH:LEV {value}")

    def get_source_temperature_protection_high_level(self) -> float:
        """Returns the high temperature trip level."""
        response = self.instrument.query(":SOUR:TEMP:PROT:HIGH:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature protection high level (not numeric): '{response}'")

    
    def set_source_temperature_protection_high_state(self, enable: bool):
        """Enables or disables the high temperature protection mechanism.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:TEMP:PROT:HIGH:STATE {scpi_value}")

    def get_source_temperature_protection_high_state(self) -> bool:
        """Returns True if the high temperature protection mechanism is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:TEMP:PROT:HIGH:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for temperature protection high state: '{response}'")

    def set_source_temperature_protection_high_tout(self, value: float):
        """Specifies the time out in the currently specified unit of time for high temperature protection.
        Parameters:
        value: The time out value (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:PROT:HIGH:TOUT {value}")

    def get_source_temperature_protection_high_tout(self) -> float:
        """Returns the time out for high temperature protection."""
        response = self.instrument.query(":SOUR:TEMP:PROT:HIGH:TOUT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature protection high TOUT (not numeric): '{response}'")

    def get_source_temperature_protection_high_tripped(self) -> bool:
        """Returns a 1 if the high temperature protection circuit is tripped and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:TEMP:PROT:HIGH:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for temperature protection high tripped status: '{response}'")

    def clear_source_temperature_protection_low(self):
        """Causes the low temperature protection circuit to be cleared.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:TEMP:PROT:LOW:CLE")

    def set_source_temperature_protection_low_level(self, value: float):
        """Specifies the low temperature trip level.
        Parameters:
        value: The low temperature trip level (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:PROT:LOW:LEV {value}")

    def get_source_temperature_protection_low_level(self) -> float:
        """Returns the low temperature trip level."""
        response = self.instrument.query(":SOUR:TEMP:PROT:LOW:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature protection low level (not numeric): '{response}'")

    def set_source_temperature_protection_low_state(self, enable: bool):
        """Enables or disables the low temperature protection mechanism.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:TEMP:PROT:LOW:STATE {scpi_value}")

    def get_source_temperature_protection_low_state(self) -> bool:
        """Returns True if the low temperature protection mechanism is enabled, False if disabled."""
        response = self.instrument.query(":SOUR:TEMP:PROT:LOW:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for temperature protection low state: '{response}'")

    
    def set_source_temperature_protection_low_tout(self, value: float):
        """Specifies the time out in the currently specified unit of time for low temperature protection.
        Parameters:
        value: The time out value (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:PROT:LOW:TOUT {value}")

    def get_source_temperature_protection_low_tout(self) -> float:
        """Returns the time out for low temperature protection."""
        response = self.instrument.query(":SOUR:TEMP:PROT:LOW:TOUT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature protection low TOUT (not numeric): '{response}'")

    def get_source_temperature_protection_low_tripped(self) -> bool:
        """This query returns a 1 if the protection circuit is tripped and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:TEMP:PROT:LOW:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for temperature protection low tripped status: '{response}'")

    def set_source_temperature_rtime(self, value: float):
        """Instructs the environmental chamber the amount of time it should take to reach the target temperature.
        Parameters:
        value: The ramp time (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:RTIM {value}")

    def get_source_temperature_rtime(self) -> float:
        """Returns the amount of time it should take to reach the target temperature."""
        response = self.instrument.query(":SOUR:TEMP:RTIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature RTIMe (not numeric): '{response}'")

    def set_source_temperature_spoint(self, value: float):
        """Sets the target temperature of the environmental chamber. The units are the current temperature units.
        Parameters:
        value: The setpoint temperature (numeric value)."""
        self.instrument.write(f":SOUR:TEMP:SPO {value}")

    def get_source_temperature_spoint(self) -> float:
        """Returns the target temperature of the environmental chamber."""
        response = self.instrument.query(":SOUR:TEMP:SPO?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for temperature SPOint (not numeric): '{response}'")

    
    def set_source_voltage_attenuation(self, value: float):
        """Sets the ATTenuation level for Voltage.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNIT system."""
        self.instrument.write(f":SOUR:VOLT:ATT {value}")

    def get_source_voltage_attenuation(self) -> float:
        """Returns the ATTenuation level for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage attenuation (not numeric): '{response}'")

    def set_source_voltage_attenuation_auto(self, enable: bool):
        """Couples the attenuator to LEVel for Voltage.
        Parameters:
        enable: True to enable auto-coupling, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:ATT:AUTO {scpi_value}")

    def get_source_voltage_attenuation_auto(self) -> bool:
        """Returns True if auto-coupling of attenuator to LEVel is enabled for Voltage, False if disabled."""
        response = self.instrument.query(":SOUR:VOLT:ATT:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage attenuation auto state: '{response}'")

    def set_source_voltage_alc_state(self, enable: bool):
        """Controls whether the ALC loop controls the output level for Voltage.
        Parameters:
        enable: True to enable ALC, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:ALC:STATE {scpi_value}")

    def get_source_voltage_alc_state(self) -> bool:
        """Returns True if the ALC loop controls the output level for Voltage, False if not."""
        response = self.instrument.query(":SOUR:VOLT:ALC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage ALC state: '{response}'")

    def set_source_voltage_alc_search(self, search_state: str):
        """Enables a form of leveling where the output level is calibrated by momentarily closing the leveling loop for Voltage.
        Parameters:
        search_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets SEARch to ON and then OFF."""
        normalized_state = search_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid search state: '{search_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:VOLT:ALC:SEAR {scpi_value}")

    def get_source_voltage_alc_search(self) -> str:
        """Returns the search state for Voltage ALC ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:VOLT:ALC:SEAR?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    
    def set_source_voltage_alc_source(self, source_type: str):
        """Selects the source of the feedback signal for ALC for Voltage.
        Parameters:
        source_type: INTernal|DIODe|PMETer|MMHead"""
        valid_types = {"INTERNAL", "DIODE", "PMETER", "MMHEAD", "INT", "DIOD", "PMET", "MMH"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid ALC source type: '{source_type}'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "DIODE": scpi_value = "DIOD"
        elif type_upper == "PMETER": scpi_value = "PMET"
        elif type_upper == "MMHEAD": scpi_value = "MMH"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:VOLT:ALC::SOUR {scpi_value}")

    def get_source_voltage_alc_source(self) -> str:
        """Returns the source of the feedback signal for ALC for Voltage ('INTernal', 'DIODe', 'PMETer', or 'MMHead')."""
        response = self.instrument.query(":SOUR:VOLT:ALC::SOUR?").strip().upper()
        if response.startswith("INT"): return "INTernal"
        elif response.startswith("DIOD"): return "DIODe"
        elif response.startswith("PMET"): return "PMETer"
        elif response.startswith("MMH"): return "MMHead"
        return response

    def set_source_voltage_alc_bandwidth(self, value: float):
        """Controls the bandwidth of the ALC feedback signal for Voltage in Hz.
        Parameters:
        value: The bandwidth in Hz (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:ALC:BAND {value}")

    def get_source_voltage_alc_bandwidth(self) -> float:
        """Returns the bandwidth of the ALC feedback signal for Voltage in Hz."""
        response = self.instrument.query(":SOUR:VOLT:ALC:BAND?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage ALC bandwidth (not numeric): '{response}'")

    def set_source_voltage_alc_bandwidth_auto(self, auto_state: str):
        """Couples the bandwidth of the ALC feedback signal to instrument-dependent parameters for Voltage.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:VOLT:ALC:BAND:AUTO {scpi_value}")

    def get_source_voltage_alc_bandwidth_auto(self) -> str:
        """Returns the auto state of the ALC bandwidth for Voltage ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:VOLT:ALC:BAND:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_voltage_center(self, value: float):
        """Sets the center amplitude for Voltage.
        Parameters:
        value: The center amplitude (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:CENT {value}")

    def get_source_voltage_center(self) -> float:
        """Returns the center amplitude for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage center (not numeric): '{response}'")

    
    def set_source_voltage_level_immediate_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Voltage in terms of current operating units.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:IMM:AMPL {value}")

    def get_source_voltage_level_immediate_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LEV:IMM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level immediate amplitude (not numeric): '{response}'")

    def set_source_voltage_level_immediate_amplitude_auto(self, auto_state: str):
        """If AUTO ON is selected, the current setting will be adjusted automatically when a new voltage setting (with the existing current setting) exceeds the maximum power limit.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:VOLT:LEV:IMM:AMPL:AUTO {scpi_value}")

    def get_source_voltage_level_immediate_amplitude_auto(self) -> str:
        """Returns the auto state of the voltage level immediate amplitude ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:VOLT:LEV:IMM:AMPL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_voltage_level_immediate_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal specified in AMPLitude, in terms of current operating units for Voltage.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:IMM:OFFS {value}")

    def get_source_voltage_level_immediate_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LEV:IMM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level immediate offset (not numeric): '{response}'")

    def set_source_voltage_level_immediate_high(self, value: float):
        """Sets the more positive peak of a time varying signal for Voltage.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:IMM:HIGH {value}")

    def get_source_voltage_level_immediate_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LEV:IMM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level immediate high (not numeric): '{response}'")

    def set_source_voltage_level_immediate_low(self, value: float):
        """Sets the more negative peak of a time varying signal for Voltage.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:IMM:LOW {value}")

    def get_source_voltage_level_immediate_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LEV:IMM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level immediate low (not numeric): '{response}'")

    
    def set_source_voltage_level_triggered_amplitude(self, value: float):
        """Sets the actual magnitude of the unswept output signal for Voltage, to be transferred upon trigger.
        Parameters:
        value: The amplitude (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:TRIG:AMPL {value}")

    def get_source_voltage_level_triggered_amplitude(self) -> float:
        """Returns the actual magnitude of the unswept output signal for Voltage (triggered)."""
        response = self.instrument.query(":SOUR:VOLT:LEV:TRIG:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level triggered amplitude (not numeric): '{response}'")

    def set_source_voltage_level_triggered_offset(self, value: float):
        """Sets the non-time varying component of the signal that is added to the time varying signal for Voltage, to be transferred upon trigger.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:TRIG:OFFS {value}")

    def get_source_voltage_level_triggered_offset(self) -> float:
        """Returns the non-time varying component of the signal that is added to the time varying signal for Voltage (triggered)."""
        response = self.instrument.query(":SOUR:VOLT:LEV:TRIG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level triggered offset (not numeric): '{response}'")

    def set_source_voltage_level_triggered_high(self, value: float):
        """This command is used to set the more positive peak of a time varying signal for Voltage. It is used in conjunction with LOW.
        Parameters:
        value: The high peak value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:TRIG:HIGH {value}")

    def get_source_voltage_level_triggered_high(self) -> float:
        """Returns the more positive peak of a time varying signal for Voltage (triggered)."""
        response = self.instrument.query(":SOUR:VOLT:LEV:TRIG:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level triggered high (not numeric): '{response}'")

    def set_source_voltage_level_triggered_low(self, value: float):
        """This command is used to set the more negative peak of a time varying signal for Voltage. It is used in conjunction with HIGH.
        Parameters:
        value: The low peak value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LEV:TRIG:LOW {value}")

    def get_source_voltage_level_triggered_low(self) -> float:
        """Returns the more negative peak of a time varying signal for Voltage (triggered)."""
        response = self.instrument.query(":SOUR:VOLT:LEV:TRIG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage level triggered low (not numeric): '{response}'")

    def set_source_voltage_limit_amplitude(self, value: float):
        """Sets the limit on the actual magnitude of the unswept output signal for Voltage.
        Parameters:
        value: The amplitude limit (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LIM:AMPL {value}")

    def get_source_voltage_limit_amplitude(self) -> float:
        """Returns the limit on the actual magnitude of the unswept output signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LIM:AMPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage limit amplitude (not numeric): '{response}'")

    
    def set_source_voltage_limit_offset(self, value: float):
        """Sets a non-time varying component limit of signal that is added to the time varying signal for Voltage.
        Parameters:
        value: The offset limit (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LIM:OFFS {value}")

    def get_source_voltage_limit_offset(self) -> float:
        """Returns a non-time varying component limit of signal that is added to the time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LIM:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage limit offset (not numeric): '{response}'")

    def set_source_voltage_limit_high(self, value: float):
        """Sets the more positive peak limit of a time varying signal for Voltage. It is used in conjunction with LOW.
        Parameters:
        value: The high peak limit (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LIM:HIGH {value}")

    def get_source_voltage_limit_high(self) -> float:
        """Returns the more positive peak limit of a time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage limit high (not numeric): '{response}'")

    def set_source_voltage_limit_low(self, value: float):
        """Sets the more negative peak limit of a time varying signal for Voltage. It is used in conjunction with HIGH.
        Parameters:
        value: The low peak limit (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:LIM:LOW {value}")

    def get_source_voltage_limit_low(self) -> float:
        """Returns the more negative peak limit of a time varying signal for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage limit low (not numeric): '{response}'")

    def set_source_voltage_limit_state(self, enable: bool):
        """Controls whether the LIMit is enabled for Voltage.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:LIM:STATE {scpi_value}")

    def get_source_voltage_limit_state(self) -> bool:
        """Returns True if the LIMit is enabled for Voltage, False if disabled."""
        response = self.instrument.query(":SOUR:VOLT:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage limit state: '{response}'")

    def set_source_voltage_manual(self, value: float):
        """Allows manual adjustment of the amplitude between the sweep limits for Voltage.
        Parameters:
        value: The manual amplitude value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:MAN {value}")

    def get_source_voltage_manual(self) -> float:
        """Returns the manual amplitude for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage manual (not numeric): '{response}'")

    def set_source_voltage_mode(self, mode_type: str):
        """Determines which set of commands control the amplitude subsystem for Voltage.
        Parameters:
        mode_type: FIXed|SWEep|LIST"""
        valid_types = {"FIXED", "SWEEP", "LIST", "FIX", "SWE"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid voltage mode: '{mode_type}'. Must be 'FIXed', 'SWEep', or 'LIST'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        else: scpi_value = type_upper

        self.instrument.write(f":SOUR:VOLT:MODE {scpi_value}")

    def get_source_voltage_mode(self) -> str:
        """Returns which set of commands control the amplitude subsystem for Voltage ('FIXed', 'SWEep', or 'LIST')."""
        response = self.instrument.query(":SOUR:VOLT:MODE?").strip().upper()
        if response.startswith("FIX"):
            return "FIXED"
        elif response.startswith("SWE"):
            return "SWEEP"
        return response

    
    def set_source_voltage_protection_level(self, value: float):
        """Sets the output level at which the output protection circuit will trip for Voltage.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:PROT:LEV {value}")

    def get_source_voltage_protection_level(self) -> float:
        """Returns the output level at which the output protection circuit will trip for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage protection level (not numeric): '{response}'")

    def set_source_voltage_protection_state(self, enable: bool):
        """Controls whether the output protection circuit is enabled for Voltage.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:PROT:STATE {scpi_value}")

    def get_source_voltage_protection_state(self) -> bool:
        """Returns True if the output protection circuit is enabled for Voltage, False if disabled."""
        response = self.instrument.query(":SOUR:VOLT:PROT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage protection state: '{response}'")

    def get_source_voltage_protection_tripped(self) -> bool:
        """Returns a 1 if the protection circuit is tripped for Voltage and a 0 if it is untripped.
        Notes: Query only."""
        response = self.instrument.query(":SOUR:VOLT:PROT:TRIP?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage protection tripped status: '{response}'")

    def clear_source_voltage_protection(self):
        """Causes the protection circuit to be cleared for Voltage.
        Notes: This command is an event and has no associated *RST condition."""
        self.instrument.write(":SOUR:VOLT:PROT:CLE")

    def set_source_voltage_range(self, value: float):
        """Sets a range for the output amplitude for Voltage.
        Parameters:
        value: The range value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:RANG {value}")

    def get_source_voltage_range(self) -> float:
        """Returns the range for the output amplitude for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:RANG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage range (not numeric): '{response}'")

    def set_source_voltage_range_auto(self, auto_state: str):
        """Couples the RANGe to an instrument-determined value for Voltage.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SOUR:VOLT:RANG:AUTO {scpi_value}")

    def get_source_voltage_range_auto(self) -> str:
        """Returns the auto state of the Voltage range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SOUR:VOLT:RANG:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_source_voltage_reference(self, value: float):
        """Sets a reference value for Voltage which, if STATe is ON, allows all amplitude parameters to be queried/set as relative to the reference value.
        Parameters:
        value: The reference value (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:REF {value}")

    def get_source_voltage_reference(self) -> float:
        """Returns the reference value for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage reference (not numeric): '{response}'")

    
    def set_source_voltage_reference_state(self, enable: bool):
        """Determines whether amplitude is measured/output in absolute or relative mode for Voltage.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:REF:STATE {scpi_value}")

    def get_source_voltage_reference_state(self) -> bool:
        """Returns True if amplitude is measured/output in relative mode for Voltage, False for absolute mode."""
        response = self.instrument.query(":SOUR:VOLT:REF:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage reference state: '{response}'")

    def set_source_voltage_slew(self, value: float):
        """Sets the slew rate of the output change when a new output level is programmed for Voltage. The units are in (the currently active) amplitude unit/sec.
        Parameters:
        value: The slew rate (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:SLEW {value}")

    def get_source_voltage_slew(self) -> float:
        """Returns the slew rate of the output change for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:SLEW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage slew (not numeric): '{response}'")

    def set_source_voltage_span(self, value: float):
        """Sets the amplitude span for Voltage. If current amplitude unit is logarithmic (dBm, dBuV, etc), then unit of SPAN is dB. Otherwise SPAN is programmed in current amplitude unit.
        Parameters:
        value: The amplitude span (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:SPAN {value}")

    def get_source_voltage_span(self) -> float:
        """Returns the amplitude span for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage span (not numeric): '{response}'")

    def set_source_voltage_span_hold(self, enable: bool):
        """Provides a mechanism to prevent the SPAN from being changed implicitly by the defined coupling between STARt, STOP, CENTer and SPAN for Voltage.
        Parameters:
        enable: True to hold SPAN, False to allow changes."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":SOUR:VOLT:SPAN:HOLD {scpi_value}")

    def get_source_voltage_span_hold(self) -> bool:
        """Returns True if SPAN is held for Voltage, False if not."""
        response = self.instrument.query(":SOUR:VOLT:SPAN:HOLD?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage span hold state: '{response}'")

    def set_source_voltage_span_link(self, link_parameter: str):
        """Allows the default couplings for SPAN to be overridden for Voltage. LINK selects the parameter, either CENTer, STARt or STOP, that shall not be changed when SPAN’s value is changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SOUR:VOLT:SPAN:LINK {scpi_value}")

    def get_source_voltage_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN’s value is changed for Voltage ('CENTer', 'STARt', or 'STOP')."""
        response = self.instrument.query(":SOUR:VOLT:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        return response

    def source_voltage_span_full(self):
        """Sets STARt amplitude to its minimum value and STOP amplitude to its maximum value for Voltage. CENTer amplitude and SPAN are set to their coupled values.
        Notes: This command is an event rather than a state."""
        self.instrument.write(":SOUR:VOLT:SPAN:FULL")

    def set_source_voltage_start(self, value: float):
        """Sets STARt amplitude for Voltage.
        Parameters:
        value: The start amplitude (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:STAR {value}")

    def get_source_voltage_start(self) -> float:
        """Returns STARt amplitude for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage start (not numeric): '{response}'")

    
    def set_source_voltage_stop(self, value: float):
        """Sets STOP amplitude for Voltage.
        Parameters:
        value: The stop amplitude (numeric value)."""
        self.instrument.write(f":SOUR:VOLT:STOP {value}")

    def get_source_voltage_stop(self) -> float:
        """Returns STOP amplitude for Voltage."""
        response = self.instrument.query(":SOUR:VOLT:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage stop (not numeric): '{response}'")
