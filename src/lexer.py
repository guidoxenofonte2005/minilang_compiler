from enum import Enum

class TAGS(Enum):
    IDENTIFIER = 256
    INTEGER = 257
    REAL = 258
    BOOL = 259
    VOID = 260

class Token:
    def __init__(self, tokenTag: str, tokenValue: any):
        self.tag: str = tokenTag
        self.value: any = tokenValue

class Lexer:
    def __init__(self):
        self.token_table: dict = {}
        

