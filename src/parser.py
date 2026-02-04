from lexer import Token
import globals


class Parser:
    def __init__(self):
        self.lookahead: Token = None

    def match_tag(self, tag: any):
        if self.lookahead.tag == tag:
            self.lookahead = globals.global_lexer.scan_file()
            return True
        return False

    def program(self):
        return self.statement_group()
    
    def statement_group():
        pass