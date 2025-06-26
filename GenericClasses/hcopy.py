class HCopy:
    """
   
    """
    def __init__(self, instrument_connection):
        """
    
        """
        self.instrument = instrument_connection

    

    def hcopy_abort(self):
        """
        Aborts the current hard copy operation.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ABOR")

    def get_hcopy_data(self) -> str:
        """
        Initiates the plot or print according to the current Hard COPy setup parameters.
        Returns all of the items under the ITEM node which are turned ON (STATE ON)
        encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The hard copy data as a string.
        """
        response = self.instrument.query("HCOP:DATA?").strip()
        # The document states the response has a leading #0 and a trailing NL^END.
        # This implementation simply returns the raw string, assuming the user will handle parsing.
        return response

    def set_hcopy_destination(self, data_handle: str):
        """
        An event which sets all :FEED connections that were set to "HCOPy" to "".
        The :FEED connection pointed to by <data_handle> is set to "HCOPY".
        :param data_handle: The data handle (string).
        """
        self.instrument.write(f"HCOP:DEST '{data_handle}'")



    def set_hcopy_device_cmap_color_hsl(self, hue: float, saturation: float, luminance: float):
        """
        Sets the instrument's color map based on the Hue/Saturation/Luminance levels color model.
        :param hue: Hue value (0 to 1, circularly).
        :param saturation: Saturation value (0 to 1).
        :param luminance: Luminance value (0 to 1).
        Notes: Coupled to RGB command. At *RST, parameters are set to default values.
        """
        if not (0 <= hue <= 1) or not (0 <= saturation <= 1) or not (0 <= luminance <= 1):
            raise ValueError("Hue, Saturation, and Luminance must be between 0 and 1.")
        self.instrument.write(f"HCOP:DEV:CMAP:COL:HSL {hue},{saturation},{luminance}")

    def get_hcopy_device_cmap_color_hsl(self) -> tuple[float, float, float]:
        """
        Queries the instrument's color map based on the Hue/Saturation/Luminance levels color model.
        :return: A tuple (hue, saturation, luminance).
        """
        response = self.instrument.query("HCOP:DEV:CMAP:COL:HSL?").strip()
        try:
            parts = [float(p) for p in response.split(',')]
            if len(parts) == 3:
                return tuple(parts)
            else:
                raise ValueError("Unexpected response format for HSL color.")
        except ValueError:
            raise ValueError(f"Failed to parse HSL color response: '{response}'")

    def set_hcopy_device_cmap_color_rgb(self, red: float, green: float, blue: float):
        """
        Sets the instrument's color map based on the Red/Green/Blue color model.
        :param red: Red intensity (0 to 1).
        :param green: Green intensity (0 to 1).
        :param blue: Blue intensity (0 to 1).
        Notes: Coupled to HSL command. At *RST, parameters are set to default values.
        """
        if not (0 <= red <= 1) or not (0 <= green <= 1) or not (0 <= blue <= 1):
            raise ValueError("Red, Green, and Blue values must be between 0 and 1.")
        self.instrument.write(f"HCOP:DEV:CMAP:COL:RGB {red},{green},{blue}")

    def get_hcopy_device_cmap_color_rgb(self) -> tuple[float, float, float]:
        """
        Queries the instrument's color map based on the Red/Green/Blue color model.
        :return: A tuple (red, green, blue).
        """
        response = self.instrument.query("HCOP:DEV:CMAP:COL:RGB?").strip()
        try:
            parts = [float(p) for p in response.split(',')]
            if len(parts) == 3:
                return tuple(parts)
            else:
                raise ValueError("Unexpected response format for RGB color.")
        except ValueError:
            raise ValueError(f"Failed to parse RGB color response: '{response}'")

    def hcopy_device_cmap_default(self):
        """
        Sets the color map to the instrument's default values for all colors.
        Notes: COLor[1] for "black," COLor2 for "white" or monochrome display color.
        """
        self.instrument.write("HCOP:DEV:CMAP:DEF")

    def set_hcopy_device_color(self, enable: bool):
        """
        Sets or queries whether color information should be sent as part of the plot or print information.
        :param enable: True to send color information, False for monochrome.
        Notes: At *RST, the value is OFF.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:DEV:COL {scpi_value}")

    def get_hcopy_device_color(self) -> bool:
        """
        Queries whether color information should be sent.
        :return: True if color information is sent, False otherwise.
        """
        response = self.instrument.query("HCOP:DEV:COL?").strip()
        return response == "1"



    def set_hcopy_device_language(self, language_type: str, version: int = None):
        """
        Selects the control language or data format to be used when sending out plot or print information.
        :param language_type: "PCL", "HPGL", or "POSTscript".
        :param version: Optional. A specific version number of that language.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        valid_languages = {"PCL", "HPGL", "POST", "POSTSCRIPT"}
        lang_upper = language_type.upper()
        if lang_upper not in valid_languages:
            raise ValueError(f"Invalid language_type: '{language_type}'. Must be 'PCL', 'HPGL', or 'POSTscript'.")

        scpi_lang = ""
        if lang_upper == "PCL": scpi_lang = "PCL"
        elif lang_upper == "HPGL": scpi_lang = "HPGL"
        elif lang_upper.startswith("POST"): scpi_lang = "POST"
        else: scpi_lang = language_type # Fallback

        if version is not None:
            self.instrument.write(f"HCOP:DEV:LANG {scpi_lang}{version}")
        else:
            self.instrument.write(f"HCOP:DEV:LANG {scpi_lang}")

    def get_hcopy_device_language(self) -> str:
        """
        Queries the control language or data format being used.
        :return: The language string (e.g., "PCL", "HPGL", "POSTscript").
        """
        response = self.instrument.query("HCOP:DEV:LANG?").strip().upper()
        if response.startswith("POST"): return "POSTscript"
        return response # Returns "PCL" or "HPGL"

    def set_hcopy_device_mode(self, mode_type: str):
        """
        Sets or queries how the data is to be represented in the hard copy.
        :param mode_type: "TABLE" (formatted into a table) or "GRAPH" (graph or picture).
        Notes: At *RST, the value of this setting is device dependent.
        """
        valid_modes = {"TABL", "TABLE", "GRAP", "GRAPH"}
        mode_upper = mode_type.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid mode_type: '{mode_type}'. Must be 'TABLE' or 'GRAPH'.")

        if mode_upper.startswith("TABL"): scpi_mode = "TABL"
        elif mode_upper.startswith("GRAP"): scpi_mode = "GRAP"
        else: scpi_mode = mode_type # Fallback

        self.instrument.write(f"HCOP:DEV:MODE {scpi_mode}")

    def get_hcopy_device_mode(self) -> str:
        """
        Queries how the data is to be represented in the hard copy.
        :return: The mode type ("TABLE" or "GRAPH").
        """
        response = self.instrument.query("HCOP:DEV:MODE?").strip().upper()
        if response.startswith("TABL"): return "TABLE"
        if response.startswith("GRAP"): return "GRAPH"
        return response



    def set_hcopy_device_resolution(self, value: float):
        """
        Sets or queries the resolution of the result on the hard copy device.
        Generally used to affect the quality of the output from a raster printer.
        :param value: The resolution value (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:DEV:RES {value}")

    def get_hcopy_device_resolution(self) -> float:
        """
        Queries the resolution of the result on the hard copy device.
        :return: The resolution value.
        """
        response = self.instrument.query("HCOP:DEV:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY DEVice RESolution (not numeric): '{response}'")

    def set_hcopy_device_resolution_unit(self, unit: str):
        """
        Sets or queries the units of the RESolution setting.
        :param unit: The suffix program data for the unit.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:DEV:RES:UNIT {unit}")

    def get_hcopy_device_resolution_unit(self) -> str:
        """
        Queries the units of the RESolution setting.
        :return: The unit string.
        """
        response = self.instrument.query("HCOP:DEV:RES:UNIT?").strip()
        return response

    def set_hcopy_device_speed(self, value: float):
        """
        Sets or queries the speed at which vectors are drawn.
        Generally used to affect the quality of the output from a pen plotter.
        :param value: The speed value (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:DEV:SPE {value}")

    def get_hcopy_device_speed(self) -> float:
        """
        Queries the speed at which vectors are drawn.
        :return: The speed value.
        """
        response = self.instrument.query("HCOP:DEV:SPE?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY DEVice SPEed (not numeric): '{response}'")

    def set_hcopy_device_speed_unit(self, unit: str):
        """
        Sets or queries the units of the SPEed setting.
        :param unit: The suffix program data for the unit.
        Notes: At *RST, the value of this parameter is cm/sec.
        """
        self.instrument.write(f"HCOP:DEV:SPE:UNIT {unit}")

    def get_hcopy_device_speed_unit(self) -> str:
        """
        Queries the units of the SPEed setting.
        :return: The unit string.
        """
        response = self.instrument.query("HCOP:DEV:SPE:UNIT?").strip()
        return response

    def set_hcopy_feed(self, data_handle: str):
        """
        Sets or queries the data flow to be fed into the Hard COPy block.
        :param data_handle: The data handle (string).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:FEED '{data_handle}'")

    def get_hcopy_feed(self) -> str:
        """
        Queries the data flow to be fed into the Hard COPy block.
        :return: The data handle string.
        """
        response = self.instrument.query("HCOP:FEED?").strip().strip("'")
        return response

    def hcopy_immediate(self):
        """
        Immediately initiates the plot or print according to the current Hard COPY setup parameters.
        All of the items under the ITEM node which are turned ON (STATE ON) are plotted or printed.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:IMM")

 

    def get_hcopy_item_all_data(self) -> str:
        """
        Returns all ITEMS, regardless of their individual states, encapsulated in an
        <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:ALL:DATA?").strip()
        return response

    def hcopy_item_all_immediate(self):
        """
        Immediately plots or prints all ITEMS, regardless of their individual states.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:ALL:IMM")

    def set_hcopy_item_annotation_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the display annotation.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:ANNOT:COL {color_value}")

    def get_hcopy_item_annotation_color(self) -> int:
        """
        Queries the color used for plotting or printing the display annotation.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:ANNOT:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM ANNotation COLor (not integer): '{response}'")

    def get_hcopy_item_annotation_data(self) -> str:
        """
        Returns the display annotation encapsulated in an <INDEFINITE LENGTH ARBITRARY
        RESPONSE DATA> element.
        :return: The annotation data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:ANNOT:DATA?").strip()
        return response

    def hcopy_item_annotation_immediate(self):
        """
        Immediately plots or prints the display annotation.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:ANNOT:IMM")

    def set_hcopy_item_annotation_state(self, enable: bool):
        """
        Sets or queries whether ANNotation should be plotted or printed when the
        HCOPY:IMMediate command or HCOPY:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:ANNOT:STATE {scpi_value}")

    def get_hcopy_item_annotation_state(self) -> bool:
        """
        Queries whether ANNotation should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:ANNOT:STATE?").strip()
        return response == "1"



    def get_hcopy_item_cut_data(self) -> str:
        """
        Returns what would be sent to the hard copy device to cut the page
        encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The cut data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:CUT:DATA?").strip()
        return response

    def hcopy_item_cut_immediate(self):
        """
        Immediately cuts the page.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:CUT:IMM")

    def set_hcopy_item_cut_state(self, enable: bool):
        """
        Sets or queries whether a page cut should be performed as part of the
        HCOPy:IMMediate command or HCOPY:DATA? query.
        :param enable: True to enable page cut, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:CUT:STATE {scpi_value}")

    def get_hcopy_item_cut_state(self) -> bool:
        """
        Queries whether a page cut should be performed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:CUT:STATE?").strip()
        return response == "1"


    def get_hcopy_item_ffeed_data(self) -> str:
        """
        Returns what would be sent to the hard copy device to do a form feed
        encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The form feed data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:FFED:DATA?").strip()
        return response

    def hcopy_item_ffeed_immediate(self):
        """
        Immediately form-feeds the page.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:FFED:IMM")

    def set_hcopy_item_ffeed_state(self, enable: bool):
        """
        Sets or queries whether a form feed should be performed as part of the
        HCOPY:IMMediate command or HCOPY:DATA? query.
        :param enable: True to enable form feed, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:FFED:STATE {scpi_value}")

    def get_hcopy_item_ffeed_state(self) -> bool:
        """
        Queries whether a form feed should be performed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:FFED:STATE?").strip()
        return response == "1"



    def set_hcopy_item_label_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the label.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:LAB:COL {color_value}")

    def get_hcopy_item_label_color(self) -> int:
        """
        Queries the color used for plotting or printing the label.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:LAB:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM LABel COLor (not integer): '{response}'")

 

    def get_hcopy_item_label_data(self) -> str:
        """
        Returns the label encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The label data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:LAB:DATA?").strip()
        return response

    def hcopy_item_label_immediate(self):
        """
        Immediately plots or prints the label.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:LAB:IMM")

    def set_hcopy_item_label_state(self, enable: bool):
        """
        Sets or queries whether the label should be plotted or printed when the
        HCOPY:IMMediate command or HCOPY:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:LAB:STATE {scpi_value}")

    def get_hcopy_item_label_state(self) -> bool:
        """
        Queries whether the label should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:LAB:STATE?").strip()
        return response == "1"

    def set_hcopy_item_label_text(self, text_string: str):
        """
        Sets or queries the contents of the user label.
        :param text_string: The string content for the label. May contain formatting characters.
        Notes: At *RST, all textual labels are set to the empty string.
        """
        # SCPI string program data typically needs to be enclosed in quotes.
        # Handle escaping internal quotes if necessary (by doubling them).
        escaped_text = text_string.replace("'", "''")
        self.instrument.write(f"HCOP:ITEM:LAB:TEXT '{escaped_text}'")

    def get_hcopy_item_label_text(self) -> str:
        """
        Queries the contents of the user label.
        :return: The label text string.
        """
        response = self.instrument.query("HCOP:ITEM:LAB:TEXT?").strip().strip("'")
        # Un-escape internal quotes if any were doubled during setting
        return response.replace("''", "'")



    def set_hcopy_item_menu_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the menu.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:MENU:COL {color_value}")

    def get_hcopy_item_menu_color(self) -> int:
        """
        Queries the color used for plotting or printing the menu.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:MENU:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM MENU COLor (not integer): '{response}'")

    def get_hcopy_item_menu_data(self) -> str:
        """
        Returns the menu encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The menu data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:MENU:DATA?").strip()
        return response

    def hcopy_item_menu_immediate(self):
        """
        Immediately plots or prints the menu.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:MENU:IMM")

    def set_hcopy_item_menu_state(self, enable: bool):
        """
        Sets or queries whether the menu should be plotted or printed when the
        HCOPY:IMMediate command or HCOPY:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:MENU:STATE {scpi_value}")

    def get_hcopy_item_menu_state(self) -> bool:
        """
        Queries whether the menu should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:MENU:STATE?").strip()
        return response == "1"



    def set_hcopy_item_tdstamp_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the time and date stamp.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:TDST:COL {color_value}")

    def get_hcopy_item_tdstamp_color(self) -> int:
        """
        Queries the color used for plotting or printing the time and date stamp.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:TDST:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM TDSTamp COLor (not integer): '{response}'")

    def get_hcopy_item_tdstamp_data(self) -> str:
        """
        Returns the time and date stamp encapsulated in an <INDEFINITE LENGTH ARBITRARY
        RESPONSE DATA> element.
        :return: The timestamp data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:TDST:DATA?").strip()
        return response

    def hcopy_item_tdstamp_immediate(self):
        """
        Immediately plots or prints the time and date stamp.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:TDST:IMM")

    def set_hcopy_item_tdstamp_state(self, enable: bool):
        """
        Sets or queries whether the time and date stamp should be plotted or printed when the
        HCOPy:IMMediate command or HCOPy:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:TDST:STATE {scpi_value}")

    def get_hcopy_item_tdstamp_state(self) -> bool:
        """
        Queries whether the time and date stamp should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:TDST:STATE?").strip()
        return response == "1"

    def get_hcopy_item_window_data(self) -> str:
        """
        Returns the window encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The window data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:DATA?").strip()
        return response

    def hcopy_item_window_immediate(self):
        """
        Immediately plots or prints the window.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:WIND:IMM")

    def set_hcopy_item_window_state(self, enable: bool):
        """
        Sets or queries whether the window should be plotted or printed when the
        HCOPy:IMMediate command or HCOPy:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:WIND:STATE {scpi_value}")

    def get_hcopy_item_window_state(self) -> bool:
        """
        Queries whether the window should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:STATE?").strip()
        return response == "1"


    def set_hcopy_item_window_text_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing TEXT.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:WIND:TEXT:COL {color_value}")

    def get_hcopy_item_window_text_color(self) -> int:
        """
        Queries the color used for plotting or printing TEXT.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TEXT:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM WINDow TEXT COLor (not integer): '{response}'")

    def get_hcopy_item_window_text_data(self) -> str:
        """
        Returns the text blocks or textual labels encapsulated in an
        <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The text data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TEXT:DATA?").strip()
        return response

    def hcopy_item_window_text_immediate(self):
        """
        Immediately plots or prints the text blocks or textual labels.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:WIND:TEXT:IMM")

    def set_hcopy_item_window_text_state(self, enable: bool):
        """
        Sets or queries whether the text blocks or textual labels should be plotted or printed when the
        HCOPy:IMMediate command or HCOPy:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:WIND:TEXT:STATE {scpi_value}")

    def get_hcopy_item_window_text_state(self) -> bool:
        """
        Queries whether the text blocks or textual labels should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TEXT:STATE?").strip()
        return response == "1"


    def set_hcopy_item_window_trace_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the trace.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:WIND:TRAC:COL {color_value}")

    def get_hcopy_item_window_trace_color(self) -> int:
        """
        Queries the color used for plotting or printing the trace.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM WINDow TRACe COLor (not integer): '{response}'")

    def get_hcopy_item_window_trace_data(self) -> str:
        """
        Returns the trace encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The trace data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:DATA?").strip()
        return response


    def set_hcopy_item_window_trace_graticule_color(self, color_value: int):
        """
        Sets or queries the color to be used for plotting or printing the graticule.
        :param color_value: The numeric value representing the color.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:ITEM:WIND:TRAC:GRAT:COL {color_value}")

    def get_hcopy_item_window_trace_graticule_color(self) -> int:
        """
        Queries the color used for plotting or printing the graticule.
        :return: The numeric color value.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:GRAT:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY ITEM WINDow TRACe GRATicule COLor (not integer): '{response}'")

    def get_hcopy_item_window_trace_graticule_data(self) -> str:
        """
        Returns the graticule encapsulated in an <INDEFINITE LENGTH ARBITRARY RESPONSE DATA> element.
        :return: The graticule data as a string.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:GRAT:DATA?").strip()
        return response

    def hcopy_item_window_trace_graticule_immediate(self):
        """
        Immediately plots or prints the graticule.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:WIND:TRAC:GRAT:IMM")

    def set_hcopy_item_window_trace_graticule_state(self, enable: bool):
        """
        Sets or queries whether the graticule should be plotted or printed when the
        HCOPy:IMMediate command or HCOPy:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:WIND:TRAC:GRAT:STATE {scpi_value}")

    def get_hcopy_item_window_trace_graticule_state(self) -> bool:
        """
        Queries whether the graticule should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:GRAT:STATE?").strip()
        return response == "1"

    def hcopy_item_window_trace_immediate(self):
        """
        Immediately plots or prints the trace.
        This command is an event (no query form).
        """
        self.instrument.write("HCOP:ITEM:WIND:TRAC:IMM")

    def set_hcopy_item_window_trace_linetype(self, line_type: str, style_n: int = None):
        """
        Sets or queries the line type to be used for plotting or printing the trace.
        :param line_type: "SOLid", "DOTTed", "DASHed", or "STYLe".
        :param style_n: Optional. A numeric suffix for "STYLe" to select a specific style.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        valid_types = {"SOL", "SOLID", "DOTT", "DOTTED", "DASH", "DASHED", "STYL", "STYLE"}
        type_upper = line_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid line_type: '{line_type}'. Must be 'SOLid', 'DOTTed', 'DASHed', or 'STYLe'.")

        scpi_type = ""
        if type_upper.startswith("SOL"): scpi_type = "SOL"
        elif type_upper.startswith("DOTT"): scpi_type = "DOTT"
        elif type_upper.startswith("DASH"): scpi_type = "DASH"
        elif type_upper.startswith("STYL"): scpi_type = "STYL"
        else: scpi_type = line_type

        if scpi_type == "STYL" and style_n is not None:
            self.instrument.write(f"HCOP:ITEM:WIND:TRAC:LTYP STYL{style_n}")
        else:
            self.instrument.write(f"HCOP:ITEM:WIND:TRAC:LTYP {scpi_type}")

    def get_hcopy_item_window_trace_linetype(self) -> str:
        """
        Queries the line type used for plotting or printing the trace.
        :return: The line type ("SOLid", "DOTTed", "DASHed", or "STYLe<n>").
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:LTYP?").strip().upper()
        if response.startswith("SOL"): return "SOLid"
        if response.startswith("DOTT"): return "DOTTed"
        if response.startswith("DASH"): return "DASHed"
        if response.startswith("STYL"): return response # Return as STYLe<n>
        return response

    def set_hcopy_item_window_trace_state(self, enable: bool):
        """
        Sets or queries whether the trace should be plotted or printed when the
        HCOPy:IMMediate command or HCOPy:DATA? query is sent.
        :param enable: True to enable plotting/printing, False to disable.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:ITEM:WIND:TRAC:STATE {scpi_value}")

    def get_hcopy_item_window_trace_state(self) -> bool:
        """
        Queries whether the trace should be plotted or printed.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:ITEM:WIND:TRAC:STATE?").strip()
        return response == "1"


    def set_hcopy_page_dimensions_auto(self, enable: bool):
        """
        When AUTO is on, the device selects the default page dimensions.
        When AUTO is OFF, the page dimensions are set by other settings in this subsystem.
        :param enable: True to enable auto dimensions, False to disable.
        Notes: At *RST, the value of this parameter is ON.
        """
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"HCOP:PAGE:DIM:AUTO {scpi_value}")

    def get_hcopy_page_dimensions_auto(self) -> bool:
        """
        Queries whether auto page dimensions are enabled.
        :return: True if enabled, False otherwise.
        """
        response = self.instrument.query("HCOP:PAGE:DIM:AUTO?").strip()
        return response == "1"

    def set_hcopy_page_dimensions_lleft(self, x_position: float, y_position: float):
        """
        Sets or queries the x,y position of the lower left corner of the page.
        Units are percent of the width and length of the page.
        :param x_position: The x-coordinate (numeric value).
        :param y_position: The y-coordinate (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:PAGE:DIM:LLEF {x_position},{y_position}")

    def get_hcopy_page_dimensions_lleft(self) -> tuple[float, float]:
        """
        Queries the x,y position of the lower left corner of the page.
        :return: A tuple (x_position, y_position).
        """
        response = self.instrument.query("HCOP:PAGE:DIM:LLEF?").strip()
        try:
            parts = [float(p) for p in response.split(',')]
            if len(parts) == 2:
                return tuple(parts)
            else:
                raise ValueError("Unexpected response format for LLEFt dimensions.")
        except ValueError:
            raise ValueError(f"Failed to parse LLEFt dimensions response: '{response}'")

    def hcopy_page_dimensions_quadrant(self, quadrant_number: int):
        """
        Sets dimensions so that the plot/print occupies one quadrant of the page.
        :param quadrant_number: The quadrant number (1-4).
                                1: upper right, 2: upper left, 3: lower left, 4: lower right.
        This command is an event only (no query form).
        """
        if not (1 <= quadrant_number <= 4):
            raise ValueError("Quadrant number must be between 1 and 4.")
        self.instrument.write(f"HCOP:PAGE:DIM:QUAD {quadrant_number}")

    def set_hcopy_page_dimensions_uright(self, x_position: float, y_position: float):
        """
        Specifies the x,y position of upper right corner of the page.
        Units are percent of the width and length of the page.
        :param x_position: The x-coordinate (numeric value).
        :param y_position: The y-coordinate (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:PAGE:DIM:URIG {x_position},{y_position}")

    def get_hcopy_page_dimensions_uright(self) -> tuple[float, float]:
        """
        Queries the x,y position of upper right corner of the page.
        :return: A tuple (x_position, y_position).
        """
        response = self.instrument.query("HCOP:PAGE:DIM:URIG?").strip()
        try:
            parts = [float(p) for p in response.split(',')]
            if len(parts) == 2:
                return tuple(parts)
            else:
                raise ValueError("Unexpected response format for URIGht dimensions.")
        except ValueError:
            raise ValueError(f"Failed to parse URIGht dimensions response: '{response}'")

    def set_hcopy_page_length(self, value: float):
        """
        Sets or queries the length of the page to be plotted or printed.
        :param value: The length value (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:PAGE:LENG {value}")

    def get_hcopy_page_length(self) -> float:
        """
        Queries the length of the page.
        :return: The length value.
        """
        response = self.instrument.query("HCOP:PAGE:LENG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY PAGE LENGth (not numeric): '{response}'")

    def set_hcopy_page_orientation(self, orientation_type: str):
        """
        Sets or queries the orientation of the plot or print.
        :param orientation_type: "LANDscape" or "PORTrait".
        Notes: Switching rotates the hardcopy result by 90 degrees; no other settings change.
               At *RST, the value of this parameter is device dependent.
        """
        valid_types = {"LAND", "LANDSCAPE", "PORT", "PORTRAIT"}
        type_upper = orientation_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid orientation_type: '{orientation_type}'. Must be 'LANDscape' or 'PORTrait'.")

        if type_upper.startswith("LAND"): scpi_type = "LAND"
        elif type_upper.startswith("PORT"): scpi_type = "PORT"
        else: scpi_type = orientation_type

        self.instrument.write(f"HCOP:PAGE:ORI {scpi_type}")

    def get_hcopy_page_orientation(self) -> str:
        """
        Queries the orientation of the plot or print.
        :return: The orientation type ("LANDscape" or "PORTrait").
        """
        response = self.instrument.query("HCOP:PAGE:ORI?").strip().upper()
        if response.startswith("LAND"): return "LANDscape"
        if response.startswith("PORT"): return "PORTrait"
        return response

    def set_hcopy_page_scale(self, value: float):
        """
        Sets or queries a scaling factor which is applied to the hard copy output.
        This factor applies to both dimensions.
        :param value: The scaling factor (numeric value).
        Notes: At *RST, the value of this setting is one.
        """
        self.instrument.write(f"HCOP:PAGE:SCAL {value}")

    def get_hcopy_page_scale(self) -> float:
        """
        Queries the scaling factor.
        :return: The scaling factor.
        """
        response = self.instrument.query("HCOP:PAGE:SCAL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY PAGE SCALe (not numeric): '{response}'")



    def set_hcopy_page_size(self, size_type: str):
        """
        Sets or queries the size of the paper in terms of a standard paper size.
        If LENGth or WIDth are set, the value of this setting becomes CUSTom.
        :param size_type: "CUSTom", "A", "B", "C", "D", "E", "A0" through "A4", "B0" through "B5".
        Notes: At *RST, the value of this parameter is device dependent.
        """
        valid_sizes = {
            "CUSTOM", "A", "B", "C", "D", "E",
            "A0", "A1", "A2", "A3", "A4",
            "B0", "B1", "B2", "B3", "B4", "B5"
        }
        size_upper = size_type.upper()
        if size_upper not in valid_sizes:
            raise ValueError(f"Invalid size_type: '{size_type}'. Refer to documentation for valid sizes.")

        if size_upper == "CUSTOM": scpi_value = "CUST"
        else: scpi_value = size_upper

        self.instrument.write(f"HCOP:PAGE:SIZE {scpi_value}")

    def get_hcopy_page_size(self) -> str:
        """
        Queries the size of the paper.
        :return: The paper size string.
        """
        response = self.instrument.query("HCOP:PAGE:SIZE?").strip().upper()
        if response == "CUST": return "CUSTom"
        return response

    def set_hcopy_page_unit(self, unit: str):
        """
        Sets or queries the units for LENGth and WIDTh under DIMensions.
        :param unit: The suffix program data for the unit.
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:PAGE:UNIT {unit}")

    def get_hcopy_page_unit(self) -> str:
        """
        Queries the units for LENGth and WIDTh under DIMensions.
        :return: The unit string.
        """
        response = self.instrument.query("HCOP:PAGE:UNIT?").strip()
        return response

    def set_hcopy_page_width(self, value: float):
        """
        Sets or queries the width of the page to be plotted or printed.
        :param value: The width value (numeric value).
        Notes: At *RST, the value of this parameter is device dependent.
        """
        self.instrument.write(f"HCOP:PAGE:WIDT {value}")

    def get_hcopy_page_width(self) -> float:
        """
        Queries the width of the page.
        :return: The width value.
        """
        response = self.instrument.query("HCOP:PAGE:WIDT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for HCOPY PAGE WIDTh (not numeric): '{response}'")

   

    def get_hcopy_sdump_data(self) -> str:
        """
        Returns the whole DISPlay encapsulated in an <INDEFINITE LENGTH ARBITRARY
        RESPONSE DATA> element.
        :return: The screen dump data as a string.
        """
        response = self.instrument.query("HCOP:SDUM:DATA?").strip()
        return response

    def hcopy_sdump_immediate(self):
        """
        Causes the whole DISPlay to be plotted or printed.
        This event (no query form).
        """
        self.instrument.write("HCOP:SDUM:IMM")
