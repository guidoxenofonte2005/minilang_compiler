from globals import TAGS


class Token:
    def __init__(self, tokenTag: str, tokenValue: any):
        self.tag: str = tokenTag
        self.value: any = tokenValue
    
    def __str__(self):
        return f"<{self.tag}, {self.value}>"


class Lexer:
    def __init__(self, file: str):
        self.token_table: dict = {}
        self._init_reserved_table()

        for item in self._reserved_table.values():
            print(item)

    def _init_reserved_table(self):
        # TODO: terminar tabela de palavras reservadas
        self._reserved_table = {
            "int": Token(TAGS.INTEGER, "int"),
            "real": Token(TAGS.REAL, "real"),
            "bool": Token(TAGS.BOOL, "bool"),
            "void": Token(TAGS.VOID, "void"),
            "true": Token(TAGS.TRUE, "true"),
            "false": Token(TAGS.FALSE, "false"),
            "print": Token(TAGS.PRINT, "print"),
        }
    

