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
        if isinstance(self.parameter, Terminal):
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
        # initialize all terminal, nonterminals, nodes, and links
        # keep nodes in a dict
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
                    self._handle_missing_non_term(NonTerminal.PROGRAM.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.program()
            elif self.current_node == 1:
                if self.lookahead[1] is TokenType.END:
                    self._add_leaf_to_tree(children, parent, 2)
                else:
                    self._handle_missing_token("$", 2)
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
                    self._handle_missing_non_term(NonTerminal.DECLARATION_LIST.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration_list()
            elif self.current_node == 4:
                self.current_node = 3
                children.append(self.declaration_list())
                self.current_node = 5
        return self._make_tree(parent, children)

    def declaration(self):
        parent = Node(NonTerminal.DECLARATION.value)
        children = []
        while self.current_node != 8:
            if self.current_node == 6:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_INITIAL):
                    self.current_node = 9
                    children.append(self.declaration_initial())
                    self.current_node = 7
                elif self._is_in_follow_set(NonTerminal.DECLARATION):
                    self._handle_missing_non_term(NonTerminal.DECLARATION.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration()
            if self.current_node == 7:
                self.current_node = 12
                children.append(self.declaration_prime())
                self.current_node = 9
        return self._make_tree(parent, children)

    def declaration_initial(self):
        parent = Node(NonTerminal.DECLARATION_INITIAL.value)
        children = []
        while self.lookahead != 11:
            if self.current_node == 9:
                if self._is_nt_edge_valid(NonTerminal.TYPE_SPECIFIER):
                    self.current_node = 25
                    children.append(self.type_specifier())
                    self.current_node = 10
                elif self._is_in_follow_set(NonTerminal.DECLARATION):
                    self._handle_missing_non_term(NonTerminal.DECLARATION_INITIAL.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration_initial()
            if self.current_node == 10:
                self._move_terminal_edge(children, parent, TokenType.ID, 11)
        return self._make_tree(parent, children)

    def declaration_prime(self):
        parent = Node(NonTerminal.DECLARATION_PRIME.value)
        children = []
        while self.current_node != 13:
            if self._is_nt_edge_valid(NonTerminal.FUN_DECLARATION_PRIME):
                self.current_node = 20
                children.append(self.fun_declaration_prime())
                self.current_node = 13
            elif self._is_nt_edge_valid(NonTerminal.VAR_DECLARATION_PRIME):
                self.current_node = 14
                children.append(self.var_declaration_prime())
                self.current_node = 13
            elif self._is_in_follow_set(NonTerminal.DECLARATION_PRIME):
                self._handle_missing_non_term(NonTerminal.DECLARATION_PRIME.value)
                return None
            else:
                self._handle_invalid_input()
                return self.declaration_prime()
        return self._make_tree(parent, children)

    def var_declaration_prime(self):
        parent = Node(NonTerminal.VAR_DECLARATION_PRIME.value)
        children = []
        while self.current_node != 19:
            if self.current_node == 14:
                if self.lookahead[0] == '[':
                    self._add_leaf_to_tree(children, parent, 15)
                elif self.lookahead[0] == ';':
                    self._add_leaf_to_tree(children, parent, 19)
                elif self._is_in_follow_set(NonTerminal.VAR_DECLARATION_PRIME):
                    self._handle_missing_non_term(NonTerminal.VAR_DECLARATION_PRIME.value)
                    return None
                else:
                    # TODO: which edge ??!
                    self._handle_missing_token('[', 15)
            elif self.current_node == 15:
                self._move_terminal_edge(children, parent, TokenType.NUM, 17)
            elif self.current_node == 17:
                self._move_terminal_edge(children, parent, ']', 18)
            elif self.current_node == 18:
                if self.lookahead[0] == ';':
                    self._move_terminal_edge(children, parent, ';', 19)
        return self._make_tree(parent, children)

    def fun_declaration_prime(self):
        parent = Node(NonTerminal.FUN_DECLARATION_PRIME.value)
        children = []
        while self.current_node != 24:
            if self.current_node == 20:
                if self.lookahead[0] == '(':
                    self._add_leaf_to_tree(children, parent, 21)
                elif self._is_in_follow_set(NonTerminal.FUN_DECLARATION_PRIME):
                    self._handle_missing_non_term(NonTerminal.FUN_DECLARATION_PRIME.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.fun_declaration_prime()
            elif self.current_node == 21:
                self.current_node = 27
                children.append(self.params())
                self.current_node = 22
            elif self.current_node == 22:
                self._move_terminal_edge(children, parent, ')', 23)
            elif self.current_node == 23:
                self.current_node = 42
                children.append(self.compound_stmt())
                self.current_node = 24
        return self._make_tree(parent, children)

    def type_specifier(self):
        parent = Node(NonTerminal.TYPE_SPECIFIER.value)
        children = []
        while self.current_node != 26:
            if self.current_node == 25:
                if self.lookahead[0] == 'int':
                    self._add_leaf_to_tree(children, parent, 26)
                elif self.lookahead[0] == 'void':
                    self._add_leaf_to_tree(children, parent, 26)
                if self._is_in_follow_set(NonTerminal.TYPE_SPECIFIER):
                    self._handle_missing_non_term(NonTerminal.TYPE_SPECIFIER.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.type_specifier()

    def params(self):
        parent = Node(NonTerminal.PARAMS.value)
        children = []
        while self.current_node != 31:
            if self.current_node == 27:
                if self.lookahead[0] == 'int':
                    self._add_leaf_to_tree(children, parent, 28)
                elif self.lookahead[0] == 'void':
                    self._add_leaf_to_tree(children, parent, 31)
                elif self._is_in_follow_set(NonTerminal.PARAMS):
                    self._handle_missing_non_term(NonTerminal.PARAMS.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.params()
            elif self.current_node == 28:
                self._move_terminal_edge(children, parent, TokenType.ID, 29)
            elif self.current_node == 29:
                self.current_node = 39
                children.append(self.param_prime())
                self.current_node = 30
            elif self.current_node == 30:
                self.current_node = 32
                self.param_list()
                self.current_node = 31
        return self._make_tree(parent, children)

    def param_list(self):
        parent = Node(NonTerminal.PARAM_LIST.value)
        children = []
        while self.current_node != 35:
            if self.current_node == 32:
                if self.lookahead[0] == ',':
                    self._add_leaf_to_tree(children, parent, 33)
                elif self._is_epsilon_move_valid(NonTerminal.PARAM_LIST):
                    return None
                elif self._is_in_follow_set(NonTerminal.PARAM_LIST):
                    self._handle_missing_non_term(NonTerminal.PARAMS.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.param_list()
            elif self.current_node == 33:
                self.current_node = 36
                children.append(self.param())
                self.current_node = 34
            elif self.current_node == 34:
                self.current_node = 32
                children.append(self.param_list())
                self.current_node = 35
        return self._make_tree(parent, children)

    def param(self):
        parent = Node(NonTerminal.PARAM.value)
        children = []
        while self.current_node != 38:
            if self.current_node == 36:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_INITIAL):
                    self.current_node = 9
                    children.append(self.declaration_initial())
                    self.current_node = 37
                if self._is_in_follow_set(NonTerminal.DECLARATION_INITIAL):
                    self._handle_missing_non_term(NonTerminal.PARAM.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.param()
            elif self.current_node == 37:
                self.current_node = 39
                children.append(self.param_prime())
                self.current_node = 38
        return self._make_tree(parent, children)

    def param_prime(self):
        parent = Node(NonTerminal.PARAM_PRIME.value)
        children = []
        while self.current_node != 41:
            if self.current_node == 39:
                if self.lookahead[0] == '[':
                    self._add_leaf_to_tree(children, parent, 40)
                elif self._is_epsilon_move_valid(NonTerminal.PARAM_PRIME):
                    return None
                elif self._is_in_follow_set(NonTerminal.PARAM_PRIME):
                    self._handle_missing_non_term(NonTerminal.PARAM_PRIME.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.param_prime()
            elif self.current_node == 40:
                self._move_terminal_edge(children, parent, ']', 41)
        return self._make_tree(parent, children)

    def compound_stmt(self):
        parent = Node(NonTerminal.COMPOUND_STMT.value)
        children = []
        while self.current_node != 46:
            if self.current_node == 42:
                if self.lookahead[0] == '{':
                    self._add_leaf_to_tree(children, parent, 43)
                elif self._is_in_follow_set(NonTerminal.COMPOUND_STMT):
                    self._handle_missing_non_term(NonTerminal.COMPOUND_STMT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.compound_stmt()
            elif self.current_node == 43:
                self.current_node = 3
                children.append(self.declaration_list())
                self.current_node = 44
            elif self.current_node == 44:
                self.current_node = 47
                children.append(self.statement_list())
                self.current_node = 45
            elif self.current_node == 45:
                self._move_terminal_edge(children, parent, '}', 46)
        return self._make_tree(parent, children)

    def statement_list(self):
        parent = Node(NonTerminal.STATEMENT_LIST.value)
        children = []
        while self.current_node != 49:
            if self.current_node == 47:
                if self._is_nt_edge_valid(NonTerminal.STATEMENT):
                    self.current_node = 50
                    children.append(self.statement())
                    self.current_node = 48
                elif self._is_epsilon_move_valid(NonTerminal.STATEMENT_LIST):
                    return None
                elif self._is_in_follow_set(NonTerminal.STATEMENT_LIST):
                    self._handle_missing_non_term(NonTerminal.STATEMENT_LIST.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.statement_list()
            elif self.current_node == 48:
                self.current_node = 47
                children.append(self.statement_list())
                self.current_node = 49
        return self._make_tree(parent, children)

    def statement(self):
        parent = Node(NonTerminal.STATEMENT.value)
        children = []
        while self.current_node != 51:
            if self.current_node == 50:
                if self._is_nt_edge_valid(NonTerminal.EXPRESSION_STMT):
                    self.current_node = 52
                    children.append(self.expression_stmt())
                    self.current_node = 51
                elif self._is_nt_edge_valid(NonTerminal.COMPOUND_STMT):
                    self.current_node = 42
                    children.append(self.compound_stmt())
                    self.current_node = 51
                elif self._is_nt_edge_valid(NonTerminal.SELECTION_STMT):
                    self.current_node = 56
                    children.append(self.selection_stmt())
                    self.current_node = 51
                elif self._is_nt_edge_valid(NonTerminal.ITERATION_STMT):
                    self.current_node = 67
                    children.append(self.iteration_stmt())
                    self.current_node = 51
                elif self._is_nt_edge_valid(NonTerminal.RETURN_STMT):
                    self.current_node = 74
                    children.append(self.return_stmt())
                    self.current_node = 51
                elif self._is_in_follow_set(NonTerminal.STATEMENT):
                    self._handle_missing_non_term(NonTerminal.STATEMENT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.statement()
        return self._make_tree(parent, children)

    def expression_stmt(self):
        parent = Node(NonTerminal.EXPRESSION_STMT.value)
        children = []
        while self.current_node != 55:
            if self.current_node == 52:
                if self._is_nt_edge_valid(NonTerminal.EXPRESSION):
                    self.current_node = 80
                    children.append(self.expression())
                    self.current_node = 54
                elif self.lookahead[0] == 'break':
                    self._add_leaf_to_tree(children, parent, 53)
                elif self.lookahead[0] == ';':
                    self._add_leaf_to_tree(children, parent, 55)
                elif self._is_in_follow_set(NonTerminal.EXPRESSION_STMT):
                    self._handle_missing_non_term(NonTerminal.EXPRESSION_STMT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.expression_stmt()
            elif self.current_node == 54:
                self._move_terminal_edge(children, parent, ';', 55)
            elif self.current_node == 53:
                self._move_terminal_edge(children, parent, ';', 55)
        return self._make_tree(parent, children)

    def selection_stmt(self):
        parent = Node(NonTerminal.SELECTION_STMT.value)
        children = []
        while self.current_node != 62:
            if self.current_node == 56:
                if self.lookahead[0] == 'if':
                    self._add_leaf_to_tree(children, parent, 57)
                elif self._is_in_follow_set(NonTerminal.SELECTION_STMT):
                    self._handle_missing_non_term(NonTerminal.SELECTION_STMT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.statement_list()
            elif self.current_node == 57:
                self._move_terminal_edge(children, parent, '(', 58)
            elif self.current_node == 58:
                self.current_node = 80
                children.append(self.expression())
                self.current_node = 59
            elif self.current_node == 59:
                self._move_terminal_edge(children, parent, ')', 60)
            elif self.current_node == 60:
                self.current_node = 50
                children.append(self.statement())
                self.current_node = 61
            elif self.current_node == 61:
                self.current_node = 63
                children.append(self.else_stmt())
                self.current_node = 62
        return self._make_tree(parent, children)

    def else_stmt(self):
        parent = Node(NonTerminal.ELSE_STMT.value)
        children = []
        while self.current_node != 66:
            if self.current_node == 63:
                if self.lookahead[0] == 'else':
                    self._add_leaf_to_tree(children, parent, 64)
                elif self.lookahead[0] == 'endif':
                    self._add_leaf_to_tree(children, parent, 66)
                elif self._is_in_follow_set(NonTerminal.ELSE_STMT):
                    self._handle_missing_non_term(NonTerminal.ELSE_STMT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.else_stmt()
            elif self.current_node == 64:
                self.current_node = 50
                children.append(self.statement())
                self.current_node = 65
            elif self.current_node == 65:
                self._move_terminal_edge(children, parent, 'endif', 66)
        return self._make_tree(parent, children)

    def iteration_stmt(self):
        parent = Node(NonTerminal.ITERATION_STMT.value)
        children = []
        while self.current_node != 73:
            if self.current_node == 67:
                if self.lookahead[0] == 'repeat':
                    self._add_leaf_to_tree(children, parent, 68)
                elif self._is_in_follow_set(NonTerminal.ITERATION_STMT):
                    self._handle_missing_non_term(NonTerminal.ITERATION_STMT.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.iteration_stmt()
            elif self.current_node == 68:
                self.current_node = 50
                children.append(self.statement())
                self.current_node = 69
            elif self.current_node == 69:
                self._move_terminal_edge(children, parent, 'until', 70)
            elif self.current_node == 70:
                self._move_terminal_edge(children, parent, '(', 71)
            elif self.current_node == 71:
                self.current_node = 80
                children.append(self.expression())
                self.current_node = 72
            elif self.current_node == 72:
                self._move_terminal_edge(children, parent, ')', 73)
        return self._make_tree(parent, children)

    def return_stmt(self):
        parent = Node(NonTerminal.RETURN_STMT.value)
        children = []
        while self.current_node != 76:
            if self.current_node == 74:
                if self.lookahead[0] == 'return':
                    self._add_leaf_to_tree(children, parent, 75)
                elif self._is_in_follow_set(NonTerminal.RETURN_STMT):
                    self._handle_missing_non_term(NonTerminal.RETURN_STMT.value)
                    return None
            elif self.current_node == 75:
                self.current_node = 77
                children.append(self.return_stmt_prime())
                self.current_node = 76
        return self._make_tree(parent, children)

    def return_stmt_prime(self):
        parent = Node(NonTerminal.RETURN_STMT_PRIME.value)
        children = []
        while self.current_node != 79:
            if self.current_node == 77:
                if self._is_nt_edge_valid(NonTerminal.EXPRESSION):
                    self.current_node = 80
                    children.append(self.expression())
                    self.current_node = 78
                elif self.lookahead[0] == ';':
                    self._add_leaf_to_tree(children, parent, 79)
                elif self._is_in_follow_set(NonTerminal.RETURN_STMT_PRIME):
                    self._handle_missing_non_term(NonTerminal.RETURN_STMT_PRIME.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.return_stmt_prime()
            elif self.current_node == 78:
                self._move_terminal_edge(children, parent, ';', 79)
        return self._make_tree(parent, children)

    def expression(self):
        parent = Node(NonTerminal.EXPRESSION.value)
        children = []
        while self.current_node != 82:
            if self.current_node == 80:
                if self._is_nt_edge_valid(NonTerminal.SIMPLE_EXPRESSION_ZEGOND):
                    self.current_node = 94
                    children.append(self.simple_expression_zegond())
                    self.current_node = 82
                elif self.lookahead[1] is TokenType.ID:
                    self._add_leaf_to_tree(children, parent, 81)
                elif self._is_in_follow_set(NonTerminal.EXPRESSION):
                    self._handle_missing_non_term(NonTerminal.EXPRESSION.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.expression()
            elif self.current_node == 81:
                self.current_node = 83
                children.append(self.b())
                self.current_node = 82
        return self._make_tree(parent, children)

    def b(self):
        parent = Node(NonTerminal.B.value)
        children = []
        while self.current_node != 88:
            if self.current_node == 83:
                if self._is_nt_edge_valid(NonTerminal.SIMPLE_EXPRESSION_PRIME):
                    self.current_node = 97
                    children.append(self.simple_expression_prime())
                    self.current_node = 88
                elif self.lookahead[0] == '[':
                    self._add_leaf_to_tree(children, parent, 84)
                elif self.lookahead[0] == '=':
                    self._add_leaf_to_tree(children, parent, 87)
                elif self._is_in_follow_set(NonTerminal.B):
                    self._handle_missing_non_term(NonTerminal.B.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.b()
            elif self.current_node == 87:
                self.current_node = 80
                children.append(self.expression())
                self.current_node = 88
            elif self.current_node == 84:
                self.current_node = 80
                children.append(self.expression())
                self.current_node = 85
            elif self.current_node == 85:
                self._move_terminal_edge(children, parent, ']', 86)
            elif self.current_node == 86:
                self.current_node = 89
                children.append(self.h())
                self.current_node = 88
        return self._make_tree(parent, children)

    def h(self):
        parent = Node(NonTerminal.H.value)
        children = []
        while self.current_node != 93:
            if self.current_node == 89:
                if self.lookahead[0] == '=':
                    self._add_leaf_to_tree(children, parent, 92)
                elif self._is_nt_edge_valid(NonTerminal.G):
                    self.current_node = 129
                    children.append(self.g())
                    self.current_node = 90
                elif self._is_in_follow_set(NonTerminal.H):
                    self._handle_missing_non_term(NonTerminal.H.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.h()
            elif self.current_node == 92:
                self.current_node = 80
                children.append(self.expression())
                self.current_node = 93
            elif self.current_node == 90:
                self.current_node = 114
                children.append(self.d())
                self.current_node = 91
            elif self.current_node == 91:
                self.current_node = 100
                children.append(self.c())
                self.current_node = 93
        return self._make_tree(parent, children)

    def simple_expression_zegond(self):
        parent = Node(NonTerminal.ADDITIVE_EXPRESSION_ZEGOND.value)
        children = []
        while self.current_node != 96:
            if self.current_node == 94:
                if self._is_nt_edge_valid(NonTerminal.ADDITIVE_EXPRESSION_ZEGOND):
                    self.current_node = 111
                    children.append(self.additive_expression_zegond())
                    self.current_node = 95
                elif self._is_in_follow_set(NonTerminal.SIMPLE_EXPRESSION_ZEGOND):
                    self._handle_missing_non_term(NonTerminal.SIMPLE_EXPRESSION_ZEGOND.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.simple_expression_zegond()
            elif self.current_node == 95:
                self.current_node = 100
                children.append(self.c())
                self.current_node = 96
        return self._make_tree(parent, children)

    def simple_expression_prime(self):
        parent = Node(NonTerminal.ADDITIVE_EXPRESSION_PRIME.value)
        children = []
        while self.current_node != 99:
            if self.current_node == 97:
                if self._is_nt_edge_valid(NonTerminal.ADDITIVE_EXPRESSION_PRIME):
                    self.current_node = 108
                    children.append(self.additive_expression_prime())
                    self.current_node = 98
                elif self._is_in_follow_set(NonTerminal.SIMPLE_EXPRESSION_PRIME):
                    self._handle_missing_non_term(NonTerminal.SIMPLE_EXPRESSION_PRIME.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.simple_expression_prime()
            elif self.current_node == 98:
                self.current_node = 100
                children.append(self.c())
                self.current_node = 99
        return self._make_tree(parent, children)

    def c(self):
        parent = Node(NonTerminal.C.value)
        children = []
        while self.current_node != 102:
            if self.current_node == 100:
                if self._is_nt_edge_valid(NonTerminal.RELOP):
                    self.current_node = 103
                    children.append(self.relop())
                    self.current_node = 101
                elif self._is_epsilon_move_valid(NonTerminal.C):
                    return None
                elif self._is_in_follow_set(NonTerminal.C):
                    self._handle_missing_non_term(NonTerminal.C.value)
                else:
                    self._handle_invalid_input()
                    return self.c()
            elif self.current_node == 101:
                self.current_node = 105
                children.append(self.additive_expression())
                self.current_node = 102
        return self._make_tree(parent, children)

    def relop(self):
        parent = Node(NonTerminal.RELOP.value)
        children = []
        while self.current_node != 104:
            if self.current_node == 103:
                if self.lookahead[0] == '<':
                    self._add_leaf_to_tree(children, parent, 104)
                elif self.lookahead[0] == '==':
                    self._add_leaf_to_tree(children, parent, 104)
                elif self._is_in_follow_set(NonTerminal.RELOP):
                    self._handle_missing_non_term(NonTerminal.RELOP.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.relop()
        return self._make_tree(parent, children)

    def additive_expression(self):
        parent = Node(NonTerminal.ADDITIVE_EXPRESSION.value)
        children = []
        while self.current_node != 107:
            if self.current_node == 105:
                if self._is_nt_edge_valid(NonTerminal.TERM):
                    self.current_node = 120
                    children.append(self.term())
                    self.current_node = 106
                elif self._is_in_follow_set(NonTerminal.ADDITIVE_EXPRESSION):
                    self._handle_missing_non_term(NonTerminal.ADDITIVE_EXPRESSION.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.additive_expression()
            elif self.current_node == 106:
                self.current_node = 114
                children.append(self.d())
                self.current_node = 107
        return self._make_tree(parent, children)

    def additive_expression_prime(self):
        parent = Node(NonTerminal.ADDITIVE_EXPRESSION_PRIME.value)
        children = []
        while self.current_node != 110:
            if self.current_node == 108:
                if self._is_nt_edge_valid(NonTerminal.TERM_PRIME):
                    self.current_node = 123
                    children.append(self.term_prime())
                    self.current_node = 109
                elif self._is_in_follow_set(NonTerminal.ADDITIVE_EXPRESSION_PRIME):
                    self._handle_missing_non_term(NonTerminal.ADDITIVE_EXPRESSION_PRIME.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.additive_expression_prime()
            elif self.current_node == 109:
                self.current_node = 114
                children.append(self.d())
                self.current_node = 110
        return self._make_tree(parent, children)

    def additive_expression_zegond(self):
        parent = Node(NonTerminal.ADDITIVE_EXPRESSION_ZEGOND.value)
        children = []
        while self.current_node != 113:
            if self.current_node == 111:
                if self._is_nt_edge_valid(NonTerminal.TERM_ZEGOND):
                    self.current_node = 126
                    children.append(self.term_zegond())
                    self.current_node = 112
                elif self._is_in_follow_set(NonTerminal.ADDITIVE_EXPRESSION_ZEGOND):
                    self._handle_missing_non_term(NonTerminal.ADDITIVE_EXPRESSION_ZEGOND.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.additive_expression_zegond()
            elif self.current_node == 112:
                self.current_node = 114
                children.append(self.d())
                self.current_node = 113
        return self._make_tree(parent, children)

    def d(self):
        parent = Node(NonTerminal.D.value)
        children = []
        while self.current_node != 117:
            if self.current_node == 114:
                if self._is_nt_edge_valid(NonTerminal.ADDOP):
                    self.current_node = 118
                    children.append(self.addop())
                    self.current_node = 115
                elif self._is_epsilon_move_valid(NonTerminal.D):
                    return None
                else:
                    self._handle_invalid_input()
                    return self.d()
            elif self.current_node == 115:
                self.current_node = 120
                children.append(self.term())
                self.current_node = 116
            elif self.current_node == 116:
                self.current_node = 114
                children.append(self.d())
                self.current_node = 117
        return self._make_tree(parent, children)

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

    def _get_leaf_node(self, parent):
        return Node(str((self.lookahead[0], self.lookahead[1])), parent)

    def _handle_missing_non_term(self, non_term: str):
        # TODO: write error
        pass

    def _handle_invalid_input(self):
        # TODO: write invalid input
        self._move_lookahead()

    def _handle_missing_token(self, missed, next_state):
        # TODO: handle missing token
        self.current_node = next_state

    def _add_leaf_to_tree(self, children, parent, next):
        children.append(self._get_leaf_node(parent))
        self._move_lookahead()
        self.current_node = next

    def _move_terminal_edge(self, children, parent, expected, next):
        """
        This method makes move on terminal edges. If there is a mismatch, it will handle the error
        It also adds a leaf node to 'children list"
        ATTENTION: TRY NOT TO USE THIS FUNCTION FOR INITIAL STATES.
        :param children:
        :param parent:
        :param expected: the expected token (on the edge). It can be a string or a token TokenType(like: TokenType.ID)
        :param next: the next state that we should go
        :return:
        """
        if type(expected) == str:
            if self.lookahead[0] == expected:
                self._add_leaf_to_tree(children, parent, next)
            else:
                self._handle_missing_token(expected, next)
        else:
            if self.lookahead[1] is expected:
                self._add_leaf_to_tree(children, parent, next)
            else:
                self._handle_missing_token(expected.value, next)
