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


