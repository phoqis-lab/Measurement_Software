import instrument
from ds1054z import DS1054Z
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
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
