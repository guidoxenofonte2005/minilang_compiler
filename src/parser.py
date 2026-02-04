from errors.parse_error import ParseError

from lexer import Token
import globals


class Parser:
    def __init__(self):
        self.lookahead: Token = None

    @staticmethod
    def get_current_line() -> int:
        return globals.global_lexer.get_current_line()

    def match_tag(self, tag: any) -> bool:
        if self.lookahead.tag == tag:
            self.lookahead = globals.global_lexer.scan_file()
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
        if self.lookahead.tag == globals.TAGS.VAR.value:
            pass

        elif self.lookahead.tag == globals.TAGS.SET.value:
            pass

        elif self.lookahead.tag == globals.TAGS.PRINT.value:
            return 

        # TODO: adaptar essas tags depois
        # elif self.lookahead.tag == globals.TAGS.IF.value:
        #     pass

        # elif self.lookahead.tag == globals.TAGS.WHILE.value:
        #     pass

        # elif self.lookahead.tag == globals.TAGS.RETURN.value:
        #     pass

        # elif self.lookahead.tag == globals.TAGS.FUNCTION.value:
        #     pass

        elif self.lookahead.tag == ord("{"):
            return self.block()

        else:
            raise SyntaxError
