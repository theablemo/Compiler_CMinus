from enum import Enum, auto


class NonTerminal:
    def __init__(self, name, first, follow) -> None:
        self.name = name
        self.first = first
        self.follow = follow

class Terminal:
    def __init__(self, lexeme) -> None:
        self.lexeme = lexeme

class Link:
    def __init__(self, parameter, father, child) -> None:
        self.parameter = parameter
        self.father = father
        self.child = child
    
    def is_terminal(self):
        if isinstance (self.parameter, Terminal):
            return True
        return False


class Node:
    def __init__(self, father_NT, out_links, number) -> None:
        self.father_NT = father_NT
        self.out_links = out_links
        self.number = number
        
class ErrorType(Enum):
    NOT_IN_FOLLOW = auto()
    IN_FOLLOW = auto()
    TERMINALS_NOT_MATCH = auto()


class Parser:
    def __init__(self) -> None:
        #initialize all terminal, nonterminals, nodes, and links
        #keep nodes in a dict
        self.nodes = {}
        self.current_node = 0
        pass

    def move(self, token):
        node = self.nodes[self.current_node]
        for link in node.out_links:
            if link.is_terminal():
                pass
            else:
                pass
        
    def handle_error(self, error_type):
        pass

    def program(self):
        pass

    def declaration_list(self):
        pass

    def declaration(self):
        pass

    def declaration_initial(self):
        pass

    def declaration_prime(self):
        pass

    def var_declaration_prime(self):
        pass

    def fun_declaration_prime(self):
        pass

    def type_specifier(self):
        pass

    def params(self):
        pass

    def param_list(self):
        pass

    def param(self):
        pass

    def param_prime(self):
        pass

    def compound_stmt(self):
        pass

    def statement_list(self):
        pass

    def statement(self):
        pass

    def expression_stmt(self):
        pass

    def selection_stmt(self):
        pass

    def else_stmt(self):
        pass

    def iteration_stmt(self):
        pass

    def return_stmt(self):
        pass

    def return_stmt_prime(self):
        pass

    def expression(self):
        pass

    def b(self):
        pass

    def h(self):
        pass

    def simple_expression_zegond(self):
        pass

    def simple_expression_prime(self):
        pass

    def c(self):
        pass

    def relop(self):
        pass

    def additive_expression(self):
        pass

    def additive_expression_prime(self):
        pass

    def additive_expression_zegond(self):
        pass

    def d(self):
        pass

    def addop(self):
        pass

    def term(self):
        pass

    def term_prime(self):
        pass

    def term_zegond(self):
        pass

    def g(self):
        pass

    def factor(self):
        pass

    def var_call_prime(self):
        pass

    def var_prime(self):
        pass

    def factor_prime(self):
        pass

    def factor_zegond(self):
        pass

    def args(self):
        pass

    def arg_list(self):
        pass

    def arg_list_prime(self):
        pass



