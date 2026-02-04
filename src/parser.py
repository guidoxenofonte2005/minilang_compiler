from errors.parse_error import ParseError

from lexer import Token
from globals import global_lexer, TAGS

class Parser:
    def __init__(self):
        self.lookahead: Token = None

    @staticmethod
    def get_current_line() -> int:
        return global_lexer.get_current_line()
    
    def start(self):
        self.lookahead = global_lexer.scan_file()
        return self.program()

    def match_tag(self, tag: any) -> bool:
        if self.lookahead.tag == tag:
            self.lookahead = global_lexer.scan_file()
            return True
        return False

    def program(self):
        self.statement_group()

    def statement_group(self):
        pass

    def block(self):
        if not self.match_tag(ord("{")):
            raise SyntaxError(self.get_current_line(), "'{' esperado")

        statement_group = self.statement_group()

        if not self.match_tag(ord("}")):
            raise SyntaxError(self.get_current_line(), "'}' esperado")

        return statement_group

    def statement(self):
        if self.lookahead.tag == TAGS.VAR.value:
            pass

        elif self.lookahead.tag == TAGS.SET.value:
            pass

        elif self.lookahead.tag == TAGS.PRINT.value:
            return 

        # TODO: adaptar essas tags depois
        # elif self.lookahead.tag == TAGS.IF.value:
        #     pass

        # elif self.lookahead.tag == TAGS.WHILE.value:
        #     pass

        # elif self.lookahead.tag == TAGS.RETURN.value:
        #     pass

        # elif self.lookahead.tag == TAGS.FUNCTION.value:
        #     pass

        elif self.lookahead.tag == ord("{"):
            return self.block()

        else:
            raise SyntaxError
