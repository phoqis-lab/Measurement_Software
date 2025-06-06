import instrumentOLD
from ds1054z import DS1054Z
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
from time import sleep
from time import sleep
import pyvisa
class RigolOscilloscope(instrumentOLD.Instrument):
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
    