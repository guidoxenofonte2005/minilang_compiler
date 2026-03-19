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
    DEF = 265

    # logical
    AND = 266
    OR = 267
    NOT = 268

    # relational
    GREATER_EQUAL = 269   # >=
    LESSER_EQUAL = 270    # <=
    GREATER = 271         # >
    LESSER = 272          # <
    EQUAL = 273           # ==
    NOT_EQUAL = 274       # !=

    # arithmetic
    PLUS = 275            # +
    MINUS = 276           # -
    MULT = 277            # *
    DIV = 278             # /

    # assignment
    ASSIGN = 279          # =

    # control flow
    IF = 280
    ELSE = 281
    WHILE = 282
    RETURN = 283

    # delimiters
    LPAREN = 284
    RPAREN = 285
    LBRACE = 286
    RBRACE = 287
    COMMA = 288
    SEMICOLON = 289
    COLON = 290

    # string
    STRING = 291
    EOF = 999
    


class NODE_TYPES(Enum):
    UNKNOWN = 1
    STATEMENT = 2
    EXPRESSION = 3
    STATEMENTS = 4
    ASSIGNMENT = 5
    IDENTIFIER = 6
    LOGICAL = 7


global_lexer: "Lexer" = None ### ajuste para evitar circular import
