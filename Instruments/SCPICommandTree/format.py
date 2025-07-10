class Format():
    def __init__(self,instrument):
        self.instrument = instrument
        
    def set_format_border(self, byte_order: str):
        """Controls whether binary data is transferred in normal or swapped byte order.
        Parameters:
        byte_order: NORMal|SWAPped"""
        valid_orders = {"NORMAL", "SWAPPED", "NORM", "SWAP"}
        order_upper = byte_order.upper()
        if order_upper not in valid_orders:
            raise ValueError(f"Invalid byte order: '{byte_order}'. Must be 'NORMAL' or 'SWAPPED'.")

        if order_upper == "NORMAL": scpi_value = "NORM"
        elif order_upper == "SWAPPED": scpi_value = "SWAP"
        else: scpi_value = order_upper # Use the provided abbreviation if valid

        self.instrument.write(f":FORM:BORD {scpi_value}")

    def get_format_border(self) -> str:
        """Returns whether binary data is transferred in normal or swapped byte order."""
        response = self.instrument.query(":FORM:BORD?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("SWAP"):
            return "SWAPPED"
        return response # Return as-is if unexpected

    def set_format_data(self, data_type: str, length: float = None):
        """Selects the data format for transferring numeric and array information.
        Parameters:
        data_type: ASCii|INTeger|UINTeger|REAL|HEXadecimal|OCTal|BINary|PACKed
        length: (Optional) The length parameter, its meaning depends on the type selected."""
        valid_types = {
            "ASCII", "INT", "INTEGER", "UINT", "UINTEGER", "REAL",
            "HEX", "HEXADECIMAL", "OCT", "OCTAL", "BIN", "BINARY", "PACK", "PACKED"
        }
        data_type_upper = data_type.upper()
        if data_type_upper not in valid_types:
            raise ValueError(f"Invalid data type: '{data_type}'. Must be one of {list(valid_types)}")

        # Normalize to SCPI abbreviations if longer forms are used
        if data_type_upper == "INTEGER": scpi_value = "INT"
        elif data_type_upper == "UINTEGER": scpi_value = "UINT"
        elif data_type_upper == "HEXADECIMAL": scpi_value = "HEX"
        elif data_type_upper == "OCTAL": scpi_value = "OCT"
        elif data_type_upper == "BINARY": scpi_value = "BIN"
        elif data_type_upper == "PACKED": scpi_value = "PACK"
        else: scpi_value = data_type_upper # Use the provided abbreviation if valid

        if length is None:
            self.instrument.write(f":FORM:DATA {scpi_value}")
        else:
            self.instrument.write(f":FORM:DATA {scpi_value},{length}")

    def get_format_data(self) -> tuple[str, float]:
        """Returns the selected data format type and its length.
        Returns: A tuple containing (data_type: str, length: float or None)."""
        response = self.instrument.query(":FORM:DATA?").strip()
        parts = response.split(',')
        data_type = parts[0].strip().upper()

        # Normalize the returned data type to full names for consistency
        if data_type.startswith("ASC"): data_type = "ASCII"
        elif data_type.startswith("INT"): data_type = "INTEGER"
        elif data_type.startswith("UINT"): data_type = "UINTEGER"
        elif data_type.startswith("REA"): data_type = "REAL"
        elif data_type.startswith("HEX"): data_type = "HEXADECIMAL"
        elif data_type.startswith("OCT"): data_type = "OCTAL"
        elif data_type.startswith("BIN"): data_type = "BINARY"
        elif data_type.startswith("PAC"): data_type = "PACKED"

        length = None
        if len(parts) > 1:
            try:
                length = float(parts[1].strip())
            except ValueError:
                pass # Length might not be a valid number, or not present

        return data_type, length

    
    def set_format_dinterchange(self, enable: bool):
        """Determines whether measurement data is formatted as a <dif_expression>.
        Parameters:
        enable: True to encapsulate returned data in the DIF structure, False to disable."""
        scpi_value = "1" if enable else "0"
        self.instrument.write(f":FORM:DINT {scpi_value}")

    def get_format_dinterchange(self) -> bool:
        """Returns True if measurement data is formatted as a <dif_expression>, False if not."""
        response = self.instrument.query(":FORM:DINT?").strip()
        if response == "1" or response.upper() == "ON":
            return True
        elif response == "0" or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for data interchange state: '{response}'")

    
    def set_format_sregister(self, data_type: str):
        """Selects the data type of the response to queries for status registers.
        Parameters:
        data_type: ASCii|BINary|HEXadecimal|OCTal"""
        valid_types = {"ASCII", "BINARY", "HEXADECIMAL", "OCTAL", "ASC", "BIN", "HEX", "OCT"}
        data_type_upper = data_type.upper()
        if data_type_upper not in valid_types:
            raise ValueError(f"Invalid data type: '{data_type}'. Must be one of {list(valid_types)}")

        # Normalize to SCPI abbreviations if longer forms are used
        if data_type_upper == "ASCII": scpi_value = "ASC"
        elif data_type_upper == "BINARY": scpi_value = "BIN"
        elif data_type_upper == "HEXADECIMAL": scpi_value = "HEX"
        elif data_type_upper == "OCTAL": scpi_value = "OCT"
        else: scpi_value = data_type_upper # Use the provided abbreviation if valid

        self.instrument.write(f":FORM:SREG {scpi_value}")

    def get_format_sregister(self) -> str:
        """Returns the data type of the response to queries for status registers."""
        response = self.instrument.query(":FORM:SREG?").strip().upper()
        if response.startswith("ASC"):
            return "ASCII"
        elif response.startswith("BIN"):
            return "BINARY"
        elif response.startswith("HEX"):
            return "HEXADECIMAL"
        elif response.startswith("OCT"):
            return "OCTAL"
        return response # Return as-is if unexpected