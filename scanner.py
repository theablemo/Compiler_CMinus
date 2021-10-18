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

    def get_next_token(self):
        a = self.inputFile.get_char()
        self.dfa.reset_current_state()  # Make sure that we are at state 0
        token = self._handle_input(a)
        print(token)
        if token is None:
            return self.get_next_token()
        return token

    def print_token(self):
        self.tokenFile.write_token(10, "asdfa", TokenType.KEYWORD)

    def _handle_input(self, initial):
        if input_check.is_EOF(initial):
            return initial, TokenType.END
        if initial.isalpha():
            return self._handle_id_and_keyword(initial)
        elif initial.isnumeric():
            return self._handle_num(initial)
        elif input_check.is_symbol(initial):
            return initial, TokenType.SYMBOL
        elif initial == '=':
            return self._handle_equality(initial)
        elif initial == '*':
            return self._handle_star(initial)
        elif initial == '/':
            return self._handle_comment(initial)
        elif initial.isspace():
            return None
        else:
            self.errorFile.write_error(self.inputFile.lineno, initial, ErrorType.INVALID_INPUT)

    def _handle_id_and_keyword(self, initial):
        token = ""
        token += initial
        self.dfa.move(initial)
        while True:
            character = self.inputFile.get_char()
            self.dfa.move(character)
            if self.dfa.is_accepting_with_return():
                self.inputFile.go_to_previous_char()
                if input_process.is_keyword(token):
                    return token, TokenType.KEYWORD
                self.symbolTableFile.write_identifier(token)
                return token, TokenType.ID
            token += character
            if self.dfa.is_error():
                return self._handle_error(token)

    def _handle_error(self, token, line=-1):
        error = self.dfa.get_error()
        line_num = line if line != -1 else self.inputFile.lineno
        self.errorFile.write_error(line_num, token, error)
        return None

    def _handle_num(self, initial):
        token = ""
        token += initial
        self.dfa.move(initial)
        while True:
            character = self.inputFile.get_char()
            self.dfa.move(character)
            if self.dfa.is_accepting_with_return():
                self.inputFile.go_to_previous_char()
                return token, TokenType.NUM
            token += character
            if self.dfa.is_error():
                return self._handle_error(token)

    def _handle_equality(self, initial):
        token = ""
        token += initial
        self.dfa.move(initial)
        character = self.inputFile.get_char()
        self.dfa.move(character)
        if self.dfa.is_accepting():
            token += character
            return token, TokenType.SYMBOL
        if self.dfa.is_accepting_with_return():
            self.inputFile.go_to_previous_char()
            return token, TokenType.SYMBOL

    def _handle_star(self, initial):
        self.dfa.move(initial)
        character = self.inputFile.get_char()
        self.dfa.move(character)
        if self.dfa.is_accepting_with_return():
            self.inputFile.go_to_previous_char()
            return initial, TokenType.SYMBOL
        if self.dfa.is_error():
            return self._handle_error(initial)

    def _handle_comment(self, initial):
        token = ""
        token += initial
        line_num = self.inputFile.lineno
        self.dfa.move(initial)
        while True:
            character = self.inputFile.get_char()
            token += character
            self.dfa.move(character)
            if self.dfa.is_accepting():
                return None
            if self.dfa.is_error():
                # To write the unclosed comment error with the correct line number, we should pass the "starting
                # line" of the comment, which is line_num
                return self._handle_error(token, line_num)

    def write_token(self, token):
        self.tokenFile.write_token(self.inputFile.lineno, token[0], token[1])
