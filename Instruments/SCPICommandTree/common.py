class Mandatory():
    def __init__(self, instrument):
        self.instrument = instrument
    def save(self):
        """
        Save the current state of the instrument to non-volatile memory.
        This command is typically used to save settings that will persist across power cycles.
        """
        self.instrument.write("*SAV")
    