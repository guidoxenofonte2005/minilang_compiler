from globals import NODE_TYPES

from typing import override

from lexer import Token


class Node:
    # TODO: criar classe Node
    def __init__(self, node_type=NODE_TYPES.UNKNOWN):
        self.node_type: NODE_TYPES = node_type

    def ToString(self) -> str:
        return ""


class Statement(Node):
    def __init__(self, node_type=NODE_TYPES.STATEMENT):
        super().__init__(node_type)


class Expression(Node):
    def __init__(self, token: Token, node_type=NODE_TYPES.EXPRESSION):
        super().__init__(node_type)
        self.token: Token = token


class StatementSequence(Statement):
    def __init__(
        self,
        statement: Statement,
        statements: StatementSequence,
        node_type=NODE_TYPES.STATEMENTS,
    ):
        super().__init__(node_type)
        self.statement = statement
        self.statements = statements


class VariableDeclaration(Statement):
    def __init__(self, identifier, expression):
        super().__init__(NODE_TYPES.ASSIGNMENT)
        self.identifier = identifier
        self.expression = expression


class Identifier(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.IDENTIFIER)


class LogicalExpr(Expression):
    def __init__(self, token, expression):
        super().__init__(token, NODE_TYPES.LOGICAL)
        self.expression = expression

class RelationalExpr(Expression):
    def __init__(self, token, node_type=NODE_TYPES.EXPRESSION):
        super().__init__(token, node_type)