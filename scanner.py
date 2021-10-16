from IO.file_IO import ErrorType, TokenType, InputFileIO, LexicalErrorIO, SymbolTableIO, TokenIO
from IO import input_check, input_process
from dfa import Dfa


class Scanner:
    def __init__(self) -> None:
        self.inputFile = InputFileIO()
        self.errorFile = LexicalErrorIO()
        self.symbolTableFile = SymbolTableIO()
        self.tokenFile = TokenIO()
        self.dfa = Dfa()

    def do_before_terminate(self):
        self.inputFile.close_file()
        self.errorFile.close_file()

    def get_next_token(self) -> bool:
        a = self.inputFile.get_char()
        token = self._handle_input(a)
        if input_check.is_EOF(a):
            return True
        print(a)
        return False

    def print_token(self):
        self.tokenFile.write_token(10, "asdfa", TokenType.KEYWORD)

    def _handle_input(self, initial):
        self.dfa.reset_current_state()  # Make sure that we are at state 0
        if initial.isalpha():
            return self._handle_id_and_keyword(initial)
        elif initial.isnumeric():
            return self._handle_num(initial)
        elif input_check.is_symbol(initial):
            self._handle_symbol(initial)
        elif initial == '=':
            self._handle_equality(initial)
        elif initial == '*':
            self._handle_star(initial)
        elif initial == '/':
            self._handle_comment(initial)
        elif initial.isspace():
            self._handle_whitespace(initial)
        else:
            self.errorFile.write_error(self.inputFile.lineno, initial, ErrorType.INVALID_INPUT)

    def _handle_id_and_keyword(self, initial):
        token = ""
        token += initial
        while True:
            character = self.inputFile.get_char()
            token += character
            self.dfa.move(character)
            if self.dfa.is_accepting_with_return():
                self.inputFile.go_to_previous_char()
                if input_process.is_keyword(token):
                    return token, TokenType.KEYWORD
                return token, TokenType.ID
            if self.dfa.is_error():
                error = self.dfa.get_error()
                self.errorFile.write_error(self.inputFile.lineno, token, error)
                return None


    def _handle_num(self, initial):
        pass

    def _handle_symbol(self, initial):
        pass

    def _handle_equality(self, initial):
        pass

    def _handle_star(self, initial):
        pass

    def _handle_comment(self, initial):
        pass

    def _handle_whitespace(self, initial):
        pass
