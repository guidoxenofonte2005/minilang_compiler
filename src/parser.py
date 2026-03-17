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
    
    def block(self):
        """
        ### REGRA:
        <block> := "{" <statement_group> "}"
        """
        if not self.match_tag(ord("{")):
            raise ParseError("Esperado '{'")

        stmts = self.statements_group()

        if not self.match_tag(ord("}")):
            raise ParseError("Esperado '}'")

        return Block(stmts)

    def statements_group(self) -> StatementSequence | None:
        """
        ### REGRA:
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
        ### REGRA:
        <function-decl> := "def" <identifier> "(" <formal_param_optional> ")" ":" <type> <block>
        """

        if not self.match_tag(TAGS.DEF.value):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado 'def'"
            )

        identifier = self.identifier()

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

        return FunctionDecl(identifier, params, return_type_token, block)
    
    def formal_param_optional(self):
        """
        ### REGRA:
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
        ### REGRA:
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
        ### REGRA:
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
    
    def while_statement(self):
        """
        ### REGRA:
        <while-statement> := "while" "(" <expression> ")" <block>
        """
        
        if not self.match_tag(TAGS.WHILE.value):
            raise ParseError("Esperado 'while'")

        if not self.match_tag(ord("(")):
            raise ParseError("Esperado '('")

        expr = self.expression()

        if not self.match_tag(ord(")")):
            raise ParseError("Esperado ')'")

        block = self.block()

        return WhileStatement(expr, block)

    def if_statement(self):
        """
        ### REGRA:
        <if-statement> := "if" "(" <expression> ")" <block> <else_block> 
        """

        if not self.match_tag(TAGS.IF.value):
            raise ParseError("Esperado 'if'")

        if not self.match_tag(ord("(")):
            raise ParseError("Esperado '(' após if")

        expr = self.expression()

        if not self.match_tag(ord(")")):
            raise ParseError("Esperado ')'")

        block = self.block()
        else_block = self.else_block()

        return IfStatement(expr, block, else_block)


    def else_block(self):
        """
        ### REGRA:
        <else_block> := "else" <block> | e 
        """
        if self.lookahead.tag == TAGS.ELSE.value:
            self.match_tag(TAGS.ELSE.value)
            return self.block()
        return None

    def return_statement(self):
        """
        ### REGRA:
        <return-statement> := "return" <expression> 
        """
        if not self.match_tag(TAGS.RETURN.value):
            raise ParseError("Esperado 'return'")
        expr = self.expression()
        return ReturnStatement(expr)

    def print_statement(self):
        """
        ### REGRA:
        <print-statement> := "print" <expression> 
        """
        if not self.match_tag(TAGS.PRINT.value):
            raise ParseError("Esperado 'print'")
        expr = self.expression()
        return PrintStatement(expr)

    def variable_decl(self):
        """
        ### REGRA:
        <variable-decl> := "var" <identifier> ":" <type> "=" <expression>
        """

        if not self.match_tag(TAGS.VAR.value):
            raise ParseError("Esperado 'var'")

        identifier = self.identifier()

        if not self.match_tag(ord(":")):
            raise ParseError("Esperado ':'")

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError("Esperado tipo")

        type_token = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        if not self.match_tag(ord("=")):
            raise ParseError("Esperado '='")

        expr = self.expression()

        return VariableDecl(identifier, type_token, expr)

    def assignment(self):
        """
        ### REGRA:
        <assignment> := "set" <identifier> "=" <expression>
        """

        if not self.match_tag(TAGS.SET.value):
            raise ParseError("Esperado 'set'")

        identifier = self.identifier()

        if not self.match_tag(ord("=")):
            raise ParseError("Esperado '='")

        expr = self.expression()

        return Assignment(identifier, expr)

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

    def simple_expression(self):
        """
        ### REGRA:
        <simple-expression> := <term> <sum-simple-expression>
        """
        simple_expression = self.term()
        sum_simple_expression = self.sum_simple_expression()
        return SimpleExpression(simple_expression, sum_simple_expression)
    
    def sum_simple_expression(self):
        """
        ### REGRA:
        <sum-simple-expression> := <additive-op> <term> <sum-simple-expression> | e
        """
        if self.lookahead.tag == TAGS.ADDITIVE_OP.value:
            op = self.lookahead
            self.match_tag(TAGS.ADDITIVE_OP.value)

            term = self.term()
            next_expr = self.sum_simple_expression()

            return SumSimpleExpression(op, term, next_expr)

        return None

    def term(self):
        """
        ### REGRA:
        term := <factor> <multiplicative-expr>
        """
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

    def factor(self):
        """
        ### REGRA:
        <factor> := <literal>
                 |  <identifier>
                 |  <sub-expression>
                 |  <unary>
        """

        # literal
        if self.lookahead.tag == TAGS.LITERAL.value:
            token = self.lookahead
            self.match_tag(TAGS.LITERAL.value)
            return Literal(token)
        
        # identifier
        if self.lookahead.tag == TAGS.IDENTIFIER.value:
            identifier = self.identifier()
            return self.factor_tail(identifier)

        # sub-expression
        if self.lookahead.tag == ord("("):
            return self.sub_expression()

        # unary
        if self.lookahead.tag in (ord("+"), ord("-"), TAGS.NOT.value):
            return self.unary()

        raise ParseError("Factor inválido")

    def factor_tail(self, identifier):
        """
        ### REGRA:
        <factor_tail> := "(" <actual-params> ")" | e
        """

        if self.match_tag(ord("(")):
            params = self.actual_params()

            if not self.match_tag(ord(")")):
                raise ParseError("Esperado ')'")

            return FunctionCall(identifier, params)

        return identifier

    def unary(self):
        """
        ### REGRA:
        unary := ("+" | "-" | "not") { expression }
        """
        if self.lookahead.tag in (ord("+"), ord("-"), TAGS.NOT.value):
            op = self.lookahead
            self.match_tag(self.lookahead.tag)

            expr = self.unary_expression()

            return UnaryExpr(op, expr)

        raise ParseError(
            f"ERRO NA LINHA {self.get_current_line()}: operador unário esperado"
        )
    
    def unary_expression(self):
        """
        ### REGRA:
        <unary-expression> := <expression> <unary-expression> | e
        """
        if self.lookahead.tag in (
            TAGS.IDENTIFIER.value,
            ord("("),
            TAGS.LITERAL.value,
        ):
            expr = self.expression()
            next_expr = self.unary_expression()
            return UnaryExpression(expr, next_expr)

        return None

    def sub_expression(self):
        """
        ### REGRA:
        sub-expr := "(" expression ")"
        """

        if not self.match_tag(ord("(")):
            raise ParseError("Esperado '('")
        
        expr = self.expression()

        if not self.match_tag(ord(")")):
            raise ParseError("Esperado ')'")

        return expr
    
    def actual_params(self):
        """
        ### REGRA:
        <actual-params> := <expression> <maybe-expression> | e
        """
        if self.lookahead.tag in (
            TAGS.IDENTIFIER.value,
            ord("("),
            TAGS.LITERAL.value,
        ):
            expr = self.expression()
            rest = self.maybe_expression()
            return ActualParams(expr, rest)

        return None

    def maybe_expression(self):
        """
        ### REGRA:
        <maybe-expression> := "," <expression> <maybe-expression> | e
        """
        if self.lookahead.tag == ord(","):
            self.match_tag(ord(","))

            expr = self.expression()
            rest = self.maybe_expression()

            return MaybeExpression(expr, rest)

        return None

    def identifier(self) -> Identifier:
        """
        ### REGRA:
        <identifier> := <valid_char> <maybe_valid_char>
        """

        token = self.lookahead

        if not self.match_tag(TAGS.IDENTIFIER.value):
            raise ParseError(
                f"ERRO NA LINHA {self.get_current_line()}: esperado identificador"
            )

        return Identifier(token)