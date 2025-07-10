import Instruments.instrument as instrument

from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
from rigol_ds1000z import process_display, process_waveform
from time import sleep
from time import sleep
import pyvisa

from SCPICommandTree import calculate
from SCPICommandTree import calibration
from SCPICommandTree import control
from SCPICommandTree import data
from SCPICommandTree import display
from SCPICommandTree import format
from SCPICommandTree import hcopy
from SCPICommandTree import input
from SCPICommandTree import instrumentcommands
from SCPICommandTree import measure
from SCPICommandTree import memory
from SCPICommandTree import mmemory
from SCPICommandTree import output
from SCPICommandTree import program
from SCPICommandTree import route
from SCPICommandTree import sense
from SCPICommandTree import source
from SCPICommandTree import status
from SCPICommandTree import system
from SCPICommandTree import trace
from SCPICommandTree import trigger
from SCPICommandTree import unit
from SCPICommandTree import vxi


class Instrument(calculate.Calculate, calibration.Calibration, control.Control, data.Data, display.Display,
                  format.Format, hcopy.HCopy, instrumentcommands.InstrumentCommands,  memory.Memory,
                  mmemory.Mmemory, output.Output, route.Route, sense.Sense, source.Source, status.Status,
                  system.System, trace.Trace, trigger.Trigger, unit.Unit, vxi.VXI): 

    def __init__(self, name, instrument):
        self.name = name
        self.instrument = instrument
        self.saved_output_path = ""

    #Mandatory Commands
    def clear_event_registers(self):
        """
        Clear all the event registers and clear the error queue (*CLS).
        """
        self.instrument.write("*CLS")
    
    def set_enable_event_status(self, value):
        """
        Set the enable register for the standard event status register set (*ESE).

        Parameters:
        value (int): An integer value where bit 1 and bit 6 are not used (always 0).
                     The range corresponds to binary numbers X0XXXX0X.
        """
        # Basic validation for the value based on the description
        if isinstance(value, int) and 0 <= value <= 255: # Max 255 for an 8-bit register
            # Further validation for bits 1 and 6 being 0 could be added:
            # if (value & 0b01000010) == 0: # Check if bit 1 (0b00000010) or bit 6 (0b01000000) are set
            self.instrument.write(f"*ESE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 1 and 6 effectively 0).")
    
    def get_standard_event_status_enable(self):
        """
        Query the enable register for the standard event status register set (*ESE?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have
             already been set in the register.
        """
        response = self.instrument.query("*ESE?")
        return int(response.strip())
    
    def get_and_clear_standard_event_status_register(self):
        """
        Query and clear the event register for the standard event status register (*ESR?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
             The value of the register is set to 0 after this command is executed.
        """
        response = self.instrument.query("*ESR?")
        return int(response.strip())
    
    def get_id(self):
        """
        Query the ID string of the instrument (*IDN?).

        Returns:
        str: The ID string in the format "RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>".
        """
        response = self.instrument.query("*IDN?")
        return response.strip()
    
    def set_operation_complete(self):
        """
        Set the Operation Complete bit (bit 0) in the standard event status register to 1
        after the current operation is finished (*OPC).
        """
        self.instrument.write("*OPC")

    def is_operation_complete(self):
        """
        Query whether the current operation is finished (*OPC?).

        Returns:
        bool: True (1) if the current operation is finished; False (0) otherwise.
        """
        response = self.instrument.query("*OPC?")
        return bool(int(response.strip()))


    def reset_instrument(self):
            """
            Restore the instrument to the default state (*RST).
            """
            self.instrument.write("*RST")

    def set_enable_service_request(self, value):
        """
        Set the enable register for the status byte register set (*SRE).

        Parameters:
        value (int): An integer value from 0 to 255. Bit 0 and bit 1 of the status byte register
                     are not used and are always treated as 0.
        """
        # Basic validation for the value
        if isinstance(value, int) and 0 <= value <= 255:
            # Further validation for bits 0 and 1 being 0 could be added:
            # if (value & 0b00000011) == 0: # Check if bit 0 (0b00000001) or bit 1 (0b00000010) are set
            self.instrument.write(f"*SRE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 0 and 1 effectively 0).")

    def get_enable_service_request(self):
        """
        Query the enable register for the status byte register set (*SRE?).

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have
             already been set in the register.
        """
        response = self.instrument.query("*SRE?")
        return int(response.strip())
    
    def read_status_byte(self):
        """
        Query the event register for the status byte register (*STB?).
        The value of the status byte register is set to 0 after this command is executed.

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
        """
        response = self.instrument.query("*STB?")
        return int(response.strip())

    def self_test(self):
        """
        Perform a self-test and then return the self-test results (*TST?).

        Returns:
        int: A decimal integer representing the self-test results.
        """
        response = self.instrument.query("*TST?")
        return int(response.strip())

    def add_wait_for_operation_finish(self):
        """
        Wait for the current operation to finish (*WAI).
        The subsequent command can only be carried out after the current command has been executed.
        """
        self.instrument.write("*WAI")