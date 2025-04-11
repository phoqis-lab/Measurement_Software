import visa
class Instrument:
    def __init__(self, name):
        self.name = name
        self.instrument = None
        self.saved_output_path = ""
    
    #Basic Commands
    def get_id(self):

        return self.instrument.query('*IDN?')
    def reset(self):
        """Reset the oscilloscope to default settings."""
        self.instrument.write("*RST")

    def run(self):
        """Runs the oscillscope"""
        self.instrument.write(":run")

    def stop(self):
        """Stops the oscillscope"""
        self.instrument.write(":stop")

    def get_channel_list(self):
        x =0

    def check_status(self):
        return True
    


    def connect(self):
        x = 0
    def set_frequency(self, frequency, channel = 1):
        x = 0
    
    
    def set_channel(self, channelNumber = 1):
        x = 0

    #Trigger commands
    def get_trigger_mode(self):
       """Get current trigger mode"""
       self.instrument.query(":trigger:sweep?")

    def set_trigger_mode(self,mode):
       """Set trigger mode - auto, normal, single"""
       comm_mode = ":trigger:sweep "+mode
       self.instrument.write(comm_mode)
    
    def force_trigger(self):
        """Generates forced trigger signal. Only for Normal and Single trigger modes."""
        self.instrument.write(":tforce")

    
    #Acquisition Commands
    def set_acquistion_mode(self, mode):
        """Set acquisition mode. Normal:  Samples the signal at equal time interval to
rebuild the waveform. Averages:  Averages the waveforms from multiple
samples to reduce the random noise of the input signal. Peak: Acquires the maximum and
minimum values of the signal within the sample interval to get the envelope of the
signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise
on the input signal and generate much smoother waveforms """
        comm_mode = ":ACQuire:TYPE "+mode
        self.instrument.write(comm_mode)

    def get_acquistion_mode(self, mode):
        """Get acquisition mode. Normal:  Samples the signal at equal time interval to
rebuild the waveform. Averages:  Averages the waveforms from multiple
samples to reduce the random noise of the input signal. Peak: Acquires the maximum and
minimum values of the signal within the sample interval to get the envelope of the
signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise
on the input signal and generate much smoother waveforms """
        comm_mode = ":ACQuire:TYPE?"
        self.instrument.query(comm_mode)

    
#Calibrate Commands
    def calibrate(self):
        """The oscilloscope starts to execute self-calibration."""
        self.instrument.write(":CALibrate:STARt")
    
    def stop_calibrate(self):
        """Exit the self-calibration at any time."""
        self.instrument.write(":CALibrate:QUIT")

#    #Display Commands
    def clear_screen(self):
        """Clears display screen"""
        self.instrument.write(":display:clear")
    
    def autoscale(self):
        """Display adjusts to fit the waveform on the screen"""
        self.instrument.write(":autoscale")

    def set_channel_display(self, channel, display):
        """Enable or disable the specified channel or query the status of the specified channel."""
#TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["ON","OFF",1, 2]
        if channel in allowed_chnl_values or display in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":DISPlay "+display
            self.instrument.write(comm)
        else:
            print("Invalid channel or mode")

    def get_channel_display(self, channel):
        """Check the specified channel or query the status of the specified channel."""
        comm_mode = ":CHANnel"+channel+":Display?"
        self.instrument.query(comm_mode)

    #Time base
    def set_timebase_scale(self, scale):
        """Set main timebase scale (in seconds/div)."""
        self.instrument.write(f":TIMebase:MAIN:SCALe {scale}")

    def get_timebase_scale(self):
        """Query the main timebase scale."""
        return self.instrument.query(":TIMebase:MAIN:SCALe?")

    def set_timebase_mode(self, mode):
        """Set timebase mode: MAIN, XY, ROLL."""
        self.instrument.write(f":TIMebase:MODE {mode}")

    def get_timebase_mode(self):
        """Query current timebase mode."""
        return self.instrument.query(":TIMebase:MODE?")
    def set_ouput_path(self, path):
        """Output Commands"""
        self.saved_output_path = path