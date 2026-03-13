from globals import TAGS


class Token:
    def __init__(self, tokenTag: str, tokenValue: any = ""):
        self.tag: str = tokenTag
        self.value: any = tokenValue

    def __repr__(self):
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
            "and": Token(TAGS.AND.value, "and"),
            "or": Token(TAGS.OR.value, "or"),
            "not": Token(TAGS.NOT.value, "not"),
            "def": Token(TAGS.DEF.value, "def"),
            "print": Token(TAGS.PRINT.value, "print"),
            "if": Token(TAGS.IF.value, "if"),  
            "else": Token(TAGS.ELSE.value, "else"),
            "while": Token(TAGS.WHILE.value, "while"),
            "return": Token(TAGS.RETURN.value, "return"),

        }

    def get_current_line(self) -> int:
        return self._current_line

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

        # numbers
        if self.peek().isdigit():
            digit_string: str = ""
            is_decimal: bool = False

            while self.peek() and (self.peek().isdigit() or self.peek() == "."):
                current_char: str = self._advance_position()
                if current_char == ".":
                    if is_decimal:
                        # TODO: criar exception específica depois
                        break
                    is_decimal = True
                digit_string += current_char

            if is_decimal:
                return Token(TAGS.REAL.value, digit_string)
            return Token(TAGS.INTEGER.value, digit_string)

        # identifiers
        if self.peek().isalpha() or self.peek() == "_":
            identifier_string = ""

            while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
                identifier_string += self._advance_position()

            if identifier_string in self._reserved_table:
                return self._reserved_table[identifier_string]

            token = Token(TAGS.IDENTIFIER.value, identifier_string)
            self.token_table[identifier_string] = token

            return token
        # strings
        if self.peek() == '"':
            self._advance_position() 

            string_value = ""

            while self.peek() and self.peek() != '"':
                string_value += self._advance_position()

            if self.peek() != '"':
                #detecta o erro lexico
                raise Exception(f"String não fechada na linha {self._current_line}")

            self._advance_position()  

            return Token(TAGS.STRING.value, string_value)
        # operators
        current_char: str = self.peek()
        if (
            (current_char == "<")
            and (self._current_position + 1 < len(self._source_code))
            and self._source_code[self._current_position + 1] == "="
        ):
            for i in range(2): self._advance_position()
            return Token(TAGS.LESSER_EQUAL.value, "<=")
        if (
            (current_char == ">")
            and (self._current_position + 1 < len(self._source_code))
            and self._source_code[self._current_position + 1] == "="
        ):
            for i in range(2): self._advance_position()
            return Token(TAGS.GREATER_EQUAL.value, ">=")
        if (
            (current_char == "=")
            and (self._current_position + 1 < len(self._source_code))
            and self._source_code[self._current_position + 1] == "="
        ):
            for i in range(2): self._advance_position()
            return Token(TAGS.EQUAL.value, "==")
        if current_char:
            self._advance_position()
            return Token(ord(current_char), current_char)
        return Token(0)
