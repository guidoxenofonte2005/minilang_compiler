class Token:
    def __init__(self, tokenTag: str, tokenValue: any):
        self.tag: str = tokenTag
        self.value: any = tokenValue


class Lexer:
    def __init__(self):
        self.token_table: dict = {}
