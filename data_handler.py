class DataHandler():
    def __init__(self, format):
        self.writer = None
        self.reader = None
    def set_file_type(self, format):
        self.format = format
        #TODO Change readers and writers