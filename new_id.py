import string
from random import choices

class NewID():

    def __init__(self):
        # ID data strings
        self.characters = string.ascii_letters + string.digits
    
    def generate(self, length=16):
        id_string = "".join(choices(self.characters, k=length))
        return id_string