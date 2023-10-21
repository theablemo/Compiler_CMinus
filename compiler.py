# Mohammad Abolnejadian - 98103867
# Matin Daghyani - 98106456
from IO.code_gen_IO import CodeGenIO
from IO.file_IO import TokenType
from code_generator import program_block
from parser import Parser
from scanner import Scanner

scanner = Scanner()

parser = Parser(scanner)
parser.run_parser(make_parse_tree=False)
code_gen_IO = CodeGenIO()
code_gen_IO.save_output(program_block)