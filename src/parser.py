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
