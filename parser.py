from enum import Enum, auto
from anytree import Node

from IO.file_IO import TokenType
from parser_sup.non_terminal import first_dictionary, follow_dictionary, NonTerminal

#
# class NonTerminal:
#     def __init__(self, name, first, follow) -> None:
#         self.name = name
#         self.first = first
#         self.follow = follow

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


# class Node:
#     def __init__(self, father_NT, out_links, number) -> None:
#         self.father_NT = father_NT
#         self.out_links = out_links
#         self.number = number
        
class ErrorType(Enum):
    NOT_IN_FOLLOW = auto()
    IN_FOLLOW = auto()
    TERMINALS_NOT_MATCH = auto()


class Parser:
    def __init__(self, scanner) -> None:
        #initialize all terminal, nonterminals, nodes, and links
        #keep nodes in a dict
        self.nodes = {}
        self.current_node = 0
        self.scanner = scanner
        self.lookahead = scanner.get_next_token()
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
        children = []
        parent = Node(NonTerminal.PROGRAM.value)
        while self.current_node != 2:
            if self.current_node == 0:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_LIST):
                    self.current_node = 3
                    children.append(self.declaration_list())
                    self.current_node = 1
                if self._is_in_follow_set(NonTerminal.PROGRAM):
                    # TODO: handle missing NT
                    return None
                else:
                    # TODO: handle invalid input
                    self._move_lookahead()
                    return self.program()
            elif self.current_node == 1:
                if self.lookahead[1] is TokenType.END:
                    self.current_node = 2
                else:
                    # TODO: handle missing token
                    self.current_node = 2
                    self._move_lookahead()
        return self._make_tree(parent, children)

    def declaration_list(self):
        children = []
        parent = Node(NonTerminal.DECLARATION_LIST.value)
        while self.current_node != 5:
            if self.current_node == 3:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION):
                    self.current_node = 6
                    children.append(self.declaration())
                    self.current_node = 4
                if self._is_epsilon_move_valid(NonTerminal.DECLARATION_LIST):
                    return None
                if self._is_in_follow_set(NonTerminal.DECLARATION_LIST):
                    # TODO: handle missing NT
                    return None
                else:
                    # TODO: handle invalid input
                    self._move_lookahead()
                    return self.declaration_list()
            elif self.current_node == 4:
                self.current_node = 3
                children.append(self.declaration_list())
                self.current_node = 5
        return self._make_tree(parent, children)

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

    def _is_nt_edge_valid(self, non_term):
        """
        Return True if we can move with the 'non_term' edge
        """
        token = self.lookahead[0]
        if token in first_dictionary.get(non_term):
            return True
        if '' in first_dictionary.get(non_term) and token in follow_dictionary.get(token):
            return True
        return False

    @staticmethod
    def _make_tree(parent, children):
        """
        :param parent:  Node
        :param children: list of Nodes
        :return: A tree with 'parent' as root and 'children' as its children
        """
        for child in children:
            if child is not None:
                child.parent = parent
        return parent

    def _is_epsilon_move_valid(self, non_term):
        return self.lookahead[0] in follow_dictionary.get(non_term)

    def _move_lookahead(self):
        self.lookahead = self.scanner.get_next_token()

    def _is_in_follow_set(self, non_term):
        return self.lookahead[0] in follow_dictionary(non_term)




