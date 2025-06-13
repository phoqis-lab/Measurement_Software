import instrument
from time import sleep
from time import sleep
import pyvisa
class SpectrumAnalyzer(instrument.Instrument):
    x = 0 

    #DS
    """ def __init__():
        #DA1054z library
        #Would need to check IP address of scope
        instrument = DS1054Z('192.168.0.23')
        print("Connected to: ", instrument.idn)

        print("Currently displayed channels: ", str(instrument.displayed_channels))"""
    #TODO: Check all SCPI commands work with this library, if not switch to standard pyvisa
    def __init__():
        
    