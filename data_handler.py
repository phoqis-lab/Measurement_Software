import json
import csv
import os
from EFIleType import EFileType
class DataHandler():
    def __init__(self, format):
        self.writer = None
        self.reader = None
        self.format = EFileType.CSV

    def set_default_file_type(self, format):
        """"Sets default file type for reading and writing files."""
        if type(format) is str:
            format = EFileType(format).name
        self.format = format
        #TODO Change readers and writers
    
    def read_file(self, file_path):
        """Reads file and returns data"""
        if self.format == EFileType.CSV:
            with open(file_path, mode='r', newline='') as csvfile:
                self.reader = csv.reader(csvfile)
                return list(self.reader)
        elif self.format == EFileType.JSON:
            with open(file_path, 'r') as jsonfile:
                return json.load(jsonfile)
        
        else:
            raise ValueError(f"Unsupported file format: {self.format}")
        
    def write_to_file(self, file_path, data, file_type = None, headers = None):
        """Writes data to file
        params: file_path: str - path to file
                data: list or dict - data to write to file
                file_type: EFileType - type of file to write to, if None then uses default format
                headers: list - headers for file, if None then numerical headers are used. Only used in json if data is not a dictionary"""
        
        format = self.format
        if file_type is not None:
            format = file_type
        file_path = file_path + format.value if not file_path.endswith(format.value) else file_path
        file_exists = os.path(file_path).isfile()

        m = 'a' if file_exists else 'w'
        if headers is None:
            headers = range(0, len(data))
            
        if format == EFileType.CSV:
            with open(file_path, mode=m, newline='') as csvfile:
                self.writer = csv.writer(csvfile)
                self.writer.writerows(data)

        elif format == EFileType.JSON:
            with open(file_path, 'w') as jsonfile:
                json.dump(data, jsonfile)

        elif format == EFileType.TXT:
            with open(file_path, m) as txtfile:
                if isinstance(data, list):
                    for item in data:
                        txtfile.write(f"{item}\n")
                elif isinstance(data, dict):
                    for key, value in data.items():
                        txtfile.write(f"{key}: {value}\n")
                else:
                    raise ValueError("Data must be a list or dictionary for TXT format.")
        else:
            raise ValueError(f"Unsupported file format: {self.format}")