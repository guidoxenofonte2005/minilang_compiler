from errors.parse_error import ParseError

from lexer import Token
from globals import global_lexer, TAGS

from abstract_syntax_tree import *


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
        """
        ### REGRA:
        program := \{ statements \}
        """
        return self.statements()

    def statements(self) -> StatementSequence | None:
        """
        ### REGRA:
        statements := statement statements | ϵ
        """
        if self.lookahead.tag in (TAGS.IDENTIFIER.value, TAGS.PRINT.value):
            statement = self.statement()
            statement_group = self.statements()
            return StatementSequence(statement, statement_group)

    def statement(self):
        """
        ### REGRA:
        statement := variable-decl ";"
                    | assignment ";"
                    | print-statement ";"
                    | if-statement
                    | while-statement
                    | return-statement ";"
                    | function-decl ";"
                    | block
        """
        if self.lookahead.tag == TAGS.VAR:
            left_hand_expr: Identifier = self.identifier()
            if not self.match_tag(ord("=")):
                raise ParseError(
                    f"ERRO NA LINHA {self.get_current_line()}: esperado símbolo '=' em atribuição"
                )

            # TODO: expressão à direita da igualdade
            right_hand_expr = self.expression()
            statement: VariableDeclaration = VariableDeclaration(
                left_hand_expr, right_hand_expr
            )
            if not self.match_tag(ord(";")):
                raise ParseError(
                    f"ERRO NA LINHA {self.get_current_line()}: esperado símbolo ';' ao final da linha"
                )

            return statement

    def identifier(self) -> Identifier:
        var_token: Token = self.lookahead

        self.match_tag(TAGS.IDENTIFIER.value)

        return Identifier(token=var_token)

    def expression(self) -> Expression:
        """
        ### REGRA:
        expression := simple-expression \{ relational-op simple-expression \}
        """
        expression = self.simple_expr()

        # TODO: fazer checagem de relational-op
        while (self.lookahead.tag == TAGS.RELATIONAL_OP.value):
            token = self.lookahead
            self.match_tag(self.lookahead.tag)
            right_hand_expr = self.simple_expr()
            expression = LogicalExpr(token, )
        return expression

    def simple_expr(self):
        """
        ### REGRA:
        simple-expression := term \{ additive-op term \}
        """

        simple_expression = self.term()

        # TODO: fazer checagem de additive-op
        while (self.lookahead.tag == TAGS.ADDITIVE_OP.value):
            pass

        return simple_expression

    def term(self):
        """
        ### REGRA:
        term := factor \{ multiplicative-op factor \}
        """
        term = self.factor()

        # TODO: fazer checagem de multiplicative-op
        while (self.lookahead.tag == TAGS.MULTIPLICATIVE_OP):
            pass

        return term

    def factor(self):
        """
        ### REGRA:
        factor := literal
                | identifier
                | function-call
                | sub-expression
                | unary
        """
        # identifier
        if self.lookahead.tag == TAGS.IDENTIFIER.value:
            return self.identifier()

        # sub-expression
        if self.lookahead.tag == ord("("):
            expr: Expression = self.expression()

            if not self.match_tag(ord(")")):
                raise ParseError(
                    f"ERRO NA LINHA {self.get_current_line()}: esperado fechamento de parênteses ')'"
                )
            
            return expr
        
        # unary
        # TODO: refatorar isso
        if self.lookahead.tag in (ord("+"), ord("-"), ord("not")):
            pass

    def unary(self):
        """
        ### REGRA:
        unary := ("+" | "-" | "not") { expression }
        """
        pass

    def sub_expression(self):
        """
        ### REGRA:
        sub-expr := "(" expression ")"
        """
        pass

    def function_call(self):
        """
        ### REGRA:
        function_call := identifier "(" [actual-params] ")"
        """
        pass
