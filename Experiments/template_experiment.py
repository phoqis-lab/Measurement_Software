"""READ ME: All experiments must start with a few sentence readme giving a summation of what the experiment is."""
from Instruments.helper import Helper
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.oscilloscope_helper import OscilloscopeHelper
from Instruments.spectrum_analyzer_signal_hound import SignalHound
from Instruments.spectrum_analyzer_helper import SignalHoundHelper

def __main__():
    helper = Helper()
    instruments = helper.connect_instruments()
    #Insert your instrument calls here
    