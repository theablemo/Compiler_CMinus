from enum import Enum, auto
from IO import input_check


class Transition(Enum):
    LETTER = auto(),
    DIGIT = auto(),
    LETTER_OR_DIGIT = auto(),
    INVALID_TOKEN = auto(),
    INVALID_TOKEN_OR_LETTER = auto(),
    WHITESPACE = auto(),
    SYMBOL = auto(),
    EOF = auto(),
    ENTER = auto(),
    OTHER1 = auto(),
    OTHER2 = auto(),
    OTHER3 = auto(),
    OTHER4 = auto(),
    OTHER5 = auto(),
    OTHER6 = auto(),
    OTHER7 = auto(),
    NONE = auto(),

    @staticmethod
    def get_transition(c: str, state: str):
        if state == '0' and c.isalpha():
            return Transition.LETTER
        if state == '0' and c.isnumeric():
            return Transition.DIGIT
        if state == '1' and c.isalnum():
            return Transition.LETTER_OR_DIGIT
        if state == '1' and Transition.is_invalid_token(c):
            return Transition.INVALID_TOKEN
        if state == '1' and (c.isalpha() or Transition.is_invalid_token(c)):
            return Transition.INVALID_TOKEN_OR_LETTER
        if state == '1' and (not (Transition.is_invalid_token(c) or c.isalnum())):
            return Transition.OTHER1
        if state == '3' and (not (Transition.is_invalid_token(c) or c.isalpha())):
            return Transition.OTHER2
        if state == '6' and (c != '=' and not Transition.is_invalid_token(c)):
            return Transition.OTHER3
        if state == '8' and (c != '*' or not Transition.is_invalid_token(c)):
            return Transition.OTHER4
        if state == 'b' and input_check.is_newLine(c):
            return Transition.ENTER
        if state == 'b' and not input_check.is_newLine(c):
            return Transition.OTHER5
        if state == 'd' and c != '*':
            return Transition.OTHER6
        if state == 'e' and c != '*' and c != '/':
            return Transition.OTHER7
        if c.isspace():
            return Transition.WHITESPACE
        if input_check.is_symbol(c):
            return Transition.SYMBOL
        if input_check.is_EOF(c):
            return Transition.EOF
        return c

    @staticmethod
    def is_invalid_token(c):
        return not (
                c.isalnum() or
                input_check.is_symbol(c) or
                c == '=' or
                c == '*' or
                c == '/' or
                c.isspace()
        )
