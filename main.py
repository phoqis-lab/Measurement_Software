from instrument import Instrument
from RigolOscilloscope import RigolOscilloscope
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
import pyvisa
inst = Instrument("Test")
with Rigol_DS1000Z() as oscope:
        # reset to defaults and print the IEEE 488.2 instrument identifier
        ieee = oscope.ieee(rst=True)
        print(ieee.idn)
#ro = RigolOscilloscope("Test")