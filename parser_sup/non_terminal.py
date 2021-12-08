from enum import Enum
class NonTerminal(Enum):
    PROGRAM = 'Program'
    DECLARATION_LIST = 'Declaration-list'
    DECLARATION = 'Declaration'
    DECLARATION_INITIAL = 'Declaration-initial'
    DECLARATION_PRIME = 'Declaration-prime'
    VAR_DECLARATION_PRIME = 'Var-declaration-prime'
    FUN_DECLARATION_PRIME = 'Fun-declaration-prime'
    TYPE_SPECIFIER = 'Type-specifier'
    PARAMS = 'Params'
    PARAM_LIST = 'Param-list'
    PARAM = 'Param'
    PARAM_PRIME = 'Param-prime'
    COMPOUND_STMT = 'Compound-stmt'
    STATEMENT_LIST = 'Statement-list'
    STATEMENT = 'Statement'
    EXPRESSION_STMT = 'Expression-stmt'
    SELECTION_STMT = 'Selection-stmt'
    ELSE_STMT = 'Else-stmt'
    ITERATION_STMT = 'Iteration-stmt'
    RETURN_STMT = 'Return-stmt'
    RETURN_STMT_PRIME = 'Return-stmt-prime'
    EXPRESSION = 'Expression'
    B = 'B'
    H = 'H'
    SIMPLE_EXPRESSION_ZEGOND = 'Simple-expression-zegond'
    SIMPLE_EXPRESSION_PRIME = 'Simple-expression-prime'
    C = 'C'
    RELOP = 'Relop' 
    ADDITIVE_EXPRESSION = 'Additive-expression'
    ADDITIVE_EXPRESSION_PRIME = 'Additive-expression-prime'
    ADDITIVE_EXPRESSION_ZEGOND = 'Additive-expression-zegond'
    D = 'D'
    ADDOP = 'Addop'
    TERM = 'Term'
    TERM_PRIME = 'Term-prime'
    TERM_ZEGOND = 'Term-zegond'
    G = 'G'
    FACTOR = 'Factor'
    VAR_CALL_PRIME = 'Var-call-prime'
    VAR_PRIME = 'Var-prime'
    FACTOR_PRIME = 'Factor-prime'
    FACTOR_ZEGOND = 'Factor-zegond'
    ARGS = 'Args'
    ARG_LIST = 'Arg-list'
    ARG_LIST_PRIME = 'Arg-list-prime'

#epsilon was shown with '' (empty string)
#end is '$'
first_dictionary = {
    NonTerminal.PROGRAM : {'int', 'void', ''},
    NonTerminal.DECLARATION_LIST : {'int', 'void', ''},
    NonTerminal.DECLARATION : {'int', 'void'},
    NonTerminal.DECLARATION_INITIAL : {'int', 'void'},
    NonTerminal.DECLARATION_PRIME : {';', '[', '(', },
    NonTerminal.VAR_DECLARATION_PRIME : {';', '['},
    NonTerminal.FUN_DECLARATION_PRIME : {'(', },
    NonTerminal.TYPE_SPECIFIER : {'int', 'void'},
    NonTerminal.PARAMS : {'int', 'void'},
    NonTerminal.PARAM_LIST : {',', ''},
    NonTerminal.PARAM : {'int', 'void'},
    NonTerminal.PARAM_PRIME : {'[', ''},
    NonTerminal.COMPOUND_STMT : {'{'},
    NonTerminal.STATEMENT_LIST : {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', ''},
    NonTerminal.STATEMENT : {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'},
    NonTerminal.EXPRESSION_STMT : {'ID', ';', 'NUM', '(', 'break'},
    NonTerminal.SELECTION_STMT : {'if'},
    NonTerminal.ELSE_STMT : {'endif', 'else'},
    NonTerminal.ITERATION_STMT : {'repeat'},
    NonTerminal.RETURN_STMT : {'return'},
    NonTerminal.RETURN_STMT_PRIME : {'ID', ';', 'NUM', '('},
    NonTerminal.EXPRESSION : {'ID', 'NUM', '('},
    NonTerminal.B : {'[', '(', '=', '<', '==', '+', '-', '*', ''},
    NonTerminal.H : {'=', '<', '==', '+', '-', '*', ''},
    NonTerminal.SIMPLE_EXPRESSION_ZEGOND : {'NUM', '('},
    NonTerminal.SIMPLE_EXPRESSION_PRIME : {'(', '<', '==', '+', '-', '*', ''},
    NonTerminal.C : {'<', '==', ''},
    NonTerminal.RELOP : {'<', '=='},
    NonTerminal.ADDITIVE_EXPRESSION : {'ID', 'NUM', '('},
    NonTerminal.ADDITIVE_EXPRESSION_PRIME : {'(', '+', '-', '*', ''},
    NonTerminal.ADDITIVE_EXPRESSION_ZEGOND : {'NUM', '('},
    NonTerminal.D : {'+', '-', ''},
    NonTerminal.ADDOP : {'+', '-'},
    NonTerminal.TERM : {'ID', 'NUM', '('},
    NonTerminal.TERM_PRIME : {'(', '*', ''},
    NonTerminal.TERM_ZEGOND : {'NUM', '('},
    NonTerminal.G : {'*', ''},
    NonTerminal.FACTOR: {'ID', 'NUM', '('},
    NonTerminal.VAR_CALL_PRIME : {'[', '(', ''},
    NonTerminal.VAR_PRIME : {'[', ''},
    NonTerminal.FACTOR_PRIME : {'(', ''},
    NonTerminal.FACTOR_ZEGOND : {'NUM', '('},
    NonTerminal.ARGS : {'ID', 'NUM', '(', ''},
    NonTerminal.ARG_LIST : {'ID', 'NUM', '('},
    NonTerminal.ARG_LIST_PRIME : {',', ''}
}

follow_dictionary = {
    NonTerminal.PROGRAM : {'$'},
    NonTerminal.DECLARATION_LIST : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return', '$'},
    NonTerminal.DECLARATION : {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'},
    NonTerminal.DECLARATION_INITIAL : {';', '[', '(', ')', ','},
    NonTerminal.DECLARATION_PRIME : {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'},
    NonTerminal.VAR_DECLARATION_PRIME : {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'},
    NonTerminal.FUN_DECLARATION_PRIME : {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return', '$'},
    NonTerminal.TYPE_SPECIFIER : {'ID'},
    NonTerminal.PARAMS : {')'},
    NonTerminal.PARAM_LIST : {')'},
    NonTerminal.PARAM : {')', ','},
    NonTerminal.PARAM_PRIME : {')', ','},
    NonTerminal.COMPOUND_STMT : {'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return', '$'},
    NonTerminal.STATEMENT_LIST : {'}'},
    NonTerminal.STATEMENT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.EXPRESSION_STMT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.SELECTION_STMT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.ELSE_STMT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.ITERATION_STMT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.RETURN_STMT : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.RETURN_STMT_PRIME : {'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'},
    NonTerminal.EXPRESSION : {';', ']', ')', ','},
    NonTerminal.B : {';', ']', ')', ','},
    NonTerminal.H : {';', ']', ')', ','},
    NonTerminal.SIMPLE_EXPRESSION_ZEGOND : {';', ']', ')', ','},
    NonTerminal.SIMPLE_EXPRESSION_PRIME : {';', ']', ')', ','},
    NonTerminal.C : {';', ']', ')', ','},
    NonTerminal.RELOP : {'ID', 'NUM', '('},
    NonTerminal.ADDITIVE_EXPRESSION : {';', ']', ')', ','},
    NonTerminal.ADDITIVE_EXPRESSION_PRIME : {';', ']', ')', ',', '<', '=='},
    NonTerminal.ADDITIVE_EXPRESSION_ZEGOND : {';', ']', ')', ',', '<', '=='},
    NonTerminal.D : {';', ']', ')', ',', '<', '=='},
    NonTerminal.ADDOP : {'ID', 'NUM', '('},
    NonTerminal.TERM : {';', ']', ')', ',', '<', '==', '+', '-'},
    NonTerminal.TERM_PRIME : {';', ']', ')', ',', '<', '==', '+', '-'},
    NonTerminal.TERM_ZEGOND : {';', ']', ')', ',', '<', '==', '+', '-'},
    NonTerminal.G : {';', ']', ')', ',', '<', '==', '+', '-'},
    NonTerminal.FACTOR : {';', ']', ')', ',', '<', '==', '+', '-', '*'},
    NonTerminal.VAR_CALL_PRIME : {';', ']', ')', ',', '<', '==', '+', '-', '*'},
    NonTerminal.VAR_PRIME : {';', ']', ')', ',', '<', '==', '+', '-', '*'},
    NonTerminal.FACTOR_PRIME : {';', ']', ')', ',', '<', '==', '+', '-', '*'},
    NonTerminal.FACTOR_ZEGOND : {';', ']', ')', ',', '<', '==', '+', '-', '*'},
    NonTerminal.ARGS : {')'},
    NonTerminal.ARG_LIST : {')'},
    NonTerminal.ARG_LIST_PRIME : {')'}
}

    