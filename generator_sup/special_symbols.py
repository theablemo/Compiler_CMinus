from enum import Enum


class SpecialSymbol(Enum):
    SYMBOL_TABLE_STOP = 'STOP',
    BREAK_CHECKPOINT = 'BREAK_CHECKPOINT',
    RETURN_STACK_START = 'RETURN_STACK_START'
