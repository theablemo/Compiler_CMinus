from IO.file_IO import ErrorType, InputFileIO,LexicalErrorIO
from IO import input_check
class Scanner:
    def __init__(self) -> None:
        self.inputFile = InputFileIO()
        self.errorFile = LexicalErrorIO()

    def do_before_terminate(self):
        self.inputFile.close_file()
        self.errorFile.close_file()
    def get_next_token(self) -> bool:
        end = False
        a = self.inputFile.get_char()
        if input_check.is_EOF(a):
            
            end = True
        print(a)
        return end

