import json

class Reader:
    def __init__(self, in_file):
        self.in_dir = in_file
    
    def convert_to_dictionary(self):
        with open(self.in_file) as f:
            self.dict = json.load(f)