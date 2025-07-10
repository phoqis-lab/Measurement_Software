import re

class Trigger:
    """
    
    """
    def __init__(self,instrument):
        """
        Initializes the InstrumentControl with an instrument connection.
        :param instrument_connection: An object capable of sending/receiving
                                      SCPI commands (e.g., pyvisa resource).
        """
        self.instrument = instrument

    
    def abort(self):
        """
        Resets the trigger system and places all trigger sequences in the IDLE state.
        Any actions related to the trigger system that are in progress shall also be aborted.
        This command is an event and has no associated *RST condition or query form.
        """
        self.instrument.write(":ABORt")

    """def arm(self):
        
        #Initializes the ARM subsystem.
        #This command is an event and has no query form.
        
        self.instrument.write(":ARM")"""

    """def initiate(self):
        
        Initiates all trigger sequences as a group, except those defined otherwise.
        This command is an event and has no query form.
        
        self.instrument.write("INITiate")"""

    """def trigger(self):
        
        Purpose of the TRIGger subsystem is to qualify a single event before enabling
        the triggered sequence operation, such as enabling a sweep, starting a measurement,
        or changing the state of the device.
        This command is an event and has no query form.
        
        self.instrument.write("TRIGger")"""

    
    def set_arm_sequence_define(self, sequence_name: str, sequence_number: int = None):
        """
        Sets the SEQuence alias for a particular sequence in the trigger system.
        This command is an alias to TRIGger:SEQuence:DEFine.
        :param sequence_name: The character data string for the sequence alias.
        :param sequence_number: Optional. The numeric suffix (sequence number) to apply the alias to.
        Notes: Overwrites previously defined name. *RST has no effect on the defined name.
        """
        if sequence_number is not None:
            self.instrument.write(f":ARM:SEQ{sequence_number}:DEF '{sequence_name}'")
        else:
            self.instrument.write(f":ARM:SEQ:DEF '{sequence_name}'")

    def get_arm_sequence_define(self, sequence_number: int = None) -> str:
        """
        Queries the SEQuence alias for a particular sequence.
        :param sequence_number: Optional. The numeric suffix (sequence number) to query.
        :return: The character data string of the sequence alias, or a null string if nothing is defined.
        """
        if sequence_number is not None:
            response = self.instrument.query(f":ARM:SEQ{sequence_number}:DEF?").strip()
        else:
            response = self.instrument.query(":ARM:SEQ:DEF?").strip()
        return response.strip("'") # Remove quotes if present

    def set_arm_sequence_define_mgrules(self, enable: bool, sequence_number: int = None):
        """
        Sets the state of MGRules (Mnemonic Generation Rules) for sequence aliases.
        :param enable: True to enable MGRules, False to disable.
        :param sequence_number: Optional. The numeric suffix (sequence number) for which to set MGRules.
        Notes: At *RST, the value is OFF.
        """
        scpi_value = "1" if enable else "0"
        if sequence_number is not None:
            self.instrument.write(f":ARM:SEQ{sequence_number}:DEF:MGR {scpi_value}")
        else:
            self.instrument.write(f":ARM:SEQ:DEF:MGR {scpi_value}")

    def get_arm_sequence_define_mgrules(self, sequence_number: int = None) -> bool:
        """
        Queries the state of MGRules (Mnemonic Generation Rules) for sequence aliases.
        :param sequence_number: Optional. The numeric suffix (sequence number) to query.
        :return: True if MGRules is enabled, False if disabled.
        """
        if sequence_number is not None:
            response = self.instrument.query(f":ARM:SEQ{sequence_number}:DEF:MGR?").strip()
        else:
            response = self.instrument.query(":ARM:SEQ:DEF:MGR?").strip()
        return response == "1"

    
    def set_arm_sequence_layer_count(self, value: int, sequence_number: int = None, layer_number: int = None):
        """
        Controls the path of the trigger system in the upward traverse of the event detection layer.
        :param value: The count value (numeric value, 1 or greater).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is set to 1.
        """
        if value < 1:
            raise ValueError("COUNt must be 1 or greater.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:COUN {value}")

    def get_arm_sequence_layer_count(self, sequence_number: int = None, layer_number: int = None) -> int:
        """
        Queries the count for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The count value.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM sequence layer COUNt (not integer): '{response}'")

    def set_arm_sequence_layer_coupling(self, coupling_type: str, sequence_number: int = None, layer_number: int = None):
        """
        Selects AC or DC coupling for the SOURced signal. Only has effect if the source
        for the event detector is an analog electrical signal (e.g., INTernal, LINE, EXTernal).
        :param coupling_type: "AC", "DC", "LFReject" and  "HFReject".
        TODO: Define LFReject and HFRd
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        valid_types = {"AC", "DC", "LFR", "HFR", "LFReject", "HFReject"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC' or 'DC'.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:COUP {type_upper}")

    def get_arm_sequence_layer_coupling(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the coupling type for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The coupling type ("AC" or "DC").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:COUP?").strip().upper()
        return response

    def set_arm_sequence_layer_delay(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Sets the time duration between the recognition of an event(s) and the downward exit of the specified layer.
        :param value: The delay time in seconds (numeric value, zero or positive).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is set to 0 or the smallest available positive value.
        """
        if value < 0:
            raise ValueError("DELay must be zero or a positive value.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:DEL {value}")

    def get_arm_sequence_layer_delay(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the delay time for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The delay time in seconds.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:DEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM sequence layer DELay (not numeric): '{response}'")

    def set_arm_sequence_layer_delay_auto(self, auto_state: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets auto-delay for sensor devices with internal settling delays.
        :param auto_state: "ON" (enables auto-delay), "OFF" (disables), or "ONCE" (adjusts once then OFF).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, AUTO is set ON.
        """
        normalized_state = auto_state.upper()
        if normalized_state not in {"ON", "OFF", "ONCE"}:
            raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:DEL:AUTO {normalized_state}")

    def get_arm_sequence_layer_delay_auto(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the auto-delay state for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The auto-delay state ("ON", "OFF", or "ONCE").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:DEL:AUTO?").strip().upper()
        # Convert 1/0 to ON/OFF for consistency with setter
        if response == "1": return "ON"
        if response == "0": return "OFF"
        return response

    
    def arm_sequence_layer_ecl(self, sequence_number: int = None, layer_number: int = None):
        """
        Presets LEVel, HYSTeresis, COUPling, and DELay to values appropriate for an ECL signal.
        This command is an event and cannot be queried.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:ECL")

    def set_arm_sequence_layer_ecount(self, value: int, sequence_number: int = None, layer_number: int = None):
        """
        Specifies a particular number of occurrences of the same event that must be recognized.
        :param value: The event count (numeric value, 1 or greater).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is set to 1.
        """
        if value < 1:
            raise ValueError("ECOunt must be 1 or greater.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:ECO {value}")

    def get_arm_sequence_layer_ecount(self, sequence_number: int = None, layer_number: int = None) -> int:
        """
        Queries the event count for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The event count.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:ECO?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM sequence layer ECOunt (not integer): '{response}'")

    def set_arm_sequence_layer_filter_hpass_frequency(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Determines the cutoff frequency of the high pass filter.
        :param value: The frequency in Hertz (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:FILT:HPAS:FREQ {value}")

    def get_arm_sequence_layer_filter_hpass_frequency(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the cutoff frequency of the high pass filter for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The frequency in Hertz.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:FILT:HPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM filter HPASS FREQuency (not numeric): '{response}'")

    def set_arm_sequence_layer_filter_hpass_state(self, enable: bool, sequence_number: int = None, layer_number: int = None):
        """
        Turns the high pass filter ON or OFF.
        :param enable: True to turn ON, False to turn OFF.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        scpi_value = "1" if enable else "0"
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:FILT:HPAS:STATE {scpi_value}")

    def get_arm_sequence_layer_filter_hpass_state(self, sequence_number: int = None, layer_number: int = None) -> bool:
        """
        Queries the state of the high pass filter for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: True if ON, False if OFF.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:FILT:HPAS:STATE?").strip()
        return response == "1"

    def set_arm_sequence_layer_filter_lpass_frequency(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Determines the cutoff frequency of the low pass filter.
        :param value: The frequency in Hertz (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:FILT:LPAS:FREQ {value}")

    def get_arm_sequence_layer_filter_lpass_frequency(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the cutoff frequency of the low pass filter for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The frequency in Hertz.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:FILT:LPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM filter LPASS FREQuency (not numeric): '{response}'")

    def set_arm_sequence_layer_filter_lpass_state(self, enable: bool, sequence_number: int = None, layer_number: int = None):
        """
        Turns the low pass filter ON or OFF.
        :param enable: True to turn ON, False to turn OFF.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        scpi_value = "1" if enable else "0"
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:FILT:LPAS:STATE {scpi_value}")

    def get_arm_sequence_layer_filter_lpass_state(self, sequence_number: int = None, layer_number: int = None) -> bool:
        """
        Queries the state of the low pass filter for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: True if ON, False if OFF.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:FILT:LPAS:STATE?").strip()
        return response == "1"

    
    def set_arm_sequence_layer_hysteresis(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Sets how far a signal must fall below LEVel before a rising edge can again be detected,
        and how far a signal must rise above LEVel before a falling edge can again be detected.
        Units default to current amplitude units.
        :param value: The hysteresis value (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:HYST {value}")

    def get_arm_sequence_layer_hysteresis(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the hysteresis value for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The hysteresis value.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:HYST?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM hysteresis (not numeric): '{response}'")

    def arm_sequence_layer_immediate(self, sequence_number: int = None, layer_number: int = None):
        """
        Provides a one-time override of the normal process of the downward traverse of the event detection layer.
        Causes immediate exit of the specified event detection layer if the trigger system is in that layer.
        This command is an event and has no *RST condition and cannot be queried.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:IMM")

    def set_arm_sequence_layer_level(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Qualifies the characteristic of the selected SOURce signal that generates an event.
        Only has effect if the source is an analog electrical signal (e.g., INTernal, LINE, EXTernal).
        Units default to current amplitude unit.
        :param value: The level value (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is instrument-dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:LEV {value}")

    def get_arm_sequence_layer_level(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the level value for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The level value.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM level (not numeric): '{response}'")

    def set_arm_sequence_layer_level_auto(self, auto_state: str, sequence_number: int = None, layer_number: int = None):
        """
        Dynamically selects the best arm level based on a device-dependent algorithm.
        :param auto_state: "ON" (enables auto-level), "OFF" (disables), or "ONCE" (adjusts once then OFF).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: Setting the arm LEVel turns AUTO OFF. At *RST, the value of this parameter is OFF.
        """
        normalized_state = auto_state.upper()
        if normalized_state not in {"ON", "OFF", "ONCE"}:
            raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:LEV:AUTO {normalized_state}")

    def get_arm_sequence_layer_level_auto(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the auto-level state for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The auto-level state ("ON", "OFF", or "ONCE").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:LEV:AUTO?").strip().upper()
        # Convert 1/0 to ON/OFF for consistency with setter
        if response == "1": return "ON"
        if response == "0": return "OFF"
        return response

    
    def set_arm_sequence_layer_link(self, event_handle: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets the internal event that is LINKed to the event detector in the ARM layer.
        :param event_handle: STRING PROGRAM DATA for the event (e.g., "ARM[:SEQuence[:LAYer]]" or "TRIGger[:SEQuence]").
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:LINK '{event_handle}'")

    def get_arm_sequence_layer_link(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the internal event that is LINKed to the event detector in the ARM layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The event handle string.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:LINK?").strip().strip("'")
        return response

    def set_arm_sequence_layer_protocol_vxi(self, protocol_type: str, sequence_number: int = None, layer_number: int = None):
        """
        Selects the trigger protocol for the VXI TTLTrg or ECLTrg trigger line when used as the arm source.
        :param protocol_type: "SYNChronous", "SSYNchronous", or "ASYNchronous".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the SYNChronous protocol is selected.
        """
        valid_types = {"SYN", "SYNCHRONOUS", "SSYN", "SSYNCHRONOUS", "ASYN", "ASYNCHRONOUS"}
        type_upper = protocol_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid protocol_type: '{protocol_type}'. Must be 'SYNChronous', 'SSYNchronous', or 'ASYNchronous'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if type_upper.startswith("SYN"): scpi_type = "SYN"
        elif type_upper.startswith("SSYN"): scpi_type = "SSYN"
        elif type_upper.startswith("ASYN"): scpi_type = "ASYN"
        else: scpi_type = type_upper

        self.instrument.write(f"{path}:PROT:VXI {scpi_type}")

    def get_arm_sequence_layer_protocol_vxi(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the trigger protocol for the VXI TTLTrg or ECLTrg trigger line when used as the arm source.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The protocol type ("SYNChronous", "SSYNchronous", or "ASYNchronous").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:PROT:VXI?").strip().upper()
        if response.startswith("SYN") and not response.startswith("SSYN"): return "SYNChronous"
        if response.startswith("SSYN"): return "SSYNchronous"
        if response.startswith("ASYN"): return "ASYNchronous"
        return response

    def arm_sequence_layer_signal(self, sequence_number: int = None, layer_number: int = None):
        """
        Provides a one-time override of the normal process of the downward traverse through the event detector.
        Causes immediate exit of the event detector block if the trigger system is waiting for the event.
        This command defines an event and has no associated query form or *RST condition.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:SIGN")

    
    def set_arm_sequence_layer_slope(self, slope_type: str, sequence_number: int = None, layer_number: int = None):
        """
        Qualifies whether the event occurs on the rising edge, falling edge, or either edge of the signal.
        :param slope_type: "POSitive", "NEGative", or "EITHer".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is set to POS.
        """
        valid_types = {"POS", "POSITIVE", "NEG", "NEGATIVE", "EITH", "EITHER"}
        type_upper = slope_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid slope_type: '{slope_type}'. Must be 'POSitive', 'NEGative', or 'EITHer'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if type_upper.startswith("POS"): scpi_type = "POS"
        elif type_upper.startswith("NEG"): scpi_type = "NEG"
        elif type_upper.startswith("EITH"): scpi_type = "EITH"
        else: scpi_type = type_upper

        self.instrument.write(f"{path}:SLOP {scpi_type}")

    def get_arm_sequence_layer_slope(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the slope type for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The slope type ("POSitive", "NEGative", or "EITHer").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:SLOP?").strip().upper()
        if response.startswith("POS"): return "POSitive"
        if response.startswith("NEG"): return "NEGative"
        if response.startswith("EITH"): return "EITHer"
        return response

    def set_arm_sequence_layer_source(self, source_type: str, source_index: int = None, sequence_number: int = None, layer_number: int = None):
        """
        Selects the source for the event detector. Only one source may be specified at a time.
        :param source_type: The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                            "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
        :param source_index: Optional. Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, IMMediate shall be selected as the SOURce.
        """
        valid_types = {
            "AINT", "AINTERNAL", "BUS", "ECLTRG", "EXT", "EXTERNAL", "HOLD",
            "IMM", "IMMEDIATE", "INT", "INTERNAL", "LINE", "LINK", "MAN", "MANUAL",
            "OUTP", "OUTPUT", "TIM", "TIMER", "TTLTRG"
        }
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid source_type: '{source_type}'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        scpi_source = ""
        if type_upper.startswith("AINT"): scpi_source = "AINT"
        elif type_upper.startswith("BUS"): scpi_source = "BUS"
        elif type_upper.startswith("ECLTRG"): scpi_source = "ECLTrg"
        elif type_upper.startswith("EXT"): scpi_source = "EXT"
        elif type_upper.startswith("HOLD"): scpi_source = "HOLD"
        elif type_upper.startswith("IMM"): scpi_source = "IMM"
        elif type_upper.startswith("INT") and not type_upper.startswith("AINT"): scpi_source = "INT"
        elif type_upper.startswith("LINE"): scpi_source = "LINE"
        elif type_upper.startswith("LINK"): scpi_source = "LINK"
        elif type_upper.startswith("MAN"): scpi_source = "MAN"
        elif type_upper.startswith("OUTP"): scpi_source = "OUTP"
        elif type_upper.startswith("TIM"): scpi_source = "TIM"
        elif type_upper.startswith("TTLTRG"): scpi_source = "TTLTrg"
        else: scpi_source = type_upper # Fallback for exact match

        if source_index is not None:
            self.instrument.write(f"{path}:SOUR {scpi_source}{source_index}")
        else:
            self.instrument.write(f"{path}:SOUR {scpi_source}")

    def get_arm_sequence_layer_source(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the source for the event detector for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The source type string (e.g., "IMMediate", "TTLTrg0").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:SOUR?").strip().upper()
        # Attempt to map short form back to common long forms or keep as-is
        if response.startswith("AINT"): return "AINTernal"
        if response.startswith("ECLTRG"): return response # Return as is with index
        if response.startswith("EXT"): return response # Return as is with index
        if response.startswith("IMM"): return "IMMediate"
        if response.startswith("INT"): return response # Return as is with index
        if response.startswith("MAN"): return "MANual"
        if response.startswith("OUTP"): return response # Return as is with index
        if response.startswith("TIM"): return "TIMer"
        if response.startswith("TTLTRG"): return response # Return as is with index
        return response # Default to returning the exact response

    
    def set_arm_sequence_layer_timer(self, value: float, sequence_number: int = None, layer_number: int = None):
        """
        Sets the period of an internal periodic signal source.
        :param value: The timer period in seconds (numeric value, positive).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device-dependent.
        """
        if value <= 0:
            raise ValueError("TIMer value must be positive.")
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:TIM {value}")

    def get_arm_sequence_layer_timer(self, sequence_number: int = None, layer_number: int = None) -> float:
        """
        Queries the period of an internal periodic signal source for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The timer period in seconds.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:TIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM timer (not numeric): '{response}'")

    def arm_sequence_layer_ttl(self, sequence_number: int = None, layer_number: int = None):
        """
        Presets LEVel, HYSTeresis, COUPling, and DELay to values appropriate for a TTL signal.
        This command is an event and cannot be queried.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:TTL")

    def set_arm_sequence_layer_type(self, type_value: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets the type of triggering.
        :param type_value: "EDGE" or "VIDeo".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is EDGE.
        """
        valid_types = {"EDGE", "VID", "VIDEO"}
        type_upper = type_value.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid type_value: '{type_value}'. Must be 'EDGE' or 'VIDeo'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if type_upper.startswith("VID"): scpi_type = "VID"
        else: scpi_type = type_upper

        self.instrument.write(f"{path}:TYPE {scpi_type}")

    def get_arm_sequence_layer_type(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the type of triggering for the ARM sequence layer.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The type of triggering ("EDGE" or "VIDeo").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:TYPE?").strip().upper()
        if response.startswith("VID"): return "VIDeo"
        return response

    
    def set_arm_sequence_layer_video_field_number(self, value: int, sequence_number: int = None, layer_number: int = None):
        """
        Sets the field number to trigger on if FIELD:SELect is set to NUMBer.
        :param value: The field number (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is 1. Setting has no effect on SELect parameter.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:VID:FIELD:NUMB {value}")

    def get_arm_sequence_layer_video_field_number(self, sequence_number: int = None, layer_number: int = None) -> int:
        """
        Queries the field number to trigger on for the ARM video field.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The field number.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:FIELD:NUMB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM video FIELD NUMBer (not integer): '{response}'")

    def set_arm_sequence_layer_video_field_select(self, select_mode: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets the video field selection method to be used.
        :param select_mode: "ODD", "EVEN", "ALL", or "NUMBer".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is ALL.
        """
        valid_modes = {"ODD", "EVEN", "ALL", "NUMB", "NUMBER"}
        mode_upper = select_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid select_mode: '{select_mode}'. Must be 'ODD', 'EVEN', 'ALL', or 'NUMBer'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if mode_upper.startswith("NUMB"): scpi_mode = "NUMB"
        else: scpi_mode = mode_upper

        self.instrument.write(f"{path}:VID:FIELD:SEL {scpi_mode}")

    def get_arm_sequence_layer_video_field_select(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the video field selection method for the ARM video field.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The video field selection method ("ODD", "EVEN", "ALL", or "NUMBer").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:FIELD:SEL?").strip().upper()
        if response.startswith("NUMB"): return "NUMBer"
        return response

    
    def set_arm_sequence_layer_video_format_lpframe(self, value: int, sequence_number: int = None, layer_number: int = None):
        """
        Sets the lines per frame associated with the signal formatting standard being used.
        :param value: Lines Per Frame (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, this value is device dependent.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:VID:FORM:LPFR {value}")

    def get_arm_sequence_layer_video_format_lpframe(self, sequence_number: int = None, layer_number: int = None) -> int:
        """
        Queries the lines per frame for the ARM video format.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: Lines Per Frame.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:FORM:LPFR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM video FORMat LPFRame (not integer): '{response}'")
    

    def set_arm_sequence_layer_video_line_number(self, value: int, sequence_number: int = None, layer_number: int = None):
        """
        Sets the line number to arm on if LINE:SELect is set to NUMBer.
        :param value: The line number (numeric value).
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is device dependent. Setting has no effect on SELect parameter.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        self.instrument.write(f"{path}:VID:LINE:NUMB {value}")

    def get_arm_sequence_layer_video_line_number(self, sequence_number: int = None, layer_number: int = None) -> int:
        """
        Queries the line number to arm on for the ARM video line.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The line number.
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:LINE:NUMB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for ARM video LINE NUMBer (not integer): '{response}'")

    def set_arm_sequence_layer_video_line_select(self, select_mode: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets the video line selection method to be used.
        :param select_mode: "ALL" or "NUMBer".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is ALL.
        """
        valid_modes = {"ALL", "NUMB", "NUMBER"}
        mode_upper = select_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid select_mode: '{select_mode}'. Must be 'ALL' or 'NUMBer'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if mode_upper.startswith("NUMB"): scpi_mode = "NUMB"
        else: scpi_mode = mode_upper

        self.instrument.write(f"{path}:VID:LINE:SEL {scpi_mode}")

    def get_arm_sequence_layer_video_line_select(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries the video line selection method for the ARM video line.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The video line selection method ("ALL" or "NUMBer").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:LINE:SEL?").strip().upper()
        if response.startswith("NUMB"): return "NUMBer"
        return response

    
    def set_arm_sequence_layer_video_ssignal_polarity(self, polarity_type: str, sequence_number: int = None, layer_number: int = None):
        """
        Sets sync pulse triggering polarity.
        :param polarity_type: "POSitive" or "NEGative".
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        Notes: At *RST, the value of this parameter is NEGative.
        """
        valid_types = {"POS", "POSITIVE", "NEG", "NEGATIVE"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity_type: '{polarity_type}'. Must be 'POSitive' or 'NEGative'.")

        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"

        if type_upper.startswith("POS"): scpi_type = "POS"
        elif type_upper.startswith("NEG"): scpi_type = "NEG"
        else: scpi_type = type_upper

        self.instrument.write(f"{path}:VID:SSIG:POL {scpi_type}")

    def get_arm_sequence_layer_video_ssignal_polarity(self, sequence_number: int = None, layer_number: int = None) -> str:
        """
        Queries sync pulse triggering polarity for the ARM video synchronizing signal.
        :param sequence_number: Optional. The numeric suffix for SEQuence.
        :param layer_number: Optional. The numeric suffix for LAYer.
        :return: The polarity type ("POSitive" or "NEGative").
        """
        path = ":ARM"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if layer_number is not None:
            path += f":LAY{layer_number}"
        response = self.instrument.query(f"{path}:VID:SSIG:POL?").strip().upper()
        if response.startswith("POS"): return "POSitive"
        if response.startswith("NEG"): return "NEGative"
        return response

    
    def set_initiate_continuous(self, enable: bool):
        """
        Selects whether the trigger system is continuously initiated or not.
        :param enable: True for continuous initiation, False to remain in IDLE until IMMediate.
        Notes: At *RST, this value is set to OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"INIT:CONT {scpi_value}")

    def get_initiate_continuous(self) -> bool:
        """
        Queries whether the trigger system is continuously initiated.
        :return: True if continuous initiation, False otherwise.
        """
        response = self.instrument.query("INIT:CONT?").strip()
        return response == "1"

    def set_initiate_continuous_all(self, enable: bool):
        """
        Sets whether or not all sequences are continuously initiated.
        :param enable: True to continuously initiate all sequences, False otherwise.
        Notes: At *RST, this value is set to OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"INIT:CONT:ALL {scpi_value}")

    def get_initiate_continuous_all(self) -> bool:
        """
        Queries whether or not all sequences are continuously initiated.
        :return: True if all sequences are continuously initiated, False otherwise.
        """
        response = self.instrument.query("INIT:CONT:ALL?").strip()
        return response == "1"

    
    def set_initiate_continuous_name(self, sequence_name: str, enable: bool):
        """
        Sets whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
        :param sequence_name: The character program data for the sequence alias.
        :param enable: True for continuous initiation, False otherwise.
        Notes: At *RST, this value is set to OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"INIT:CONT:NAME '{sequence_name}',{scpi_value}")

    def get_initiate_continuous_name(self, sequence_name: str) -> bool:
        """
        Queries whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
        :param sequence_name: The character program data for the sequence alias.
        :return: True if continuously initiated, False otherwise.
        """
        response = self.instrument.query(f"INIT:CONT:NAME? '{sequence_name}'").strip()
        return response == "1"

    def set_initiate_continuous_sequence(self, sequence_number: int, enable: bool):
        """
        Sets whether or not the specified SEQuence is continuously initiated.
        :param sequence_number: The numeric suffix on SEQuence corresponds to the sequence number.
        :param enable: True for continuous initiation, False otherwise.
        Notes: If NAME is implemented, this command shall also be implemented. At *RST, this value is set to OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"INIT:CONT:SEQ{sequence_number} {scpi_value}")

    def get_initiate_continuous_sequence(self, sequence_number: int) -> bool:
        """
        Queries whether or not the specified SEQuence is continuously initiated.
        :param sequence_number: The numeric suffix on SEQuence corresponds to the sequence number.
        :return: True if continuously initiated, False otherwise.
        """
        response = self.instrument.query(f"INIT:CONT:SEQ{sequence_number}?").strip()
        return response == "1"

    def initiate_immediate(self):
        """
        Causes all sequences to exit the IDLE state; they are initiated.
        The IMMediate command causes the trigger system to initiate and complete one full trigger cycle,
        returning to IDLE on completion.
        This command is an event and cannot be queried as there is no state associated with it.
        """
        self.instrument.write("INIT:IMM")

    def initiate_immediate_all(self):
        """
        Causes all SEQuences to be INITiated, except those defined to behave otherwise.
        This command is an event and has no query form.
        """
        self.instrument.write("INIT:IMM:ALL")

    
    def initiate_immediate_name(self, sequence_name: str):
        """
        Causes the SEQuence with the alias specified by <sequence_name> to be INITiated.
        :param sequence_name: The character program data for the sequence alias.
        This command is an event and has no query form.
        """
        self.instrument.write(f"INIT:IMM:NAME '{sequence_name}'")

    def initiate_immediate_sequence(self, sequence_number: int):
        """
        Causes the specified SEQuence to be INITiated.
        :param sequence_number: The numeric suffix on SEQuence corresponds to the sequence number.
        This command is an event and has no query form. If NAME is implemented, this command shall also be implemented.
        """
        self.instrument.write(f"INIT:IMM:SEQ{sequence_number}")

    def set_initiate_poflag(self, flag_mode: str):
        """
        Allows the Pending-Operation flag associated with the initiation of a trigger sequence
        to be included or excluded from the No-Operation-Pending flag set.
        :param flag_mode: "INCLude" or "EXCLude".
        Notes: At *RST, the value of this parameter is INCLude.
        """
        valid_modes = {"INC", "INCLUDE", "EXC", "EXCLUDE"}
        mode_upper = flag_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid flag_mode: '{flag_mode}'. Must be 'INCLude' or 'EXCLude'.")

        if mode_upper.startswith("INC"): scpi_mode = "INC"
        elif mode_upper.startswith("EXC"): scpi_mode = "EXC"
        else: scpi_mode = mode_upper

        self.instrument.write(f"INIT:POFL {scpi_mode}")

    def get_initiate_poflag(self) -> str:
        """
        Queries the Pending-Operation flag setting.
        :return: The flag mode ("INCLude" or "EXCLude").
        """
        response = self.instrument.query("INIT:POFL?").strip().upper()
        if response.startswith("INC"): return "INCLude"
        if response.startswith("EXC"): return "EXCLude"
        return response

    
    def set_trigger_sequence_atrigger_state(self, enable: bool):
        """
        Sets and queries the state of the auto trigger function.
        :param enable: True to enable the function, False to disable it.
        Notes: At *RST, the value of this parameter is OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":TRIG:SEQ:ATR:STATE {scpi_value}")

    def get_trigger_sequence_atrigger_state(self) -> bool:
        """
        Queries the state of the auto trigger function.
        :return: True if enabled, False if disabled.
        """
        response = self.instrument.query(":TRIG:SEQ:ATR:STATE?").strip()
        return response == "1"

    
    def set_trigger_sequence_count(self, value: int):
        """
        Controls the path of the trigger system in the upward traverse of the event detection layer.
        :param value: The count value (numeric value, 1 or greater).
        Notes: At *RST, this value is set to 1.
        """
        if value < 1:
            raise ValueError("COUNt must be 1 or greater.")
        self.instrument.write(f":TRIG:SEQ:COUN {value}")

    def get_trigger_sequence_count(self) -> int:
        """
        Queries the count for the TRIGger sequence.
        :return: The count value.
        """
        response = self.instrument.query(":TRIG:SEQ:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger sequence COUNt (not integer): '{response}'")

    def set_trigger_sequence_coupling(self, coupling_type: str, sequence_number: int = None):
        """
        Selects AC or DC coupling for the SOURced signal. Only has effect if the source
        for the event detector is an analog electrical signal.
        :param coupling_type: "AC" or "DC".
        Notes: At *RST, this value is device-dependent.
        """
        valid_types = {"AC", "DC", "LFR", "HFR", "LFReject", "HFReject"}
        type_upper = coupling_type.upper()
        path = ":TRIG:"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC' or 'DC'.")
        self.instrument.write(f"{path}:COUP {type_upper}")

    def get_trigger_sequence_coupling(self, sequence_number:int = None) -> str:
        """
        Queries the coupling type for the TRIGger sequence.
        :return: The coupling type ("AC" or "DC").
        """
        path = ":TRIG:"
        if sequence_number is not None:
            path += f":SEQ{sequence_number}"
        response = self.instrument.query(f"{path}:COUP?").strip().upper()
        return response

    def set_trigger_sequence_define(self, sequence_name: str, sequence_number: int = None):
        """
        Sets the SEQuence alias. This command is an alias to :ARM:SEQuence:DEFine.
        :param sequence_name: The character data string for the sequence alias.
        :param sequence_number: Optional. The numeric suffix (sequence number) to apply the alias to.
        Notes: Overwrites previously defined name. *RST has no effect on the defined name.
        """
        if sequence_number is not None:
            self.instrument.write(f":TRIG:SEQ{sequence_number}:DEF '{sequence_name}'")
        else:
            self.instrument.write(f":TRIG:SEQ:DEF '{sequence_name}'")

    def get_trigger_sequence_define(self, sequence_number: int = None) -> str:
        """
        Queries the SEQuence alias.
        :param sequence_number: Optional. The numeric suffix (sequence number) to query.
        :return: The character data string of the sequence alias, or a null string if nothing is defined.
        """
        if sequence_number is not None:
            response = self.instrument.query(f":TRIG:SEQ{sequence_number}:DEF?").strip()
        else:
            response = self.instrument.query(":TRIG:SEQ:DEF?").strip()
        return response.strip("'") # Remove quotes if present

    
    def set_trigger_sequence_define_mgrules(self, enable: bool, sequence_number: int = None):
        """
        Sets the state of MGRules (Mnemonic Generation Rules) for sequence aliases.
        :param enable: True to enable MGRules, False to disable.
        :param sequence_number: Optional. The numeric suffix (sequence number) for which to set MGRules.
        Notes: At *RST, the value of this parameter is OFF.
        """
        scpi_value = "1" if enable else "0"
        if sequence_number is not None:
            self.instrument.write(f":TRIG:SEQ{sequence_number}:DEF:MGR {scpi_value}")
        else:
            self.instrument.write(f":TRIG:SEQ:DEF:MGR {scpi_value}")

    def get_trigger_sequence_define_mgrules(self, sequence_number: int = None) -> bool:
        """
        Queries the state of MGRules (Mnemonic Generation Rules) for sequence aliases.
        :param sequence_number: Optional. The numeric suffix (sequence number) to query.
        :return: True if MGRules is enabled, False if disabled.
        """
        if sequence_number is not None:
            response = self.instrument.query(f":TRIG:SEQ{sequence_number}:DEF:MGR?").strip()
        else:
            response = self.instrument.query(":TRIG:SEQ:DEF:MGR?").strip()
        return response == "1"

    def set_trigger_sequence_delay(self, value: float, seq:bool = None):
        """
        Sets the time duration between the recognition of an event(s) and the downward exit of the specified layer.
        :param value: The delay time in seconds (numeric value, zero or positive).
        Notes: At *RST, this value is set to 0 or the smallest available positive value.
        """
        if value < 0:
            raise ValueError("DELay must be zero or a positive value.")
        path = ":TRIG:"
        if seq is not None:
            path += f":SEQ"
        self.instrument.write(f"{path}:DEL {value}")

    def get_trigger_sequence_delay(self, seq:bool=None) -> float:
        """
        Queries the delay time for the TRIGger sequence.
        :return: The delay time in seconds.
        """
        path = ":TRIG:"
        if seq is not None:
            path += f":SEQ"
        response = self.instrument.query(f"{path}:DEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger sequence DELay (not numeric): '{response}'")

    
    def set_trigger_sequence_delay_auto(self, auto_state: str):
        """
        Sets auto-delay for sensor devices with internal settling delays.
        :param auto_state: "ON" (enables auto-delay), "OFF" (disables), or "ONCE" (adjusts once then OFF).
        Notes: At *RST, AUTO is set ON.
        """
        normalized_state = auto_state.upper()
        if normalized_state not in {"ON", "OFF", "ONCE"}:
            raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":TRIG:SEQ:DEL:AUTO {normalized_state}")

    def get_trigger_sequence_delay_auto(self) -> str:
        """
        Queries the auto-delay state for the TRIGger sequence delay.
        :return: The auto-delay state ("ON", "OFF", or "ONCE").
        """
        response = self.instrument.query(":TRIG:SEQ:DEL:AUTO?").strip().upper()
        if response == "1": return "ON"
        if response == "0": return "OFF"
        return response

    def trigger_sequence_ecl(self):
        """
        Presets LEVel, HYSTeresis, COUPling, and DELay to values appropriate for an ECL signal.
        This command is an event and cannot be queried.
        """
        self.instrument.write(":TRIG:SEQ:ECL")

    def set_trigger_sequence_ecount(self, value: int):
        """
        Specifies a particular number of occurrences of the same event that must be recognized.
        :param value: The event count (numeric value, 1 or greater).
        Notes: At *RST, this value is set to 1.
        """
        if value < 1:
            raise ValueError("ECOunt must be 1 or greater.")
        self.instrument.write(f":TRIG:SEQ:ECO {value}")

    def get_trigger_sequence_ecount(self) -> int:
        """
        Queries the event count for the TRIGger sequence.
        :return: The event count.
        """
        response = self.instrument.query(":TRIG:SEQ:ECO?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger sequence ECOunt (not integer): '{response}'")

    def set_trigger_sequence_filter_hpass_frequency(self, value: float):
        """
        Determines the cutoff frequency of the high pass filter.
        :param value: The frequency in Hertz (numeric value).
        Notes: At *RST, this value is device-dependent.
        """
        self.instrument.write(f":TRIG:SEQ:FILT:HPAS:FREQ {value}")

    def get_trigger_sequence_filter_hpass_frequency(self) -> float:
        """
        Queries the cutoff frequency of the high pass filter for the TRIGger sequence.
        :return: The frequency in Hertz.
        """
        response = self.instrument.query(f":TRIG:SEQ:FILT:HPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger filter HPASS FREQuency (not numeric): '{response}'")

    def set_trigger_sequence_filter_hpass_state(self, enable: bool):
        """
        Turns the high pass filter ON or OFF.
        :param enable: True to turn ON, False to turn OFF.
        Notes: At *RST, this value is device-dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":TRIG:SEQ:FILT:HPAS:STATE {scpi_value}")

    def get_trigger_sequence_filter_hpass_state(self) -> bool:
        """
        Queries the state of the high pass filter for the TRIGger sequence.
        :return: True if ON, False if OFF.
        """
        response = self.instrument.query(f":TRIG:SEQ:FILT:HPAS:STATE?").strip()
        return response == "1"

    def set_trigger_sequence_filter_lpass_frequency(self, value: float):
        """
        Determines the cutoff frequency of the low pass filter.
        :param value: The frequency in Hertz (numeric value).
        Notes: At *RST, this value is device-dependent.
        """
        self.instrument.write(f":TRIG:SEQ:FILT:LPAS:FREQ {value}")

    def get_trigger_sequence_filter_lpass_frequency(self) -> float:
        """
        Queries the cutoff frequency of the low pass filter for the TRIGger sequence.
        :return: The frequency in Hertz.
        """
        response = self.instrument.query(f":TRIG:SEQ:FILT:LPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger filter LPASS FREQuency (not numeric): '{response}'")

    def set_trigger_sequence_filter_lpass_state(self, enable: bool):
        """
        Turns the low pass filter ON or OFF.
        :param enable: True to turn ON, False to turn OFF.
        Notes: At *RST, this value is device-dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":TRIG:SEQ:FILT:LPAS:STATE {scpi_value}")

    def get_trigger_sequence_filter_lpass_state(self) -> bool:
        """
        Queries the state of the low pass filter for the TRIGger sequence.
        :return: True if ON, False if OFF.
        """
        response = self.instrument.query(f":TRIG:SEQ:FILT:LPAS:STATE?").strip()
        return response == "1"

    
    def set_trigger_sequence_holdoff(self, value: float, seq: int = None):
        """
        Controls the time during which the event detector is inhibited from acting on any new trigger.
        :param value: The holdoff value (numeric value, zero to one).
        Notes: At *RST, the value of the parameter is zero.
        """
        path = ":TRIG:"
        if seq is not None:
            path = path + "SEQ:"

        self.instrument.write(f"{path}:HOLD {value}")

    def get_trigger_sequence_holdoff(self, seq: int = None) -> float:
        """
        Queries the holdoff value for the TRIGger sequence.
        :return: The holdoff value.
        """
        path = ":TRIG:"
        if seq is not None:
            path = path + "SEQ:"
        response = self.instrument.query(f"{path}:HOLD?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger holdoff (not numeric): '{response}'")

    def set_trigger_sequence_hysteresis(self, value: float):
        """
        Sets how far a signal must fall below LEVel before a rising edge can again be detected,
        and how far a signal must rise above LEVel before a falling edge can again be detected.
        Units default to current amplitude units.
        :param value: The hysteresis value (numeric value).
        Notes: At *RST, this value is device-dependent.
        """
        self.instrument.write(f":TRIG:SEQ:HYST {value}")

    def get_trigger_sequence_hysteresis(self) -> float:
        """
        Queries the hysteresis value for the TRIGger sequence.
        :return: The hysteresis value.
        """
        response = self.instrument.query(f":TRIG:SEQ:HYST?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger hysteresis (not numeric): '{response}'")

    def trigger_sequence_immediate(self):
        """
        Provides a one-time override of the normal process of the downward traverse of the event detection layer.
        Causes immediate exit of the specified event detection layer if the trigger system is in that layer.
        This command is an event, has no *RST condition, and cannot be queried.
        """
        self.instrument.write(":TRIG:SEQ:IMM")

    def set_trigger_sequence_level(self, value: float):
        """
        Qualifies the characteristic of the selected SOURce signal that generates an event.
        Only has effect if the source is an analog electrical signal.
        Units default to current amplitude unit.
        :param value: The level value (numeric value).
        Notes: At *RST, this value is instrument-dependent.
        """
        self.instrument.write(f":TRIG:SEQ:LEV {value}")

    def get_trigger_sequence_level(self) -> float:
        """
        Queries the level value for the TRIGger sequence.
        :return: The level value.
        """
        response = self.instrument.query(f":TRIG:SEQ:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger level (not numeric): '{response}'")

    def set_trigger_sequence_level_auto(self, auto_state: str):
        """
        Dynamically selects the best trigger level based on a device-dependent algorithm.
        :param auto_state: "ON" (enables auto-level), "OFF" (disables), or "ONCE" (adjusts once then OFF).
        Notes: Setting the trigger LEVel turns AUTO OFF. At *RST, the value of this parameter is OFF.
        """
        normalized_state = auto_state.upper()
        if normalized_state not in {"ON", "OFF", "ONCE"}:
            raise ValueError(f"Invalid auto_state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":TRIG:SEQ:LEV:AUTO {normalized_state}")

    def get_trigger_sequence_level_auto(self) -> str:
        """
        Queries the auto-level state for the TRIGger sequence level.
        :return: The auto-level state ("ON", "OFF", or "ONCE").
        """
        response = self.instrument.query(f":TRIG:SEQ:LEV:AUTO?").strip().upper()
        if response == "1": return "ON"
        if response == "0": return "OFF"
        return response

    
    def set_trigger_sequence_link(self, event_handle: str):
        """
        Sets the internal event that is LINKed to the event detector in the TRIGger layer.
        :param event_handle: STRING PROGRAM DATA for the event.
        Notes: At *RST, this value is device-dependent.
        """
        self.instrument.write(f":TRIG:SEQ:LINK '{event_handle}'")

    def get_trigger_sequence_link(self) -> str:
        """
        Queries the internal event that is LINKed to the event detector in the TRIGger layer.
        :return: The event handle string.
        """
        response = self.instrument.query(f":TRIG:SEQ:LINK?").strip().strip("'")
        return response

    def set_trigger_sequence_protocol_vxi(self, protocol_type: str):
        """
        Selects the trigger protocol for the VXI TTLTrg or ECLTrg trigger line when used as the trigger source.
        :param protocol_type: "SYNChronous", "SSYNchronous", or "ASYNchronous".
        Notes: At *RST, the SYNChronous protocol is selected.
        """
        valid_types = {"SYN", "SYNCHRONOUS", "SSYN", "SSYNCHRONOUS", "ASYN", "ASYNCHRONOUS"}
        type_upper = protocol_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid protocol_type: '{protocol_type}'. Must be 'SYNChronous', 'SSYNchronous', or 'ASYNchronous'.")

        if type_upper.startswith("SYN"): scpi_type = "SYN"
        elif type_upper.startswith("SSYN"): scpi_type = "SSYN"
        elif type_upper.startswith("ASYN"): scpi_type = "ASYN"
        else: scpi_type = type_upper

        self.instrument.write(f":TRIG:SEQ:PROT:VXI {scpi_type}")

    def get_trigger_sequence_protocol_vxi(self) -> str:
        """
        Queries the trigger protocol for the VXI TTLTrg or ECLTrg trigger line when used as the trigger source.
        :return: The protocol type ("SYNChronous", "SSYNchronous", or "ASYNchronous").
        """
        response = self.instrument.query(f":TRIG:SEQ:PROT:VXI?").strip().upper()
        if response.startswith("SYN") and not response.startswith("SSYN"): return "SYNChronous"
        if response.startswith("SSYN"): return "SSYNchronous"
        if response.startswith("ASYN"): return "ASYNchronous"
        return response

    def trigger_sequence_signal(self):
        """
        Provides a one-time override of the normal process of the downward traverse through the event detector.
        Causes immediate exit of the event detector block if the trigger system is waiting for the event.
        This command defines an event and has no associated query form or *RST condition.
        """
        self.instrument.write(":TRIG:SEQ:SIGN")

    
    def set_trigger_sequence_slope(self, slope_type: str):
        """
        Qualifies whether the event occurs on the rising edge, falling edge, or either edge of the signal.
        :param slope_type: "POSitive", "NEGative", or "EITHer".
        Notes: At *RST, this value is set to POS.
        """
        valid_types = {"POS", "POSITIVE", "NEG", "NEGATIVE", "EITH", "EITHER"}
        type_upper = slope_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid slope_type: '{slope_type}'. Must be 'POSitive', 'NEGative', or 'EITHer'.")

        if type_upper.startswith("POS"): scpi_type = "POS"
        elif type_upper.startswith("NEG"): scpi_type = "NEG"
        elif type_upper.startswith("EITH"): scpi_type = "EITH"
        else: scpi_type = type_upper

        self.instrument.write(f":TRIG:SEQ:SLOP {scpi_type}")

    def get_trigger_sequence_slope(self) -> str:
        """
        Queries the slope type for the TRIGger sequence.
        :return: The slope type ("POSitive", "NEGative", or "EITHer").
        """
        response = self.instrument.query(f":TRIG:SEQ:SLOP?").strip().upper()
        if response.startswith("POS"): return "POSitive"
        if response.startswith("NEG"): return "NEGative"
        if response.startswith("EITH"): return "EITHer"
        return response

    def set_trigger_sequence_source(self, source_type: str, source_index: int = None):
        """
        Selects the source for the event detector. Only one source may be specified at a time.
        :param source_type: The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                            "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
        :param source_index: Optional. Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
        Notes: At *RST, IMMediate shall be selected as the SOURce.
        """
        valid_types = {
            "AINT", "AINTERNAL", "BUS", "ECLTRG", "EXT", "EXTERNAL", "HOLD",
            "IMM", "IMMEDIATE", "INT", "INTERNAL", "LINE", "LINK", "MAN", "MANUAL",
            "OUTP", "OUTPUT", "TIM", "TIMER", "TTLTRG"
        }
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid source_type: '{source_type}'.")

        scpi_source = ""
        if type_upper.startswith("AINT"): scpi_source = "AINT"
        elif type_upper.startswith("BUS"): scpi_source = "BUS"
        elif type_upper.startswith("ECLTRG"): scpi_source = "ECLTrg"
        elif type_upper.startswith("EXT"): scpi_source = "EXT"
        elif type_upper.startswith("HOLD"): scpi_source = "HOLD"
        elif type_upper.startswith("IMM"): scpi_source = "IMM"
        elif type_upper.startswith("INT") and not type_upper.startswith("AINT"): scpi_source = "INT"
        elif type_upper.startswith("LINE"): scpi_source = "LINE"
        elif type_upper.startswith("LINK"): scpi_source = "LINK"
        elif type_upper.startswith("MAN"): scpi_source = "MAN"
        elif type_upper.startswith("OUTP"): scpi_source = "OUTP"
        elif type_upper.startswith("TIM"): scpi_source = "TIM"
        elif type_upper.startswith("TTLTRG"): scpi_source = "TTLTrg"
        else: scpi_source = type_upper # Fallback for exact match

        if source_index is not None:
            self.instrument.write(f":TRIG:SEQ:SOUR {scpi_source}{source_index}")
        else:
            self.instrument.write(f":TRIG:SEQ:SOUR {scpi_source}")

    def get_trigger_sequence_source(self) -> str:
        """
        Queries the source for the event detector for the TRIGger sequence.
        :return: The source type string (e.g., "IMMediate", "TTLTrg0").
        """
        response = self.instrument.query(f":TRIG:SEQ:SOUR?").strip().upper()
        if response.startswith("AINT"): return "AINTernal"
        if response.startswith("ECLTRG"): return response # Return as is with index
        if response.startswith("EXT"): return response # Return as is with index
        if response.startswith("IMM"): return "IMMediate"
        if response.startswith("INT"): return response # Return as is with index
        if response.startswith("MAN"): return "MANual"
        if response.startswith("OUTP"): return response # Return as is with index
        if response.startswith("TIM"): return "TIMer"
        if response.startswith("TTLTRG"): return response # Return as is with index
        return response # Default to returning the exact response

    
    def set_trigger_sequence_timer(self, value: float):
        """
        Sets the period of an internal periodic signal source.
        :param value: The timer period in seconds (numeric value, positive).
        Notes: At *RST, this value is device-dependent.
        """
        if value <= 0:
            raise ValueError("TIMer value must be positive.")
        self.instrument.write(f":TRIG:SEQ:TIM {value}")

    def get_trigger_sequence_timer(self) -> float:
        """
        Queries the period of an internal periodic signal source for the TRIGger sequence.
        :return: The timer period in seconds.
        """
        response = self.instrument.query(f":TRIG:SEQ:TIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger timer (not numeric): '{response}'")

    def trigger_sequence_ttl(self):
        """
        Presets LEVel, HYSTeresis, COUPling, and DELay to values appropriate for a TTL signal.
        This command is an event and cannot be queried.
        """
        self.instrument.write(":TRIG:SEQ:TTL")

    def set_trigger_sequence_type(self, type_value: str):
        """
        Sets the type of triggering.
        :param type_value: "EDGE" or "VIDeo".
        Notes: At *RST, the value of this parameter is EDGE.
        """
        valid_types = {"EDGE", "VID", "VIDEO"}
        type_upper = type_value.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid type_value: '{type_value}'. Must be 'EDGE' or 'VIDeo'.")

        if type_upper.startswith("VID"): scpi_type = "VID"
        else: scpi_type = type_upper

        self.instrument.write(f":TRIG:SEQ:TYPE {scpi_type}")

    def get_trigger_sequence_type(self) -> str:
        """
        Queries the type of triggering for the TRIGger sequence.
        :return: The type of triggering ("EDGE" or "VIDeo").
        """
        response = self.instrument.query(f":TRIG:SEQ:TYPE?").strip().upper()
        if response.startswith("VID"): return "VIDeo"
        return response

    
    def set_trigger_sequence_video_field_number(self, value: int):
        """
        Sets the field number to trigger on if FIELd:SELect is set to NUMBer.
        :param value: The field number (numeric value).
        Notes: At *RST, the value of this parameter is 1. Setting has no effect on SELect parameter.
        """
        self.instrument.write(f":TRIG:SEQ:VID:FIELD:NUMB {value}")

    def get_trigger_sequence_video_field_number(self) -> int:
        """
        Queries the field number to trigger on for the TRIGger video field.
        :return: The field number.
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:FIELD:NUMB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger video FIELD NUMBer (not integer): '{response}'")

    def set_trigger_sequence_video_field_select(self, select_mode: str):
        """
        Sets the video field selection method to be used.
        :param select_mode: "ODD", "EVEN", "ALL", or "NUMBer".
        Notes: At *RST, the value of this parameter is ALL.
        """
        valid_modes = {"ODD", "EVEN", "ALL", "NUMB", "NUMBER"}
        mode_upper = select_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid select_mode: '{select_mode}'. Must be 'ODD', 'EVEN', 'ALL', or 'NUMBer'.")

        if mode_upper.startswith("NUMB"): scpi_mode = "NUMB"
        else: scpi_mode = mode_upper

        self.instrument.write(f":TRIG:SEQ:VID:FIELD:SEL {scpi_mode}")

    def get_trigger_sequence_video_field_select(self) -> str:
        """
        Queries the video field selection method for the TRIGger video field.
        :return: The video field selection method ("ODD", "EVEN", "ALL", or "NUMBer").
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:FIELD:SEL?").strip().upper()
        if response.startswith("NUMB"): return "NUMBer"
        return response

    def set_trigger_sequence_video_format_lpframe(self, value: int):
        """
        Sets the lines per frame associated with the signal formatting standard being used.
        :param value: Lines Per Frame (numeric value).
        Notes: At *RST, this value is device dependent.
        """
        self.instrument.write(f":TRIG:SEQ:VID:FORM:LPFR {value}")

    def get_trigger_sequence_video_format_lpframe(self) -> int:
        """
        Queries the lines per frame for the TRIGger video format.
        :return: Lines Per Frame.
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:FORM:LPFR?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger video FORMat LPFRame (not integer): '{response}'")

    def set_trigger_video_line(self, line_number, seq: int = None):
        """
        Set the line number when the sync type in video trigger is LINE.

        Parameters:
        line_number (int): The line number. Range depends on video standard (e.g., 1 to 525 for NTSC).
        TODO: Insert different standards potential values, maybe add a check.
        """
        if isinstance(line_number, int) and line_number >= 1: # Minimum line number is 1
            self.instrument.write(f":TRIGger:VIDeo:LINE {line_number}")
        else:
            print(f"Invalid video line number ({line_number}). Must be an integer >= 1.")

    def get_trigger_video_line(self, seq: int = None):
        """
        Query the line number when the sync type in video trigger is LINE.

        Returns:
        int: The line number.
        TODO: Add option for boolean or int of sequence
        """
        path = ":TRIG"
        if seq is not None:
            path += f":SEQ{seq}"
        response = self.instrument.query(f"{path}:VIDeo:LINE?")
        return int(response.strip())
    def set_trigger_sequence_video_line_number(self, value: int, seq:int=None):
        """
        Sets the line number to trigger on if LINE:SELect is set to NUMBer.
        :param value: The line number (numeric value).
        Notes: At *RST, the value of this parameter is device dependent. Setting has no effect on SELect parameter.
        """
        path = ":TRIG"
        if seq is not None:
            path += f":SEQ{seq}"
        self.instrument.write(f":TRIG:SEQ:VID:LINE:NUMB {value}")

    def get_trigger_sequence_video_line_number(self) -> int:
        """
        Queries the line number to trigger on for the TRIGger video line.
        :return: The line number.
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:LINE:NUMB?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRIGger video LINE NUMBer (not integer): '{response}'")

    def set_trigger_sequence_video_line_select(self, select_mode: str):
        """
        Sets the video line selection method to be used.
        :param select_mode: "ALL" or "NUMBer".
        Notes: At *RST, the value of this parameter is ALL.
        """
        valid_modes = {"ALL", "NUMB", "NUMBER"}
        mode_upper = select_mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid select_mode: '{select_mode}'. Must be 'ALL' or 'NUMBer'.")

        if mode_upper.startswith("NUMB"): scpi_mode = "NUMB"
        else: scpi_mode = mode_upper

        self.instrument.write(f":TRIG:SEQ:VID:LINE:SEL {scpi_mode}")

    def get_trigger_sequence_video_line_select(self) -> str:
        """
        Queries the video line selection method for the TRIGger video line.
        :return: The video line selection method ("ALL" or "NUMBer").
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:LINE:SEL?").strip().upper()
        if response.startswith("NUMB"): return "NUMBer"
        return response

    def set_trigger_sequence_video_ssignal_polarity(self, polarity_type: str):
        """
        Sets sync pulse triggering polarity.
        :param polarity_type: "POSitive" or "NEGative".
        Notes: At *RST, the value of this parameter is NEGative.
        """
        valid_types = {"POS", "POSITIVE", "NEG", "NEGATIVE"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity_type: '{polarity_type}'. Must be 'POSitive' or 'NEGative'.")

        if type_upper.startswith("POS"): scpi_type = "POS"
        elif type_upper.startswith("NEG"): scpi_type = "NEG"
        else: scpi_type = type_upper

        self.instrument.write(f":TRIG:SEQ:VID:SSIG:POL {scpi_type}")

    def get_trigger_sequence_video_ssignal_polarity(self) -> str:
        """
        Queries sync pulse triggering polarity for the TRIGger video synchronizing signal.
        :return: The polarity type ("POSitive" or "NEGative").
        """
        response = self.instrument.query(f":TRIG:SEQ:VID:SSIG:POL?").strip().upper()
        if response.startswith("POS"): return "POSitive"
        if response.startswith("NEG"): return "NEGative"
        return response
