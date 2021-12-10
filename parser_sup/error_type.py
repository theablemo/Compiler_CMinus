from enum import Enum
class ParserErrorType(Enum):
    MISSING = 'missing'
    ILLEGAL = 'illegal'
    # NOT_IN_FOLLOW = auto()
    # IN_FOLLOW = auto()
    # TERMINALS_NOT_MATCH = auto()