from IO.file_IO import ErrorType, TokenType, InputFileIO,LexicalErrorIO, SymbolTableIO, TokenIO
from IO import input_check
class Scanner:
    def __init__(self) -> None:
        self.inputFile = InputFileIO()
        self.errorFile = LexicalErrorIO()
        self.symbolTableFile = SymbolTableIO()
        self.tokenFile = TokenIO()

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
    
    def print_token(self):
        self.tokenFile.write_token(10,"asdfa",TokenType.KEYWORD)
