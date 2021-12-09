# Mohammad Abolnejadian - 98103867
# Matin Daghyani - 98106456
from IO.file_IO import TokenType
import Parser
from scanner import Scanner

scanner = Scanner()
# while (True):
    # token = scanner.get_next_token()
#     if token[1] == TokenType.END:
#         break
#     scanner.write_token(token)

parser = Parser(scanner)
parser.program()


