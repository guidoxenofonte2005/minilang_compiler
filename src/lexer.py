from globals import TAGS


class Token:
    def __init__(self, tokenTag: str, tokenValue: any = ""):
        self.tag: str = tokenTag
        self.value: any = tokenValue

    def __str__(self):
        return f"<{self.tag}, {self.value}>" if self.value != "" else f"<{self.tag}>"


class Lexer:
    def __init__(self, file: str):
        self._source_code = file.read()

        self.token_table: dict = {}
        self._current_position: int = 0
        self._current_line: int = 1

        self._init_reserved_table()

    def _init_reserved_table(self):
        # TODO: terminar tabela de palavras reservadas
        self._reserved_table = {
            "var": Token(TAGS.VAR.value, "var"),
            "set": Token(TAGS.SET.value, "set"),
            "int": Token(TAGS.TYPE.value, "int"),
            "real": Token(TAGS.TYPE.value, "real"),
            "bool": Token(TAGS.TYPE.value, "bool"),
            "void": Token(TAGS.TYPE.value, "void"),
            "true": Token(TAGS.TRUE.value, "true"),
            "false": Token(TAGS.FALSE.value, "false"),
            "print": Token(TAGS.PRINT.value, "print"),
        }

    def peek(self, index_advance: int = 0) -> str:
        if self._current_position < len(self._source_code):
            return self._source_code[self._current_position + index_advance]
        return ""

    def _advance_position(self) -> None:
        char: str = self.peek()

        if char != "":
            self._current_position += 1

        if char == "\n":
            self._current_line += 1

        return char

    def scan_file(self) -> Token:
        if not self.peek():
            return Token(0)

        while self.peek().isspace():
            self._advance_position()

        if self.peek().isdigit():
            digit_string: str = ""
            is_decimal: bool = False

            while self.peek() and (self.peek().isdigit() or self.peek() == "."):
                current_char: str = self._advance_position()
                if current_char == ".":
                    if is_decimal:
                        # TODO criar exception específica depois
                        break
                    is_decimal = True
                digit_string += current_char

            if is_decimal:
                return Token(TAGS.REAL.value, digit_string)
            return Token(TAGS.INTEGER.value, digit_string)

        if self.peek().isalnum():
            identifier_string: str = ""
            while self.peek() and self.peek().isalnum():
                identifier_string += self._advance_position()

            if identifier_string in self._reserved_table:
                return self._reserved_table[identifier_string]

            return_token: Token = Token(TAGS.IDENTIFIER.value, identifier_string)
            self.token_table[identifier_string] = return_token

            return return_token

        current_char: str = self.peek()
        if current_char:
            self._advance_position()
            return Token(ord(current_char), current_char)
