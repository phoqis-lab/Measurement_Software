import instrument
from ds1054z import DS1054Z
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from time import sleep

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
        x = 0