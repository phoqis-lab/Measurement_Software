import instrument
import time

class SpectrumAnalyzer(instrument.Instrument):
    def __init__(self, device):
       #TODO Add in 
       self.instrument = device
       self.valid_booleans = ['ON', 'OFF', 1, 0]

    #Helper Functions
    def _validate_line_num(self, line_num):
        """Helper to validate if line_num is within the allowed range (1-6)."""
        if not 1 <= line_num <= 6:
            raise ValueError("Limit line number must be an integer between 1 and 6.")
    def _validate_pathloss_table_num(self, table_num):
        """Helper to validate if path loss table number is within the allowed range (1-8)."""
        if not 1 <= table_num <= 8:
            raise ValueError("Path loss table number must be an integer between 1 and 8.")
    #Display
    '''SPIKE pplication display controls.'''
    def is_spike_hidden(self):
        #TODO: Test that :DATA unneeded
        """ Queries if the spike application is hidden."""
        comm = ":DISP:HIDE?"
        response = self.instrument.query(comm)
        if response in ['ON', 1]:
            return True
        elif response in ['OFF', 0]:
            return False
        else:
            print("Invalid response received: " + response)
            return None

    def hide_spike(self, to_hide):
        """When set to true, hides the Spike application. The application will 
        be hidden in the taskbar but will continue to be visible in the task manager.
        The SCPI lockout dialog, device connecting progress dialog, no device 
        connected alert dialog and multiple devices connected alert dialog will be 
        hidden, overriding related settings in the preferences menu."""
    
        
        if to_hide in self.valid_booleans:
            comm = ":DISP:HIDE " + str(to_hide).upper()
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(self.valid_booleans))
    
    def get_measurement_title(self):
        """ Get the measurement title."""
        comm = ":DISP:ANN:TITLE?"
        return self.instrument.query(comm)
    
    def set_measurement_title(self, title):
        """ Set the measurement title."""
        if isinstance(title, str):
            comm = ":DISP:ANN:TITLE " + title
            self.instrument.write(comm)
        else:
            print("Invalid type. Title must be a string.")
    
    def clear_measurement_title(self):
        """ Clear the measurement title."""
        comm = ":DISP:ANN:CLEar"
        self.instrument.write(comm)

    #Format Trace Controls
    def get_trace_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the trace data is returned in."""
        comm = ":FORM:TRAC?"
        return self.instrument.query(comm)

    def set_trace_format(self, format):
        """Set the format the trace data is returned in.
        form: 'ASCii', 'REAL'"""
    
        allowed_type_values = ['ASCII', 'REAL','ASC']
        if format.upper() in allowed_type_values:
            comm = ":FORM:TRAC " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    def get_iq_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the iq data is returned in."""
        comm = ":FORM:IQ?"
        return self.instrument.query(comm)

    def set_iq_format(self, format):
        """Set the format the iq data is returned in.
        form: 'ASCii', 'BINary'"""
    
        allowed_type_values = ['ASCII', 'BINARY','BIN','ASC']
        if format.upper() in allowed_type_values:
            comm = ":FORM:IQ " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    #System Controls
    """The following commands are used to 
    perform system level software actions and query information about the system."""
    def close_system(self):
        """
        Disconnects any active device and closes the Spike software.
        There is no way to reopen the software using SCPI commands.
        This will also terminate the socket connection with the Spike software.
        """
        comm = ":SYST:CLOS"
        self.instrument.write(comm)
        print("System close command sent. Socket connection terminated.")

    def preset_system(self):
        """
        Presets the active device. This will power cycled the active device and
        return the software to the initial power on state. This process can take
        between 6-20 seconds depending on the device type.
        """
        comm = ":SYST:PRES"
        self.instrument.write(comm)

    def is_preset_successful(self):
        """
        Queries the preset status of the active device. This will close and reopen
        the active device. This process can take between 6-20 seconds depending
        on the device type. R
        """
        comm = ":SYST:PRES?"
        response = self.instrument.query(comm)
        try:
            status = int(response)
            if status == 1:
                print("System preset successful.")
            else:
                print("System preset failed or in progress.")
            return (1==status)
        except ValueError:
            print(f"Invalid response for preset status: {response}")
            return None

    def save_image(self, filename):
        """
        Saves a screenshot with the given file name. The file will be in .ini format.
        params: filename (str): The name of the file to save the image as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:IMAG:SAVE {filename}"
        self.instrument.write(comm)

    def save_image_quick(self):
        """
        Saves a quick image. Same functionality as the Image quick save file menu option.
        """
        comm = ":SYST:IMAG:SAVE:QUICK"
        self.instrument.write(comm)

    def load_user_preset(self, filename):
        """
        Loads the preset given by the file name. If the preset does not exist,
        nothing occurs.
        params: filename (str): The name of the preset file to load. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:PRES:USER:LOAD {filename}"
        self.instrument.write(comm)

    def save_user_preset(self, filename):
        """
        Saves the user preset with the given file name. The file name should have
        extension ".ini".
        params: filename (str): The name of the file to save the user preset as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:PRES:USER:SAVE {filename}"
        self.instrument.write(comm)

    def communicate_gtlocal(self):
        """
        Puts Spike in local mode.
        """
        comm = ":SYST:COMM:GTL"
        self.instrument.write(comm)

    def print_system(self):
        """
        Prints the default system print settings.
        """
        comm = ":SYST:PRIN"
        self.instrument.write(comm)

    def get_temperature(self):
        """
        Returns the current internal temperature of the active device, in degrees Clsius.
        """
        comm = ":SYST:TEMP?"
        temperature = self.instrument.query(comm)
        try:
            temp_float = float(temperature)
          
            return temp_float
        except ValueError:
            print(f"Invalid response for temperature: {temperature}")
            return None

    def get_voltage(self):
        """
        Returns the measured voltage of the active device, in volts.
        """
        comm = ":SYST:VOLT?"
        voltage = self.instrument.query(comm)
        try:
            volt_float = float(voltage)
            
            return volt_float
        except ValueError:
            print(f"Invalid response for voltage: {voltage}")
            return None

    def get_current(self):
        """
        Returns the measured current of the active device, in amps.
        (BB and SM series devices only. SA series devices return 0.)
        """
        comm = ":SYST:CURR?"
        current = self.instrument.query(comm)
        try:
            current_float = float(current)
         
            return current_float
        except ValueError:
            print(f"Invalid response for current: {current}")
            return None
    

    #Device Management Controls
    """The functions below allow you to remotely manage the active device 
    in the Spike software. This is useful for error recovery in the event a 
    device disconnect occurs due, or if one is managing multiple Signal Hound devices on one PC."""
    
    def get_device_active_status(self):
        """
        Returns whether or not a device is currently connected and active in the software.
        Look at the *IDN? function to request information about the device.
        """
        comm = ":SYST:DEV:ACT?"
        response = self.instrument.query(comm)
        try:
            status = int(response)
            if status == 1:
                print("Device is active.")
                return True
            else:
                print("No device is active.")
                return False
        except ValueError:
            print(f"Invalid response for device active status: {response}")
            return None

    def get_device_count(self):
        """
        Returns the number of devices connected to the PC. No device may be
        active when this function is called. IE, you must call DISConnect? before calling
        this function. Any networked device that have been configured will be counted
        in the returned value.
        """
        comm = ":SYST:DEV:COUN?"
        response = self.instrument.query(comm)
        try:
            count = int(response)
            print(f"Number of connected devices: {count}")
            return count
        except ValueError:
            print(f"Invalid response for device count: {response}")
            return None

    def get_device_list(self):
        """
        Returns the connection strings for all devices available to connect in the
        Spike software. For USB devices, this is serial numbers returned as ascii integers
        and comma separated. If any networked devices have been configured they will be
        returned in the list with the following form: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        This entire string can be sent to the connect function to connect to a networked device.
        """
        comm = ":SYST:DEV:LIST?"
        response = self.instrument.query(comm)
        device_list = [d.strip() for d in response.split(',')]
        print(f"Available devices: {device_list}")
        return device_list

    def get_current_device_connection_string(self):
        """
        Returns the currently active device's connection string. See LIST? for format.
        """
        comm = ":SYST:DEV:CURR?"
        response = self.instrument.query(comm)
        print(f"Current active device connection string: {response}")
        return response

    def connect_device(self, connection_string):
        """
        Connects a device in the Spike software. For USB devices, you need to
        provide the serial number of the device to connect. For networked devices,
        send a string with form: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        Returns 0 or 1 depending on if the device successfully opened.
        params: connection_string (str): The connection string of the device to connect.
                                         For USB, this is the serial number. For networked,
                                         it's in the format SOCKET::IP::PORT.
        """
        comm = f":SYST:DEV:CON {connection_string}"
        self.instrument.write(comm)
        # The documentation states it returns 0 or 1, but this is a 'write' command,
        # so we'd typically query a status afterward if available.
        # For now, we'll just print a message indicating the command was sent.

    def disconnect_device(self):
        """
        Disconnects any device actively connected in Spike.
        """
        comm = ":SYST:DEV:DISC"
        response = self.instrument.query(comm) # This command is a query that returns 1
        try:
            status = int(response)
            if status == 1:
                print("Device disconnected successfully.")
                return True
            else:
                print("Device disconnection failed.")
                return False
        except ValueError:
            print(f"Invalid response for disconnect status: {response}")
            return None
    
    #Error Controls
    '''These commands control the measurement mode of the Spike software.'''
        #COUNT already implemented
        #NEXT already implemented
    def clear_all_errors(self):
        """
        Remove all errors from the queue, returns nothing.
        """
        comm = ":SYST:ERR:CLE"
        self.instrument.write(comm)
        print("All errors cleared from the error queue.")
    
    #Measurement Mode Controls
    def set_mode(self, mode):
        """
        Determines the current measurement mode.
        params: mode (str): The desired measurement mode. Allowed values are:
                      'SA', 'RTSA', 'ZS', 'HARMonics', 'NA', 'PNoise', 'DDEMod',
                      'EMI', 'ADEMod', 'IH', 'SEMask', 'NFIGure', 'WLAN', 'BLE', 'LTE'.
        """
        if mode.upper() in self.allowed_modes:
            comm = f":INST:SEL {mode.upper()}"
            self.instrument.write(comm)
            
        else:
            print(f"Invalid mode: '{mode}'. Allowed modes are: {', '.join(self.allowed_modes)}")

    def get_mode(self):
        """
        Queries the current measurement mode.
        """
        comm = ":INST:SEL?"
        current_mode = self.instrument.query(comm)
    
        return current_mode

    def recalibrate_device(self):
        """
        Performs a device recalibration.
        """
        comm = ":INST:REC"
        self.instrument.write(comm)
       
        # Recalibration might take time, consider adding a delay or status check if available
    #Initiate Commands
    """The commands are used to control when 
    measurements are performed in the application.
    For automated measurements, it is common/recommended 
    to disable CONTinuous measurement and control when 
    the software performs the next measurement 
    (sweep/IQ acquisition/etc) with the INIT:IMM command."""
    def enable_continous_measurement(self, enable):
        """
        Enables or disables continuous measurement operation.
        params: enable (bool): True to enable continuous measurement, False to disable.
        """
        comm = ":INIT:CONT " + ('ON' if enable else 'OFF')
        self.instrument.write(comm)
    
    def is_continuous_measurement_enabled(self):
        """
        Queries the current status of continuous measurement operation.
        Returns '1' if ON, '0' if OFF.
        """
        comm = ":INIT:CONT?"
        status = self.instrument.query(comm)
        return (1 == status)

    def trigger_immediate_measurement(self):
        """
        Triggers a measurement. Has no effect if CONTINUOUS is enabled.
        """
        comm = ":INITiate:IMMediate"
        self.instrument.write(comm)
        # If continuous is enabled, this command has no effect as per documentation.
        # You might want to check get_continuous_measurement_status() before call

    #Limit Lines
    """These commands control the limit lines which are available in sweep, 
    real-time, and network analysis measurement modes. """
    def enable_limit_line_testing(self, line_num, enable):
        """
        Enables or disables limit line testing.
        params: line_num (int): The limit line number to enable/disable (1-6).
                enable (bool): True to enable limit line testing, False to disable.
        """
        comm = ":CALC:LLINE"+str(line_num)+":STAT" + ('ON' if enable else 'OFF')
        self.instrument.write(comm)

    def is_limit_line_testing_enabled(self, line_num):
        """
        Queries if limit line testing is enabled for a specific limit line.
        params: line_num (int): The limit line number to check (1-6).
        Returns '1' if enabled, '0' if disabled.
        """
        comm = ":CALC:LLINE"+str(line_num)+":STAT?"
        status = self.instrument.query(comm)
        return (status==1)
        
    
    def set_limit_line_state(self, line_num, state):
        """
        Enables or disables limit line testing. If there are not at least 2 points
        in the limit line, testing doesn't occur despite being enabled.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")


    def set_limit_line_title(self, line_num, title):
        """
        Specifies the name of the limit line.
        params: line_num (int): The limit line number (1-6).
                title (str): The name of the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TITL '{title}'" # SCPI strings often need quotes
        self.instrument.write(comm)

    def get_limit_line_title(self, line_num):
        """
        Queries the name of the limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The name of the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TITL?"
        title = self.instrument.query(comm)
        return title

    def set_limit_line_trace(self, line_num, trace_number):
        """
        Specifies which trace is tested against this limit line.
        params: line_num (int): The limit line number (1-6).
                trace_number (int): The trace number to test against.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TRAC {trace_number}"
        self.instrument.write(comm)

    def get_limit_lines_trace(self, line_num):
        """
        Queries which trace is tested against this limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The trace number.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TRAC?"
        trace = self.instrument.query(comm)
        return trace

    def set_limit_line_type(self, line_num, line_type):
        """
        Specifies whether the limit line is an upper or lower bound.
        params: line_num (int): The limit line number (1-6).
                line_type (str): 'UPPer' for upper bound, 'LOWer' for lower bound.
        """
        self._validate_line_num(line_num)
        line_type_upper = line_type.upper()
        if line_type_upper in ['UPPER', 'LOWER']:
            comm = f":CALC:LLINE{line_num}:TYPE {line_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid limit line type: '{line_type}'. Allowed values are 'UPPer' or 'LOWer'.")

    def get_limit_line_type(self, line_num):
        """
        Queries whether the limit line is an upper or lower bound.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'UPPer' or 'LOWer'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TYPE?"
        line_type = self.instrument.query(comm)
        return line_type

    def set_limit_line_reference(self, line_num, reference_type):
        """
        Specifies whether the limit line values are fixed/absolute or relative
        to the center frequency and ref level.
        params: line_num (int): The limit line number (1-6).
                reference_type (str): 'FIXed' for fixed/absolute, 'RELative' for relative.
        """
        self._validate_line_num(line_num)
        reference_type_upper = reference_type.upper()
        if reference_type_upper in ['FIXED', 'RELATIVE']:
            comm = f":CALC:LLINE{line_num}:REFerence {reference_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid reference type: '{reference_type}'. Allowed values are 'FIXed' or 'RELative'.")

    def get_limit_line_reference(self, line_num):
        """
        Queries whether the limit line values are fixed/absolute or relative.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'FIXed' or 'RELative'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:REFerence?"
        reference = self.instrument.query(comm)
        return reference

    def transform_limit_line_reference(self, line_num):
        """
        Builds limit line points from trace, max holding across frequency sections.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:REFerence:TRANsform"
        self.instrument.write(comm)

    def set_limit_line_interpolation(self, line_num, interpolation_type):
        """
        Specifies whether the limit line uses linear or logarithmic interpolation.
        params: line_num (int): The limit line number (1-6).
                interpolation_type (str): 'LINear' for linear, 'LOGarithmic' for logarithmic.
        """
        self._validate_line_num(line_num)
        interpolation_type_upper = interpolation_type.upper()
        if interpolation_type_upper in ['LINEAR', 'LOGARITHMIC']:
            comm = f":CALC:LLINE{line_num}:INTerpolate {interpolation_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid interpolation type: '{interpolation_type}'. Allowed values are 'LINear' or 'LOGarithmic'.")

    def get_limit_line_interpolation(self, line_num):
        """
        Queries whether the limit line uses linear or logarithmic interpolation.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'LINear' or 'LOGarithmic'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:INTerpolate?"
        interpolation = self.instrument.query(comm)
        return interpolation

    def set_limit_line_pause_state(self, line_num, state):
        """
        When enabled, a failure of this limit will pause the sweep update.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:PAUSE:STATe {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def get_limit_line_pause_state(self, line_num):
        """
        Queries if a failure of this limit will pause the sweep update.
        params: line_num (int): The limit line number (1-6).
        Returns: True is enabled, False if disabled.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:PAUSE:STATe?"
        status = self.instrument.query(comm)
        return (1==status)

    def set_limit_line_display_visibility(self, line_num, state):
        """
        When enabled, the limit line will be visible on the graticule.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:DISP:STATe {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def is_limit_line_display_visible(self, line_num):
        """
        Queries if the limit line is visible on the graticule.
        params: line_num (int): The limit line number (1-6).
        Returns: str: '1' if visible, '0' if hidden.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DISP:STATe?"
        status = self.instrument.query(comm)
        return (1==status)

    def change_limit_line_result_visibility(self, line_num, state):
        """
        When enabled, the limit line pass/fail result will be visible on the graticule.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:DISP:RES:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def is_limit_line_result_visible(self, line_num):
        """
        Queries if the limit line pass/fail result is visible on the graticule.
        params: line_num (int): The limit line number (1-6).
        Returns: str: '1' if visible, '0' if hidden.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DISP:RES:STAT?"
        status = self.instrument.query(comm)
        return (status == 1)

    def set_limit_line_offset_y(self, line_num, offset_value):
        """
        Specifies a dB offset to the limit line.
        params: line_num (int): The limit line number (1-6).
                offset_value (float): The offset value in dB.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:OFFSet:Y {offset_value}"
        self.instrument.write(comm)

    def get_limit_line_offset_y(self, line_num):
        """
        Queries the dB offset of the limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The offset value in dB.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:OFFSet:Y?"
        offset = self.instrument.query(comm)
        return offset

    def build_limit_line(self, line_num):
        """
        Builds limit line points from trace, max holding across frequency sections.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:BUILD"
        self.instrument.write(comm)

    def get_limit_line_build_points(self, line_num):
        """
        Returns the number of points in the limit line as an integer.
        params: line_num (int): The limit line number (1-6).
        Returns: int: The number of points in the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:BUILD:POIN?"
        points = self.instrument.query(comm)
        try:
            num_points = int(points)
            return num_points
        except ValueError:
            print(f"Invalid response for limit line build points: {points}")
            return None

    def save_limit_line_points(self, line_num):
        """
        Specifies the points in the limit line will overwrite any existing points.
        Points are specified as freq/amplitude pairs where the amplitude is specified as dBm.
        This command saves the currently defined points.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:SAVE"
        self.instrument.write(comm)

    def get_limit_line_data(self, line_num):
        """
        Returns the points in the limit line. Points are returned as freq/amplitude pairs
        where the frequencies are specified as Hz and the amplitudes as dBm.
        params: line_num (int): The limit line number (1-6).
        Returns: str: A string of comma-separated frequency and amplitude pairs (e.g., "freq1,amp1,freq2,amp2,...").
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DATA?"
        data = self.instrument.query(comm)
        return data

    def get_limit_line_test_status(self, line_num):
        """
        Returns 1 when the limit test has failed, 0 if passed.
        params: line_num (int): The limit line number (1-6).
        Returns: True if passed.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:FAIL?"
        status = self.instrument.query(comm)
        return (status == 0)

    def clear_all_limit_lines(self):
        """
        Resets all limit lines. Removes all points stored.
        """
        comm = ":CALC:LLINE:ALL:CLE"
        self.instrument.write(comm)
    
    #Path Loss Table Controls
    """These commands control the path loss tables which are available in sweep, 
    real-time, zero-span, harmonics, digital modulation analysis, 
    EMC precompliance, analog demod, and interference hunting measurement modes."""

    def set_path_loss_table_state(self, table_num, state):
        """
        Enables or disables application of this path loss table.
        params: table_num (int): The path loss table number (1-8).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_pathloss_table_num(table_num)
        
        if state in self.valid_booleans:
            comm = f":SENS:CORR:PATH{table_num}:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def get_path_loss_table_state(self, table_num):
        """
        Queries if the path loss table is enabled.
        params: table_num (int): The path loss table number (1-8).
        Returns: bool: True if enabled, False if disabled.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:STAT?"
        status = self.instrument.query(comm)
        return (status == '1')

    def set_path_loss_table_description(self, table_num, description):
        """
        Specifies the name/description of this path loss table.
        params: table_num (int): The path loss table number (1-8).
                description (str): The name or description of the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DESC '{description}'"
        self.instrument.write(comm)

    def get_path_loss_table_description(self, table_num):
        """
        Queries the name/description of this path loss table.
        params: table_num (int): The path loss table number (1-8).
        Returns: str: The name or description of the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DESC?"
        description = self.instrument.query(comm)
        return description

    def set_path_loss_table_total_points(self, table_num, points_data):
        """
        Specifies the number of points in the path loss table, will overwrite any existing points.
        Points are specified as freq/offset pairs where the offset is specified as dB.
        params: table_num (int): The path loss table number (1-8).
                points_data (dict): (frequency, offset) pairs where frequency is in Hz and offset is in dB.
        """
        data = ""
        for key in points_data.keys():
            data = data + str(key) + "," + str(points_data[key]) + ","

        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DATA {data[0:data.__len__()-1]}"
        self.instrument.write(comm)

    def get_path_loss_table_points_count(self, table_num):
        """
        Returns the number of points in the path loss table as an integer.
        params: table_num (int): The path loss table number (1-8).
        Returns: int: The number of points in the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:POIN?"
        points = self.instrument.query(comm)
        return int(points)

    def get_path_loss_table_data(self, table_num):
        """
        Returns the points in the path loss table. Points are returned as freq/offset
        pairs where the frequencies are specified as Hz and the offsets as dB.
        params: table_num (int): The path loss table number (1-8).
        Returns: dict : (frequency,offset) 
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DATA?"
        data = self.instrument.query(comm)
        #TODO Test data is correct in unit test
        data_list = data.split(',')
        data_dict = {}
        for i in range(0,data_list,2):
            data_dict[data_list[i]] = data_list[i+1]

        return data_dict

    def clear_path_loss_table(self, table_num):
        """
        Resets the selected path loss table. Removes all points stored.
        params: table_num (int): The path loss table number (1-8).
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:CLE"
        self.instrument.write(comm)

    def clear_all_path_loss_tables(self):
        """
        Resets all path loss tables. Removes all points stored.
        """
        comm = ":SENS:CORR:PATH:ALL:CLE"
        self.instrument.write(comm)
#Reference Oscillscope Controls
    """These commands control the reference oscillator settings the of the spectrum analyzer."""
    def set_reference_oscillator_source(self, source):
        """
        Configures the reference oscillator source of the spectrum analyzer.
        params: source (str): The desired reference source. Allowed values are:
                              'INTERNAL', 'EXTERNAL', 'OUTPUT'.
        """
        allowed_sources = ['INTERNAL', 'EXTERNAL', 'OUTPUT', 'INT', 'EXT', 'OUT']
        source_upper = source.upper()
        if source_upper in allowed_sources:
            comm = f":SENSE:ROSCILLATOR:SOURCE {source_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid source: '{source}'. Allowed values are: {', '.join(allowed_sources)}")

    def get_reference_oscillator_source(self):
        """
        Queries the current reference oscillator source of the spectrum analyzer.
        Returns: str: The current reference source ('INTERNAL', 'EXTERNAL', 'OUTPUT').
        """
        comm = ":SENSE:ROSCILLATOR:SOURCE?"
        source = self.instrument.query(comm)
        return source

#Frequency Controls
    """These commands control the frequency settings of the spectrum analyzer."""
    def set_sense_frequency_center_step(self, step_size_hz: float):
        """
        Sets the step amount the center frequency changes by when using the UP or DOWN parameters on the CENTer command.
        Parameters:
        step_size_hz: The step size in Hz (numeric value).
        """
        self.instrument.write(f"SENSE:FREQ:CENT:STEP {step_size_hz}")

    def get_sense_frequency_center_step(self) -> float:
        """
        Queries the center frequency step size in Hz.
        Returns: The step size in Hz (numeric value).
        """
        response = self.instrument.query("SENSE:FREQ:CENT:STEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency center step size (not numeric): '{response}'")

#Power Controls
    """These commands affect the RF front end of the device.    
    Not all settings are available for each Signal Hound spectrum analyzer. 
    It is recommended to leave attenuation/gain/preamp set to auto and control the RF leveling with reference level."""
    
    def set_rf_reference_level(self, amplitude: float, direction: str = None):
        """
        Sets the RF reference level. If UP or DOWN is specified, the reference level is increased or decreased by the amplitude.
        Parameters:
        amplitude (float): The reference level in dBm.
        direction (str): 'UP' or 'DOWN' to adjust the reference level incrementally.
        """
        if direction:
            comm = f":SENSE:POWER:RF:RLEVEL {amplitude} {direction.upper()}"
        else:
            comm = f":SENSE:POWER:RF:RLEVEL {amplitude}"
        self.instrument.write(comm)

    def get_rf_reference_level(self) -> float:
        """
        Queries the current RF reference level in dBm.
        Returns: float: The reference level in dBm.
        """
        response = self.instrument.query(":SENSE:POWER:RF:RLEVEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF reference level: '{response}'")

    def get_rf_reference_level_unit(self) -> str:
        """
        Queries the current amplitude unit used to express the RF reference level.
        Returns: str: The amplitude unit (e.g., 'dBm').
        """
        return self.instrument.query(":SENSE:POWER:RF:RLEVEL:UNIT?").strip()

    def set_rf_reference_level_offset(self, offset: float):
        """
        Sets the RF reference level offset in dB.
        Parameters:
        offset (float): The offset value in dB.
        """
        comm = f":SENSE:POWER:RF:RLEVEL:OFFSET {offset}"
        self.instrument.write(comm)

    def get_rf_reference_level_offset(self) -> float:
        """
        Queries the RF reference level offset in dB.
        Returns: float: The offset value in dB.
        """
        response = self.instrument.query(":SENSE:POWER:RF:RLEVEL:OFFSET?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF reference level offset: '{response}'")

    def set_rf_plot_division(self, division: float):
        """
        Specifies the plot vertical division (1/10th of the plot height) as dB.
        Parameters:
        division (float): The division value in dB.
        """
        comm = f":SENSE:POWER:RF:PDIVISION {division}"
        self.instrument.write(comm)

    def get_rf_plot_division(self) -> float:
        """
        Queries the plot vertical division as dB.
        Returns: float: The division value in dB.
        """
        response = self.instrument.query(":SENSE:POWER:RF:PDIVISION?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF plot division: '{response}'")

    def set_rf_attenuation(self, attenuation: int):
        """
        Sets the RF attenuation index.
        Parameters:
        attenuation (int): The attenuation index.
        """
        comm = f":SENSE:POWER:RF:ATTENUATION {attenuation}"
        self.instrument.write(comm)

    def get_rf_attenuation(self) -> int:
        """
        Queries the RF attenuation index.
        Returns: int: The attenuation index.
        """
        response = self.instrument.query(":SENSE:POWER:RF:ATTENUATION?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF attenuation: '{response}'")

    def set_rf_attenuation_auto(self, enable: bool):
        """
        Enables or disables automatic RF attenuation.
        Parameters:
        enable (bool): True to enable automatic attenuation, False to disable.
        """
        comm = f":SENSE:POWER:RF:ATTENUATION:AUTO {'1' if enable else '0'}"
        self.instrument.write(comm)

    def get_rf_attenuation_auto(self) -> bool:
        """
        Queries if automatic RF attenuation is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENSE:POWER:RF:ATTENUATION:AUTO?").strip()
        return response == '1'

    def set_rf_gain(self, gain: int):
        """
        Sets the RF gain index.
        Parameters:
        gain (int): The gain index.
        """
        comm = f":SENSE:POWER:RF:GAIN {gain}"
        self.instrument.write(comm)
    def get_rf_gain(self) -> int:
        """
        Queries the RF gain index.
        Returns: int: The gain index.
        """
        response = self.instrument.query(":SENSE:POWER:RF:GAIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF gain: '{response}'")

    def set_rf_gain_auto(self, enable: bool):
        """
        Enables or disables automatic RF gain.
        Parameters:
        enable (bool): True to enable automatic gain, False to disable.
        """
        comm = f":SENSE:POWER:RF:GAIN:AUTO {'1' if enable else '0'}"
        self.instrument.write(comm)

    def get_rf_gain_auto(self) -> bool:
        """
        Queries if automatic RF gain is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENSE:POWER:RF:GAIN:AUTO?").strip()
        return response == '1'

    def set_rf_preamp(self, preamp: int):
        """
        Sets the RF preamp index.
        Parameters:
        preamp (int): The preamp index.
        """
        comm = f":SENSE:POWER:RF:PREAMP {preamp}"
        self.instrument.write(comm)

    def get_rf_preamp(self) -> int:
        """
        Queries the RF preamp index.
        Returns: int: The preamp index.
        """
        response = self.instrument.query(":SENSE:POWER:RF:PREAMP?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF preamp: '{response}'")

    def set_rf_preamp_auto(self, enable: bool):
        """
        Enables or disables automatic RF preamp.
        Parameters:
        enable (bool): True to enable automatic preamp, False to disable.
        """
        comm = f":SENSE:POWER:RF:PREAMP:AUTO {'1' if enable else '0'}"
        self.instrument.write(comm)

    def get_rf_preamp_auto(self) -> bool:
        """
        Queries if automatic RF preamp is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENSE:POWER:RF:PREAMP:AUTO?").strip()
        return response == '1'

    def set_rf_spur_reject(self, enable: bool):
        """
        Enables or disables RF spur rejection.
        Parameters:
        enable (bool): True to enable spur rejection, False to disable.
        """
        comm = f":SENSE:POWER:RF:SPURREJECT {'1' if enable else '0'}"
        self.instrument.write(comm)

    def get_rf_spur_reject(self) -> bool:
        """
        Queries if RF spur rejection is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENSE:POWER:RF:SPURREJECT?").strip()
        return response == '1'
#Bandwidth
    """These commands control the FFT processing for the receivers. 
    These settings are highly coupled with the frequency range and sweep time."""
    
    def set_sense_bandwidth_shape(self, shape_type: str):
        """
        Specifies the FFT window function for bandwidth shaping.
        Parameters:
        shape_type (str): The shape type. Allowed values are 'FLATTOP', 'NUTTALL', 'GAUSSIAN'.
        """
        valid_shapes = {"FLATTOP", "NUTTALL", "GAUSSIAN", "FLAT", "NUT", "GAUS"}
        shape_upper = shape_type.upper()
        if shape_upper not in valid_shapes:
            raise ValueError(f"Invalid shape type: '{shape_type}'. Must be 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'.")
        

        self.instrument.write(f"SENSE:BAND:SHAP {shape_type}")

    def get_sense_bandwidth_shape(self) -> str:
        """
        Queries the FFT window function for bandwidth shaping.
        Returns:
        str: The shape type ('FLATTOP', 'NUTTALL', or 'GAUSSIAN').
        """
        response = self.instrument.query("SENSE:BAND:SHAP?").strip()
        return response
#Sweep Controls
    """The sweep commands control additional FFT settings of the receiver."""
    def set_sweep_detector_function(self, function_type: str):
        """
        Controls how the VBW processing is performed.
        Parameters:
        function_type (str): Allowed values are 'AVERAGE', 'MINMAX', 'MIN', 'MAX'.
        """
        valid_functions = {"AVERAGE", "MINMAX", "MIN", "MAX", "AVER", "MINM", "MIN", "MAX"}
        function_upper = function_type.upper()
        if function_upper not in valid_functions:
            raise ValueError(f"Invalid detector function type: '{function_type}'. Must be 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'.")
        

        self.instrument.write(f"SENSE:SWE:DET:FUNC {function_upper}")

    def get_sweep_detector_function(self) -> str:
        """
        Queries how the VBW processing is performed.
        Returns:
        str: The detector function type ('AVERAGE', 'MINMAX', 'MIN', or 'MAX').
        """
        response = self.instrument.query("SENSE:SWE:DET:FUNC?").strip().upper()
        if response.startswith("AVER"):
            return "AVERAGE"
        elif response.startswith("MINM"):
            return "MINMAX"
        elif response.startswith("MIN"):
            return "MIN"
        elif response.startswith("MAX"):
            return "MAX"
        return response

    def set_sweep_detector_units(self, units_type: str):
        """
        Controls the units in which the detector function is performed.
        Parameters:
        units_type (str): Allowed values are 'POWER', 'SAMPLE', 'VOLTAGE', 'LOG'.
        """
        valid_units = {"POWER", "SAMPLE", "VOLTAGE", "LOG", "POW", "SAMP", "VOLT", "LOG"}
        units_upper = units_type.upper()
        if units_upper not in valid_units:
            raise ValueError(f"Invalid detector units type: '{units_type}'. Must be 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'.")
        

        self.instrument.write(f"SENSE:SWE:DET:UNIT {units_upper}")

    def get_sweep_detector_units(self) -> str:
        """
        Queries the units in which the detector function is performed.
        Returns:
        str: The detector units type ('POWER', 'SAMPLE', 'VOLTAGE', or 'LOG').
        """
        response = self.instrument.query("SENSE:SWE:DET:UNIT?").strip().upper()
        return response
#Trace Controls
    def select_trace(self, trace_index: int):
        """
        Specifies a trace index [1,6] for operations to occur on.
        Parameters:
        trace_index (int): The index of the trace to select (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f"TRACE:SELECT {trace_index}")

    def get_trace_select(self) -> int:
        """
        Queries the currently selected trace index.
        Returns:
        int: The index of the currently selected trace (1-6).
        """
        response = self.instrument.query("TRACE:SELECT?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRACE:SELECT? (not numeric): '{response}'")

    def set_trace_type(self, trace_type: str):
        """
        Specifies the behavior of the trace.
        Parameters:
        trace_type (str): Allowed values are 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', 'MINMAX'.
        """
        valid_types = {"OFF", "WRITE", "AVERAGE", "MAXHOLD", "MINHOLD", "MINMAX"}
        trace_type_upper = trace_type.upper()
        if trace_type_upper not in valid_types:
            raise ValueError(f"Invalid trace type: '{trace_type}'. Must be one of {valid_types}.")
        self.instrument.write(f":TRAC:TYPE {trace_type_upper}")

    def set_trace_average_count(self, count: int):
        """
        Specifies the number of traces that are averaged together to create the final sweep.
        Parameters:
        count (int): The number of traces to average.
        """
        if count < 1:
            raise ValueError("Average count must be a positive integer.")
        self.instrument.write(f":TRAC:AVER:COUN {count}")

    def get_trace_average_count(self) -> int:
        """
        Queries the number of traces that are averaged together to create the final sweep.
        Returns:
        int: The number of traces averaged.
        """
        response = self.instrument.query(":TRAC:AVER:COUN?")
        return int(response)

    def get_trace_average_current(self) -> int:
        """
        Retrieves the current number of traces that have been averaged together to create the final sweep.
        Returns:
        int: The current number of averaged traces.
        """
        response = self.instrument.query(":TRAC:AVER:CURR?")
        return int(response)

    def set_trace_update_state(self, enable: bool):
        """
        Specifies if the trace updates when a new sweep is acquired from the device.
        Parameters:
        enable (bool): True to enable updates, False to disable.
        """
        self.instrument.write(f":TRAC:UPD {'1' if enable else '0'}")

    def get_trace_update_state(self) -> bool:
        """
        Queries if the trace updates when a new sweep is acquired from the device.
        Returns:
        bool: True if updates are enabled, False otherwise.
        """
        response = self.instrument.query(":TRAC:UPD?")
        return response == '1'

    def set_trace_display_state(self, enable: bool):
        """
        Specifies if the trace is hidden or displayed.
        Parameters:
        enable (bool): True to display the trace, False to hide it.
        """
        self.instrument.write(f":TRAC:DISP {'1' if enable else '0'}")

    def is_trace_display_visible(self) -> bool:
        """
        Queries if the trace is hidden or displayed.
        Returns:
        bool: True if the trace is displayed, False if hidden.
        """
        response = self.instrument.query(":TRAC:DISP?")
        return response == '1'

    def clear_trace(self):
        """
        Clears the selected trace. For example, if the current sweep is a max hold sweep,
        and is cleared, the trace will be replaced with the next sweep from the device.
        """
        self.instrument.write(":TRAC:CLE")

    def clear_all_traces(self):
        """
        Clears all traces.
        """
        self.instrument.write(":TRAC:CLE:ALL")

    def get_trace_xstart(self) -> float:
        """
        Retrieves the frequency of the first point in the sweep as Hz.
        Useful for calculating the frequency of each point in the trace data returned from the TRACE:DATA? command.
        Returns:
        float: The frequency of the first point in Hz.
        """
        response = self.instrument.query(":TRAC:XSTA?")
        return float(response)

    def get_trace_xincrement(self) -> float:
        """
        Retrieves the frequency step between two points in the trace data as Hz.
        Useful for calculating the frequency of each point in the trace data.
        Returns:
        float: The frequency increment in Hz.
        """
        response = self.instrument.query(":TRAC:XINC?")
        return float(response)
    
#Marker Controls
    """The marker commands control the Spike sweep markers."""
    def select_marker(self, marker_index: int):
        """
        Selects the active marker.
        Parameters:
        marker_index (int): The index of the marker to select.
        """
        self.instrument.write(f":CALC:MARK:SEL {marker_index}")

    def selected_marker_index(self) -> int:
        """
        Queries the currently selected marker index.
        Returns:
        int: The index of the currently selected marker.
        """
        response = self.instrument.query(":CALC:MARK:SEL?")
        return int(response)

    def enable_marker(self, enable: bool):
        """
        Turns the marker on or off.
        Parameters:
        enable (bool): True to turn the marker on, False to turn it off.
        """
        self.instrument.write(f":CALC:MARK:STAT {'1' if enable else '0'}")

    def is_marker_visible(self) -> bool:
        """
        Queries the marker state (on or off).
        Returns:
        bool: True if the marker is on, False if it is off.
        """
        response = self.instrument.query(":CALC:MARK:STAT?")
        return response == '1'

    def set_marker_trace(self, trace_index: int):
        """
        Specifies which trace to place the marker on.
        Parameters:
        trace_index (int): The index of the trace to place the marker on.
        """
        self.instrument.write(f":CALC:MARK:TRAC {trace_index}")

    def get_marker_trace(self) -> int:
        """
        Queries which trace the marker is placed on.
        Returns:
        int: The index of the trace the marker is placed on.
        """
        response = self.instrument.query(":CALC:MARK:TRAC?")
        return int(response)

    def set_marker_mode(self, mode: str):
        """
        Switches between positional and noise marker modes.
        Parameters:
        mode (str): 'POSITION', 'NOISE', 'CHPOWER', 'NDB'.
        """
        valid_modes = {"POSITION", "NOISE", "POS", "CHPOWER","CHP","NDB"}
        mode_upper = mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid marker mode: '{mode}'. Must be 'POSITION' or 'NOISE'.")
        self.instrument.write(f":CALC:MARK:MODE {mode_upper}")

    def get_marker_mode(self) -> str:
        """
        Queries the current marker mode.
        Returns:
        str: The current marker mode ('POSITION' or 'NOISE').
        """
        response = self.instrument.query(":CALC:MARK:MODE?")
        return response.upper()

    def enable_marker_update(self, enable: bool):
        """
        Enables or disables marker updates on future sweep updates.
        Parameters:
        enable (bool): True to enable updates, False to disable.
        """
        self.instrument.write(f":CALC:MARK:UPD {'1' if enable else '0'}")

    def is_marker_update_enabled(self) -> bool:
        """
        Queries if marker updates are enabled on future sweep updates.
        Returns:
        bool: True if updates are enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:UPD?")
        return response == '1'

    def enable_marker_delta(self, enable: bool):
        """
        Enables or disables delta marker mode.
        Parameters:
        enable (bool): True to enable delta mode, False to disable.
        """
        self.instrument.write(f":CALC:MARK:DELT {'1' if enable else '0'}")

    def is_marker_delta_enabled(self) -> bool:
        """
        Queries if delta marker mode is enabled.
        Returns:
        bool: True if delta mode is enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:DELT?")
        return response == '1'

    def enable_marker_peak_track(self, enable: bool):
        """
        Enables or disables peak tracking for the marker.
        Parameters:
        enable (bool): True to enable peak tracking, False to disable.
        """
        self.instrument.write(f":CALC:MARK:PKTR {'1' if enable else '0'}")

    def is_marker_peak_track_enabled(self) -> bool:
        """
        Queries if peak tracking is enabled for the marker.
        Returns:
        bool: True if peak tracking is enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:PKTR?")
        return response == '1'

    def set_marker_position(self, frequency_hz: float):
        """
        Moves the marker position to the specified frequency.
        Parameters:
        frequency_hz (float): The frequency in Hz to move the marker to.
        """
        self.instrument.write(f":CALC:MARK:X {frequency_hz}")

    def get_marker_position_frequency(self) -> float:
        """
        Retrieves the marker position frequency in Hz.
        Returns:
        float: The marker position frequency in Hz.
        """
        response = self.instrument.query(":CALC:MARK:X?")
        return float(response)

    def get_marker_position_amplitude(self) -> float:
        """
        Retrieves the marker position amplitude according to marker type.
        Returns:
        float: The marker position amplitude in dBm or dBm/Hz.
        """
        response = self.instrument.query(":CALC:MARK:Y?")
        return float(response)

    def perform_peak_search(self):
        """
        Performs a peak search for the marker.
        """
        self.instrument.write(":CALC:MARK:MAX")

    def move_marker_to_next_peak(self):
        """
        Moves the marker to the next highest peak.
        """
        self.instrument.write(":CALC:MARK:MAX:NEXT")

    def move_marker_to_left_peak(self):
        """
        Moves the marker to the next peak to the left of its current position.
        """
        self.instrument.write(":CALC:MARK:MAX:LEFT")

    def move_marker_to_right_peak(self):
        """
        Moves the marker to the next peak to the right of its current position.
        """
        self.instrument.write(":CALC:MARK:MAX:RIGHT")

    def perform_minimum_search(self):
        """
        Performs a minimum peak search for the marker.
        """
        self.instrument.write(":CALC:MARK:MIN")

    def set_peak_excursion(self, excursion_db: float):
        """
        Specifies the peak excursion in dB.
        Parameters:
        excursion_db (float): The peak excursion in dB.
        """
        self.instrument.write(f":CALC:MARK:PEAK:EXC {excursion_db}")

    def get_peak_excursion(self) -> float:
        """
        Queries the peak excursion in dB.
        Returns:
        float: The peak excursion in dB.
        """
        response = self.instrument.query(":CALC:MARK:PEAK:EXC?")
        return float(response)

    def set_peak_threshold(self, threshold_db: float):
        """
        Specifies the peak threshold in dB.
        Parameters:
        threshold_db (float): The peak threshold in dB.
        """
        self.instrument.write(f":CALC:MARK:PEAK:THR {threshold_db}")

    def get_peak_threshold(self) -> float:
        """
        Queries the peak threshold in dB.
        Returns:
        float: The peak threshold in dB.
        """
        response = self.instrument.query(":CALC:MARK:PEAK:THR?")
        return float(response)

#Trace Math
#TODO: Add description
    def enable_trace_math(self, enable: bool):
        """
        Enables or disables the trace math function.
        Parameters:
        enable (bool): True to enable trace math, False to disable.
        """
        self.instrument.write(f":CALC:MATH:STAT {'1' if enable else '0'}")

    def is_trace_math_enabled(self) -> bool:
        """
        Queries if the trace math function is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MATH:STAT?")
        return response == '1'

    def set_trace_math_first_operand(self, trace_index: int):
        """
        Specifies the first operand trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the first operand trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:FIRST {trace_index}")

    def get_trace_math_first_operand(self) -> int:
        """
        Queries the first operand trace in the selected trace math function.
        Returns:
        int: The index of the first operand trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:FIRST?")
        return int(response)

    def set_trace_math_second_operand(self, trace_index: int):
        """
        Specifies the second operand trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the second operand trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:SECOND {trace_index}")

    def get_trace_math_second_operand(self) -> int:
        """
        Queries the second operand trace in the selected trace math function.
        Returns:
        int: The index of the second operand trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:SECOND?")
        return int(response)

    def set_trace_math_result_trace(self, trace_index: int):
        """
        Specifies the result trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the result trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:RES {trace_index}")

    def get_trace_math_result_trace(self) -> int:
        """
        Queries the result trace in the selected trace math function.
        Returns:
        int: The index of the result trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:RES?")
        return int(response)

    def set_trace_math_operation(self, operation: str):
        """
        Specifies the trace math function.
        Parameters:
        operation (str): Allowed values are 'PDIFF', 'PSUM', 'LOFFSET', 'LDIFF'.
        """
        valid_operations = {"PDIFF", "PSUM", "LOFFSET", "LDIFF"}
        operation_upper = operation.upper()
        if operation_upper not in valid_operations:
            raise ValueError(f"Invalid operation: '{operation}'. Must be one of {valid_operations}.")
        self.instrument.write(f":CALC:MATH:OP {operation_upper}")

    def get_trace_math_operation(self) -> str:
        """
        Queries the trace math function.
        Returns:
        str: The trace math function ('PDIFF', 'PSUM', 'LOFFSET', 'LDIFF').
        """
        response = self.instrument.query(":CALC:MATH:OP?")
        return response.upper()

    def set_trace_math_offset(self, offset_value: float):
        """
        Specifies the offset to use in the logarithm trace math functions.
        Parameters:
        offset_value (float): The offset value in dB.
        """
        self.instrument.write(f":CALC:MATH:OFFS {offset_value}")

    def get_trace_math_offset(self) -> float:
        """
        Queries the offset used in the logarithm trace math functions.
        Returns:
        float: The offset value in dB.
        """
        response = self.instrument.query(":CALC:MATH:OFFS?")
        return float(response)

#Channel Power
    """These commands control the channel power measurement in the Spike software. 
    Through these commands you can configure a main channel and up to 5 adjacent 
    channels and simultaneously measure channel and adjacent channel power."""
    def enable_channel_power(self, enable: bool):
        """
        Enables or disables the channel power measurement.
        Parameters:
        enable (bool): True to enable channel power measurement, False to disable.
        """
        self.instrument.write(f":SENS:CHP:STAT {'1' if enable else '0'}")

    def is_channel_power_enabled(self) -> bool:
        """
        Queries if the channel power measurement is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:CHP:STAT?")
        return response == '1'

    def set_channel_power_trace(self, trace_index: int):
        """
        Selects which trace the channel power measurement is performed on.
        Parameters:
        trace_index (int): The index of the trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":SENS:CHP:TRAC {trace_index}")

    def get_channel_power_trace(self) -> int:
        """
        Queries which trace the channel power measurement is performed on.
        Returns:
        int: The index of the trace (1-6).
        """
        response = self.instrument.query(":SENS:CHP:TRAC?")
        return int(response)

    def set_channel_power_width(self, width_hz: float):
        """
        Specifies the width of the main channel power measurement as a frequency.
        Parameters:
        width_hz (float): The width in Hz.
        """
        self.instrument.write(f":SENS:CHP:WIDT {width_hz}")

    def get_channel_power_width(self) -> float:
        """
        Queries the width of the main channel power measurement as a frequency.
        Returns:
        float: The width in Hz.
        """
        response = self.instrument.query(":SENS:CHP:WIDT?")
        return float(response)

    def enable_adjacent_channel_power(self, channel_index: int, enable: bool):
        """
        Enables or disables the measurement of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        enable (bool): True to enable measurement, False to disable.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:STAT {channel_index},{'1' if enable else '0'}")

    def is_adjacent_channel_power_enabled(self, channel_index: int) -> bool:
        """
        Queries if the measurement of an adjacent channel is enabled.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        bool: True if enabled, False otherwise.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:STAT? {channel_index}")
        return response == '1'

    def set_adjacent_channel_offset(self, channel_index: int, offset_hz: float):
        """
        Specifies the offset from the center of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        offset_hz (float): The offset in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:OFFS {channel_index},{offset_hz}")

    def get_adjacent_channel_offset(self, channel_index: int) -> float:
        """
        Queries the offset from the center of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        float: The offset in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:OFFS? {channel_index}")
        return float(response)

    def set_adjacent_channel_width(self, channel_index: int, width_hz: float):
        """
        Specifies the width of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        width_hz (float): The width in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:WIDT {channel_index},{width_hz}")

    def get_adjacent_channel_width(self, channel_index: int) -> float:
        """
        Queries the width of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        float: The width in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:WIDT? {channel_index}")
        return float(response)

    def get_main_channel_power(self) -> float:
        """
        Queries the channel power of the main channel.
        Returns:
        float: The channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP?")
        return float(response)

    def get_adjacent_channel_power_lower(self) -> float:
        """
        Queries the lower adjacent channel power.
        Returns:
        float: The lower adjacent channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP:LOW?")
        return float(response)

    def get_adjacent_channel_power_upper(self) -> float:
        """
        Queries the upper adjacent channel power.
        Returns:
        float: The upper adjacent channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP:UPP?")
        return float(response)

    def get_adjacent_channel_ac_power_lower(self) -> float:
        """
        Queries the lower adjacent channel AC power.
        Returns:
        float: The lower adjacent channel AC power in dBc.
        """
        response = self.instrument.query(":SENS:CHP:ACP:LOW?")
        return float(response)

    def get_adjacent_channel_ac_power_upper(self) -> float:
        """
        Queries the upper adjacent channel AC power.
        Returns:
        float: The upper adjacent channel AC power in dBc.
        """
        response = self.instrument.query(":SENS:CHP:ACP:UPP?")

        return float(response)
# Occupied Bandwidth Controls
    """These commands allow you to configure the occupied bandwidth 
    measurement in the Spike software"""
    def enable_occupied_bandwidth(self, enable: bool):
        """
        Enables or disables the occupied bandwidth measurement.
        Parameters:
        enable (bool): True to enable, False to disable.
        """
        self.instrument.write(f":SENS:OBW:STAT {'1' if enable else '0'}")

    def is_occupied_bandwidth_enabled(self) -> bool:
        """
        Queries if the occupied bandwidth measurement is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:OBW:STAT?")
        return response == '1'

    def set_occupied_bandwidth_trace(self, trace_index: int):
        """
        Specifies which trace the occupied bandwidth measurement is performed on.
        Parameters:
        trace_index (int): The index of the trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":SENS:OBW:TRAC {trace_index}")

    def get_occupied_bandwidth_trace(self) -> int:
        """
        Queries which trace the occupied bandwidth measurement is performed on.
        Returns:
        int: The index of the trace (1-6).
        """
        response = self.instrument.query(":SENS:OBW:TRAC?")
        return int(response)

    def set_occupied_bandwidth_percent(self, percent: float):
        """
        Specifies the percentage of the total energy of the sweep for the occupied bandwidth measurement.
        Parameters:
        percent (float): The percentage value.
        """
        self.instrument.write(f":SENS:OBW:PERC {percent}")

    def get_occupied_bandwidth_percent(self) -> float:
        """
        Queries the percentage of the total energy of the sweep for the occupied bandwidth measurement.
        Returns:
        float: The percentage value.
        """
        response = self.instrument.query(":SENS:OBW:PERC?")
        return float(response)

    def get_occupied_bandwidth(self) -> float:
        """
        Queries the bandwidth of the occupied bandwidth measurement as Hz.
        Returns:
        float: The bandwidth in Hz.
        """
        response = self.instrument.query(":SENS:OBW:OBW?")
        return float(response)

    def get_occupied_bandwidth_center_frequency(self) -> float:
        """
        Queries the center frequency of the occupied bandwidth measurement as Hz.
        Returns:
        float: The center frequency in Hz.
        """
        response = self.instrument.query(":SENS:OBW:CENT?")
        return float(response)

    def get_occupied_bandwidth_power(self) -> float:
        """
        Queries the power of the occupied bandwidth measurement.
        Returns:
        float: The power value.
        """
        response = self.instrument.query(":SENS:OBW:POW?")
        return float(response)
