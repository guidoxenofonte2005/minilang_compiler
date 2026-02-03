from enum import Enum


class TAGS(Enum):
    IDENTIFIER = 256

    # variables
    VAR = 257
    SET = 258

    # types
    TYPE = 259
    INTEGER = 260
    REAL = 261
    BOOL = 262
    VOID = 263

    TRUE = 264
    FALSE = 265

    # basic functions
    PRINT = 266
