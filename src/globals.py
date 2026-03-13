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
    
    #more basic functions
    IF= 279
    ELSE = 280
    WHILE = 281
    RETURN = 282
    
    #strings opcional
    STRING= 283
    
   
    


class NODE_TYPES(Enum):
    UNKNOWN = 1
    STATEMENT = 2
    EXPRESSION = 3
    STATEMENTS = 4
    VAR_DECLARATION = 5
    ASSIGNMENT = 6
    IF_STATEMENT = 7
    WHILE_STATEMENT = 8
    RETURN_STATEMENT = 9
    FUNCTION_DECLARATION = 10

    IDENTIFIER = 11
    LITERAL = 12
    BINARY_EXPR = 13
    UNARY_EXPR = 14
    FUNCTION_CALL = 15

    FORMAL_PARAMS = 16


global_lexer: "Lexer" = None ### ajuste para evitar circular import
