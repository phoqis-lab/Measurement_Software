"""READ ME: All experiments must start with a few sentence readme giving a summation of what the experiment is."""
from Instruments.helper import Helper
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.oscilloscope_helper import OscilloscopeHelper
from Instruments.spectrum_analyzer_signal_hound import SignalHound
from Instruments.spectrum_analyzer_helper import SignalHoundHelper
from EInstrument import EInstrument
def __main__():
    helper = Helper()
    instruments = helper.connect_instruments()
    inst_dict = {}
    #Insert your instrument calls here
    for i in instruments:
        i.enable_auto_saving_data()
        inst_dict[i.name] = i
    
    inst_dict[EInstrument.OSCILLOSCOPE].set_acquistion_mode("normal")
    inst_dict[EInstrument.OSCILLOSCOPE].set_trigger_sweep_mode("auto")
    #....
    
    helper.disconnect(instruments)