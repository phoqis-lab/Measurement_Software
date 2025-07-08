import instrument
import time

class SpectrumAnalyzer(instrument.Instrument):
    def __init__(self, device):
       #TODO Add in 
       self.instrument = device
    #Display
    def is_spike_hidden(self):
        #TODO: Test that :DATA unneeded
        """ Queries if the spike application is hidden."""
        comm = ":DISPlay:HIDE?"
        response = self.instrument.query(comm)
        if response.upper() in ['ON', '1']:
            return True
        elif response.upper() in ['OFF', '0']:
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
    
        allowed_type_values = ['ON', 'OFF',1,0]
        if str(to_hide).upper() in allowed_type_values:
            comm = ":DISPlay:HIDE " + str(to_hide).upper()
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    def get_measurement_title(self):
        """ Get the measurement title."""
        comm = ":DISPlay:ANN:TITLE?"
        return self.instrument.query(comm)
    def set_measurement_title(self, title):
        """ Set the measurement title."""
        if isinstance(title, str):
            comm = ":DISPlay:ANN:TITLE " + title
            self.instrument.write(comm)
        else:
            print("Invalid type. Title must be a string.")
    
    def clear_measurement_title(self):
        """ Clear the measurement title."""
        comm = ":DISPlay:ANN:CLEar"
        self.instrument.write(comm)

    #Format Trace Controls
    def get_trace_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the trace data is returned in."""
        comm = ":FORMat:TRACe?"
        return self.instrument.query(comm)

    def set_trace_format(self, format):
        """Set the format the trace data is returned in.
        format: 'ASCii', 'REAL'"""
    
        allowed_type_values = ['ASCii', 'REAL','ASC']
        if format in allowed_type_values:
            comm = ":FORMat:TRACe " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    def get_iq_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the iq data is returned in."""
        comm = ":FORMat:IQ?"
        return self.instrument.query(comm)

    def set_iq_format(self, format):
        """Set the format the iq data is returned in.
        format: 'ASCii', 'BINary'"""
    
        allowed_type_values = ['ASCii', 'BINary','BIN','ASC']
        if format in allowed_type_values:
            comm = ":FORMat:IQ " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    #System Controls
    def close_system(self):
        """
        Disconnects any active device and closes the Spike software.
        There is no way to reopen the software using SCPI commands.
        This will also terminate the socket connection with the Spike software.
        """
        comm = ":SYSTem:CLOSe"
        self.instrument.write(comm)
        print("System close command sent. Socket connection terminated.")

    def preset_system(self):
        """
        Presets the active device. This will power cycled the active device and
        return the software to the initial power on state. This process can take
        between 6-20 seconds depending on the device type.
        """
        comm = ":SYSTem:PRESet"
        self.instrument.write(comm)
        print("System preset command sent. Device will power cycle.")
        # It's good practice to add a delay if the operation takes time
        time.sleep(10) # Wait for 10 seconds as per documentation

    def get_preset_status(self):
        """
        Queries the preset status of the active device. This will close and reopen
        the active device. This process can take between 6-20 seconds depending
        on the device type. Returns 0 or 1 depending on success. (1 for success)
        """
        comm = ":SYSTem:PRESet?"
        response = self.instrument.query(comm)
        try:
            status = int(response)
            if status == 1:
                print("System preset successful.")
            else:
                print("System preset failed or in progress.")
            return status
        except ValueError:
            print(f"Invalid response for preset status: {response}")
            return None

    def save_image(self, filename):
        """
        Saves a screenshot with the given file name. The file name should have
        extension ".ini".
        params: filename (str): The name of the file to save the image as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            print("Warning: Filename should have a '.ini' extension.")
        comm = f":SYSTem:IMAGe:SAVE {filename}"
        self.instrument.write(comm)
        print(f"Image save command sent for: {filename}")

    def save_image_quick(self):
        """
        Saves a quick image. Same functionality as the Image quick save file menu option.
        """
        comm = ":SYSTem:IMAGe:SAVE:QUICK"
        self.instrument.write(comm)
        print("Quick image save command sent.")

    def load_user_preset(self, filename):
        """
        Loads the preset given by the file name. If the preset does not exist,
        nothing occurs. The file name should have extension ".ini".
        params: filename (str): The name of the preset file to load. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            print("Warning: Filename should have a '.ini' extension.")
        comm = f":SYSTem:PRESet:USER:LOAD {filename}"
        self.instrument.write(comm)
        print(f"User preset load command sent for: {filename}")

    def save_user_preset(self, filename):
        """
        Saves the user preset with the given file name. The file name should have
        extension ".ini".
        params: filename (str): The name of the file to save the user preset as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            print("Warning: Filename should have a '.ini' extension.")
        comm = f":SYSTem:PRESet:USER:SAVE {filename}"
        self.instrument.write(comm)
        print(f"User preset save command sent for: {filename}")

    def communicate_gtlocal(self):
        """
        Puts Spike in local mode.
        """
        comm = ":SYSTem:COMMunicate:GTLocal"
        self.instrument.write(comm)
        print("Spike set to local mode.")

    def print_system(self):
        """
        Prints the default system print settings.
        """
        comm = ":SYSTem:PRINt"
        self.instrument.write(comm)
        print("System print command sent.")

    def get_temperature(self):
        """
        Returns the current internal temperature of the active device, in degrees Celsius.
        """
        comm = ":SYSTem:TEMPerature?"
        temperature = self.instrument.query(comm)
        try:
            temp_float = float(temperature)
            print(f"Device temperature: {temp_float}°C")
            return temp_float
        except ValueError:
            print(f"Invalid response for temperature: {temperature}")
            return None

    def get_voltage(self):
        """
        Returns the measured voltage of the active device, in volts.
        """
        comm = ":SYSTem:VOLTage?"
        voltage = self.instrument.query(comm)
        try:
            volt_float = float(voltage)
            print(f"Device voltage: {volt_float} V")
            return volt_float
        except ValueError:
            print(f"Invalid response for voltage: {voltage}")
            return None

    def get_current(self):
        """
        Returns the measured current of the active device, in amps.
        (BB and SM series devices only. SA series devices return 0.)
        """
        comm = ":SYSTem:CURRent?"
        current = self.instrument.query(comm)
        try:
            current_float = float(current)
            print(f"Device current: {current_float} A")
            return current_float
        except ValueError:
            print(f"Invalid response for current: {current}")
            return None
        
    def get_version(self):
        """ Get the system version."""
        return super().get_system_version()
    

    #Device Management Controls
    """The functions below allow you to remotely manage the active device 
    in the Spike software. This is useful for error recovery in the event a 
    device disconnect occurs due, or if one is managing multiple Signal Hound devices on one PC."""
    
    def get_device_active_status(self):
        """
        Returns whether or not a device is currently connected and active in the software.
        Look at the *IDN? function to request information about the device.
        """
        comm = ":SYSTem:DEVice:ACTive?"
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
        comm = ":SYSTem:DEVice:COUNt?"
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
        returned in the list with the following format: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        This entire string can be sent to the connect function to connect to a networked device.
        """
        comm = ":SYSTem:DEVice:LIST?"
        response = self.instrument.query(comm)
        device_list = [d.strip() for d in response.split(',')]
        print(f"Available devices: {device_list}")
        return device_list

    def get_current_device_connection_string(self):
        """
        Returns the currently active device's connection string. See LIST? for format.
        """
        comm = ":SYSTem:DEVice:CURRent?"
        response = self.instrument.query(comm)
        print(f"Current active device connection string: {response}")
        return response

    def connect_device(self, connection_string):
        """
        Connects a device in the Spike software. For USB devices, you need to
        provide the serial number of the device to connect. For networked devices,
        send a string with format: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        Returns 0 or 1 depending on if the device successfully opened.
        params: connection_string (str): The connection string of the device to connect.
                                         For USB, this is the serial number. For networked,
                                         it's in the format SOCKET::IP::PORT.
        """
        comm = f":SYSTem:DEVice:CONnect {connection_string}"
        self.instrument.write(comm)
        print(f"Attempting to connect to device: {connection_string}")
        # The documentation states it returns 0 or 1, but this is a 'write' command,
        # so we'd typically query a status afterward if available.
        # For now, we'll just print a message indicating the command was sent.

    def disconnect_device(self):
        """
        Disconnects any device actively connected in Spike.
        """
        comm = ":SYSTem:DEVice:DISConnect"
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
    get_system_error
    #Frequency Controls
    def get_center_frequency(self):
        """ Get the measurement center frequency."""
        return super().get_sense_frequency_center()

    def set_center_frequency(self):
        """ Set the measurement center frequency. This can cause the start or stop 
        frequency to change if the device is unable to maintain the current span with the new center frequency. 
        This can have the side effect of changing the span/start/stop frequencies."""
        return super().get_sense_frequency_center()
    
    def get_center_frequency(self):
        """ Get the measurement center frequency."""
        return super().get_sense_frequency_center()

    def set_center_frequency(self):
        """ Set the measurement center frequency. This can cause the start or stop 
        frequency to change if the device is unable to maintain the current span with the new center frequency. 
        This can have the side effect of changing the span/start/stop frequencies."""
        return super().get_sense_frequency_center()