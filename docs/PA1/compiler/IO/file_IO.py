import os
from IO import input_check, input_process
from enum import Enum
class InputFileIO:
    
    def __init__(self) -> None:
        self.file = open("input.txt","rt")
        self.lineno = 1
        self.inputStack = []
        self.previous_char_stack = []
        self.previous_char_count = 0
        self.previous_char = ''
        self.backed = False
    
    def get_char(self):
        if not input_check.is_EOF(self.previous_char) and ord(self.previous_char) == 10:
            if not self.backed:
                self.lineno += 1
            # else:
            #     self.lineno -= 1
        
        if self.previous_char_count == 0:
            a = self.file.read(1)
            self.backed = False
        else:
            a = self.previous_char_stack.pop()
            self.previous_char_count -= 1
            self.backed = True
        self.previous_char = a

        self.inputStack.append(a)
        if len(self.inputStack) > 5:
            self.inputStack.reverse()
            self.inputStack.pop()
            self.inputStack.reverse()
        # if not input_check.is_EOF(a) and ord(a) == 10:
        #     self.lineno += 1

        #printing outputs
        # if self.lineno < 10:
        #     if ord(a) < 127 and ord(a) > 32:
        #         print(f"{self.lineno}: {a}")
        #     else:
        #         print(f"{self.lineno}: ord({ord(a)})")
            
        return a

    def go_to_previous_char(self):
        self.previous_char_stack.append(self.inputStack.pop())
        self.previous_char_count += 1

    def close_file(self):
        self.file.close()

class ErrorType(Enum):
    INVALID_INPUT = 'Invalid input'
    INVALID_NUMBER = 'Invalid number'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UNMACHED_COMMENT = 'Unmatched comment'

#Writes error in the file after termination
class LexicalErrorIO:
    def __init__(self) -> None:
        if os.path.exists("lexical_errors.txt"):
            os.remove("lexical_errors.txt")
        self.file = open("lexical_errors.txt","at")
        self.written = False
        self.current_lineno = 0
    
    def write_error(self,lineno: int,lexeme: str,errorType: ErrorType):
        if errorType == ErrorType.UNCLOSED_COMMENT and len(lexeme) > 7:
            lexeme = input_process.truncate_unclosed_comment(lexeme)
        if lineno != self.current_lineno:
            # self.file.write(str(lineno)+'.' + chr(9) + '(' + lexeme + ', ' + errorType.value + ') ' + chr(10))
            if self.written:
                self.file.write(chr(10))
            self.file.write(str(lineno)+'.' + chr(9) + '(' + lexeme + ', ' + errorType.value + ') ')
            self.current_lineno = lineno
        else:
            self.file.write('(' + lexeme + ', ' + errorType.value + ') ')
        self.written = True
        
    def close_file(self):
        if self.written == False:
            self.file.write('There is no lexical error.')
        else:
            self.file.write(chr(10))
        self.file.close()

#Writes symbols one at a time
class SymbolTableIO:
    def __init__(self) -> None:
        if os.path.exists("symbol_table.txt"):
            os.remove("symbol_table.txt")
        self.file = open("symbol_table.txt", "wt")
        self.file.write(input_process.write_keywords())
        self.entry_count = input_process.number_of_keywords()+ 1
        self.file.close()
        self.identifiers = set()

    def write_identifier(self, lexeme: str):
        if lexeme not in self.identifiers:
            self.identifiers.add(lexeme)
            self.file = open("symbol_table.txt", "at")
            self.file.write(str(self.entry_count) + '.' + chr(9) + lexeme + chr(10))
            self.entry_count += 1
            self.file.close()


class TokenType(Enum):
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    SYMBOL = 'SYMBOL'
    END = 'END'

#Writes tokens one at a time
class TokenIO:
    def __init__(self) -> None:
        if os.path.exists("tokens.txt"):
            os.remove("tokens.txt")
        self.current_lineno = 1
        self.has_written = False
    def write_token(self, lineno: int, lexeme: str, token_type: TokenType):
        file = open("tokens.txt" , "at")
        if not self.has_written:
            file.write(str(lineno) + '.' + chr(9))
            self.has_written = True
            self.current_lineno = lineno
        if self.current_lineno != lineno:
            file.write(chr(10) + str(lineno) + '.' + chr(9))
            self.current_lineno = lineno
        file.write('(' + token_type.value + ', ' + lexeme  + ') ')
        file.close()


