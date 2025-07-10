class Calculate():
    def __init__(self):
        self.instrument = None
    
    def clear_average_data(self):
        """Clears the average data and resets the average counter to zero."""
        self.instrument.write(":CALC:AVER:CLE")

    def set_count_of_results_in_average(self, auto: bool, count: int, once: bool = False):
        """Specifies the number of measurements to combine.
        Parameters:
        auto: True to enable auto-counting, False for manual count.
        count: The number of measurements to average (used when auto is False).
        once: (Optional) If auto is True, sets auto mode to 'ONCE' if True, otherwise 'AUTO ON' (Boolean equivalent)."""
        if auto:
            if once:
                self.instrument.write(f":CALC:AVER:COUNT:AUTO ONCE")
            else:
                self.instrument.write(f":CALC:AVER:COUNT:AUTO 1") # SCPI '1' for ON
        else:
            self.instrument.write(f":CALC:AVER:COUNT {count}")

    def get_count_of_results_in_average(self):
        """Returns the current average count and auto-count setting.
        Returns: A tuple containing (current_count: int, auto_setting: str ('1', '0', or 'ONCE'))"""
        auto_response = self.instrument.query(f":CALC:AVER:COUNT:AUTO?").strip()
        count_response = self.instrument.query(f":CALC:AVER:COUNT?").strip()
        
        # Convert count to int, handle potential errors
        try:
            count = int(count_response)
        except ValueError:
            count = -1 # Indicate an error or unexpected response

        return count, auto_response

    def set_averaging(self, turn_on: bool):
        """Turns averaging ON or OFF.
        Parameters:
        turn_on: True to turn averaging ON, False to turn averaging OFF."""
        if turn_on:
            self.instrument.write(f":CALC:AVER:STATE 1")
        else:
            self.instrument.write(f":CALC:AVER:STATE 0")
    
    def is_averaging_on(self) -> bool:
        """Returns True if averaging is ON, False if OFF."""
        response = self.instrument.query(":CALC:AVER:STATE?").strip()
        if response == "1":
            return True
        elif response == "0":
            return False
        else:
            raise ValueError(f"Unexpected response for averaging state: '{response}'") # Retain error for robustness
            
    def make_average_weighted(self, update: str = "NORM"):
        """Set how to update average when new data points are added to it.
        Parameters:
        update: EXPonential|MOVing|NORMal|REPeat"""
        valid_update = ["EXPONENTIAL", "EXP", "MOVING", "MOV", "NORMAL", "NORM", "REPEAT", "REP"]
        update_upper = update.upper()
        if update_upper not in valid_update:
            # Re-raise as ValueError to align with other functions' error handling
            raise ValueError(f"Value '{update}' is not accepted. Please enter one of the following arguments for update: {valid_update}")
        
        # Use abbreviated form if a long form is provided
        if update_upper == "EXPONENTIAL": update_upper = "EXP"
        elif update_upper == "MOVING": update_upper = "MOV"
        elif update_upper == "NORMAL": update_upper = "NORM"
        elif update_upper == "REPEAT": update_upper = "REP"

        self.instrument.write(f"CALCulate:AVERage:TCONtrol {update_upper}")

    def get_how_average_weighted(self) -> str:
        """Returns how the average is updated when new data points are added to it."""
        return self.instrument.query("CALCulate:AVERage:TCONtrol?").strip().upper() # Ensure consistent return format
    
    def set_average_type(self, type: str):
        """Set type of averaging fomula used. For complete formula see SCPI-99 doc Sec 4.1.5.
        Parameters: 
        type: COMPlex | ENVelope | MAXimum | MINimum | RMS | SCALar"""
        valid_type = ["COMPLEX", "COMP", "ENVELOPE", "ENV", "MAXIMUM", "MAX", "MINIMUM", "MIN", "RMS", "SCALAR", "SCAL"]
        type_upper = type.upper()
        if type_upper not in valid_type:
            raise ValueError(f"Value '{type}' is not accepted. Please enter one of the following arguments: {valid_type}")

        # Use abbreviated form if a long form is provided
        if type_upper == "COMPLEX": type_upper = "COMP"
        elif type_upper == "ENVELOPE": type_upper = "ENV"
        elif type_upper == "MAXIMUM": type_upper = "MAX"
        elif type_upper == "MINIMUM": type_upper = "MIN"
        elif type_upper == "SCALAR": type_upper = "SCAL"

        self.instrument.write(f"CALCulate:AVERage:TYPE {type_upper}")
    
    def get_average_type(self) -> str:
        """Returns type of averaging fomula used. For complete formula see SCPI-99 doc Sec 4.1.5."""
        return self.instrument.query(f"CALCulate:AVERage:TYPE?").strip().upper() # Ensure consistent return format
    
    def get_limit_fail(self) -> int:
        """Returns 0 if no limit failure, 1 if a limit failure occurred."""
        response = self.instrument.query("CALCulate:CLIMits:FAIL?").strip()
        try:
            status = int(response)
            if status in (0, 1):
                return status
            else:
                raise ValueError(f"Unexpected response for limit fail status (not 0 or 1): '{response}'")
        except ValueError:
            raise ValueError(f"Unexpected response for limit fail status (not integer): '{response}'")

    def get_failed_limit_list(self) -> list[str]:
        """Returns list of limits that have failed. Empty list if there are none."""
        response = self.instrument.query("CALCulate:CLIMits:FLIMITS:DATA?").strip()
        if not response: # Handles case of "" or "None" if instrument returns it
            return []
        return [item.strip() for item in response.split(',')]

    def get_failed_limit_count(self) -> int:
        """Returns the number of limits that have failed."""
        response = self.instrument.query("CALCulate:CLIMits:FLIMITS:POINTS?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for failed limit count (not an integer): '{response}'")
    
    def get_calc_system_results(self):
        """Returns all data linked to the calculate system."""
        return self.instrument.query("CALCulate:DATA?")

    def get_calc_system_preamble_results(self):
        """Returns an overview of calculate system data."""
        return self.instrument.query("CALCulate:DATA:PREamble?")
    
    def set_derivative_state(self, enable: bool):
        """Sets whether the derivative function is enabled.
        Parameters:
        enable: True to enable the derivative function, False to disable it."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":CALC:DER:STATE {scpi_value}")

    def get_derivative_state(self) -> bool:
        """Returns True if the derivative function is enabled, False if disabled."""
        response = self.instrument.query(":CALC:DER:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for derivative state: '{response}'")

    def set_derivative_points(self, points: int):
        """Specifies the number of points provided to the differential algorithm.
        Parameters:
        points: The number of points (integer) for the algorithm. Must be a non-negative integer."""
        if not isinstance(points, int) or points < 0:
            raise ValueError("Derivative points must be a non-negative integer.")
        self.instrument.write(f":CALC:DER:POIN {points}")

    def get_derivative_points(self) -> int:
        """Returns the number of points provided to the differential algorithm."""
        response = self.instrument.query(":CALC:DER:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for derivative points (not an integer): '{response}'")

    def set_feed_source(self, feed_source: str):
        """Sets the data flow to be fed into the CALCulate block.
        Parameters:
        feed_source: A string representing the data source (e.g., 'TWIR01p13')."""
        self.instrument.write(f":CALC:FEED {feed_source}")

    def get_feed_source(self) -> str:
        """Returns the data flow currently fed into the CALCulate block."""
        response = self.instrument.query(":CALC:FEED?").strip()
        return response.strip('"')

    def set_filter_gate_time_state(self, enable: bool):
        """Sets whether the time filter is enabled.
        Parameters:
        enable: True to enable the time filter, False to disable it."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":CALC:FILT:GATE:TIME:STATE {scpi_value}")

    def get_filter_gate_time_state(self) -> bool:
        """Returns True if the time filter is enabled, False if disabled."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter gate time state: '{response}'")

    def set_filter_gate_time_type(self, filter_type: str):
        """Specifies what occurs to the data in the specific time region for the filter.
        Parameters:
        filter_type: The type of filter. Must be 'BPASS' or 'NOTCH'."""
        valid_types = {"BPASS", "NOTCH"}
        filter_type_upper = filter_type.upper()
        if filter_type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f":CALC:FILT:GATE:TIME:TYPE {filter_type_upper}")

    def get_filter_gate_time_type(self) -> str:
        """Returns the type of filter ('BPASS' or 'NOTCH')."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:TYPE?").strip()
        if response.upper().startswith("BPAS"):
            return "BPASS"
        elif response.upper().startswith("NOTC"):
            return "NOTCH"
        else:
            return response

    def set_filter_gate_time_start(self, start_time: float):
        """Specifies the start time of the filter in seconds.
        Parameters:
        start_time: The start time in seconds (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:STAR {start_time}")

    def get_filter_gate_time_start(self) -> float:
        """Returns the start time of the filter in seconds."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time start (not numeric): '{response}'")

    def set_filter_gate_time_stop(self, stop_time: float):
        """Specifies the stop time of the filter in seconds.
        Parameters:
        stop_time: The stop time in seconds (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:STOP {stop_time}")

    def get_filter_gate_time_stop(self) -> float:
        """Returns the stop time of the filter in seconds."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time stop (not numeric): '{response}'")

    def set_filter_gate_time_span(self, span_time: float):
        """Specifies the time span of the filter in seconds.
        Parameters:
        span_time: The time span in seconds (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:SPAN {span_time}")

    def get_filter_gate_time_span(self) -> float:
        """Returns the time span of the filter in seconds."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time span (not numeric): '{response}'")

    def set_filter_gate_time_center(self, center_time: float):
        """Specifies the center time of the filter in seconds.
        Parameters:
        center_time: The center time in seconds (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:CENT {center_time}")

    def get_filter_gate_time_center(self) -> float:
        """Returns the center time of the filter in seconds."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time center (not numeric): '{response}'")

    def set_filter_gate_time_points(self, points: int):
        """Specifies the number of points output by the filter subsystem.
        Parameters:
        points: The number of points (integer) to be output."""
        if not isinstance(points, int) or points < 0:
            raise ValueError("Filter gate time points must be a non-negative integer.")
        self.instrument.write(f":CALC:FILT:GATE:TIME:POIN {points}")

    def get_filter_gate_time_points(self) -> int:
        """Returns the number of points output by the filter subsystem."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate time points (not an integer): '{response}'")

    def set_filter_gate_time_points_auto(self, auto_mode: str):
        """Controls whether the filter output points are automatically set.
        Parameters:
        auto_mode: The auto mode setting. Must be 'AUTO' or 'ONCE'."""
        valid_modes = {"AUTO", "ONCE"}
        auto_mode_upper = auto_mode.upper()
        if auto_mode_upper not in valid_modes:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be one of {list(valid_modes)}")
        self.instrument.write(f":CALC:FILT:GATE:TIME:POIN:AUTO {auto_mode_upper}")

    def get_filter_gate_time_points_auto(self) -> str:
        """Returns whether the filter output points are automatically set ('AUTO' or 'ONCE')."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:POIN:AUTO?").strip()
        if response == "1" or response.upper() == "AUTO":
            return "AUTO"
        elif response == "0" or response.upper() == "ONCE":
            return "ONCE"
        else:
            return response

    def set_filter_gate_time_window(self, window_type: str):
        """Specifies the type of data windowing (shaping) done prior to the filter.
        Parameters:
        window_type: The type of window. Valid types: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential."""
        valid_windows = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING",
            "HANNING", "KBESSEL", "FORCE", "EXPONENTIAL"
        }
        window_type_upper = window_type.upper()
        if window_type_upper not in valid_windows:
            raise ValueError(
                f"Invalid window type: '{window_type}'. Must be one of {list(valid_windows)}"
            )
        self.instrument.write(f":CALC:FILT:GATE:TIME:WIND {window_type_upper}")

    def get_filter_gate_time_window(self) -> str:
        """Returns the type of data windowing done prior to the filter."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:WIND?").strip()
        return response.upper()

    def set_filter_gate_time_kbessel_parameter(self, parameter: float):
        """Sets the parametric window parameter for the Kaiser Bessel window.
        Parameters:
        parameter: The parameter for the Kaiser Bessel window (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:KBES {parameter}")

    def get_filter_gate_time_kbessel_parameter(self) -> float:
        """Returns the parametric window parameter for the Kaiser Bessel window."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Kaiser Bessel parameter (not numeric): '{response}'")
            
    def set_filter_gate_time_exponential_parameter(self, decay_time_constant: float):
        """Enters the exponential decay time constant which characterizes the EXPonential window.
        Parameters:
        decay_time_constant: The exponential decay time constant (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:TIME:EXP {decay_time_constant}")

    def get_filter_gate_time_exponential_parameter(self) -> float:
        """Returns the exponential decay time constant which characterizes the EXPonential window."""
        response = self.instrument.query(":CALC:FILT:GATE:TIME:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for exponential decay time constant (not numeric): '{response}'")

    def set_filter_gate_frequency_state(self, enable: bool):
        """Sets whether the frequency filter is enabled.
        Parameters:
        enable: True to enable the frequency filter, False to disable it."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":CALC:FILT:GATE:FREQ:STATE {scpi_value}")

    def get_filter_gate_frequency_state(self) -> bool:
        """Returns True if the frequency filter is enabled, False if disabled."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter gate frequency state: '{response}'")

    def set_filter_gate_frequency_type(self, filter_type: str):
        """Specifies what occurs to the data in the specific frequency region.
        Parameters:
        filter_type: The type of filter. Must be 'BPASS' or 'NOTCH'."""
        valid_types = {"BPASS", "NOTCH"}
        filter_type_upper = filter_type.upper()
        if filter_type_upper not in valid_types:
            raise ValueError(f"Invalid filter type: '{filter_type}'. Must be one of {list(valid_types)}")
        self.instrument.write(f":CALC:FILT:GATE:FREQ:TYPE {filter_type_upper}")

    def get_filter_gate_frequency_type(self) -> str:
        """Returns the type of filter ('BPASS' or 'NOTCH')."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:TYPE?").strip()
        if response.upper().startswith("BPAS"):
            return "BPASS"
        elif response.upper().startswith("NOTC"):
            return "NOTCH"
        else:
            return response

    def set_filter_gate_frequency_start(self, start_freq: float):
        """Specifies the start frequency of the filter in Hertz.
        Parameters:
        start_freq: The start frequency in Hertz (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:FREQ:STAR {start_freq}")

    def get_filter_gate_frequency_start(self) -> float:
        """Returns the start frequency of the filter in Hertz."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency start (not numeric): '{response}'")

    def set_filter_gate_frequency_stop(self, stop_freq: float):
        """Specifies the stop frequency of the filter in Hertz.
        Parameters:
        stop_freq: The stop frequency in Hertz (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:FREQ:STOP {stop_freq}")

    def get_filter_gate_frequency_stop(self) -> float:
        """Returns the stop frequency of the filter in Hertz."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency stop (not numeric): '{response}'")

    def set_filter_gate_frequency_span(self, span_freq: float):
        """Specifies the frequency span of the filter in Hertz.
        Parameters:
        span_freq: The frequency span in Hertz (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:FREQ:SPAN {span_freq}")

    def get_filter_gate_frequency_span(self) -> float:
        """Returns the frequency span of the filter in Hertz."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency span (not numeric): '{response}'")

    def set_filter_gate_frequency_center(self, center_freq: float):
        """Specifies the center frequency of the filter in Hertz.
        Parameters:
        center_freq: The center frequency in Hertz (float or int)."""
        self.instrument.write(f":CALC:FILT:GATE:FREQ:CENT {center_freq}")

    def get_filter_gate_frequency_center(self) -> float:
        """Returns the center frequency of the filter in Hertz."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency center (not numeric): '{response}'")

    def set_filter_gate_frequency_points(self, points: int):
        """Specifies the number of points output by the filter subsystem for frequency domain.
        Parameters:
        points: The number of points (integer) to be output."""
        if not isinstance(points, int) or points < 0:
            raise ValueError("Filter gate frequency points must be a non-negative integer.")
        self.instrument.write(f":CALC:FILT:GATE:FREQ:POIN {points}")

    def get_filter_gate_frequency_points(self) -> int:
        """Returns the number of points output by the filter subsystem for frequency domain."""
        response = self.instrument.query(":CALC:FILT:GATE:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter gate frequency points (not an integer): '{response}'")