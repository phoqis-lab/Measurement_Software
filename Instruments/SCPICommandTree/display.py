class Display():
    def __init__(self,instrument):
        self.instrument = instrument
    def set_display_annotation_all(self, enable: bool):
        """Controls ALL of the annotation information.
        Parameters:
        enable: True to enable all annotations, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:ANN:ALL {scpi_value}")

    def get_display_annotation_all(self) -> bool:
        """Returns True if all annotation information is controlled (enabled), False if disabled."""
        response = self.instrument.query("DISP:ANN:ALL?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display annotation all state: '{response}'")

    def set_display_annotation_amplitude(self, enable: bool):
        """Controls the amplitude annotation information.
        Parameters:
        enable: True to enable amplitude annotation, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:ANN:AMPL {scpi_value}")

    def get_display_annotation_amplitude(self) -> bool:
        """Returns True if amplitude annotation information is enabled, False if disabled."""
        response = self.instrument.query("DISP:ANN:AMPL?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display annotation amplitude state: '{response}'")

    def set_display_annotation_frequency(self, enable: bool):
        """Controls the frequency annotation information.
        Parameters:
        enable: True to enable frequency annotation, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:ANN:FREQ {scpi_value}")

    def get_display_annotation_frequency(self) -> bool:
        """Returns True if frequency annotation information is enabled, False if disabled."""
        response = self.instrument.query("DISP:ANN:FREQ?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display annotation frequency state: '{response}'")

    def set_display_brightness(self, brightness_value: float):
        """Controls the intensity of the display.
        Parameters:
        brightness_value: The intensity value (0 to 1, where 1 is full intensity and 0 is fully blanked)."""
        if not (0 <= brightness_value <= 1):
            raise ValueError("Brightness value must be between 0 and 1.")
        self.instrument.write(f"DISP:BRIG {brightness_value}")

    def get_display_brightness(self) -> float:
        """Returns the intensity of the display (0 to 1)."""
        response = self.instrument.query("DISP:BRIG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for display brightness (not numeric): '{response}'")

    def set_display_cmap_default(self):
        """Sets the color map to the instrument's default values for all colors."""
        self.instrument.write(f"DISP:CMAP:DEF")

    def set_display_cmap_color_hsl(self, hue: float, saturation: float, luminance: float):
        """Sets the instrument's color map based on the Hue/Saturation/Luminance levels color model.
        Parameters:
        hue: Hue value (0 to 1, circularly).
        saturation: Saturation value (0 to 1).
        luminance: Luminance value (0 to 1)."""
        if not (0 <= hue <= 1 and 0 <= saturation <= 1 and 0 <= luminance <= 1):
            raise ValueError("HSL parameters must be between 0 and 1.")
        self.instrument.write(f"DISP:CMAP:COL:HSL {hue},{saturation},{luminance}")

    def get_display_cmap_color_hsl(self) -> tuple[float, float, float]:
        """Returns the instrument's color map based on the Hue/Saturation/Luminance levels color model."""
        response = self.instrument.query("DISP:CMAP:COL:HSL?").strip()
        try:
            h, s, l = map(float, response.split(','))
            return h, s, l
        except ValueError:
            raise ValueError(f"Unexpected response for CMAP HSL: '{response}'")

    def set_display_cmap_color_rgb(self, red: float, green: float, blue: float):
        """Sets the instrument's color map based on the Red/Green/Blue color model.
        Parameters:
        red: Red intensity (0 to 1).
        green: Green intensity (0 to 1).
        blue: Blue intensity (0 to 1)."""
        if not (0 <= red <= 1 and 0 <= green <= 1 and 0 <= blue <= 1):
            raise ValueError("RGB parameters must be between 0 and 1.")
        self.instrument.write(f"DISP:CMAP:COL:RGB {red},{green},{blue}")

    def get_display_cmap_color_rgb(self) -> tuple[float, float, float]:
        """Returns the instrument's color map based on the Red/Green/Blue color model."""
        response = self.instrument.query("DISP:CMAP:COL:RGB?").strip()
        try:
            r, g, b = map(float, response.split(','))
            return r, g, b
        except ValueError:
            raise ValueError(f"Unexpected response for CMAP RGB: '{response}'")

    
    def set_display_contrast(self, contrast_value: float):
        """Determines the relative difference in brightness between 'full' intensity and 'no' intensity as displayed.
        Parameters:
        contrast_value: Contrast value (0 to 1, where 0 indicates no difference and 1 indicates maximum contrast)."""
        if not (0 <= contrast_value <= 1):
            raise ValueError("Contrast value must be between 0 and 1.")
        self.instrument.write(f"DISP:CONT {contrast_value}")

    def get_display_contrast(self) -> float:
        """Returns the relative difference in brightness between 'full' intensity and 'no' intensity."""
        response = self.instrument.query("DISP:CONT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for display contrast (not numeric): '{response}'")

    def set_display_enable(self, enable: bool):
        """Controls whether the whole display is visible.
        Parameters:
        enable: True to enable the display, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:ENAB {scpi_value}")

    def get_display_enable(self) -> bool:
        """Returns True if the whole display is visible, False if not."""
        response = self.instrument.query("DISP:ENAB?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display enable state: '{response}'")

    
    def set_display_menu_name(self, menu_name: str):
        """Selects a menu by name from an instrument-predefined list of valid menu names.
        Parameters:
        menu_name: The name of the menu to select."""
        self.instrument.write(f"DISP:MENU:NAME '{menu_name}'") # Use quotes for string parameters as good practice

    def get_display_menu_name(self) -> str:
        """Returns the name of the currently selected menu."""
        response = self.instrument.query("DISP:MENU:NAME?").strip().strip("'\"") # Remove potential quotes
        return response

    def set_display_menu_state(self, enable: bool):
        """Turns the current menu page ON or OFF.
        Parameters:
        enable: True to turn the menu ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:MENU:STATE {scpi_value}")

    def get_display_menu_state(self) -> bool:
        """Returns True if the current menu page is ON, False if OFF."""
        response = self.instrument.query("DISP:MENU:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display menu state: '{response}'")

    def set_display_menu_key(self, key_string: str):
        """Assigns the soft key label to a key.
        Parameters:
        key_string: The soft key label string."""
        self.instrument.write(f"DISP:MENU:KEY '{key_string}'") # Use quotes for string parameters

    def get_display_menu_key(self) -> str:
        """Returns the soft key label assigned to a key."""
        response = self.instrument.query("DISP:MENU:KEY?").strip().strip("'\"")
        return response

    def set_display_window_background_color(self, color_value: int):
        """Selects from the CMAP the value to become the background color for the window.
        Parameters:
        color_value: The color number (numeric value) from the CMAP."""
        self.instrument.write(f"DISP:WIND:BACK:COL {color_value}")

    def get_display_window_background_color(self) -> int:
        """Returns the background color number for the window."""
        response = self.instrument.query("DISP:WIND:BACK:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window background color (not integer): '{response}'")

    def set_display_window_geometry_lleft(self, x_coord: float, y_coord: float):
        """Specifies the location of the lower left corner of the window in the range 0 to 1.
        Parameters:
        x_coord: The X-coordinate (0 to 1).
        y_coord: The Y-coordinate (0 to 1)."""
        if not (0 <= x_coord <= 1 and 0 <= y_coord <= 1):
            raise ValueError("Coordinates must be between 0 and 1.")
        self.instrument.write(f"DISP:WIND:GEOM:LLEF {x_coord},{y_coord}")

    def get_display_window_geometry_lleft(self) -> tuple[float, float]:
        """Returns the location of the lower left corner of the window."""
        response = self.instrument.query("DISP:WIND:GEOM:LLEF?").strip()
        try:
            x, y = map(float, response.split(','))
            return x, y
        except ValueError:
            raise ValueError(f"Unexpected response for window geometry LLEFt: '{response}'")

    
    def set_display_window_geometry_size(self, width: float, height: float):
        """Specifies the size of the display window.
        Parameters:
        width: The length in the horizontal direction (0 to 1, 0 for icon).
        height: The length in the vertical direction (0 to 1, 0 for icon)."""
        if not (0 <= width <= 1 and 0 <= height <= 1):
            raise ValueError("Width and height must be between 0 and 1.")
        self.instrument.write(f"DISP:WIND:GEOM:SIZE {width},{height}")

    def get_display_window_geometry_size(self) -> tuple[float, float]:
        """Returns the size of the display window."""
        response = self.instrument.query("DISP:WIND:GEOM:SIZE?").strip()
        try:
            width, height = map(float, response.split(','))
            return width, height
        except ValueError:
            raise ValueError(f"Unexpected response for window geometry SIZE: '{response}'")

    def set_display_window_geometry_uright(self, x_coord: float, y_coord: float):
        """Specifies the location of the upper right corner of the display window in the range 0 to 1.
        Parameters:
        x_coord: The X-coordinate (0 to 1).
        y_coord: The Y-coordinate (0 to 1)."""
        if not (0 <= x_coord <= 1 and 0 <= y_coord <= 1):
            raise ValueError("Coordinates must be between 0 and 1.")
        self.instrument.write(f"DISP:WIND:GEOM:URIG {x_coord},{y_coord}")

    def get_display_window_geometry_uright(self) -> tuple[float, float]:
        """Returns the location of the upper right corner of the display window."""
        response = self.instrument.query("DISP:WIND:GEOM:URIG?").strip()
        try:
            x, y = map(float, response.split(','))
            return x, y
        except ValueError:
            raise ValueError(f"Unexpected response for window geometry URIGht: '{response}'")

    def clear_display_window_graphics(self):
        """Erases the graphics from the window.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:GRAP:CLE")

    def set_display_window_graphics_color(self, color_value: int):
        """Selects the color for the next graphics operation from the CMAP.
        Parameters:
        color_value: The color number (numeric value) from the CMAP."""
        self.instrument.write(f"DISP:WIND:GRAP:COL {color_value}")

    def get_display_window_graphics_color(self) -> int:
        """Returns the color for the next graphics operation."""
        response = self.instrument.query("DISP:WIND:GRAP:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window graphics color (not integer): '{response}'")

    def set_display_window_graphics_csize(self, width: float, height: float = None):
        """Sets the size and optional aspect ratio (width/height) of the character cell.
        Parameters:
        width: The width of the character cell.
        height: (Optional) The height of the character cell (defaults to width if not provided)."""
        if height is None:
            self.instrument.write(f"DISP:WIND:GRAP:CSIZ {width}")
        else:
            self.instrument.write(f"DISP:WIND:GRAP:CSIZ {width},{height}")

    def get_display_window_graphics_csize(self) -> tuple[float, float]:
        """Returns the size and aspect ratio of the character cell."""
        response = self.instrument.query("DISP:WIND:GRAP:CSIZ?").strip()
        try:
            parts = [float(x) for x in response.split(',')]
            if len(parts) == 1:
                return parts[0], parts[0] # Assume square if only one value
            elif len(parts) == 2:
                return parts[0], parts[1]
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"Unexpected response for window graphics CSIZE: '{response}'")

    
    def draw_display_window_graphics_line(self, x_coord: float, y_coord: float):
        """Draws a line from the current 'pen' position to the specified X and Y coordinate.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:GRAP:DRAW {x_coord},{y_coord}")

    def send_display_window_graphics_pcl(self, block_data: bytes):
        """Sends graphics and text data to the instrument using Hewlett-Packard '<esc>*' terminal- and printer-style escape sequences.
        Parameters:
        block_data: The data block (bytes) to send."""
        num_bytes = len(block_data)
        num_digits = len(str(num_bytes))
        self.instrument.write(f"DISP:WIND:GRAP:PCL #{num_digits}{num_bytes}" + block_data.decode('latin-1'))

    def send_display_window_graphics_hpgl(self, block_data: bytes):
        """Sends graphics and text data to the instrument using HP-GL (Hewlett-Packard-Graphics Language) plotter language.
        Parameters:
        block_data: The data block (bytes) to send."""
        num_bytes = len(block_data)
        num_digits = len(str(num_bytes))
        self.instrument.write(f"DISP:WIND:GRAP:HPGL #{num_digits}{num_bytes}" + block_data.decode('latin-1'))

    def draw_display_window_graphics_idraw(self, x_offset: float, y_offset: float):
        """Draws a line from the current pen position to a new position determined by adding X and Y offsets.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:GRAP:IDRAW {x_offset},{y_offset}")

    def move_display_window_graphics_imove(self, x_offset: float, y_offset: float):
        """Updates the current pen position by adding an X offset and a Y offset to the current coordinates. No line is drawn.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:GRAP:IMOV {x_offset},{y_offset}")

    def set_display_window_graphics_label(self, text_label: str):
        """Places text on the graphics display at the current pen position.
        Parameters:
        text_label: The text string to place as a label."""
        self.instrument.write(f"DISP:WIND:GRAP:LAB '{text_label}'")

    def get_display_window_graphics_label(self) -> str:
        """Returns the text label on the graphics display."""
        response = self.instrument.query("DISP:WIND:GRAP:LAB?").strip().strip("'\"")
        return response

    def set_display_window_graphics_ldirection(self, angle_radians: float):
        """Defines the angle (in radians) at which labels are drawn.
        Parameters:
        angle_radians: The angle in radians (e.g., 0 for horizontal, PI/2 for bottom-to-top)."""
        self.instrument.write(f"DISP:WIND:GRAP:LDIR {angle_radians}")

    def get_display_window_graphics_ldirection(self) -> float:
        """Returns the angle (in radians) at which labels are drawn."""
        response = self.instrument.query("DISP:WIND:GRAP:LDIR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for graphics label direction (not numeric): '{response}'")

    def set_display_window_graphics_linetype(self, line_type: int, repeat_length: float = None):
        """Selects a line type and optional repeat length for all subsequent lines drawn.
        Parameters:
        line_type: The line type (numeric value, 1 is solid).
        repeat_length: (Optional) The repeat length for the line pattern."""
        if repeat_length is None:
            self.instrument.write(f"DISP:WIND:GRAP:LTYP {line_type}")
        else:
            self.instrument.write(f"DISP:WIND:GRAP:LTYP {line_type},{repeat_length}")

    def get_display_window_graphics_linetype(self) -> tuple[int, float]:
        """Returns the line type and repeat length for subsequent lines."""
        response = self.instrument.query("DISP:WIND:GRAP:LTYP?").strip()
        try:
            parts = [float(x) for x in response.split(',')]
            if len(parts) == 1:
                return int(parts[0]), None # No repeat length returned
            elif len(parts) == 2:
                return int(parts[0]), parts[1]
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"Unexpected response for graphics line type: '{response}'")

    
    def move_display_window_graphics_pen(self, x_coord: float, y_coord: float):
        """Updates the pen position without drawing a new line.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:GRAP:MOVE {x_coord},{y_coord}")

    def set_display_window_graphics_state(self, enable: bool):
        """Controls whether the graphics is visible or not.
        Parameters:
        enable: True to make graphics visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:GRAP:STATE {scpi_value}")

    def get_display_window_graphics_state(self) -> bool:
        """Returns True if the graphics is visible, False if not."""
        response = self.instrument.query("DISP:WIND:GRAP:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for window graphics state: '{response}'")

    def set_display_window_state(self, enable: bool):
        """Controls whether the window is visible or not.
        Parameters:
        enable: True to make the window visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:STATE {scpi_value}")

    def get_display_window_state(self) -> bool:
        """Returns True if the window is visible, False if not."""
        response = self.instrument.query("DISP:WIND:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for display window state: '{response}'")

    def set_display_window_text_attributes(self, enable: bool):
        """Allows the device to interpret ANSI Standard Terminal escape sequences when displaying TEXT:DATA.
        Parameters:
        enable: True to enable attribute interpretation, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TEXT:ATTR {scpi_value}")

    def get_display_window_text_attributes(self) -> bool:
        """Returns True if ANSI Standard Terminal escape sequence interpretation is enabled for text, False if disabled."""
        response = self.instrument.query("DISP:WIND:TEXT:ATTR?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for window text attributes state: '{response}'")

    def clear_display_window_text(self):
        """Erases the text from the window.
        Notes: This is an event command; no query."""
        self.instrument.write(f"DISP:WIND:TEXT:CLE")

    def set_display_window_text_color(self, color_value: int):
        """Selects the color for the next DATA stream (text display area).
        Parameters:
        color_value: The color number (numeric value) from the CMAP."""
        self.instrument.write(f"DISP:WIND:TEXT:COL {color_value}")

    def get_display_window_text_color(self) -> int:
        """Returns the color for the next DATA stream (text display area)."""
        response = self.instrument.query("DISP:WIND:TEXT:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window text color (not integer): '{response}'")

    
    def set_display_window_text_csize(self, width: float, height: float = None):
        """Sets the size and optional aspect ratio (width/height) of the character cell used by DATA.
        Parameters:
        width: The width of the character cell.
        height: (Optional) The height of the character cell (defaults to width if not provided)."""
        if height is None:
            self.instrument.write(f"DISP:WIND:TEXT:CSIZ {width}")
        else:
            self.instrument.write(f"DISP:WIND:TEXT:CSIZ {width},{height}")

    def get_display_window_text_csize(self) -> tuple[float, float]:
        """Returns the size and aspect ratio of the character cell used by DATA."""
        response = self.instrument.query("DISP:WIND:TEXT:CSIZ?").strip()
        try:
            parts = [float(x) for x in response.split(',')]
            if len(parts) == 1:
                return parts[0], parts[0] # Assume square if only one value
            elif len(parts) == 2:
                return parts[0], parts[1]
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"Unexpected response for window text CSIZE: '{response}'")

    def set_display_window_text_feed(self, data_handle: str):
        """Sets what data flow is fed into the TEXT display window.
        Parameters:
        data_handle: The data handle (character string) for the data flow."""
        self.instrument.write(f"DISP:WIND:TEXT:FEED '{data_handle}'")

    def get_display_window_text_feed(self) -> str:
        """Returns what data flow is fed into the TEXT display window."""
        response = self.instrument.query("DISP:WIND:TEXT:FEED?").strip().strip("'\"")
        return response

    def set_display_window_text_data(self, text_data: str):
        """Writes data to the text display area.
        Parameters:
        text_data: The text data (string) to write."""
        self.instrument.write(f"DISP:WIND:TEXT:DATA '{text_data}'") # Use quotes for string parameters

    def get_display_window_text_data(self) -> str:
        """Returns the data that gets written to the text display area."""
        response = self.instrument.query("DISP:WIND:TEXT:DATA?").strip().strip("'\"")
        return response

    def set_display_window_text_locate(self, row: int, column: int):
        """Selects the display ROW and display COLumn where the next LINE of TEXT DATA is to appear.
        Parameters:
        row: The row number (1-indexed, 1 is top row).
        column: The column number (1-indexed, 1 is left-most column)."""
        self.instrument.write(f"DISP:WIND:TEXT:LOC {row},{column}")

    def get_display_window_text_locate(self) -> tuple[int, int]:
        """Returns the display ROW and display COLumn where the next LINE of TEXT DATA will appear."""
        response = self.instrument.query("DISP:WIND:TEXT:LOC?").strip()
        try:
            r, c = map(int, response.split(','))
            return r, c
        except ValueError:
            raise ValueError(f"Unexpected response for window text locate: '{response}'")

    def set_display_window_text_page(self, page_value: str):
        """Sets the page to be displayed.
        Parameters:
        page_value: The page number (numeric value), or 'UP'|'DOWN' (implied in docs)."""
        # Document states <numeric value> but implies UP/DOWN. Handling both.
        if isinstance(page_value, (int, float)):
            self.instrument.write(f"DISP:WIND:TEXT:PAGE {page_value}")
        elif page_value.upper() in {"UP", "DOWN"}:
            self.instrument.write(f"DISP:WIND:TEXT:PAGE {page_value.upper()}")
        else:
            raise ValueError(f"Invalid page value: '{page_value}'. Must be numeric, 'UP', or 'DOWN'.")

    def get_display_window_text_page(self) -> str:
        """Returns the page currently displayed."""
        response = self.instrument.query("DISP:WIND:TEXT:PAGE?").strip()
        try:
            return str(int(float(response))) # Try to convert to int string if numeric
        except ValueError:
            return response.upper() # Return as is (e.g., "UP", "DOWN", or original string)

    def set_display_window_text_state(self, enable: bool):
        """Controls whether the TEXT is visible or not.
        Parameters:
        enable: True to make text visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TEXT:STATE {scpi_value}")

    def get_display_window_text_state(self) -> bool:
        """Returns True if the TEXT is visible, False if not."""
        response = self.instrument.query("DISP:WIND:TEXT:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for window text state: '{response}'")

    
    def set_display_window_trace_color(self, color_value: int):
        """Selects the color for the TRACE from the CMAP.
        Parameters:
        color_value: The color number (numeric value) from the CMAP."""
        self.instrument.write(f"DISP:WIND:TRAC:COL {color_value}")

    def get_display_window_trace_color(self) -> int:
        """Returns the color for the TRACE."""
        response = self.instrument.query("DISP:WIND:TRAC:COL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window trace color (not integer): '{response}'")

    def set_display_window_trace_feed(self, data_handle: str):
        """Sets what data flow is fed into the TRACe display window.
        Parameters:
        data_handle: The data handle (character string) for the data flow."""
        self.instrument.write(f"DISP:WIND:TRAC:FEED '{data_handle}'")

    def get_display_window_trace_feed(self) -> str:
        """Returns what data flow is fed into the TRACe display window."""
        response = self.instrument.query("DISP:WIND:TRAC:FEED?").strip().strip("'\"")
        return response

    def set_display_window_trace_graticule_axis_state(self, enable: bool):
        """Determines if the AXIS (X and Y or R axis) is visible or not.
        Parameters:
        enable: True to make axis visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:GRAT:AXIS:STATE {scpi_value}")

    def get_display_window_trace_graticule_axis_state(self) -> bool:
        """Returns True if the AXIS is visible, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:GRAT:AXIS:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace graticule axis state: '{response}'")

    def set_display_window_trace_graticule_frame_state(self, enable: bool):
        """Determines if the FRAMe (perimeter boundary and markings) is visible or not.
        Parameters:
        enable: True to make frame visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:GRAT:FRAM:STATE {scpi_value}")

    def get_display_window_trace_graticule_frame_state(self) -> bool:
        """Returns True if the FRAMe is visible, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:GRAT:FRAM:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace graticule frame state: '{response}'")

    def set_display_window_trace_graticule_grid_auto(self, enable: bool):
        """Couples the GRID subtree to FRAMe. Turning ON FRAMe, with AUTO set to ON, shall cause GRID to turn on also.
        Parameters:
        enable: True to enable auto-coupling of grid to frame, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:GRAT:GRID:AUTO {scpi_value}")

    def get_display_window_trace_graticule_grid_auto(self) -> bool:
        """Returns True if the GRID is auto-coupled to FRAMe, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:GRAT:GRID:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace graticule grid auto state: '{response}'")

    def set_display_window_trace_graticule_grid_state(self, enable: bool):
        """Determines if the GRID provides constant lines of X, Y or R with respect to the TRACe.
        Parameters:
        enable: True to make grid visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:GRAT:GRID:STATE {scpi_value}")

    def get_display_window_trace_graticule_grid_state(self) -> bool:
        """Returns True if the GRID is visible, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:GRAT:GRID:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace graticule grid state: '{response}'")

    def set_display_window_trace_persistence(self, persistence_seconds: float):
        """Sets how long trace data written to the screen will remain visible.
        Parameters:
        persistence_seconds: Persistence time in seconds (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:PERS {persistence_seconds}")

    def get_display_window_trace_persistence(self) -> float:
        """Returns how long trace data written to the screen will remain visible (in seconds)."""
        response = self.instrument.query("DISP:WIND:TRAC:PERS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for trace persistence (not numeric): '{response}'")

    def set_display_window_trace_persistence_auto(self, enable: bool):
        """When AUTO is set to ON, the persistence is determined by the device.
        Parameters:
        enable: True to enable auto persistence, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:PERS:AUTO {scpi_value}")

    def get_display_window_trace_persistence_auto(self) -> bool:
        """Returns True if persistence is automatically determined by the device, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:PERS:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace persistence auto state: '{response}'")

    def set_display_window_trace_state(self, enable: bool):
        """Controls whether the TRACE and related information is visible or not.
        Parameters:
        enable: True to make trace visible, False to hide."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:STATE {scpi_value}")

    def get_display_window_trace_state(self) -> bool:
        """Returns True if the TRACE and related information is visible, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:STATE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for trace state: '{response}'")

    
    def set_display_window_trace_x_label(self, label_string: str):
        """Specifies custom X-axis labeling.
        Parameters:
        label_string: The custom label string."""
        self.instrument.write(f"DISP:WIND:TRAC:X:LAB '{label_string}'")

    def get_display_window_trace_x_label(self) -> str:
        """Returns the custom X-axis labeling."""
        response = self.instrument.query("DISP:WIND:TRAC:X:LAB?").strip().strip("'\"")
        return response

    def set_display_window_trace_x_scale_auto(self, auto_mode: str):
        """Sets the display to always configure the scaling on the X-axis to best display the data.
        Parameters:
        auto_mode: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_mode = auto_mode.upper()
        if normalized_mode in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_mode in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_mode == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:AUTO {scpi_value}")

    def get_display_window_trace_x_scale_auto(self) -> str:
        """Returns the auto-scaling setting for the X-axis ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_display_window_trace_x_scale_center(self, center_value: float):
        """Sets the value represented by the center point of the x-axis.
        Parameters:
        center_value: The center value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:CENT {center_value}")

    def get_display_window_trace_x_scale_center(self) -> float:
        """Returns the value represented by the center point of the x-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis scale center (not numeric): '{response}'")

    def set_display_window_trace_x_scale_left(self, left_value: float):
        """Sets the value represented by the minimum (left) edge of the x-axis.
        Parameters:
        left_value: The left edge value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:LEF {left_value}")

    def get_display_window_trace_x_scale_left(self) -> float:
        """Returns the value represented by the minimum (left) edge of the x-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:LEF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis scale left (not numeric): '{response}'")

    
    def set_display_window_trace_x_scale_pdivision(self, pdivision_value: float):
        """Sets the value between two grid graticules (value "per division") for the X-axis.
        Parameters:
        pdivision_value: Value "per division" (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:PDIV {pdivision_value}")

    def get_display_window_trace_x_scale_pdivision(self) -> float:
        """Returns the value between two grid graticules (value "per division") for the X-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:PDIV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis scale per division (not numeric): '{response}'")

    def set_display_window_trace_x_scale_pdivision_link(self, link_parameter: str):
        """Selects the parameter (CENTer, LEFT, or RIGHt) that shall not be changed when the PDIVision value is changed.
        Parameters:
        link_parameter: LEFT|CENTer|RIGHt"""
        valid_links = {"LEFT", "CENTER", "RIGHT"}
        link_upper = link_parameter.upper()
        if link_upper not in valid_links:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be one of {list(valid_links)}")
        
        # Use abbreviated forms for SCPI
        if link_upper == "CENTER": scpi_value = "CENT"
        elif link_upper == "LEFT": scpi_value = "LEF"
        elif link_upper == "RIGHT": scpi_value = "RIGH"
        else: scpi_value = link_upper # Should not happen with valid_links check
        
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:PDIV:LINK {scpi_value}")

    def get_display_window_trace_x_scale_pdivision_link(self) -> str:
        """Returns the parameter that shall not be changed when the PDIVision value is changed for the X-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:PDIV:LINK?").strip().upper()
        if response.startswith("LEF"): return "LEFT"
        elif response.startswith("CENT"): return "CENTER"
        elif response.startswith("RIGH"): return "RIGHT"
        return response

    def set_display_window_trace_x_scale_right(self, right_value: float):
        """Sets the value represented by the maximum (right) edge of the x-axis.
        Parameters:
        right_value: The right edge value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:X:SCAL:RIGH {right_value}")

    def get_display_window_trace_x_scale_right(self) -> float:
        """Returns the value represented by the maximum (right) edge of the x-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:X:SCAL:RIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis scale right (not numeric): '{response}'")

    def set_display_window_trace_y_label(self, label_string: str):
        """Specifies custom Y-axis labeling.
        Parameters:
        label_string: The custom label string."""
        self.instrument.write(f"DISP:WIND:TRAC:Y:LAB '{label_string}'")

    def get_display_window_trace_y_label(self) -> str:
        """Returns the custom Y-axis labeling."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:LAB?").strip().strip("'\"")
        return response

    def set_display_window_trace_y_rline(self, enable: bool):
        """Turns on/off a line which is positioned on the graticule at the current Reference POSition.
        Parameters:
        enable: True to turn RLINE ON, False to turn OFF."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:Y:RLINE {scpi_value}")

    def get_display_window_trace_y_rline(self) -> bool:
        """Returns True if the RLINE is ON, False if OFF."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:RLINE?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis RLINE state: '{response}'")

    
    def set_display_window_trace_y_scale_auto(self, auto_mode: str):
        """Sets the display to always configure the scaling on the Y-axis to best display the data.
        Parameters:
        auto_mode: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_mode = auto_mode.upper()
        if normalized_mode in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_mode in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_mode == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:AUTO {scpi_value}")

    def get_display_window_trace_y_scale_auto(self) -> str:
        """Returns the auto-scaling setting for the Y-axis ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_display_window_trace_y_scale_bottom(self, bottom_value: float):
        """Sets the value represented by the minimum (bottom) edge of the display for the Y-axis.
        Parameters:
        bottom_value: The minimum edge value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:BOTT {bottom_value}")

    def get_display_window_trace_y_scale_bottom(self) -> float:
        """Returns the value represented by the minimum (bottom) edge of the display for the Y-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:BOTT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis scale bottom (not numeric): '{response}'")

    def set_display_window_trace_y_scale_pdivision(self, pdivision_value: float):
        """Sets the value between two grid graticules (value "per division") for the Y-axis.
        Parameters:
        pdivision_value: Value "per division" (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:PDIV {pdivision_value}")

    def get_display_window_trace_y_scale_pdivision(self) -> float:
        """Returns the value between two grid graticules (value "per division") for the Y-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:PDIV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis scale per division (not numeric): '{response}'")

    def set_display_window_trace_y_scale_rlevel(self, reference_level: float):
        """Sets the value represented at the designated Reference POSition on the y-axis.
        Parameters:
        reference_level: The reference level (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:RLEVel {reference_level}")

    def get_display_window_trace_y_scale_rlevel(self) -> float:
        """Returns the value represented at the designated Reference POSition on the y-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:RLEVel?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis scale reference level (not numeric): '{response}'")

    def set_display_window_trace_y_scale_rlevel_auto(self, enable: bool):
        """Causes the display to automatically choose a reference level to best display the particular data.
        Parameters:
        enable: True to enable auto reference level, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:RLEVel:AUTO {scpi_value}")

    def get_display_window_trace_y_scale_rlevel_auto(self) -> bool:
        """Returns True if the display automatically chooses a reference level, False if not."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:RLEVel:AUTO?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis reference level auto state: '{response}'")

    
    def set_display_window_trace_y_scale_rposition(self, reference_position: float):
        """Sets the point on the y-axis to be used as the reference position as a percentage of the length of the y-axis.
        Parameters:
        reference_position: The reference position (0 to 100 representing percentage)."""
        if not (0 <= reference_position <= 100):
            raise ValueError("Reference position must be between 0 and 100.")
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:RPOS {reference_position}")

    def get_display_window_trace_y_scale_rposition(self) -> float:
        """Returns the point on the y-axis used as the reference position as a percentage."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:RPOS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis scale reference position (not numeric): '{response}'")

    def set_display_window_trace_y_scale_top(self, top_value: float):
        """Sets the value represented by the top edge of the display for the Y-axis.
        Parameters:
        top_value: The top edge value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:Y:SCAL:TOP {top_value}")

    def get_display_window_trace_y_scale_top(self) -> float:
        """Returns the value represented by the top edge of the display for the Y-axis."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SCAL:TOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis scale top (not numeric): '{response}'")

    def set_display_window_trace_y_spacing(self, spacing_type: str):
        """Sets the Y-axis scale to either linear or log.
        Parameters:
        spacing_type: LOGarithmic|LINear"""
        valid_types = {"LOGARITHMIC", "LINEAR", "LOG", "LIN"}
        spacing_type_upper = spacing_type.upper()
        if spacing_type_upper not in valid_types:
            raise ValueError(f"Invalid spacing type: '{spacing_type}'. Must be 'LOGARITHMIC' or 'LINEAR'.")
        
        if spacing_type_upper == "LOGARITHMIC": scpi_value = "LOG"
        elif spacing_type_upper == "LINEAR": scpi_value = "LIN"
        else: scpi_value = spacing_type_upper
        
        self.instrument.write(f"DISP:WIND:TRAC:Y:SPAC {scpi_value}")

    def get_display_window_trace_y_spacing(self) -> str:
        """Returns the Y-axis scale type ('LOGARITHMIC' or 'LINEAR')."""
        response = self.instrument.query("DISP:WIND:TRAC:Y:SPAC?").strip().upper()
        if response.startswith("LOG"):
            return "LOGARITHMIC"
        elif response.startswith("LIN"):
            return "LINEAR"
        return response

    def set_display_window_trace_r_label(self, label_string: str):
        """Specifies custom R-axis (radial) labeling.
        Parameters:
        label_string: The custom label string."""
        self.instrument.write(f"DISP:WIND:TRAC:R:LAB '{label_string}'")

    def get_display_window_trace_r_label(self) -> str:
        """Returns the custom R-axis (radial) labeling."""
        response = self.instrument.query("DISP:WIND:TRAC:R:LAB?").strip().strip("'\"")
        return response

    def set_display_window_trace_r_scale_auto(self, auto_mode: str):
        """Sets the display to always configure the scaling on the R-axis to best display the data.
        Parameters:
        auto_mode: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_mode = auto_mode.upper()
        if normalized_mode in {"1", "ON"}:
            scpi_value = "ON"
        elif normalized_mode in {"0", "OFF"}:
            scpi_value = "OFF"
        elif normalized_mode == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto mode: '{auto_mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f"DISP:WIND:TRAC:R:SCAL:AUTO {scpi_value}")

    def get_display_window_trace_r_scale_auto(self) -> str:
        """Returns the auto-scaling setting for the R-axis ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query("DISP:WIND:TRAC:R:SCAL:AUTO?").strip()
        if response == "1":
            return "ON"
        elif response == "0":
            return "OFF"
        else:
            return response.upper()

    def set_display_window_trace_r_scale_cpoint(self, center_point_value: float):
        """Sets the value represented by the minimum (Center POint) of the circular display (R-axis).
        Parameters:
        center_point_value: The center point value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:R:SCAL:CPO {center_point_value}")

    def get_display_window_trace_r_scale_cpoint(self) -> float:
        """Returns the value represented by the minimum (Center POint) of the circular display (R-axis)."""
        response = self.instrument.query("DISP:WIND:TRAC:R:SCAL:CPO?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for R-axis scale center point (not numeric): '{response}')")

    
    def set_display_window_trace_r_scale_oedge(self, outside_edge_value: float):
        """Sets the value represented by the Outside EDGe of the circular display (R-axis).
        Parameters:
        outside_edge_value: The outside edge value (numeric value)."""
        self.instrument.write(f"DISP:WIND:TRAC:R:SCAL:OEDG {outside_edge_value}")

    def get_display_window_trace_r_scale_oedge(self) -> float:
        """Returns the value represented by the Outside EDGe of the circular display (R-axis)."""
        response = self.instrument.query("DISP:WIND:TRAC:R:SCAL:OEDG?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for R-axis scale outside edge (not numeric): '{response}')")

    def set_display_window_trace_r_spacing(self, spacing_type: str):
        """Sets the R-axis scale to either linear or log.
        Parameters:
        spacing_type: LOGarithmic|LINear"""
        valid_types = {"LOGARITHMIC", "LINEAR", "LOG", "LIN"}
        spacing_type_upper = spacing_type.upper()
        if spacing_type_upper not in valid_types:
            raise ValueError(f"Invalid spacing type: '{spacing_type}'. Must be 'LOGARITHMIC' or 'LINEAR'.")

        if spacing_type_upper == "LOGARITHMIC": scpi_value = "LOG"
        elif spacing_type_upper == "LINEAR": scpi_value = "LIN"
        else: scpi_value = spacing_type_upper

        self.instrument.write(f"DISP:WIND:TRAC:R:SPAC {scpi_value}")

    def get_display_window_trace_r_spacing(self) -> str:
        """Returns the R-axis scale type ('LOGARITHMIC' or 'LINEAR')."""
        response = self.instrument.query("DISP:WIND:TRAC:R:SPAC?").strip().upper()
        if response.startswith("LOG"):
            return "LOGARITHMIC"
        elif response.startswith("LIN"):
            return "LINEAR"
        return response