from enum import Enum

import lexer


class TAGS(Enum):
    IDENTIFIER = 256

    # variables
    VAR = 257
    SET = 258

    # types
    TYPE = 259
    INTEGER = 260
    REAL = 261

    TRUE = 262
    FALSE = 263

    # basic functions
    PRINT = 264

    FUNCTION_CALL = 266


class NODE_TYPES(Enum):
    UNKNOWN = 1
    STATEMENT = 2
    EXPRESSION = 3
    STATEMENTS = 4
    ASSIGNMENT = 5
    IDENTIFIER = 6


global_lexer: lexer.Lexer = None
