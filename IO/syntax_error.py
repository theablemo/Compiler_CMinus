from parser_sup.error_type import ParserErrorType
from anytree import RenderTree
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
        file.write('#' + str(lineno) + ' : ' + 'syntax error, ' + error_type.value + ' ' + lexeme + '\n')
        file.close()
    

    def print_no_syntax_error(self):
        if not self.syntax_error_found:
            file = open(self.file_name, "at")
            file.write('There is no syntax error.')
            file.close()
    
    def print_unexpected_eof(self, lineno):
        file = open(self.file_name, "at")
        file.write('#' + str(lineno) + ' : ' + 'syntax error, Unexpected EOF' + '\n')
        file.close()
    
class TreeIO:
    def __init__(self, file_name = "parse_tree.txt") -> None:
        self.file_name = file_name
        if os.path.exists(file_name):
            os.remove(file_name)

    def print_tree(self, root):
        file = open(self.file_name, "at")
        for pre, fill, node in RenderTree(root):
            file.write("%s%s" % (pre, node.name) + '\n')
        #     print("%s%s" % (pre, node.name))
        # file.write(line)
        file.close()
    