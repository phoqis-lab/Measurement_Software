import Instruments.instrument as instrument

from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
from time import sleep
from time import sleep
import pyvisa

from Instruments.SCPICommandTree import calculate
from Instruments.SCPICommandTree import calibration
from Instruments.SCPICommandTree import control
from Instruments.SCPICommandTree import data
from Instruments.SCPICommandTree import display
from Instruments.SCPICommandTree import format
from Instruments.SCPICommandTree import hcopy
from Instruments.SCPICommandTree import input
from Instruments.SCPICommandTree import instrumentcommands
from Instruments.SCPICommandTree import measure
from Instruments.SCPICommandTree import memory
from Instruments.SCPICommandTree import mmemory
from Instruments.SCPICommandTree import output
from Instruments.SCPICommandTree import program
from Instruments.SCPICommandTree import route
from Instruments.SCPICommandTree import sense
from Instruments.SCPICommandTree import source
from Instruments.SCPICommandTree import status
from Instruments.SCPICommandTree import system
from Instruments.SCPICommandTree import trace
from Instruments.SCPICommandTree import trigger
from Instruments.SCPICommandTree import unit
from Instruments.SCPICommandTree import vxi


class Instrument(calculate.Calculate, calibration.Calibration, control.Control, data.Data, display.Display,
                  format.Format, hcopy.HCopy, instrumentcommands.InstrumentCommands,  memory.Memory,
                  mmemory.Mmemory, output.Output, route.Route, sense.Sense, source.Source, status.Status,
                  system.System, trace.Trace, trigger.Trigger, unit.Unit, vxi.VXI): 

    def __init__(self, name, instrument):
        self.name = name
        self.instrument = instrument
        self.saved_output_path = ""

    #Mandatory Commands
    