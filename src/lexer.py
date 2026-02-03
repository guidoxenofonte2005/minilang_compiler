from globals import TAGS


class Token:
    def __init__(self, tokenTag: str, tokenValue: any):
        self.tag: str = tokenTag
        self.value: any = tokenValue

    def __str__(self):
        return f"<{self.tag}, {self.value}>"


class Lexer:
    def __init__(self, file: str):
        self._source_code = file.read()

        self.token_table: dict = {}
        self._current_position = 0
        self._current_line = 1

        self._init_reserved_table()

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

    def peek(self) -> str:
        if self._current_position < len(self._source_code):
            return self._source_code[self._current_position]
        return ''
    
    def _advance_position(self) -> None:
        char: str = self.peek()
        
        if char != '':
            self._current_position += 1
        
        if char == '\n':
            self._current_line += 1
        
        return char

