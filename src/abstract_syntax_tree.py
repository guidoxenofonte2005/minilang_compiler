from globals import NODE_TYPES

from typing import override

from lexer import Token


class Node:
    def __init__(self, node_type=NODE_TYPES.UNKNOWN):
        self.node_type: NODE_TYPES = node_type
        # self.line: int

    def ToString(self) -> str:
        return ""


# STATEMENTS NÃO PRODUZEM VALOR
class Statement(Node):
    def __init__(self):
        super().__init__(NODE_TYPES.STATEMENT)


class StatementSequence(Statement):
    def __init__(self, statement: Statement, statements: StatementSequence | None):
        super().__init__(NODE_TYPES.STATEMENTS)
        self.statement = statement
        self.statements = statements


class VariableDeclaration(Statement):
    def __init__(self, identifier, type, expression):
        super().__init__(NODE_TYPES.VAR_DECLARATION)
        self.identifier = identifier
        self.type = type
        self.expression = expression


class Assignment(Statement):
    def __init__(self, identifier, type, expression):
        super().__init__(NODE_TYPES.ASSIGNMENT)
        self.identifier = identifier
        self.type = type
        self.expression = expression


class PrintStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.STATEMENT)
        self.expression = expression


class ReturnStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.RETURN_STATEMENT)
        self.expression = expression


class IfStatement(Statement):
    def __init__(
        self,
        condition: Expression,
        then_expression: StatementSequence,
        else_block: StatementSequence | None,
    ):
        super().__init__(NODE_TYPES.IF_STATEMENT)
        self.condition = condition
        self.then_expression = then_expression
        if else_block:
            self.else_block = else_block


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: StatementSequence):
        super().__init__(NODE_TYPES.WHILE_STATEMENT)
        self.condition = condition
        self.body = body


class FunctionDeclaration(Statement):
    def __init__(
        self,
        identifier: Identifier,
        params: list | None,
        return_type,
        body: StatementSequence,
    ):
        super().__init__(NODE_TYPES.FUNCTION_DECLARATION)
        self.identifier = identifier
        if params:
            self.params = params
        self.return_type = return_type
        self.body = body


# EXPRESSÕES PRODUZEM VALOR
class Expression(Node):
    def __init__(
        self,
        token: Token,
    ):
        super().__init__(NODE_TYPES.EXPRESSION)
        self.token: Token = token


class Identifier(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.IDENTIFIER)


class Literal(Expression):
    def __init__(self, token, type):
        super().__init__(token)
        self.type = type


class BinaryExpression(Expression):
    def __init__(self, left_hand_expr: Expression, token, right_hand_expr: Expression):
        super().__init__(token)
        self.left_hand_expr = left_hand_expr
        self.right_hand_expr = right_hand_expr


class UnaryExpression(Expression):
    def __init__(self, token, operand: Expression):
        super().__init__(token)
        self.operand = operand


class FunctionCall(Expression):
    def __init__(self, token, arguments: list | None):
        super().__init__(token)
        if arguments:
            self.arguments = arguments
