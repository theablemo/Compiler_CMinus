class InputFileIO:
    def __init__(self) -> None:
        self.file = open("input.txt","rt")
    
    def get_char(self):
        return self.file.read(1)