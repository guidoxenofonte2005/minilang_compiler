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
    ADDITIVE_OP = 267
    MULTIPLICATIVE_OP = 268
    RELATIONAL_OP = 269

    AND = 270
    OR = 271
    NOT = 272

    GREATER_EQUAL = 273
    LESSER_EQUAL = 274
    GREATER = 275
    LESSER = 276
    EQUAL = 277
    NOT_EQUAL = 278


class NODE_TYPES(Enum):
    UNKNOWN = 1
    STATEMENT = 2
    EXPRESSION = 3
    STATEMENTS = 4
    ASSIGNMENT = 5
    IDENTIFIER = 6
    LOGICAL = 7


global_lexer: lexer.Lexer = None
