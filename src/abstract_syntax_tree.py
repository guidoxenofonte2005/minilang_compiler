from globals import NODE_TYPES
from typing import List
from lexer import Token


# ======================
# BASE
# ======================

class Node:
    def __init__(self, node_type=NODE_TYPES.UNKNOWN):
        self.node_type = node_type

    def to_string(self, level=0):
        return "  " * level + f"{self.__class__.__name__}"

    def Generate(self):
        pass


class Statement(Node):
    def __init__(self, node_type=NODE_TYPES.STATEMENT):
        super().__init__(node_type)


class Expression(Node):
    def __init__(self, token: Token, node_type=NODE_TYPES.EXPRESSION):
        super().__init__(node_type)
        self.token: Token = token


# ======================
# BLOCK
# ======================

class Block(Statement):
    def __init__(self, statements: List[Statement]):
        super().__init__(NODE_TYPES.BLOCK)
        self.statements = statements

    def to_string(self, level=0):
        result = "  " * level + "Block\n"
        for stmt in self.statements:
            result += stmt.to_string(level + 1) + "\n"
        return result.rstrip()


# ======================
# STATEMENTS
# ======================

class VariableDeclaration(Statement):
    def __init__(self, identifier, type_token, expression):
        super().__init__(NODE_TYPES.VARIABLE_DECL)
        self.identifier = identifier
        self.type = type_token
        self.expression = expression

    def to_string(self, level=0):
        return (
            "  " * level + f"VarDecl({self.identifier.token.value}:{self.type.value})\n" +
            self.expression.to_string(level + 1)
        )


class Assignment(Statement):
    def __init__(self, identifier, expression):
        super().__init__(NODE_TYPES.ASSIGNMENT)
        self.identifier = identifier
        self.expression = expression

    def to_string(self, level=0):
        return (
            "  " * level + f"Assign({self.identifier.token.value})\n" +
            self.expression.to_string(level + 1)
        )


class PrintStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.PRINT)
        self.expression = expression

    def to_string(self, level=0):
        return (
            "  " * level + "Print\n" +
            self.expression.to_string(level + 1)
        )


# ======================
# EXPRESSIONS
# ======================

class Identifier(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.IDENTIFIER)

    def to_string(self, level=0):
        return "  " * level + f"Id({self.token.value})"


class Literal(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.LITERAL)

    def to_string(self, level=0):
        return "  " * level + f"Literal({self.token.value})"


class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__(op, NODE_TYPES.BINARY)
        self.left = left
        self.right = right

    def to_string(self, level=0):
        return (
            "  " * level + f"Binary({self.token.value})\n" +
            self.left.to_string(level + 1) + "\n" +
            self.right.to_string(level + 1)
        )


class FunctionCall(Expression):
    def __init__(self, identifier, params: List[Expression]):
        super().__init__(identifier.token, NODE_TYPES.FUNCTION_CALL)
        self.identifier = identifier
        self.params = params

    def to_string(self, level=0):
        result = "  " * level + f"Call({self.identifier.token.value})\n"
        for p in self.params:
            result += p.to_string(level + 1) + "\n"
        return result.rstrip()
    
class FunctionDecl(Statement):
    def __init__(self, identifier, params, return_type, block):
        super().__init__(NODE_TYPES.FUNCTION_DECL)
        self.identifier = identifier
        self.params = params
        self.return_type = return_type
        self.block = block

    def to_string(self, level=0):
        result = "  " * level + f"Function({self.identifier.token.value})\n"
        for p in self.params:
            result += p.to_string(level + 1) + "\n"
        result += "  " * (level + 1) + f"ReturnType({self.return_type.value})\n"
        result += self.block.to_string(level + 1)
        return result
    
class WhileStatement(Statement):
    def __init__(self, condition, block):
        super().__init__(NODE_TYPES.WHILE)
        self.condition = condition
        self.block = block

    def to_string(self, level=0):
        return (
            "  " * level + "While\n" +
            self.condition.to_string(level + 1) + "\n" +
            self.block.to_string(level + 1)
        )
        
class IfStatement(Statement):
    def __init__(self, condition, block, else_block):
        super().__init__(NODE_TYPES.IF)
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def to_string(self, level=0):
        result = "  " * level + "If\n"
        result += self.condition.to_string(level + 1) + "\n"
        result += self.block.to_string(level + 1)

        if self.else_block:
            result += "\n" + "  " * level + "Else\n"
            result += self.else_block.to_string(level + 1)

        return result
    
class ReturnStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.RETURN)
        self.expression = expression

    def to_string(self, level=0):
        return (
            "  " * level + "Return\n" +
            self.expression.to_string(level + 1)
        )

class FormalParam(Node):
    def __init__(self, identifier, type_token):
        super().__init__(NODE_TYPES.FORMAL_PARAM)
        self.identifier = identifier
        self.type = type_token

    def to_string(self, level=0):
        return "  " * level + f"Param({self.identifier.token.value}:{self.type.value})"