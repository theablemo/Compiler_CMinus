# Mohammad Abolnejadian - 98103867
# Matin Daghyani - 98106456
from IO.file_IO import TokenIO, InputFileIO, TokenType
from scanner import Scanner

scanner = Scanner()
while (True):
    a = input()
    token = scanner.get_next_token()
    if token[1] == TokenType.END:
        break
    scanner.write_token(token)
