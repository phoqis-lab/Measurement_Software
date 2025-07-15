from Instruments.SCPICommandTree import mandatory
import pyvisa

class Instrument(mandatory.Mandatory):

    def __init__(self, instrument):
        
        self.name = "Insert_instrument_name_here"
        self.instrument = instrument
    
    #TODO: Add SCPI functions below
