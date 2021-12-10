# Mohammad Abolnejadian - 98103867
# Matin Daghyani - 98106456
from IO.file_IO import TokenType
from parser import Parser
from scanner import Scanner

scanner = Scanner()

parser = Parser(scanner)
parser.run_parser()