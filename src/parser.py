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
        program := <statement_group>
        """
        return self.statements_group()

    def statements_group(self) -> StatementSequence | None:
        """
        statement_group := <statement> <statement_group> | ε
        """
        if self.lookahead.tag in (
            TAGS.VAR.value,
            TAGS.SET.value,
            TAGS.PRINT.value,
            TAGS.IF.value,
            TAGS.WHILE.value,
            TAGS.RETURN.value,
            TAGS.DEF.value,
            ord("{"),
        ):
            statement = self.statement()
            statement_group = self.statements_group()
            return StatementSequence(statement, statement_group)

        return None
        
    # antes de atualizar remover caso necessario apos o pr
    # def statements(self) -> StatementSequence | None:
    #     """
    #     ### REGRA:
    #     statements := statement statements | ϵ
    #     """
    #     if self.lookahead.tag in (TAGS.IDENTIFIER.value, TAGS.PRINT.value):
    #         statement = self.statement()
    #         statement_group = self.statements()
    #         return StatementSequence(statement, statement_group)

    def statement(self):
        if self.lookahead.tag == TAGS.VAR.value:
                stmt = self.variable_decl()
                if not self.match_tag(ord(";")):
                    raise ParseError("Esperado ';'")
                return stmt
        elif self.lookahead.tag == TAGS.SET.value:
            stmt = self.assignment()
            if not self.match_tag(ord(";")):
                raise ParseError("Esperado ';'")
            return stmt
        elif self.lookahead.tag == TAGS.PRINT.value:
            stmt = self.print_statement()
            if not self.match_tag(ord(";")):
                raise ParseError("Esperado ';'")
            return stmt
        elif self.lookahead.tag == TAGS.IF.value:
            return self.if_statement()
        elif self.lookahead.tag == TAGS.WHILE.value:
            return self.while_statement()
        elif self.lookahead.tag == TAGS.RETURN.value:
            stmt = self.return_statement()
            if not self.match_tag(ord(";")):
                raise ParseError("Esperado ';'")
            return stmt
        elif self.lookahead.tag == TAGS.DEF.value:
            return self.function_decl()
        elif self.lookahead.tag == ord("{"):
            return self.block()
        else:   
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: statement inválido"
            )


    def function_decl(self):
        """
        function-decl := "def" identifier "(" formal_param_optional ")" ":" type block
        """

        if not self.match_tag(TAGS.DEF.value):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado 'def'"
            )

        func_name_token = self.lookahead

        if not self.match_tag(TAGS.IDENTIFIER.value):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado identificador para nome da função"
            )

        if not self.match_tag(ord("(")):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado '(' após nome da função"
            )

        params = self.formal_param_optional()

        if not self.match_tag(ord(")")):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado ')'"
            )

        if not self.match_tag(ord(":")):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado ':'"
            )

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado tipo de retorno da função"
            )

        return_type_token = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        block = self.block()

        return FunctionDecl(func_name_token, params, return_type_token, block)
    
    def formal_param_optional(self):
        """
        <formal_param_optional> := <formal-param> <formal_param_list> | e
        """
        if self.lookahead.tag == TAGS.IDENTIFIER.value:
            param = self.formal_param()
            param_list = self.formal_param_list()
            return FormalParamOptional(param, param_list)
        else:
            return None
    
    def formal_param_list(self):
        """
        <formal_param_list> := "," <formal-param> <formal_param_list> | e
        """
        if self.lookahead.tag == ord(","):
            self.match_tag(ord(","))
            param = self.formal_param()
            param_list = self.formal_param_list()
            return FormalParamList(param, param_list)
        else:
            return None
        
    def formal_param(self):
        """
        <formal-param> := identifier ":" type
        """
        if self.lookahead.tag != TAGS.IDENTIFIER.value:
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado identificador para nome do parâmetro"
            )

        param_name_token = self.lookahead
        self.match_tag(TAGS.IDENTIFIER.value)

        if not self.match_tag(ord(":")):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado ':' após nome do parâmetro"
            )

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado tipo do parâmetro"
            )

        param_type_token = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        return FormalParam(param_name_token, param_type_token)
    
    # antes de atualizar remover caso necessario apos o pr
    # def expression(self) -> Expression:
    #     """
    #     ### REGRA:
    #     expression := simple-expression \{ relational-op simple-expression \}
    #     """
    #     expression = self.simple_expr()

    #     # TODO: fazer checagem de relational-op
    #     while (self.lookahead.tag == TAGS.RELATIONAL_OP.value):
    #         token = self.lookahead
    #         self.match_tag(self.lookahead.tag)
    #         right_hand_expr = self.simple_expr()
    #         expression = LogicalExpr(token, )
    #     return expression

    def expression(self) -> Expression:
        """
        ### REGRA:
        <expression> := <simple-expression> <relational-expression-list>
        """
        expression = self.simple_expression()
        relational_expr_list = self.relational_expression_list()
        return Expression(expression, relational_expr_list)
    def relational_expression_list(self):
        """
        ### REGRA:
        <relational_expression_list> := <relational-op> <simple-expression> <relational_expression_list> | e
        """
        if self.lookahead.tag == TAGS.RELATIONAL_OP.value:
            token = self.lookahead
            self.match_tag(TAGS.RELATIONAL_OP.value)
            simple_expr = self.simple_expression()
            relational_expr_list = self.relational_expression_list()
            return RelationalExpressionList(token, simple_expr, relational_expr_list)
        else:
            return None   
    # antes de atualizar remover caso necessario apos o pr
    # def simple_expr(self):
    #     """
    #     ### REGRA:
    #     simple-expression := term \{ additive-op term \}
    #     """

    #     simple_expression = self.term()

    #     # TODO: fazer checagem de additive-op
    #     while (self.lookahead.tag == TAGS.ADDITIVE_OP.value):
    #         pass

    #     return simple_expression

    def simple_expression(self):
        """
        ### REGRA:
        <simple-expression> := <term> <sum-simple-expression>
        """
        simple_expression = self.term()
        sum_simple_expression = self.sum_simple_expression()
        return SimpleExpression(simple_expression, sum_simple_expression)
    
    # antes de atualizar remover caso necessario apos o pr
    # def term(self):
    #     """
    #     ### REGRA:
    #     term := factor \{ multiplicative-op factor \}
    #     """
    #     term = self.factor()

    #     # TODO: fazer checagem de multiplicative-op
    #     while (self.lookahead.tag == TAGS.MULTIPLICATIVE_OP):
    #         pass

    #     return term

    def term(self):
        left = self.factor()
        rest = self.multiplicative_expr()
        return Term(left, rest)

    def multiplicative_expr(self):
        if self.lookahead.tag == TAGS.MULTIPLICATIVE_OP.value:
            op = self.lookahead
            self.match_tag(TAGS.MULTIPLICATIVE_OP.value)

            right = self.factor()
            next_expr = self.multiplicative_expr()

            return MultiplicativeExpr(op, right, next_expr)

        return None
    
    ##parei por aqui

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
    
    def identifier(self) -> Identifier:
        ### REGRA:
        ## <identifier> := <valid_char> <maybe_valid_char>
        ###
        if self.lookahead.tag != TAGS.IDENTIFIER.value:
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado identificador"
            )
        token = self.lookahead
        self.match_tag(TAGS.IDENTIFIER.value)
        return Identifier(token)