import instrument
from ds1054z import DS1054Z
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
from time import sleep
from time import sleep
import pyvisa
class RigolOscilloscope(instrument.Instrument):
    x = 0 

    #DS
    def __init__():
        #DA1054z library
        #Would need to check IP address of scope
        scope = DS1054Z('192.168.0.23')
        print("Connected to: ", scope.idn)

        print("Currently displayed channels: ", str(scope.displayed_channels))
    
    def __init__():
        with Rigol_DS1000Z() as oscope:
            # reset to defaults and print the IEEE 488.2 instrument identifier
            ieee = oscope.ieee(rst=True)
            print(ieee.idn)
    
    #Can modify waveform by changing horzontal or vertical position
    #Trigger types intclude auto normal and single
    #Trigger level goes from 0 to XX mV volts - put check in for max
    #clear
    #call auto for pre made settings for display
    #can modify what is measured - see full lsit of measureument setting here 
    #Has six menu measure, acquire (mode and memory depth), storage (disk management), display, utility, cursor (XY modes)
    #16 measurement parameters H and V each
    #Need to change where trigger source comes from four channels or AC Line
    #set probe ratio
    #turn bandwidth limit on or off
    #channels coupling modes can be AC or DC of GND
    #Can change time mode from YT and XY - XY requires two channels

    #Acquisition Commands
    def set_number_of_averages(self, avg):
        """In the average acquisition mode, greater number of averages can lower the noise
        and increase the vertical resolution, but will also slow the response of the displayed
        waveform to the waveform changes. Avg: 2 to 1024"""
        if avg<2 or avg>1024:
            print("Average is an invalid value. Please enter a number between 2 and 1024")
        else:
            comm_mode = ":ACQuire:AVERages "+avg
            self.instrument.write(comm_mode)

    def get_number_of_averages(self, avg):
        """In the average acquisition mode, greater number of averages can lower the noise
        and increase the vertical resolution."""
        comm_mode = ":ACQuire:AVERages?"
        self.instrument.query(comm_mode)
    
    def set_memory_depth(self, mdpth):
        """ Set memory depth of the oscilloscope (namely the number of waveform
points that can be stored in a single trigger sample). Single Channel: AUTO|12000|
120000|1200000|12000000|24000000. Dual Channel:  {AUTO|6000|60000|
600000|6000000|12000000}."""
#TODO: Add in check of channel status
        sc_allowed_values = ["AUTO",12000,120000,1200000,12000000,24000000]
        dc_allowed_values = ["AUTO",6000,60000,600000,6000000,12000000]
        if mdpth in sc_allowed_values or mdpth in dc_allowed_values:
            comm_mode = ":ACQuire:MDEPth "+mdpth
            self.instrument.write(comm_mode)
        else:
            print("Invalid memory depth.")

    def get_memory_depth(self):
        """ Get memory depth of the oscilloscope (namely the number of waveform
points that can be stored in a single trigger sample)."""
        comm_mode = ":ACQuire:MDEPth?"
        self.instrument.query(comm_mode)

   
    def get_sample_rate(self):
        """ Query the current sample rate. The default unit is Sa/s."""
        comm_mode = ":ACQuire:SRATe?"
        self.instrument.query(comm_mode)

    #Channel Commands
    def set_channel_bandwidth_limit(self, channel, bw):
        """ Set or query the bandwidth limit parameter of the specified channel. OFF: disable the bandwidth limit and the high frequency components of the signal
under test can pass the channel.
20M: enable the bandwidth limit and the high frequency components of the signal
under test that exceed 20 MHz are attenuated. """
#TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["20M", "OFF"]
        if channel in allowed_chnl_values or bw in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":BWLimit "+bw
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_bandwidth_limit(self, channel):
        """ Query the bandwidth limit parameter of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":BWLimit?"
        self.instrument.query(comm_mode)

    def set_channel_coupling_mode(self, channel, coupling_mode):
        """ Set the coupling mode of the specified channel."""
#TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values or bw in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":COUPling "+coupling_mode
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_coupling_mode(self, channel):
        """ Query the coupling mode of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":COUPling?"
        self.instrument.query(comm_mode)
    
    def invert_waveform(self, channel, param1):
        """ Set the coupling mode of the specified channel."""
        #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["ON","OFF",1, 2]
        if channel in allowed_chnl_values or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":INVert "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def is_inverted(self, channel):
        """ Query the coupling mode of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":INVert?"
        self.instrument.query(comm_mode)
    
    def set_channel_offset(self, channel, param1):
        """ Set the vertical offset of the specified channel. The default unit is V."""
    #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        #allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values: #or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":OFFSet "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_offset(self, channel):
        """ Query the vertical offset of the specified channel. The default unit is V."""
        comm_mode = ":CHANnel"+str(channel)+":OFFSet?"
        self.instrument.query(comm_mode)
    
    def set_channel_range(self, channel, param1):
        """ Set the vertical offset of the specified channel. The default unit is V."""
    #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        #allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values: #or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":OFFSet "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_range(self, channel):
        """ Query the vertical offset of the specified channel. The default unit is V."""
        comm_mode = ":CHANnel"+str(channel)+":OFFSet?"
        self.instrument.query(comm_mode)
    
    def set_channel_tcal(self, channel, val):
        """
        Set delay calibration time for the specified channel.
        val: delay time in seconds (e.g., 20e-9 for 20ns). Valid range: -100e-9 to 100e-9.
        NOTE: Must match timing step for current timebase scale; oscilloscope rounds if needed.
        """
        if channel in [1, 2] and isinstance(val, (float, int)) and -100e-9 <= val <= 100e-9:
            self.instrument.write(f":CHANnel{channel}:TCAL {val}")
        else:
            print("Invalid channel or value (must be float between -100e-9 and 100e-9)")

    def get_channel_tcal(self, channel):
        """
        Query delay calibration time for the specified channel (in seconds).
        Returns value in scientific notation as float.
        """
        if channel in [1, 2]:
            response = self.instrument.query(f":CHANnel{channel}:TCAL?")
            return float(response)
        else:
            print("Invalid channel number.")
            return None
    
    def set_channel_scale(self, channel, scale):
        """Set vertical scale of the channel (in V/div)."""
        self.instrument.write(f":CHANnel{channel}:SCALe {scale}")

    def get_channel_scale(self, channel):
        """Query vertical scale of the channel."""
        return self.instrument.query(f":CHANnel{channel}:SCALe?")

    def set_probe_ratio(self, channel, ratio):
        """Set the probe attenuation ratio for a channel."""
        self.instrument.write(f":CHANnel{channel}:PROBe {ratio}")

    def get_probe_ratio(self, channel):
        """Query the probe attenuation ratio for a channel."""
        return self.instrument.query(f":CHANnel{channel}:PROBe?")

    def set_channel_units(self, channel, unit):
        """Set the amplitude display unit for a channel. Options: VOLTage, WATT, AMPere, UNKNown."""
        self.instrument.write(f":CHANnel{channel}:UNITs {unit}")

    def get_channel_units(self, channel):
        """Query the amplitude display unit for a channel."""
        return self.instrument.query(f":CHANnel{channel}:UNITs?")

    def set_vernier(self, channel, state):
        """Enable or disable fine adjustment (vernier) for vertical scale."""
        self.instrument.write(f":CHANnel{channel}:VERNier {state}")

    def get_vernier(self, channel):
        """Query vernier setting."""
        return self.instrument.query(f":CHANnel{channel}:VERNier?")
    
    #Cursor Commands
    def set_cursor_mode(self, mode):
        """
        Set cursor measurement mode.

        Parameters:
        mode (str): One of {"OFF", "MANual", "TRACk", "AUTO", "XY"}
        Note: XY mode only valid when timebase mode is also XY.
        """
        valid_modes = {"OFF", "MANual", "TRACk", "AUTO", "XY"}
        mode = mode.upper()
        if mode in {m.upper() for m in valid_modes}:
            self.instrument.write(f":CURSor:MODE {mode}")
        else:
            print(f"Invalid mode. Must be one of: {valid_modes}")

    def get_cursor_mode(self):
        """
        Query the current cursor measurement mode.

        Returns:
        str: One of {"OFF", "MAN", "TRAC", "AUTO", "XY"}
        """
        return self.instrument.query(":CURSor:MODE?")
    
    def set_cursor_manual_type(self, cursor_type):
        """
        Set the type of manual cursor.

        Parameters:
        cursor_type (str): Either "X" for vertical cursors (time) or "Y" for horizontal cursors (voltage).
        """
        cursor_type = cursor_type.upper()
        if cursor_type in ["X", "Y"]:
            self.instrument.write(f":CURSor:MANual:TYPE {cursor_type}")
        else:
            print("Invalid cursor type. Use 'X' or 'Y'.")
    
    def get_cursor_manual_type(self):
        """
        Query the current manual cursor type.

        Returns:
        str: "X" or "Y"
        """
        return self.instrument.query(":CURSor:MANual:TYPE?")

    def get_cursor_manual_source(self):
        """
        Query the current source for manual cursor measurement.

        Returns:
        str: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")
    
    def set_cursor_manual_source(self, source):
        """
        Set the source for manual cursor measurement.

        Parameters:
        source (str): Channel or source name. Valid options include:
                    "CHAN1", "CHAN2", "MATH", "REF1", "REF2", "REF3", "REF4"
        """
        source = source.upper()
        valid_sources = {"CHAN1", "CHAN2", "MATH"}

        if source in valid_sources:
            self.instrument.write(f":CURSor:MANual:SOURce {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_cursor_manual_source(self):
        """
        Query the current source for manual cursor measurement.

        Returns:
        str: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")

    def get_cursor_manual_tunit(self):
        """ Query the current horizontal unit in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:TUNit?")

    def set_cursor_manual_tunit(self, unit):
        """ Set the horizontal unit for manual cursor measurement. """
        valid_units = ["S", "HZ", "DEGRee", "PERCent"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:TUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")
    def get_cursor_manual_vunit(self):
        """ Query the current vertical unit in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:VUNit?")

    def set_cursor_manual_vunit(self, unit):
        """ Set the vertical unit for manual cursor measurement. """
        valid_units = ["PERCent", "SOURce"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:VUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def set_cursor_manual(self, cursor, x, y):
        """ Set the horizontal position of cursor A or Bb  in the manual cursor measurement mode. """
        if 5 <= x <= 594:  # Ensure the position is within the valid range
            self.instrument.write(f":CURSor:MANual:"+cursor+"X {x}")
        else:
            print("Invalid position. x must be between 5 and 594.")
        
        if 5 <= y <= 394:  # Ensure the position is within the valid range
            self.instrument.write(f":CURSor:MANual:"+cursor+"Y {y}")
        else:
            print("Invalid position. y must be between 5 and 394.")

    def get_cursor_manual(self,cursor):
        """ Query the horizontal position of cursor A or B in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:"+cursor+"X?;"+cursor+"Y?")

    def get_cursor_manual_xdelta(self):
        """ Query the difference between the X values of cursor A and cursor B (BX - AX) in the manual cursor measurement mode. """
        response = self.instrument.query(":CURSor:MANual:XDELta?")
        return float(response)  # Returns the difference in scientific notation

    def get_cursor_manual_ixdelta(self):
        """ Query the reciprocal of the absolute value of the difference between the X values of cursor A and cursor B (1/|dX|). """
        response = self.instrument.query(":CURSor:MANual:IXDELta?")
        return float(response)  # Returns the reciprocal in scientific notation
    
    def get_cursor_manual_ydelta(self):
        """ Query the difference between the Y values of cursor A and cursor B (BY - AY) in the manual cursor measurement mode. """
        response = self.instrument.query(":CURSor:MANual:YDELta?")
        return float(response)  # Returns the difference in scientific notation

    def set_cursor_track_source(self, source, n):
        """ Set the channel source of cursor A in the track cursor measurement mode. """
        valid_sources = ["OFF", "CHANnel1", "CHANnel2", "MATH"]
        source = source.upper()  # Ensure source is in uppercase

        if source in valid_sources:
            self.instrument.write(f":CURSor:TRACk:SOURce"+str(n)+ " {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_cursor_track_source(self, n):
        """ Query the channel source of cursor A in the track cursor measurement mode. """
        return self.instrument.query(":CURSor:TRACk:SOURce"+str(n)+"?")
    
    def set_cursor_xy(self, cursor, x, y):
        """ Set the horizontal position of cursor A in the XY cursor measurement mode. """
        if 5 <= x <= 394 and 5 <= y <= 394:
            self.instrument.write(f":CURSor:XY:"+cursor+"X {x};"+cursor+"Y {y};")
        else:
            print("Invalid x or y position. Must be between 5 and 394.")

    def get_cursor_xy(self, cursor):
        """ Query the horizontal position of cursor A in the XY cursor measurement mode. """
        response = self.instrument.query(":CURSor:XY:)"+cursor+"X?;"+cursor+"Y?")
        return response # Returns an integer between 5 and 394

    #Decoding
    def set_decoder_mode(self, n, mode):
        """
        Set the decoder type for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        mode (str): The decoder type, one of {"PARallel", "UART", "SPI", "IIC"}.
        """
        valid_decoders = [1, 2]
        valid_modes = ["PARallel", "UART", "SPI", "IIC"]

        if n in valid_decoders and mode.upper() in valid_modes:
            self.instrument.write(f":DECoder{n}:MODE {mode.upper()}")
        else:
            print(f"Invalid decoder or mode. Decoder: {valid_decoders}, Mode: {valid_modes}")

    def get_decoder_mode(self, n):
        """
        Query the decoder type for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        str: The decoder type, one of {"PAR", "UART", "SPI", "IIC"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:MODE?")
            return response.strip().upper()  # Returns the mode (e.g., PAR, UART, SPI, IIC)
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_format(self, n, fmt):
        """
        Set the bus display format for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        fmt (str): The bus display format, one of {"HEX", "ASCii", "DEC", "BIN", "LINE"}.
        """
        valid_decoders = [1, 2]
        valid_formats = ["HEX", "ASCii", "DEC", "BIN", "LINE"]

        if n in valid_decoders and fmt.upper() in valid_formats:
            self.instrument.write(f":DECoder{n}:FORMat {fmt.upper()}")
        else:
            print(f"Invalid decoder or format. Decoder: {valid_decoders}, Format: {valid_formats}")

    def get_decoder_format(self, n):
        """
        Query the bus display format for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        str: The bus display format, one of {"HEX", "ASC", "DEC", "BIN", "LINE"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:FORMat?")
            return response.strip().upper()  # Returns the format (e.g., HEX, ASC, DEC, BIN, LINE)
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_threshold_channel(self, channel, n, thre):
        """
        Set the threshold level for the specified decoder channel 1.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        thre (float): The threshold level, in volts. Should be within the range of the vertical scale and offset.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:THREshold:CHANnel"+channel+" {thre}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_threshold_channel(self, channel, n):
        """
        Query the threshold level for the specified decoder channel 1 or 2.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        float: The threshold level in scientific notation (volts).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:THREshold:CHANnel1?")
            return float(response.strip())  # Returns the threshold level as a float
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_auto_threshold(self, n, auto):
        """
        Turn on or off the auto threshold function for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        auto (bool): Whether to turn on (1) or off (0) the auto threshold function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:THREshold:AUTO {'ON' if auto else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_auto_threshold(self, n):
        """
        Query the status of the auto threshold function for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the auto threshold function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:THREshold:AUTO?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_label_display(self, n, label_status):
        """
        Turn on or off the label display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        label_status (bool): Whether to turn on (1) or off (0) the label display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:LABel {'ON' if label_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_label_display(self, n):
        """
        Query the status of the label display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the label display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:LABel?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_bus_display(self, n, line_status):
        """
        Turn on or off the bus display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        line_status (bool): Whether to turn on (1) or off (0) the bus display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:LINE {'ON' if line_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_bus_display(self, n):
        """
        Query the status of the bus display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the bus display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:LINE?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_format_display(self, n, format_status):
        """
        Turn on or off the format display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        format_status (bool): Whether to turn on (1) or off (0) the format display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:FORMat {'ON' if format_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_format_display(self, n):
        """
        Query the status of the format display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the format display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:FORMat?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_endian_display(self, n, endian_status):
        """
        Turn on or off the endian display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        endian_status (bool): Whether to turn on (1) or off (0) the endian display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:ENDian {'ON' if endian_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_endian_display(self, n):
        """
        Query the status of the endian display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the endian display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:ENDian?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_width_display(self, n, width_status):
        """
        Turn on or off the width display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        width_status (bool): Whether to turn on (1) or off (0) the width display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:WIDth {'ON' if width_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_width_display(self, n):
        """
        Query the status of the width display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the width display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:WIDth?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

#Display Commands

    #Waveforms
    def set_waveform_source(self, source):
        """Set waveform source: CHANnel1, CHANnel2, MATH, REF<x>."""
        self.instrument.write(f":WAVeform:SOURce {source}")

    def get_waveform_data(self):
        """Query waveform data in current format."""
        return self.instrument.query_binary_values(":WAVeform:DATA?", datatype='B')

    def set_waveform_format(self, fmt):
        """Set waveform data format: ASCII, BYTE, WORD."""
        self.instrument.write(f":WAVeform:FORMat {fmt}")

    def get_waveform_format(self):
        """Query waveform data format."""
        return self.instrument.query(":WAVeform:FORMat?")