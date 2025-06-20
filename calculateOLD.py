class Calculate():
    def __init__(self):
        self.instrument = None
    
    #CALCULATE
    #TODO: Check that assumption about sequential calc from last data sensed is correct
    def clear_average_data(self):
        """This command causes the average data to be 
        cleared and the average counter reset to zero."""
        self.instrument.write("CALC:AVER:CLE")


    def set_count_of_results_in_average(self, auto, count, once = False):
        """TODO Check what means by using time setting and update below with function names
        Specifies the number of measurements to combine using the :TYPE setting. After :COUNt
        measurements have been averaged, the operation of the AVERage subsystem is controlled
        by the setting of the :TCONtrol node."""
        if auto:
            if once:
                self.instrument.write(f"CALC:AVER:COUNT:AUTO ONCE")
            self.instrument.write(f"CALC:AVER:COUNT:AUTO 1")

        else:
            #TODO Check if needed
            #self.instrument.write(f"CALC:AVER:COUNT:AUTO 0")
            self.instrument.write(f"CALC:AVER:COUNT {count}")
        #Further details
        """The count for array based results is independent of the number of points in the result array.
        For example, an instrument which normally provides a measurement result which is a 401
        point array would specify an average count of two to average two results, not 802.
        When averaging is ON, some devices may automatically set :COUNt values in the TRIGger
        subsystem based on the AVER:COUNt value, such that the TRIGger subsystem provides
        enough triggers for the average.
        At *RST, this value is device dependent."""

    #TODO Check if this works
    def get_count_of_results_in_average(self, check_auto):
        """Either returns if average is using"""
        a = None
        if check_auto:
            a = self.instrument.query(f"CALC:AVER:COUNT:AUTO?")
        c = self.instrument.query(f"CALC:AVER:COUNT?")
        return c, a

    def set_averaging(self, turn_on):
        """The used to turn averaging ON and OFF."""
        if turn_on:
            self.instrument.write(f"CALC:AVER:STATE 1")
        else:
            self.instrument.write(f"CALC:AVER:STATE 0")
    
    def is_averaging_on(self):
        """If averaging is ON and OFF."""
        return int(self.instrument.query("CALC:AVER:STATE?"))
    
    def make_average_weighted(self, update="NORM"):
        """Set how to update average when new data points are added to it.
        Parameters:
        update: EXPonential|MOVing|NORMal|REPeat"""

        valid_update = ["Exponential", "EXP", "Moving","MOV","Normal","NORM","Repeat","REP"]
        if update in valid_update:
            self.instrument.write(f"CALCulate:AVERage:TCONtrol {update}")
        else:
            print("Value is not accepted. Please enter one of the following arguments for update: ")
            print(valid_update)

    def get_how_average_weighted(self):
        """Check how the average is updated when new data points are added to it."""
        return self.instrument.query("CALCulate:AVERage:TCONtrol?")
    
    def set_average_type(self, type):
        """Set type of averaging fomula used. For complete formula see SCPI-99 doc Sec 4.1.5.
        Parameters: 
        type: COMPlex | ENVelope | MAXimum | MINimum | RMS | SCALar"""
        valid_type = ["COMP","Complex","ENV","Envelope", "MAX", "Maximum", "MIN","Minimum", "RMS","SCAL","Scalar"]
        if type in valid_type:
            self.instrument.write(f"CALCulate:AVERage:TYPE {type}")
        else:
            print("Value is not accepted. Please enter one of the following arguments: ")
            print(valid_type)
    
    def get_average_type(self):
        """Get type of averaging fomula used. For complete formula see SCPI-99 doc Sec 4.1.5."""
        return self.instrument.query(f"CALCulate:AVERage:TYPE?")
    
        #Limit Results Tree
    def get_limit_fail(self):
        """Gives if there is a limit with failure."""
        return self.instrument.query("CALCulate:CLIMits:FAIL?")

    def get_failed_limit_list(self):
        """Returns list of limits that have failed. None if there are none."""
        return self.instrument.query("CALCulate:CLIMits:FLIMITS:DATA?")

    def get_failed_limit_count(self):
        """Returns list of limits that have failed. None if there are none."""
        return self.instrument.query("CALCulate:CLIMits:FLIMITS:POINTS?")
    
    def get_calc_system_results(self):
        """Returns all data linked to calculate system."""
        return self.instrument.query("CALCulate:DATA?")

    def get_calc_system_preamble_results(self):
        """Returns overview of calculate system data."""
        return self.instrument.query("CALCulate:DATA:PREamble?")
    
    def set_derivative_state(self, enable: bool):
        """
        Determines whether the derivative function is enabled.

        Corresponds to the SCPI command: CALCulate:DERivative:STATe <boolean>
        At *RST, this function is OFF (False).

        :param enable: True to enable the derivative function, False to disable it.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:DER:STATE {scpi_value}")
        #print(f"Set derivative state to: {scpi_value}")

    def get_derivative_state(self) -> bool:
        """
        Queries the current state of the derivative function.

        Corresponds to the SCPI query: CALCulate:DERivative:STATe?

        :return: True if the derivative function is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:DER:STATE?")
        response = response.strip()

        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        
        else:
            raise ValueError(f"Unexpected response for derivative state: '{response}'")

    def set_derivative_points(self, points: int):
        """
        Specifies the number of points provided to the differential algorithm.
        Points will be centered about the current data point.

        Corresponds to the SCPI command: CALCulate:DERivative:POINts <NR1>
        At *RST, this value is device dependent.

        :param points: The number of points (integer) for the algorithm.
                       Must be a non-negative integer. Instrument might have
                       specific valid ranges.
        :raises ValueError: If 'points' is not a positive integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Derivative points must be a non-negative integer.")
        self.instrument.write(f"CALC:DER:POIN {points}")
        print(f"Set derivative points to: {points}")

    def get_derivative_points(self) -> int:
        """
        Queries the number of points provided to the differential algorithm.

        Corresponds to the SCPI query: CALCulate:DERivative:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:DER:POIN?")
        response = response.strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for derivative points (not an integer): '{response}'")


    def set_feed_source(self, feed_source: str):
        #TODO: Look into format of data_handle
        """
        Sets the data flow to be fed into the CALCulate block.

        Corresponds to the SCPI command: CALCulate:FEED <character_string>
        At *RST, FEED shall be set to a device dependent value.

        :param feed_source: A string representing the data source (e.g., 'TWIR01p13').
        """
        # SCPI allows bare strings or quoted strings for character data.
        # For simple identifiers, typically no quotes are needed.
        self.instrument.write(f"CALC:FEED {feed_source}")
        print(f"Set calculation feed source to: {feed_source}")

    def get_feed_source(self) -> str:
        """
        Queries the data flow currently fed into the CALCulate block.

        Corresponds to the SCPI query: CALCulate:FEED?

        :return: A string representing the current data source.
        """
        response = self.instrument.query("CALC:FEED?")
        # Remove any leading/trailing whitespace or quotes if the instrument returns them.
        return response.strip().strip('"')
    def set_filter_gate_time_state(self, enable: bool):
        #TODO: Check if :FIlter has own implementation or just subcategory
        """
        Determines whether the time filter is enabled.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:STATe <boolean>
        At *RST, this function is OFF (False).

        :param enable: True to enable the time filter, False to disable it.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:FILT:GATE:TIME:STATE {scpi_value}")

    def get_filter_gate_time_state(self) -> bool:
        """
        Queries whether the time filter is enabled.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:STATe?

        :return: True if the time filter is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter gate time state: '{response}'")

    def set_filter_gate_time_type(self, filter_type: str):
        """
        Specifies what occurs to the data in the specific time region for the filter.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:TYPE BPASs|NOTCh
        At *RST, this value is device-dependent.

        :param filter_type: The type of filter. Must be 'BPASS' or 'NOTCH'.
                            Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid filter type is provided.
        """
        valid_types = {"BPASS", "NOTCH"}
        filter_type_upper = filter_type.upper()
        if filter_type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be one of {list(valid_types)}")

        # SCPI allows abbreviated forms, e.g., 'BPAS' for 'BPASs' and 'NOTC' for 'NOTCh'.
        # Sending the full capitalized form is also common and safe.
        self.instrument.write(f"CALC:FILT:GATE:TIME:TYPE {filter_type_upper}")

    def get_filter_gate_time_type(self) -> str:
        """
        Queries what occurs to the data in the specific time region for the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:TYPE?

        :return: The type of filter ('BPASS' or 'NOTCH').
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:TYPE?").strip()
        # Instruments often return the long form or the exact form sent.
        # Normalize to 'BPASS' or 'NOTCH' for consistent Python return values.
        if response.upper().startswith("BPAS"):
            return "BPASS"
        elif response.upper().startswith("NOTC"):
            return "NOTCH"
        else:
            # Handle cases where response is unexpected or device-specific
            return response # Return raw response if not standard

    def set_filter_gate_time_start(self, start_time: float):
        """
        Specifies the start time of the filter in seconds.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:STARt <NRf>
        At *RST, STARt is set to MIN.

        :param start_time: The start time in seconds (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:STAR {start_time}")

    def get_filter_gate_time_start(self) -> float:
        """
        Queries the start time of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:STARt?

        :return: The start time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time start (not numeric): '{response}'")

    def set_filter_gate_time_stop(self, stop_time: float):
        """
        Specifies the stop time of the filter in seconds.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:STOP <NRf>
        At *RST, STOP is set to MIN.

        :param stop_time: The stop time in seconds (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:STOP {stop_time}")

    def get_filter_gate_time_stop(self) -> float:
        """
        Queries the stop time of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:STOP?

        :return: The stop time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time stop (not numeric): '{response}'")

    def set_filter_gate_time_span(self, span_time: float):
        """
        Specifies the time span of the filter in seconds.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:SPAN <NRf>
        At *RST, SPAN is set to MIN.

        :param span_time: The time span in seconds (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:SPAN {span_time}")

    def get_filter_gate_time_span(self) -> float:
        """
        Queries the time span of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:SPAN?

        :return: The time span in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time span (not numeric): '{response}'")

    def set_filter_gate_time_center(self, center_time: float):
        """
        Specifies the center time of the filter in seconds.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:CENTer <NRf>
        At *RST, CENTer is set to MIN.

        :param center_time: The center time in seconds (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:CENT {center_time}")

    def get_filter_gate_time_center(self) -> float:
        """
        Queries the center time of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:CENTer?

        :return: The center time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time center (not numeric): '{response}'")

    def set_filter_gate_time_points(self, points: int):
        """
        Specifies the number of points output by the filter subsystem.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:POINts <NR1>
        At *RST, this value is device-dependent.

        :param points: The number of points (integer) to be output.
                       Must be a non-negative integer. Instrument might have
                       specific valid ranges.
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Filter gate time points must be a non-negative integer.")
        self.instrument.write(f"CALC:FILT:GATE:TIME:POIN {points}")

    def get_filter_gate_time_points(self) -> int:
        """
        Queries the number of points output by the filter subsystem.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time points (not an integer): '{response}'")

    def set_filter_gate_time_points_auto(self, auto_mode: str):
        """
        Controls whether the filter output points are automatically set by device-dependent parameters.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:POINts:AUTO AUTO|ONCE
        At *RST, AUTO is ON.

        :param auto_mode: The auto mode setting. Must be 'AUTO' or 'ONCE'.
                          Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid auto mode is provided.
        """
        valid_modes = {"AUTO", "ONCE"}
        auto_mode_upper = auto_mode.upper()
        if auto_mode_upper not in valid_modes:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be one of {list(valid_modes)}")
        self.instrument.write(f"CALC:FILT:GATE:TIME:POIN:AUTO {auto_mode_upper}")

    def get_filter_gate_time_points_auto(self) -> str:
        """
        Queries whether the filter output points are automatically set.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:POINts:AUTO?

        :return: The auto mode setting ('AUTO' or 'ONCE').
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:POIN:AUTO?").strip()
        if response == "1" or response.upper() == "AUTO":
            return "AUTO"
        elif response == "0" or response.upper() == "ONCE":
            return "ONCE"
        else:
            return response

    def set_filter_gate_time_window(self, window_type: str):
        """
        Specifies the type of data windowing (shaping) done prior to the filter.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:WINDow <window_type>
        Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential
        At *RST, this value is device-dependent.

        :param window_type: The type of window. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid window type is provided.
        """
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f"CALC:FILT:GATE:TIME:WIND {window_type_upper}")

    def get_filter_gate_time_window(self) -> str:
        """
        Queries the type of data windowing done prior to the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:WINDow?

        :return: The type of window (e.g., 'RECTANGULAR', 'FLATTOP').
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:WIND?").strip()
        return response.upper()

    def set_filter_gate_time_kbessel_parameter(self, parameter: float):
        """
        Sets the parametric window parameter for the Kaiser Bessel window.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:KBESsel <NRf>
        At *RST, this value is device-dependent.

        :param parameter: The parameter for the Kaiser Bessel window (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:KBES {parameter}")

    def get_filter_gate_time_kbessel_parameter(self) -> float:
        """
        Queries the parametric window parameter for the Kaiser Bessel window.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:KBESsel?

        :return: The parameter for the Kaiser Bessel window (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")
        
    def set_filter_gate_time_exponential_parameter(self, decay_time_constant: float):
        """
        Enters the exponential decay time constant which characterizes the EXPonential window.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:EXPonential <NRf>
        At *RST, this value is device-dependent.

        :param decay_time_constant: The exponential decay time constant (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:EXP {decay_time_constant}")

    def get_filter_gate_time_exponential_parameter(self) -> float:
        """
        Queries the exponential decay time constant which characterizes the EXPonential window.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:EXPonential?

        :return: The exponential decay time constant (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")


    def set_filter_gate_time_force(self, value: float):
        """
        Enters the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:TIME:FORCe <NRf>
        At *RST, this value is device-dependent.

        :param value: The time value parameter (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:TIME:FORCE {value}")

    def get_filter_gate_time_force(self) -> float:
        """
        Queries the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:TIME:FORCe?

        :return: The time value parameter (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:TIME:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time force (not numeric): '{response}'")

    def set_filter_gate_frequency_state(self, enable: bool):
        """
        Determines whether the frequency filter is enabled.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:STATe <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable the frequency filter, False to disable it.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:FILT:GATE:FREQ:STATE {scpi_value}")

    def get_filter_gate_frequency_state(self) -> bool:
        """
        Queries whether the frequency filter is enabled.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:STATe?

        :return: True if the frequency filter is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter gate frequency state: '{response}'")

    def set_filter_gate_frequency_type(self, filter_type: str):
        """
        Specifies what occurs to the data in the specific frequency region.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:TYPE BPASs|NOTCh
        At *RST, this value is device-dependent.

        :param filter_type: The type of filter. Must be 'BPASS' or 'NOTCH'.
                            Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid filter type is provided.
        """
        valid_types = {"BPASS", "NOTCH"}
        filter_type_upper = filter_type.upper()
        if filter_type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:FILT:GATE:FREQ:TYPE {filter_type_upper}")

    def get_filter_gate_frequency_type(self) -> str:
        """
        Queries what occurs to the data in the specific frequency region.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:TYPE?

        :return: The type of filter ('BPASS' or 'NOTCH').
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:TYPE?").strip()
        if response.upper().startswith("BPAS"):
            return "BPASS"
        elif response.upper().startswith("NOTC"):
            return "NOTCH"
        else:
            return response

    def set_filter_gate_frequency_start(self, start_freq: float):
        """
        Specifies the start frequency of the filter in Hertz.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:STARt <NRf>
        At *RST, STARt is set to MIN.

        :param start_freq: The start frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:STAR {start_freq}")

    def get_filter_gate_frequency_start(self) -> float:
        """
        Queries the start frequency of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:STARt?

        :return: The start frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency start (not numeric): '{response}'")

    def set_filter_gate_frequency_stop(self, stop_freq: float):
        """
        Specifies the stop frequency of the filter in Hertz.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:STOP <NRf>
        At *RST, STOP is set to MIN.

        :param stop_freq: The stop frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:STOP {stop_freq}")

    def get_filter_gate_frequency_stop(self) -> float:
        """
        Queries the stop frequency of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:STOP?

        :return: The stop frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency stop (not numeric): '{response}'")


    def set_filter_gate_frequency_span(self, span_freq: float):
        """
        Specifies the frequency span of the filter in Hertz.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:SPAN <NRf>
        At *RST, SPAN is set to MIN.

        :param span_freq: The frequency span in Hertz (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:SPAN {span_freq}")

    def get_filter_gate_frequency_span(self) -> float:
        """
        Queries the frequency span of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:SPAN?

        :return: The frequency span in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency span (not numeric): '{response}'")

    def set_filter_gate_frequency_center(self, center_freq: float):
        """
        Specifies the center frequency of the filter in Hertz.
        Range is instrument- and setup-dependent.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:CENTer <NRf>
        At *RST, CENTer is set to MIN.

        :param center_freq: The center frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:CENT {center_freq}")

    def get_filter_gate_frequency_center(self) -> float:
        """
        Queries the center frequency of the filter.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:CENTer?

        :return: The center frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency center (not numeric): '{response}'")

    def set_filter_gate_frequency_points(self, points: int):
        """
        Specifies the number of points output by the filter subsystem for frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:POINts <NR1>
        At *RST, this value is device-dependent.

        :param points: The number of points (integer) to be output.
                       Must be a non-negative integer.
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Filter gate frequency points must be a non-negative integer.")
        self.instrument.write(f"CALC:FILT:GATE:FREQ:POIN {points}")

    def get_filter_gate_frequency_points(self) -> int:
        """
        Queries the number of points output by the filter subsystem for frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency points (not an integer): '{response}'")

    def set_filter_gate_frequency_points_auto(self, auto_mode: str):
        """
        Controls whether the filter output points are automatically set by device-dependent parameters
        for the frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:POINts:AUTO AUTO|ONCE
        At *RST, AUTO is ON.

        :param auto_mode: The auto mode setting. Must be 'AUTO' or 'ONCE'.
                          Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid auto mode is provided.
        """
        valid_modes = {"AUTO", "ONCE"}
        auto_mode_upper = auto_mode.upper()
        if auto_mode_upper not in valid_modes:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be one of {list(valid_modes)}")
        self.instrument.write(f"CALC:FILT:GATE:FREQ:POIN:AUTO {auto_mode_upper}")

    def get_filter_gate_frequency_points_auto(self) -> str:
        """
        Queries whether the filter output points are automatically set for the frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:POINts:AUTO?

        :return: The auto mode setting ('AUTO' or 'ONCE').
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:POIN:AUTO?").strip()
        if response == "1" or response.upper() == "AUTO":
            return "AUTO"
        elif response == "0" or response.upper() == "ONCE":
            return "ONCE"
        else:
            return response

    def set_filter_gate_frequency_window(self, window_type: str):
        """
        Specifies the type and parameter of data windowing (shaping) done prior to the filter
        for the frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:WINDow <window_type>
        Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential
        At *RST, this value is device-dependent.

        :param window_type: The type of window. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid window type is provided.
        """
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f"CALC:FILT:GATE:FREQ:WIND {window_type_upper}")

    def get_filter_gate_frequency_window(self) -> str:
        """
        Queries the type of data windowing done prior to the filter for the frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:WINDow?

        :return: The type of window (e.g., 'RECTANGULAR', 'FLATTOP').
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:WIND?").strip()
        return response.upper()

    def set_filter_gate_frequency_kbessel_parameter(self, parameter: float):
        """
        Sets the parametric window parameter for the Kaiser Bessel window for the frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:KBESsel <NRf>
        At *RST, this value is device-dependent.

        :param parameter: The parameter for the Kaiser Bessel window (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:KBES {parameter}")

    def get_filter_gate_frequency_kbessel_parameter(self) -> float:
        """
        Queries the parametric window parameter for the Kaiser Bessel window for the frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:KBESsel?

        :return: The parameter for the Kaiser Bessel window (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")

    def set_filter_gate_frequency_exponential_parameter(self, decay_time_constant: float):
        """
        Enters the exponential decay time constant which characterizes the EXPonential window
        for the frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:EXPonential <NRf>
        At *RST, this value is device-dependent.

        :param decay_time_constant: The exponential decay time constant (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:EXP {decay_time_constant}")

    def get_filter_gate_frequency_exponential_parameter(self) -> float:
        """
        Queries the exponential decay time constant which characterizes the EXPonential window
        for the frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:EXPonential?

        :return: The exponential decay time constant (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")

    def set_filter_gate_frequency_force(self, value: float):
        """
        Enters the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in the frequency domain.

        Corresponds to the SCPI command: CALCulate:FILTer:GATE:FREQuency:FORCe <NRf>
        At *RST, this value is device-dependent.

        :param value: The time value parameter (float or int).
        """
        self.instrument.write(f"CALC:FILT:GATE:FREQ:FORCE {value}")

    def get_filter_gate_frequency_force(self):
        """
        Queries the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in the frequency domain.

        Corresponds to the SCPI query: CALCulate:FILTer:GATE:FREQuency:FORCe?

        :return: The time value parameter (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FILT:GATE:FREQ:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency force (not numeric): '{response}'")

    def set_format(self, format_type: str):
        """
        Determines a simple post-processing of SENSe data.

        Corresponds to the SCPI command: CALCulate:FORMat <format_type>
        Valid types: NONE|MLINear|MLOGarithmic|PHASE|REAL|IMAGinary|SWR|GDELay|
                     COMPlex|NYQuist|NICHols|POLar|UPHase

        :param format_type: The desired format type. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid format type is provided.
        """
        valid_formats = {
            "NONE", "MLINEAR", "MLOGARITHMIC", "PHASE", "REAL", "IMAGINARY",
            "SWR", "GDELAY", "COMPLEX", "NYQUIST", "NICHOLS", "POLAR", "UPHASE"
        }
        format_type_upper = format_type.upper()
        if format_type_upper not in valid_formats:
            raise ValueError(
                f"Invalid format type: '{format_type}'. Must be one of {list(valid_formats)}"
            )
        self.instrument.write(f"CALC:FORM {format_type_upper}")

    def get_format(self):
        """
        Queries the current post-processing format of SENSe data.

        Corresponds to the SCPI query: CALCulate:FORMat?

        :return: The current format type (e.g., 'MLOGARITHMIC', 'COMPLEX').
        """
        response = self.instrument.query("CALC:FORM?").strip()
        return response.upper()


    def set_format_uphase_creference(self, reference_freq: float):
        """
        Specifies a reference position (frequency) for unwrapped phase computation.

        Corresponds to the implied SCPI command: CALCulate:FORMat:UPHase:CREFerence <NRf>

        :param reference_freq: The reference frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:FORM:UPH:CREF {reference_freq}")

    def get_format_uphase_creference(self):
        """
        Queries the reference position (frequency) for unwrapped phase computation.

        Corresponds to the implied SCPI query: CALCulate:FORMat:UPHase:CREFerence?

        :return: The reference frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:FORM:UPH:CREF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for UPHase reference frequency (not numeric): '{response}'")

    def set_format_uphase_preference(self, preference_angle: float, angle_units: str = "DEG"):
        """
        Specifies the preferred unwrapped phase angle and its units.

        Corresponds to the implied SCPI command: CALCulate:FORMat:UPHase:PREFerence <NRf>[, <units>]
        Units specified in current angle units. If current angle units are radians,
        replace the constant 360 with 2*PI.

        :param preference_angle: The preferred angle (float or int).
        :param angle_units: The units for the angle (e.g., 'DEG', 'RAD'). Defaults to 'DEG'.
                            This parameter is inferred from the document example, and
                            instrument behavior may vary regarding explicit unit setting.
        """
        self.instrument.write(f"CALC:FORM:UPH:PREF {preference_angle},{angle_units}")

    def get_format_uphase_preference(self):
        """
        Queries the preferred unwrapped phase angle and its units.

        Corresponds to the implied SCPI query: CALCulate:FORMat:UPHase:PREFerence?

        :return: A tuple containing the preferred angle (float) and its units (str).
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:FORM:UPH:PREF?").strip()
        parts = response.split(',')
        if len(parts) == 2:
            try:
                angle = float(parts[0])
                units = parts[1].strip()
                return angle, units
            except ValueError:
                raise ValueError(f"Unexpected response format for UPHase preference: '{response}'")
        elif len(parts) == 1:
            try:
                return float(parts[0]), "DEG"
            except ValueError:
                raise ValueError(f"Unexpected response format for UPHase preference: '{response}'")
        else:
            raise ValueError(f"Unexpected response format for UPHase preference: '{response}'")
    
    def set_gdaperture_span(self, span_value: float):
        """
        Specifies the aperture in Hertz for Group Delay Aperture.

        Corresponds to the SCPI command: CALCulate:GDAPerture:SPAN <NRf>
        At *RST, this function is set to MIN.

        :param span_value: The aperture span in Hertz (float or int).
        """
        self.instrument.write(f"CALC:GDAP:SPAN {span_value}")

    def get_gdaperture_span(self) -> float:
        """
        Queries the aperture in Hertz for Group Delay Aperture.

        Corresponds to the SCPI query: CALCulate:GDAPerture:SPAN?

        :return: The aperture span in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:GDAP:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for GDAPerture span (not numeric): '{response}'")

    def set_gdaperture_aperture(self, aperture_ratio: float):
        """
        Specifies the aperture as a ratio of desired aperture span/measured frequency span.

        Corresponds to the SCPI command: CALCulate:GDAPerture:APERture <NRf>
        At *RST, this value is set to MIN.

        :param aperture_ratio: The aperture ratio (float or int).
        """
        self.instrument.write(f"CALC:GDAP:APER {aperture_ratio}")

    def get_gdaperture_aperture(self) -> float:
        """
        Queries the aperture as a ratio of desired aperture span/measured frequency span.

        Corresponds to the SCPI query: CALCulate:GDAPerture:APERture?

        :return: The aperture ratio (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:GDAP:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for GDAPerture aperture (not numeric): '{response}'")


    def immediate_reprocess_data(self):
        """
        Causes the CALCulate subsystem to reprocess existing SENSe data without reacquiring.
        This command describes an event and therefore has no associated *RST condition.

        Corresponds to the SCPI command: CALCulate:IMMediate
        """
        self.instrument.write(f"CALC:IMM")

    def get_immediate_reprocessed_data(self):
        """
        Queries the results of the new calculation after reprocessing existing SENSe data.
        Semantically equivalent to CALC:IMM;DATA?.

        Corresponds to the SCPI query: CALCulate:IMMediate?

        :return: The instrument's response, which should be the calculated data.
        """
        # The documentation states CALC:IMM? is semantically equivalent to CALC:IMM;DATA?
        # So it implies it will trigger calculation and then return data.
        return self.instrument.query(f"CALC:IMM?")

    def set_immediate_auto_state(self, enable: bool):
        """
        Specifies if the CALCulate subsystem continually transforms the data (AUTO ON)
        whenever any changes are made which would affect the CALCulate subsystem output.

        Corresponds to the SCPI command: CALCulate:IMMediate:AUTO <boolean>
        At *RST, this value is set to OFF.

        :param enable: True to enable auto-transformation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:IMM:AUTO {scpi_value}")

    def get_immediate_auto_state(self) -> bool:
        """
        Queries the auto-transformation state of the CALCulate subsystem.

        Corresponds to the SCPI query: CALCulate:IMMediate:AUTO?

        :return: True if auto-transformation is ON, False if OFF.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:IMM:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for immediate auto state: '{response}'")

    def set_integral_state(self, enable: bool):
        """
        Determines whether the integrate function is enabled.

        Corresponds to the SCPI command: CALCulate:INTegral:STATe <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable the integrate function, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:INT:STATE {scpi_value}")

    def get_integral_state(self) -> bool:
        """
        Queries whether the integrate function is enabled.

        Corresponds to the SCPI query: CALCulate:INTegral:STATe?

        :return: True if the integrate function is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:INT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for integral state: '{response}'")

    def set_integral_type(self, integral_type: str):
        """
        Specifies whether the integral result is a single value (SCALar) or a set of data points (MOVing).

        Corresponds to the SCPI command: CALCulate:INTegral:TYPE SCALar|MOVing
        At *RST, this function is set to a device dependent value.

        :param integral_type: The type of integral result. Must be 'SCALAR' or 'MOVING'.
                              Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid integral type is provided.
        """
        valid_types = {"SCALAR", "MOVING"}
        integral_type_upper = integral_type.upper()
        if integral_type_upper not in valid_types:
            raise ValueError(f"Invalid integral type: '{integral_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:INT:TYPE {integral_type_upper}")

    def get_integral_type(self) -> str:
        """
        Queries whether the integral result is a single value (SCALar) or a set of data points (MOVing).

        Corresponds to the SCPI query: CALCulate:INTegral:TYPE?

        :return: The type of integral result ('SCALAR' or 'MOVING').
        """
        response = self.instrument.query("CALC:INT:TYPE?").strip()
        if response.upper().startswith("SCA"):
            return "SCALAR"
        elif response.upper().startswith("MOV"):
            return "MOVING"
        else:
            return response # Return raw response if not standard


    def set_limit_state(self, enable: bool):
        """
        Sets or queries if the LIMit test is active or not.

        Corresponds to the SCPI command: CALCulate:LIMit:STATE <boolean>
        At *RST, this is set to OFF.

        :param enable: True to activate the limit test, False to deactivate.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:LIM:STATE {scpi_value}")

    def get_limit_state(self) -> bool:
        """
        Queries if the LIMit test is active or not.

        Corresponds to the SCPI query: CALCulate:LIMit:STATE?

        :return: True if the limit test is active, False if not.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:LIM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for limit state: '{response}'")

    def set_limit_control_data(self, data_points: list[float]):
        """
        Sets the CONTrol axis data for vector limit tests.

        Corresponds to the SCPI command: CALCulate:LIMit:CONTrol:DATA <NRf>{,<NRf>}

        :param data_points: A list of numeric values representing the control axis data.
        """
        data_str = ",".join(map(str, data_points))
        self.instrument.write(f"CALC:LIM:CONT:DATA {data_str}")

    def get_limit_control_data(self) -> list[float]:
        """
        Queries the CONTrol axis data for vector limit tests.

        Corresponds to the SCPI query: CALCulate:LIMit:CONTrol:DATA?

        :return: A list of numeric values representing the control axis data.
        :raises ValueError: If the instrument returns non-numeric data or an unexpected format.
        """
        response = self.instrument.query("CALC:LIM:CONT:DATA?").strip()
        try:
            return [float(x) for x in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for limit control data: '{response}'")

    def get_limit_control_points(self) -> int:
        """
        Queries the number of points currently in CONTrol:DATA.

        Corresponds to the SCPI query: CALCulate:LIMit:CONTrol:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:LIM:CONT:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for limit control points (not an integer): '{response}'")

    def set_limit_upper_data(self, data_points: list[float]):
        """
        Sets the UPPer axis data for the limit test.

        Corresponds to the SCPI command: CALCulate:LIMit:UPPer:DATA <NRf>{,<NRf>}

        :param data_points: A list of numeric values representing the upper limit data.
        """
        data_str = ",".join(map(str, data_points))
        self.instrument.write(f"CALC:LIM:UPP:DATA {data_str}")

    def get_limit_upper_data(self) -> list[float]:
        """
        Queries the UPPer axis data for the limit test.

        Corresponds to the SCPI query: CALCulate:LIMit:UPPer:DATA?

        :return: A list of numeric values representing the upper limit data.
        :raises ValueError: If the instrument returns non-numeric data or an unexpected format.
        """
        response = self.instrument.query("CALC:LIM:UPP:DATA?").strip()
        try:
            return [float(x) for x in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for limit upper data: '{response}'")

    def get_limit_upper_points(self) -> int:
        """
        Queries the number of points currently in UPPer:DATA.

        Corresponds to the SCPI query: CALCulate:LIMit:UPPer:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:LIM:UPP:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for limit upper points (not an integer): '{response}'")

    def set_limit_upper_state(self, enable: bool):
        """
        Sets or queries if the individual UPPer limit test is enabled.

        Corresponds to the SCPI command: CALCulate:LIMit:UPPer:STATE <boolean>
        At *RST, this is set to ON.

        :param enable: True to enable the upper limit test, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:LIM:UPP:STATE {scpi_value}")

    def get_limit_upper_state(self) -> bool:
        """
        Queries if the individual UPPer limit test is enabled.

        Corresponds to the SCPI query: CALCulate:LIMit:UPPer:STATE?

        :return: True if the upper limit test is enabled, False if not.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:LIM:UPP:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for limit upper state: '{response}'")

    def set_limit_lower_data(self, data_points: list[float]):
        """
        Sets the LOWer axis data for the limit test.

        Corresponds to the SCPI command: CALCulate:LIMit:LOWer:DATA <NRf>{,<NRf>}

        :param data_points: A list of numeric values representing the lower limit data.
        """
        data_str = ",".join(map(str, data_points))
        self.instrument.write(f"CALC:LIM:LOW:DATA {data_str}")

    def get_limit_lower_data(self) -> list[float]:
        """
        Queries the LOWer axis data for the limit test.

        Corresponds to the SCPI query: CALCulate:LIMit:LOWer:DATA?

        :return: A list of numeric values representing the lower limit data.
        :raises ValueError: If the instrument returns non-numeric data or an unexpected format.
        """
        response = self.instrument.query("CALC:LIM:LOW:DATA?").strip()
        try:
            return [float(x) for x in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for limit lower data: '{response}'")

    def get_limit_lower_points(self) -> int:
        """
        Queries the number of points currently in LOWer:DATA.

        Corresponds to the SCPI query: CALCulate:LIMit:LOWer:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:LIM:LOW:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for limit lower points (not an integer): '{response}'")

    def set_limit_lower_state(self, enable: bool):
        """
        Sets or queries if the individual LOWer limit test is enabled.

        Corresponds to the SCPI command: CALCulate:LIMit:LOWer:STATE <boolean>
        At *RST, this is set to ON.

        :param enable: True to enable the lower limit test, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:LIM:LOW:STATE {scpi_value}")

    def get_limit_lower_state(self) -> bool:
        """
        Queries if the individual LOWer limit test is enabled.

        Corresponds to the SCPI query: CALCulate:LIMit:LOWer:STATE?

        :return: True if the lower limit test is enabled, False if not.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:LIM:LOW:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for limit lower state: '{response}'")

    def get_limit_fail_status(self) -> int:
        """
        Queries if the LIMit test has failed or not.

        Corresponds to the SCPI query: CALCulate:LIMit:FAIL?

        :return: 0 if pass, 1 if fail.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:LIM:FAIL?").strip()
        try:
            status = int(response)
            if status in (0, 1):
                return status
            else:
                raise ValueError(f"Unexpected response for limit fail status (not 0 or 1): '{response}'")
        except ValueError:
            raise ValueError(f"Unexpected response for limit fail status (not integer): '{response}'")

    def get_limit_fail_count(self) -> int:
        """
        Queries the number of times that the LIMit test has failed.

        Corresponds to the SCPI query: CALCulate:LIMit:FCOunt?

        :return: The number of failures (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:LIM:FCOU?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for limit fail count (not an integer): '{response}'")


    def get_limit_report_data(self) -> list[float]:
        """
        Queries a number or list of numbers, each corresponding to a value of the
        CONTrol variable where either the UPPer or LOWer limit test has failed.
        Returns NAN if no failures.

        Corresponds to the SCPI query: CALCulate:LIMit:REPort:DATA?

        :return: A list of floats, or a list containing `float('nan')` if no failures.
        :raises ValueError: If the instrument returns unparseable data.
        """
        response = self.instrument.query("CALC:LIM:REPO:DATA?").strip()
        if response.upper() == "NAN":
            return [float('nan')]
        try:
            return [float(x) for x in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for limit report data: '{response}'")

    def get_limit_report_points(self) -> int:
        """
        Queries the number of points in the REPort:DATA. Returns 0 if there are no failures.

        Corresponds to the SCPI query: CALCulate:LIMit:REPort:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:LIM:REPO:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for limit report points (not an integer): '{response}'")

    def set_limit_clear_auto_state(self, auto_state: str):
        """
        Sets or queries if the limit information is to be cleared with each INITiate command.

        Corresponds to the SCPI command: CALCulate:LIMit:CLEar:AUTO <Boolean>|ONCE
        At *RST, AUTO shall be set to ON.

        :param auto_state: The auto clear setting. 'ON' or 'OFF' (Boolean), or 'ONCE'.
                           'ONCE' is not explicitly listed as a boolean for AUTO, but implied
                           by syntax. Standard SCPI typically uses 0/1 for boolean.
        :raises ValueError: If an invalid auto_state is provided.
        """
        normalized_state = auto_state.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto clear state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"CALC:LIM:CLE:AUTO {scpi_value}")

    def get_limit_clear_auto_state(self) -> str:
        """
        Queries if the limit information is to be cleared with each INITiate command.

        Corresponds to the SCPI query: CALCulate:LIMit:CLEar:AUTO?

        :return: The auto clear setting ('ON', 'OFF', or 'ONCE').
        """
        response = self.instrument.query("CALC:LIM:CLE:AUTO?").strip()
        # Instruments may return 0/1 or ON/OFF/ONCE. Normalize for consistent Python return.
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def clear_limit_immediate(self):
        """
        Causes the information in FAIL, FCOunt and REPort to be cleared IMMediately.

        Corresponds to the SCPI command: CALCulate:LIMit:CLEar:IMMediate
        """
        self.instrument.write(f"CALC:LIM:CLE:IMM")

    def set_limit_interpolate_state(self, enable: bool):
        """
        Sets or queries whether or not limit tests will be performed at points between
        those specified by the CONTrol variable.

        Corresponds to the SCPI command: CALCulate:LIMit:INTerpolate <boolean>
        At *RST, it shall be OFF.

        :param enable: True to enable interpolation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:LIM:INT {scpi_value}")

    def get_limit_interpolate_state(self) -> bool:
        """
        Queries whether or not limit tests will be performed at points between
        those specified by the CONTrol variable.

        Corresponds to the SCPI query: CALCulate:LIMit:INTerpolate?

        :return: True if interpolation is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:LIM:INT?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for limit interpolate state: '{response}'")


    def set_math_expression(self, expression: str):
        """
        Controls which expression is used by the CALCulate block for math operations.

        Corresponds to the SCPI command: CALCulate:MATH:EXPRession <numeric_expression>
        At *RST, this function is undefined.

        :param expression: The numeric expression string (e.g., "(IMPLied - MY-TRACE)").
        """
        # Note: Expressions might require quoting depending on content and SCPI rules
        # For simplicity, sending as-is. User should provide properly formatted expression.
        self.instrument.write(f"CALC:MATH:EXPR {expression}")

    def get_math_expression(self) -> str:
        """
        Queries the expression used by the CALCulate block for math operations.

        Corresponds to the SCPI query: CALCulate:MATH:EXPRession?

        :return: The numeric expression string.
        """
        response = self.instrument.query("CALC:MATH:EXPR?").strip()
        return response

    def get_math_expression_catalog(self) -> list[str]:
        """
        Lists all the defined expressions.

        Corresponds to the SCPI query: CALCulate:MATH:EXPRession:CATalog?

        :return: A list of strings, where each string is the name of an expression.
                 Returns an empty list if no expressions are currently defined.
        """
        response = self.instrument.query("CALC:MATH:EXPR:CAT?").strip()
        if not response:
            return []
        return [name.strip() for name in response.split(',')]

    def define_math_expression(self, expression: str):
        """
        Defines the expression used for the math operations.

        Corresponds to the SCPI command: CALCulate:MATH:EXPRession:DEFine <numeric_expression>
        """
        self.instrument.write(f"CALC:MATH:EXPR:DEF {expression}")

    def delete_math_expression_selected(self, expression_name: str):
        """
        Deletes the selected expression.

        Corresponds to the SCPI command: CALCulate:MATH:EXPRession:DELete:SELected <expression_name>

        :param expression_name: The name of the expression to delete.
        """
        self.instrument.write(f"CALC:MATH:EXPR:DEL:SEL {expression_name}")

    def delete_math_expression_all(self):
        """
        Deletes all defined expressions.

        Corresponds to the SCPI command: CALCulate:MATH:EXPRession:DELete:ALL
        """
        self.instrument.write(f"CALC:MATH:EXPR:DEL:ALL")

    def set_math_expression_name(self, expression_name: str):
        """
        Defines the name of the expression to be selected. If the expression name already
        exists, that existing expression shall be selected. If it does not exist, a new name
        shall be selected, but no expression shall be defined by this selection.

        Corresponds to the SCPI command: CALCulate:MATH:EXPRession:NAME <expression_name>
        At *RST the value of NAME is device dependent.

        :param expression_name: The name of the expression (character data).
        """
        # SCPI allows bare strings or quoted strings for character data.
        # For simplicity, sending as-is. User should provide properly formatted name.
        self.instrument.write(f"CALC:MATH:EXPR:NAME {expression_name}")

    def get_math_expression_name(self) -> str:
        """
        Queries the name of the currently selected expression.

        Corresponds to the SCPI query: CALCulate:MATH:EXPRession:NAME?

        :return: The name of the expression (string).
        """
        response = self.instrument.query("CALC:MATH:EXPR:NAME?").strip()
        return response.strip('"') # Remove potential quotes

    def set_math_state(self, enable: bool):
        """
        Determines whether math processing is done.

        Corresponds to the SCPI command: CALCulate:MATH:STATE <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable math processing, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:MATH:STATE {scpi_value}")

    def get_math_state(self) -> bool:
        """
        Queries whether math processing is done.

        Corresponds to the SCPI query: CALCulate:MATH:STATE?

        :return: True if math processing is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:MATH:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for math state: '{response}'")

    def set_smoothing_state(self, enable: bool):
        """
        Determines whether the smoothing algorithm is enabled.

        Corresponds to the SCPI command: CALCulate:SMOothing:STATE <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable smoothing, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:SMO:STATE {scpi_value}")

    def get_smoothing_state(self) -> bool:
        """
        Queries whether the smoothing algorithm is enabled.

        Corresponds to the SCPI query: CALCulate:SMOothing:STATE?

        :return: True if smoothing is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:SMO:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for smoothing state: '{response}'")

    def set_smoothing_aperture(self, aperture_ratio: float):
        """
        Specifies the size of the smoothing APERture as a ratio of smoothing aperture points/trace points.

        Corresponds to the SCPI command: CALCulate:SMOothing:APERture <NRf>
        At *RST, this function is device-dependent.

        :param aperture_ratio: The aperture ratio (float or int).
        """
        self.instrument.write(f"CALC:SMO:APER {aperture_ratio}")

    def get_smoothing_aperture(self) -> float:
        """
        Queries the size of the smoothing APERture.

        Corresponds to the SCPI query: CALCulate:SMOothing:APERture?

        :return: The aperture ratio (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:SMO:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for smoothing aperture (not numeric): '{response}'")

    def set_smoothing_points(self, points: int):
        """
        Controls the number of points to be included in the running average.
        POINts is coupled to APERture by the equation: POINts = APERture * TRACE: POINts

        Corresponds to the SCPI command: CALCulate:SMOothing:POINts <NR1>

        :param points: The number of points (integer).
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Smoothing points must be a non-negative integer.")
        self.instrument.write(f"CALC:SMO:POIN {points}")

    def get_smoothing_points(self) -> int:
        """
        Queries the number of points included in the running average.

        Corresponds to the SCPI query: CALCulate:SMOothing:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:SMO:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for smoothing points (not an integer): '{response}'")

    def set_calculate_state(self, enable: bool):
        """
        Controls whether postprocessing is enabled. If disabled, this subsystem is effectively transparent.

        Corresponds to the SCPI command: CALCulate:STATE <boolean>
        At *RST, this is set ON.

        :param enable: True to enable postprocessing, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:STATE {scpi_value}")

    def get_calculate_state(self) -> bool:
        """
        Queries whether postprocessing is enabled.

        Corresponds to the SCPI query: CALCulate:STATE?

        :return: True if postprocessing is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for calculate state: '{response}'")

    def set_transform_histogram_count(self, count: int):
        """
        Specifies the number of measurements to include in the histogram.

        Corresponds to the SCPI command: CALCulate:TRANsform:HISTogram:COUNT <NR1>
        At *RST this value is device dependent.

        :param count: The number of measurements (integer).
        :raises ValueError: If 'count' is not a non-negative integer.
        """
        if not isinstance(count, int) or count < 0:
            raise ValueError("Histogram count must be a non-negative integer.")
        self.instrument.write(f"CALC:TRAN:HIST:COUN {count}")

    def get_transform_histogram_count(self) -> int:
        """
        Queries the number of measurements included in the histogram.

        Corresponds to the SCPI query: CALCulate:TRANsform:HISTogram:COUNT?

        :return: The number of measurements (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:TRAN:HIST:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform histogram count (not an integer): '{response}'")

    def set_transform_histogram_ordinate(self, ordinate_type: str):
        """
        When ORDinate is set to RATio, the output of the HISTogram function is an absolute ratio.
        When ORDinate is set to PERCent, the output is PERCent (RATio*100).
        When ORDinate is set to COUNt, the output is the number of points in that amplitude belt.

        Corresponds to the SCPI command: CALCulate:TRANsform:HISTogram:ORDinate RATio|PERCent|PCT|COUNT
        At *RST this value is device dependent.

        :param ordinate_type: The ordinate type. Must be 'RATIO', 'PERCENT', 'PCT', or 'COUNT'.
                              Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid ordinate type is provided.
        """
        valid_types = {"RATIO", "PERCENT", "PCT", "COUNT"}
        ordinate_type_upper = ordinate_type.upper()
        if ordinate_type_upper not in valid_types:
            raise ValueError(f"Invalid ordinate type: '{ordinate_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:HIST:ORD {ordinate_type_upper}")

    def get_transform_histogram_ordinate(self) -> str:
        """
        Queries the ordinate type of the histogram function.

        Corresponds to the SCPI query: CALCulate:TRANsform:HISTogram:ORDinate?

        :return: The ordinate type ('RATIO', 'PERCENT', 'PCT', or 'COUNT').
        """
        response = self.instrument.query("CALC:TRAN:HIST:ORD?").strip()
        # Normalize to the longer, clearer forms if necessary
        if response.upper() == "PCT":
            return "PERCENT"
        return response.upper()

    def set_transform_histogram_points(self, points: int):
        """
        Specifies the number of POINts (amplitude belts) in the histogram.

        Corresponds to the SCPI command: CALCulate:TRANsform:HISTogram:POINts <NR1>
        At *RST this value is device dependent.

        :param points: The number of points/amplitude belts (integer).
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Histogram points must be a non-negative integer.")
        self.instrument.write(f"CALC:TRAN:HIST:POIN {points}")

    def get_transform_histogram_points(self) -> int:
        """
        Queries the number of POINts (amplitude belts) in the histogram.

        Corresponds to the SCPI query: CALCulate:TRANsform:HISTogram:POINts?

        :return: The number of points/amplitude belts (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:TRAN:HIST:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform histogram points (not an integer): '{response}'")


    def set_transform_histogram_range_auto_state(self, enable: bool):
        """
        Controls whether the number of output points for the histogram is determined
        automatically by the amplitude of the incoming data.

        Corresponds to the SCPI command: CALCulate:TRANsform:HISTogram:RANGe:AUTO <boolean>
        At *RST this function is set to a device dependent value.

        :param enable: True to enable auto-ranging, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:TRAN:HIST:RANG:AUTO {scpi_value}")

    def get_transform_histogram_range_auto_state(self) -> bool:
        """
        Queries whether the number of output points for the histogram is determined automatically.

        Corresponds to the SCPI query: CALCulate:TRANsform:HISTogram:RANGe:AUTO?

        :return: True if auto-ranging is ON, False if OFF.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:TRAN:HIST:RANG:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for transform histogram range auto state: '{response}'")

    def set_transform_histogram_state(self, enable: bool):
        """
        Determines whether the histogram transformation is enabled.

        Corresponds to the SCPI command: CALCulate:TRANsform:HISTogram:STATe <boolean>
        At *RST this function is OFF.

        :param enable: True to enable histogram transformation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:TRAN:HIST:STATE {scpi_value}")

    def get_transform_histogram_state(self) -> bool:
        """
        Queries whether the histogram transformation is enabled.

        Corresponds to the SCPI query: CALCulate:TRANsform:HISTogram:STATe?

        :return: True if histogram transformation is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:TRAN:HIST:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for transform histogram state: '{response}'")

    def set_transform_time_state(self, enable: bool):
        """
        Determines whether the time transform is enabled.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:STATE <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable time transformation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:TRAN:TIME:STATE {scpi_value}")

    def get_transform_time_state(self) -> bool:
        """
        Queries whether the time transform is enabled.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:STATE?

        :return: True if time transformation is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for transform time state: '{response}'")

    def set_transform_time_type(self, transform_type: str):
        """
        Selects a particular method to be used in band limiting information or the
        manner in which windows should be applied for time transformation.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:TYPE LPASs|BPASs
        At *RST, this value is device-dependent.

        :param transform_type: The type of transformation. Must be 'LPASS' or 'BPASS'.
                               Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid transform type is provided.
        """
        valid_types = {"LPASS", "BPASS"}
        transform_type_upper = transform_type.upper()
        if transform_type_upper not in valid_types:
            raise ValueError(f"Invalid transform type: '{transform_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:TIME:TYPE {transform_type_upper}")

    def get_transform_time_type(self) -> str:
        """
        Queries the method used in band limiting information or the manner in which
        windows should be applied for time transformation.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:TYPE?

        :return: The type of transformation ('LPASS' or 'BPASS').
        """
        response = self.instrument.query("CALC:TRAN:TIME:TYPE?").strip()
        if response.upper().startswith("LPA"):
            return "LPASS"
        elif response.upper().startswith("BPA"):
            return "BPASS"
        else:
            return response

    def set_transform_time_stimulus(self, stimulus_type: str):
        """
        Specifies the type of stimulus to be simulated in the time transform process.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:STIMulus STEP|IMPulse
        At *RST, this value is device-dependent.

        :param stimulus_type: The type of stimulus. Must be 'STEP' or 'IMPULSE'.
                              Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid stimulus type is provided.
        """
        valid_types = {"STEP", "IMPULSE"}
        stimulus_type_upper = stimulus_type.upper()
        if stimulus_type_upper not in valid_types:
            raise ValueError(f"Invalid stimulus type: '{stimulus_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:TIME:STIM {stimulus_type_upper}")

    def get_transform_time_stimulus(self) -> str:
        """
        Queries the type of stimulus simulated in the time transform process.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:STIMulus?

        :return: The type of stimulus ('STEP' or 'IMPULSE').
        """
        response = self.instrument.query("CALC:TRAN:TIME:STIM?").strip()
        if response.upper().startswith("STE"):
            return "STEP"
        elif response.upper().startswith("IMP"):
            return "IMPULSE"
        else:
            return response

    def set_transform_time_start(self, start_time: float):
        """
        Specifies the start time of the output data record for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:STARt <NRf>
        At *RST, STARt is set to MIN.

        :param start_time: The start time in seconds (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:STAR {start_time}")

    def get_transform_time_start(self) -> float:
        """
        Queries the start time of the output data record for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:STARt?

        :return: The start time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time start (not numeric): '{response}'")

    def set_transform_time_stop(self, stop_time: float):
        """
        Specifies the stop time of the output data record for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:STOP <NRf>
        At *RST, STOP is set to MIN.

        :param stop_time: The stop time in seconds (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:STOP {stop_time}")

    def get_transform_time_stop(self) -> float:
        """
        Queries the stop time of the output data record for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:STOP?

        :return: The stop time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time stop (not numeric): '{response}')")

    def set_transform_time_span(self, span_time: float):
        """
        Specifies the time span of the output data record for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:SPAN <NRf>
        At *RST, SPAN is set to MIN.

        :param span_time: The time span in seconds (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:SPAN {span_time}")

    def get_transform_time_span(self) -> float:
        """
        Queries the time span of the output data record for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:SPAN?

        :return: The time span in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time span (not numeric): '{response}')")

    def set_transform_time_center(self, center_time: float):
        """
        Specifies the center time of the output data record for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:CENTer <NRf>
        At *RST, CENTer is set to MIN.

        :param center_time: The center time in seconds (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:CENT {center_time}")

    def get_transform_time_center(self) -> float:
        """
        Queries the center time of the output data record for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:CENTer?

        :return: The center time in seconds (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time center (not numeric): '{response}')")

    def set_transform_time_points(self, points: int):
        """
        Specifies the number of points output by the transform subsystem for time domain.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:POINts <NR1>
        At *RST, this value is device-dependent.

        :param points: The number of points (integer).
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Transform time points must be a non-negative integer.")
        self.instrument.write(f"CALC:TRAN:TIME:POIN {points}")

    def get_transform_time_points(self) -> int:
        """
        Queries the number of points output by the transform subsystem for time domain.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time points (not an integer): '{response}')")

    def set_transform_time_points_auto(self, auto_mode: str):
        """
        Controls whether the number of points for time transform is determined
        automatically by the size of the incoming SENSe Data.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:POINts:AUTO <boolean>|ONCE
        At *RST, AUTO is ON.

        :param auto_mode: The auto mode setting. Must be 'ON', 'OFF', or 'ONCE'.
                           Note: SCPI typically uses 0/1 for boolean states.
        :raises ValueError: If an invalid auto mode is provided.
        """
        normalized_state = auto_mode.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"CALC:TRAN:TIME:POIN:AUTO {scpi_value}")

    def get_transform_time_points_auto(self) -> str:
        """
        Queries whether the number of points for time transform is automatically set.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:POINts:AUTO?

        :return: The auto mode setting ('ON', 'OFF', or 'ONCE').
        """
        response = self.instrument.query("CALC:TRAN:TIME:POIN:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_transform_time_window(self, window_type: str):
        """
        Specifies the type and parameter of data windowing (shaping) done prior
        to the time transformation.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:WINDow <window_type>
        Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential
        At *RST, this value is device-dependent.

        :param window_type: The type of window. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid window type is provided.
        """
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f"CALC:TRAN:TIME:WIND {window_type_upper}")

    def get_transform_time_window(self) -> str:
        """
        Queries the type of data windowing done prior to the time transformation.

        :return: The type of window (e.g., 'RECTANGULAR', 'FLATTOP').
        """
        response = self.instrument.query("CALC:TRAN:TIME:WIND?").strip()
        return response.upper()

    def set_transform_time_kbessel_parameter(self, parameter: float):
        """
        Sets the parametric window parameter for the Kaiser Bessel window for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:KBESsel <NRf>
        At *RST, this value is device-dependent.

        :param parameter: The parameter for the Kaiser Bessel window (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:KBES {parameter}")

    def get_transform_time_kbessel_parameter(self) -> float:
        """
        Queries the parametric window parameter for the Kaiser Bessel window for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:KBESsel?

        :return: The parameter for the Kaiser Bessel window (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")

    def set_transform_time_exponential_parameter(self, decay_time_constant: float):
        """
        Enters the exponential decay time constant which characterizes the EXPonential window
        for time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:EXPonential <NRf>
        At *RST, this value is device-dependent.

        :param decay_time_constant: The exponential decay time constant (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:EXP {decay_time_constant}")

    def get_transform_time_exponential_parameter(self) -> float:
        """
        Queries the exponential decay time constant which characterizes the EXPonential window
        for time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:EXPonential?

        :return: The exponential decay time constant (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")

    def set_transform_time_force(self, value: float):
        """
        Enters the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in time transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:TIME:FORCe <NRf>
        At *RST, this value is device-dependent.

        :param value: The time value parameter (float or int).
        """
        self.instrument.write(f"CALC:TRAN:TIME:FORC {value}")

    def get_transform_time_force(self):
        """
        Queries the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in time transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:TIME:FORCe?

        :return: The time value parameter (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:TIME:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform time force (not numeric): '{response}'")

    def set_transform_distance_state(self, enable: bool):
        """
        Determines whether the distance transform is enabled.

        :param enable: True to enable distance transformation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:TRAN:DIST:STATE {scpi_value}")

    def get_transform_distance_state(self) -> bool:
        """
        Queries whether the distance transform is enabled.

        :return: True if distance transformation is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for transform distance state: '{response}'")

    def set_transform_distance_type(self, transform_type: str):
        """
        Selects a particular method to be used in limiting information or the manner
        in which windows shall be applied for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:TYPE LPASs|BPASs
        At *RST, this value is device-dependent.

        :param transform_type: The type of transformation. Must be 'LPASS' or 'BPASS'.
                               Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid transform type is provided.
        """
        valid_types = {"LPASS", "BPASS"}
        transform_type_upper = transform_type.upper()
        if transform_type_upper not in valid_types:
            raise ValueError(f"Invalid transform type: '{transform_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:DIST:TYPE {transform_type_upper}")

    def get_transform_distance_type(self) -> str:
        """
        Queries the method used in limiting information or the manner in which
        windows shall be applied for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:TYPE?

        :return: The type of transformation ('LPASS' or 'BPASS').
        """
        response = self.instrument.query("CALC:TRAN:DIST:TYPE?").strip()
        if response.upper().startswith("LPA"):
            return "LPASS"
        elif response.upper().startswith("BPA"):
            return "BPASS"
        else:
            return response

    def set_transform_distance_stimulus(self, stimulus_type: str):
        """
        Specifies the type of stimulus to be simulated in the distance transform process.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:STIMulus STEP|IMPulse
        At *RST, this value is device-dependent.

        :param stimulus_type: The type of stimulus. Must be 'STEP' or 'IMPULSE'.
                              Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid stimulus type is provided.
        """
        valid_types = {"STEP", "IMPULSE"}
        stimulus_type_upper = stimulus_type.upper()
        if stimulus_type_upper not in valid_types:
            raise ValueError(f"Invalid stimulus type: '{stimulus_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:DIST:STIM {stimulus_type_upper}")

    def get_transform_distance_stimulus(self) -> str:
        """
        Queries the type of stimulus simulated in the distance transform process.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:STIMulus?

        :return: The type of stimulus ('STEP' or 'IMPULSE').
        """
        response = self.instrument.query("CALC:TRAN:DIST:STIM?").strip()
        if response.upper().startswith("STE"):
            return "STEP"
        elif response.upper().startswith("IMP"):
            return "IMPULSE"
        else:
            return response

    def set_transform_distance_start(self, start_distance: float):
        """
        Specifies the start distance of the output data record for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:STARt <NRf>
        At *RST, STARt is set to MIN.

        :param start_distance: The start distance in meters (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:STAR {start_distance}")

    def get_transform_distance_start(self) -> float:
        """
        Queries the start distance of the output data record for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:STARt?

        :return: The start distance in meters (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance start (not numeric): '{response}'")

    def set_transform_distance_stop(self, stop_distance: float):
        """
        Specifies the stop distance of the output data record for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:STOP <NRf>
        At *RST, STOP is set to MIN.

        :param stop_distance: The stop distance in meters (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:STOP {stop_distance}")

    def get_transform_distance_stop(self) -> float:
        """
        Queries the stop distance of the output data record for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:STOP?

        :return: The stop distance in meters (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance stop (not numeric): '{response}')")

    def set_transform_distance_span(self, span_distance: float):
        """
        Specifies the distance span of the output data record for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:SPAN <NRf>
        At *RST, SPAN is set to MIN.

        :param span_distance: The distance span in meters (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:SPAN {span_distance}")

    def get_transform_distance_span(self) -> float:
        """
        Queries the distance span of the output data record for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:SPAN?

        :return: The distance span in meters (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance span (not numeric): '{response}')")

    def set_transform_distance_center(self, center_distance: float):
        """
        Specifies the center distance of the output data record for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:CENTer <NRf>
        At *RST, CENTer is set to MIN.

        :param center_distance: The center distance in meters (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:CENT {center_distance}")

    def get_transform_distance_center(self) -> float:
        """
        Queries the center distance of the output data record for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:CENTer?

        :return: The center distance in meters (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance center (not numeric): '{response}')")

    def set_transform_distance_points(self, points: int):
        """
        Specifies the number of points output by the transform subsystem for distance domain.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:POINts <NR1>
        At *RST, this is set to a device-dependent value.

        :param points: The number of points (integer).
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Transform distance points must be a non-negative integer.")
        self.instrument.write(f"CALC:TRAN:DIST:POIN {points}")

    def get_transform_distance_points(self) -> int:
        """
        Queries the number of points output by the transform subsystem for distance domain.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance points (not an integer): '{response}')")

    def set_transform_distance_points_auto(self, auto_mode: str):
        """
        Controls whether the number of points for distance transform is determined
        automatically by the size of the incoming SENSe Data.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:POINts:AUTO <boolean>|ONCE
        At *RST, AUTO is ON.

        :param auto_mode: The auto mode setting. Must be 'ON', 'OFF', or 'ONCE'.
                           Note: SCPI typically uses 0/1 for boolean states.
        :raises ValueError: If an invalid auto mode is provided.
        """
        normalized_state = auto_mode.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"CALC:TRAN:DIST:POIN:AUTO {scpi_value}")

    def get_transform_distance_points_auto(self) -> str:
        """
        Queries whether the number of points for distance transform is automatically set.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:POINts:AUTO?

        :return: The auto mode setting ('ON', 'OFF', or 'ONCE').
        """
        response = self.instrument.query("CALC:TRAN:DIST:POIN:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_transform_distance_window(self, window_type: str):
        """
        Specifies the type and parameter of data windowing (shaping) done prior
        to the distance transformation.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:WINDow <window_type>
        Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential
        At *RST, this value is device-dependent.

        :param window_type: The type of window. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid window type is provided.
        """
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f"CALC:TRAN:DIST:WIND {window_type_upper}")

    def get_transform_distance_window(self) -> str:
        """
        Queries the type of data windowing done prior to the distance transformation.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:WINDow?

        :return: The type of window (e.g., 'RECTANGULAR', 'FLATTOP').
        """
        response = self.instrument.query("CALC:TRAN:DIST:WIND?").strip()
        return response.upper()

    def set_transform_distance_kbessel_parameter(self, parameter: float):
        """
        Sets the parametric window parameter for the Kaiser Bessel window for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:KBESsel <NRf>
        At *RST, this value is device-dependent.

        :param parameter: The parameter for the Kaiser Bessel window (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:KBES {parameter}")

    def get_transform_distance_kbessel_parameter(self) -> float:
        """
        Queries the parametric window parameter for the Kaiser Bessel window for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:KBESsel?

        :return: The parameter for the Kaiser Bessel window (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")

    def set_transform_distance_exponential_parameter(self, decay_time_constant: float):
        """
        Enters the exponential decay time constant which characterizes the EXPonential window
        for distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:EXPonential <NRf>
        At *RST, this value is device-dependent.

        :param decay_time_constant: The exponential decay time constant (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:EXP {decay_time_constant}")

    def get_transform_distance_exponential_parameter(self) -> float:
        """
        Queries the exponential decay time constant which characterizes the EXPonential window
        for distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:EXPonential?

        :return: The exponential decay time constant (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")

    def set_transform_distance_force(self, value: float):
        """
        Enters the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in distance transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:DISTance:FORCe <NRf>
        At *RST, this value is device-dependent.

        :param value: The time value parameter (float or int).
        """
        self.instrument.write(f"CALC:TRAN:DIST:FORC {value}")

    def get_transform_distance_force(self) -> float:
        """
        Queries the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in distance transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:DISTance:FORCe?

        :return: The time value parameter (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:DIST:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform distance force (not numeric): '{response}'")

    def set_transform_frequency_state(self, enable: bool):
        """
        Determines whether the frequency transform is enabled.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:STATe <boolean>
        At *RST, this function is OFF.

        :param enable: True to enable frequency transformation, False to disable.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"CALC:TRAN:FREQ:STATE {scpi_value}")

    def get_transform_frequency_state(self) -> bool:
        """
        Queries whether the frequency transform is enabled.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:STATe?

        :return: True if frequency transformation is enabled, False if disabled.
        :raises ValueError: If the instrument returns an unexpected response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for transform frequency state: '{response}'")

    def set_transform_frequency_type(self, transform_type: str):
        """
        Selects a particular method to be used in limiting information or the manner
        in which windows shall be applied for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:TYPE LPASs|BPASs
        At *RST, this value is device-dependent.

        :param transform_type: The type of transformation. Must be 'LPASS' or 'BPASS'.
                               Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid transform type is provided.
        """
        valid_types = {"LPASS", "BPASS"}
        transform_type_upper = transform_type.upper()
        if transform_type_upper not in valid_types:
            raise ValueError(f"Invalid transform type: '{transform_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:FREQ:TYPE {transform_type_upper}")

    def get_transform_frequency_type(self) -> str:
        """
        Queries the method used in limiting information or the manner in which
        windows shall be applied for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:TYPE?

        :return: The type of transformation ('LPASS' or 'BPASS').
        """
        response = self.instrument.query("CALC:TRAN:FREQ:TYPE?").strip()
        if response.upper().startswith("LPA"):
            return "LPASS"
        elif response.upper().startswith("BPA"):
            return "BPASS"
        else:
            return response

    def set_transform_frequency_stimulus(self, stimulus_type: str):
        """
        Specifies the type of stimulus to be simulated in the frequency transform process.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:STIMulus STEP|IMPulse
        At *RST, this selection is device-dependent.

        :param stimulus_type: The type of stimulus. Must be 'STEP' or 'IMPULSE'.
                              Case-insensitive input will be converted to SCPI format.
        :raises ValueError: If an invalid stimulus type is provided.
        """
        valid_types = {"STEP", "IMPULSE"}
        stimulus_type_upper = stimulus_type.upper()
        if stimulus_type_upper not in valid_types:
            raise ValueError(f"Invalid stimulus type: '{stimulus_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f"CALC:TRAN:FREQ:STIM {stimulus_type_upper}")

    def get_transform_frequency_stimulus(self) -> str:
        """
        Queries the type of stimulus simulated in the frequency transform process.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:STIMulus?

        :return: The type of stimulus ('STEP' or 'IMPULSE').
        """
        response = self.instrument.query("CALC:TRAN:FREQ:STIM?").strip()
        if response.upper().startswith("STE"):
            return "STEP"
        elif response.upper().startswith("IMP"):
            return "IMPULSE"
        else:
            return response

    def set_transform_frequency_start(self, start_freq: float):
        """
        Specifies the start frequency of the output data record for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:STARt <NRf>
        At *RST, STARt is set to MIN.

        :param start_freq: The start frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:STAR {start_freq}")

    def get_transform_frequency_start(self) -> float:
        """
        Queries the start frequency of the output data record for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:STARt?

        :return: The start frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency start (not numeric): '{response}'")

    def set_transform_frequency_stop(self, stop_freq: float):
        """
        Specifies the stop frequency of the output data record for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:STOP <NRf>
        At *RST, STOP is set to MIN.

        :param stop_freq: The stop frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:STOP {stop_freq}")

    def get_transform_frequency_stop(self) -> float:
        """
        Queries the stop frequency of the output data record for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:STOP?

        :return: The stop frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency stop (not numeric): '{response}')")

    def set_transform_frequency_span(self, span_freq: float):
        """
        Specifies the frequency span of the output data record for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:SPAN <NRf>
        At *RST, SPAN is set to MIN.

        :param span_freq: The frequency span in Hertz (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:SPAN {span_freq}")

    def get_transform_frequency_span(self) -> float:
        """
        Queries the frequency span of the output data record for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:SPAN?

        :return: The frequency span in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency span (not numeric): '{response}')")

    def set_transform_frequency_center(self, center_freq: float):
        """
        Specifies the center frequency of the output data record for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:CENTer <NRf>
        At *RST, CENTer is set to MIN.

        :param center_freq: The center frequency in Hertz (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:CENT {center_freq}")

    def get_transform_frequency_center(self) -> float:
        """
        Queries the center frequency of the output data record for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:CENTer?

        :return: The center frequency in Hertz (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency center (not numeric): '{response}')")

    def set_transform_frequency_points(self, points: int):
        """
        Specifies the number of points output by the transform subsystem for frequency domain.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:POINts <NR1>
        At *RST, this value is device-dependent.

        :param points: The number of points (integer).
        :raises ValueError: If 'points' is not a non-negative integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Transform frequency points must be a non-negative integer.")
        self.instrument.write(f"CALC:TRAN:FREQ:POIN {points}")

    def get_transform_frequency_points(self) -> int:
        """
        Queries the number of points output by the transform subsystem for frequency domain.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:POINts?

        :return: The number of points (integer).
        :raises ValueError: If the instrument returns a non-integer response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency points (not an integer): '{response}')")

    def set_transform_frequency_points_auto(self, auto_mode: str):
        """
        Controls whether the number of points for frequency transform is determined
        automatically by the size of the incoming SENSe Data.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:POINts:AUTO <boolean>|ONCE
        At *RST, AUTO is ON.

        :param auto_mode: The auto mode setting. Must be 'ON', 'OFF', or 'ONCE'.
                           Note: SCPI typically uses 0/1 for boolean states.
        :raises ValueError: If an invalid auto mode is provided.
        """
        normalized_state = auto_mode.upper()
        if normalized_state in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_state in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"CALC:TRAN:FREQ:POIN:AUTO {scpi_value}")

    def get_transform_frequency_points_auto(self) -> str:
        """
        Queries whether the number of points for frequency transform is automatically set.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:POINts:AUTO?

        :return: The auto mode setting ('ON', 'OFF', or 'ONCE').
        """
        response = self.instrument.query("CALC:TRAN:FREQ:POIN:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_transform_frequency_window(self, window_type: str):
        """
        Specifies the type and parameter of data windowing (shaping) done prior
        to the frequency transformation.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:WINDow <window_type>
        Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential
        At *RST, this value is device-dependent.

        :param window_type: The type of window. Case-insensitive input will be
                            converted to SCPI format.
        :raises ValueError: If an invalid window type is provided.
        """
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f"CALC:TRAN:FREQ:WIND {window_type_upper}")

    def get_transform_frequency_window(self) -> str:
        """
        Queries the type of data windowing done prior to the frequency transformation.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:WINDow?

        :return: The type of window (e.g., 'RECTANGULAR', 'FLATTOP').
        """
        response = self.instrument.query("CALC:TRAN:FREQ:WIND?").strip()
        return response.upper()

    def set_transform_frequency_kbessel_parameter(self, parameter: float):
        """
        Sets the parametric window parameter for the Kaiser Bessel window for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:KBESsel <NRf>
        At *RST, this value is device-dependent.

        :param parameter: The parameter for the Kaiser Bessel window (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:KBES {parameter}")

    def get_transform_frequency_kbessel_parameter(self) -> float:
        """
        Queries the parametric window parameter for the Kaiser Bessel window for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:KBESsel?

        :return: The parameter for the Kaiser Bessel window (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")

    def set_transform_frequency_exponential_parameter(self, decay_time_constant: float):
        """
        Enters the exponential decay time constant which characterizes the EXPonential window
        for frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:EXPonential <NRf>
        At *RST, this value is device-dependent.

        :param decay_time_constant: The exponential decay time constant (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:EXP {decay_time_constant}")

    def get_transform_frequency_exponential_parameter(self) -> float:
        """
        Queries the exponential decay time constant which characterizes the EXPonential window
        for frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:EXPonential?

        :return: The exponential decay time constant (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")

    def set_transform_frequency_force(self, value: float):
        """
        Enters the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in frequency transform.

        Corresponds to the SCPI command: CALCulate:TRANsform:FREQuency:FORCe <NRf>
        At *RST, this value is device-dependent.

        :param value: The time value parameter (float or int).
        """
        self.instrument.write(f"CALC:TRAN:FREQ:FORC {value}")

    def get_transform_frequency_force(self) -> float:
        """
        Queries the time value parameter corresponding to the width of the gated portion
        of the input time record for FORCe windows in frequency transform.

        Corresponds to the SCPI query: CALCulate:TRANsform:FREQuency:FORCe?

        :return: The time value parameter (float).
        :raises ValueError: If the instrument returns a non-numeric response.
        """
        response = self.instrument.query("CALC:TRAN:FREQ:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for transform frequency force (not numeric): '{response}'")


    def set_calculate_path(self, path_order: list[str]):
        """
        Defines the order in which CALCulate subsystems are to be performed.

        Corresponds to the SCPI command: CALCulate:PATH <subsystem_name>{,<subsystem_name>}
        At *RST, the PATH definition is set to a device-dependent setting.

        :param path_order: A list of strings, where each string is the name of a CALCulate
                           subsystem (e.g., "TRANsform", "FILTer", "MATH").
        """
        # Ensure the subsystem names are correctly capitalized/abbreviated per SCPI if necessary.
        # Here, we assume the user provides them in a form acceptable to the instrument.
        path_str = ",".join(path_order)
        self.instrument.write(f"CALC:PATH {path_str}")

    def get_calculate_path(self) -> list[str]:
        """
        Queries the order in which CALCulate subsystems are to be performed.

        Corresponds to the SCPI query: CALCulate:PATH?

        :return: A list of strings, where each string is the name of a CALCulate subsystem.
        """
        response = self.instrument.query("CALC:PATH?").strip()
        if not response:
            return []
        # Instruments may return full names or abbreviations. Returning as-is for now.
        return [sub.strip() for sub in response.split(',')]