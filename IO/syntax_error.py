from IO.file_IO import ErrorType
from parser_sup import error_type
import os


class SyntaxIO:
    def __init__(self, file_name = "syntax_errors.txt") -> None:
        self.syntax_error_found = False
        self.file_name = file_name
        if os.path.exists(file_name):
            os.remove(file_name)

    def print_syntax_error(self, error_type, lexeme, lineno):
        self.syntax_error_found = True
        file = open(self.file_name, "at")
        file.write('#' + lineno + ' : ' + 'syntax error, ' + error_type.value + ' ' + lexeme)
        file.close()
    

    def print_no_syntax_error(self):
        if not self.syntax_error_found:
            file = open(self.file_name, "at")
            file.write('There is no syntax error.')
            file.close()
    