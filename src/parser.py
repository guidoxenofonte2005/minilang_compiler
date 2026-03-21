from errors.parse_error import ParseError
from lexer import Token
from globals import TAGS, REL_OPS, MUL_OPS, ADD_OPS
from abstract_syntax_tree import *

from symtable import SymTable


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead: Token = self.lexer.scan_file()
        self._symbol_table = SymTable()

    def get_current_line(self):
        return self.lexer.get_current_line()

    def start(self):
        return self.program()

    def match_tag(self, tag):
        if self.lookahead.tag != tag:
            raise ParseError(
                f"Esperado {tag}, encontrado {self.lookahead.tag} "
                f"('{self.lookahead.value}') na linha {self.lexer.get_current_line()}"
            )
        self.lookahead = self.lexer.scan_file()

    # ================= PROGRAM =================

    def program(self):
        statements = self.statements_group()
        return Block(statements)

    def block(self):
        self.match_tag(TAGS.LBRACE.value)

        savedTable = self._symbol_table
        self._symbol_table = SymTable(previousScope=savedTable)

        stmts = self.statements_group()
        self.match_tag(TAGS.RBRACE.value)

        self._symbol_table = savedTable

        return Block(stmts)

    def statements_group(self):
        statements = []

        while self.lookahead.tag in (
            TAGS.VAR.value,
            TAGS.SET.value,
            TAGS.PRINT.value,
            TAGS.IF.value,
            TAGS.WHILE.value,
            TAGS.RETURN.value,
            TAGS.DEF.value,
            TAGS.LBRACE.value,
        ):
            statements.append(self.statement())

        return statements

    # ================= STATEMENTS =================

    def statement(self):
        tag = self.lookahead.tag

        if tag == TAGS.VAR.value:
            stmt = self.variable_decl()
            self.match_tag(TAGS.SEMICOLON.value)
            return stmt

        elif tag == TAGS.SET.value:
            stmt = self.assignment()
            self.match_tag(TAGS.SEMICOLON.value)
            return stmt

        elif tag == TAGS.PRINT.value:
            stmt = self.print_statement()
            self.match_tag(TAGS.SEMICOLON.value)
            return stmt

        elif tag == TAGS.IF.value:
            return self.if_statement()

        elif tag == TAGS.WHILE.value:
            return self.while_statement()

        elif tag == TAGS.RETURN.value:
            stmt = self.return_statement()
            self.match_tag(TAGS.SEMICOLON.value)
            return stmt

        elif tag == TAGS.DEF.value:
            return self.function_decl()

        elif tag == TAGS.LBRACE.value:
            return self.block()

        else:
            raise ParseError(f"Statement inválido na linha {self.get_current_line()}")

    # ================= FUNCTION =================

    def function_decl(self):
        self.match_tag(TAGS.DEF.value)

        identifier = self.identifier()

        self.match_tag(TAGS.LPAREN.value)
        params = self.formal_param_optional()
        self.match_tag(TAGS.RPAREN.value)

        self.match_tag(TAGS.COLON.value)

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError("Esperado tipo de retorno")

        return_type = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        block = self.block()

        return FunctionDecl(identifier, params, return_type, block)

    def formal_param_optional(self):
        if self.lookahead.tag == TAGS.IDENTIFIER.value:
            return self.formal_param_list()
        return []

    def formal_param_list(self):
        params = [self.formal_param()]  ## existir o formal params inicial

        while self.lookahead.tag == TAGS.COMMA.value:
            self.match_tag(TAGS.COMMA.value)
            params.append(self.formal_param())

        return params

    def formal_param(self):
        name = self.identifier()
        self.match_tag(TAGS.COLON.value)

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError("Esperado tipo")

        type_token = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        return FormalParam(name, type_token)

    # ================= CONTROL =================

    def while_statement(self):
        self.match_tag(TAGS.WHILE.value)
        self.match_tag(TAGS.LPAREN.value)
        expr = self.expression()
        self.match_tag(TAGS.RPAREN.value)
        block = self.block()

        return WhileStatement(expr, block)

    def if_statement(self):
        self.match_tag(TAGS.IF.value)
        self.match_tag(TAGS.LPAREN.value)
        expr = self.expression()
        self.match_tag(TAGS.RPAREN.value)

        block = self.block()
        else_block = self.else_block()

        return IfStatement(expr, block, else_block)

    def else_block(self):
        if self.lookahead.tag == TAGS.ELSE.value:
            self.match_tag(TAGS.ELSE.value)
            return self.block()
        return None

    # ================= BASIC =================

    def return_statement(self):
        self.match_tag(TAGS.RETURN.value)
        expr = self.expression()
        return ReturnStatement(expr)

    def print_statement(self):
        self.match_tag(TAGS.PRINT.value)
        expr = self.expression()
        return PrintStatement(expr)

    def variable_decl(self):
        self.match_tag(TAGS.VAR.value)
        identifier = self.identifier()

        self.match_tag(TAGS.COLON.value)

        if self.lookahead.tag != TAGS.TYPE.value:
            raise ParseError("Esperado tipo")

        type_token = self.lookahead
        self.match_tag(TAGS.TYPE.value)

        self.match_tag(TAGS.ASSIGN.value)

        expr = self.expression()

        return VariableDeclaration(identifier, type_token, expr)

    def assignment(self):
        self.match_tag(TAGS.SET.value)
        identifier = self.identifier()
        self.match_tag(TAGS.ASSIGN.value)
        expr = self.expression()
        return Assignment(identifier, expr)

    # ================= EXPRESSIONS =================

    def expression(self):
        left = self.simple_expression()

        if self.lookahead.tag in REL_OPS:
            op = self.lookahead
            self.match_tag(op.tag)
            right = self.simple_expression()
            return BinaryExpr(
                left, op, right
            )  ## representa sum-simple-expression rel-op sum-simple-expression

        return left

    def simple_expression(self):
        left = self.term()

        while self.lookahead.tag in ADD_OPS:
            op = self.lookahead
            self.match_tag(op.tag)
            right = self.term()
            left = BinaryExpr(left, op, right)  ## representa sum-simple-expression

        return left

    def term(self):
        left = self.factor()

        while self.lookahead.tag in MUL_OPS:
            op = self.lookahead
            self.match_tag(op.tag)
            right = self.factor()
            left = BinaryExpr(left, op, right)  ## representa multiplicative-expr

        return left

    def factor(self):
        tag = self.lookahead.tag

        # literal
        if tag in (
            TAGS.INTEGER.value,
            TAGS.TRUE.value,
            TAGS.FALSE.value,
            TAGS.STRING.value,
        ):
            token = self.lookahead
            self.match_tag(tag)
            return Literal(token)

        # identifier / function call
        if tag == TAGS.IDENTIFIER.value:
            identifier = self.identifier()

            if self.lookahead.tag == TAGS.LPAREN.value:
                self.match_tag(TAGS.LPAREN.value)
                params = self.actual_params()
                self.match_tag(TAGS.RPAREN.value)
                return FunctionCall(identifier, params)

            return identifier
        # sub-expression
        # (expr)
        if tag == TAGS.LPAREN.value:
            self.match_tag(TAGS.LPAREN.value)
            expr = self.expression()
            self.match_tag(TAGS.RPAREN.value)
            return expr

        # unary
        # muito estranho na gramatica irei esperar
        if tag in (TAGS.PLUS.value, TAGS.MINUS.value, TAGS.NOT.value):
            op = self.lookahead
            self.match_tag(tag)
            expr = self.factor()
            return UnaryExpr(op, expr)

        raise ParseError(f"Factor inválido na linha {self.get_current_line()}")

    # ================= PARAMS =================

    def actual_params(self):
        params = []

        if self.lookahead.tag in (
            TAGS.IDENTIFIER.value,
            TAGS.INTEGER.value,
            TAGS.TRUE.value,
            TAGS.FALSE.value,
            TAGS.LPAREN.value,
            TAGS.PLUS.value,
            TAGS.MINUS.value,
        ):
            params.append(self.expression())

            while self.lookahead.tag == TAGS.COMMA.value:
                self.match_tag(TAGS.COMMA.value)
                params.append(self.expression())

        return params

    def identifier(self):
        token = self.lookahead
        self.match_tag(TAGS.IDENTIFIER.value)
        return Identifier(token)
