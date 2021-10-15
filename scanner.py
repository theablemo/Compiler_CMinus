from IO.fileIO import InputFileIO
class Scanner:
    def __init__(self) -> None:
        self.inputFile = InputFileIO()
    def get_next_token(self) -> bool:
        end = False
        a = self.inputFile.get_char()
        if str(a) == '':
            end = True
        print(a)
        return end
