from Instruments.instrument import Instrument
from Instruments.RigolOscilloscope import RigolOscilloscope
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
import pyvisa
inst = Instrument("Test")
rm = pyvisa.ResourceManager()
insturment_list = [] #types the name of the instruments you want to query 
print(rm.list_resources())

#Add auto connection
r = rm.open_resource('USB0::0x1AB1::0x0517::DS1ZE264M00036::INSTR')
ro = RigolOscilloscope(r)
print(ro.clear())
print(ro.get_system_beeper_enable())
ro.set_system_beeper_enable(0)
print(ro.get_system_beeper_enable())
ro.__data_copy("test", "test")



