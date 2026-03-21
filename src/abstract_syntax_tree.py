from typing import List
from lexer import Token

from globals import NODE_TYPES, TAGS

# ======================
# BASE
# ======================


class Node:
    def __init__(self, node_type=NODE_TYPES.UNKNOWN):
        self.node_type = node_type

    def to_string(self, level=0):
        return "  " * level + f"{self.__class__.__name__}"

    def Generate(self, level=0):
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

    def Generate(self, level=0):
        result = ""
        if not self.statements:
            return ("  " * level) + "pass\n"

        for statement in self.statements:
            result += statement.Generate(level)
        return result


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
            "  " * level
            + f"VarDecl({self.identifier.token.value}:{self.type.value})\n"
            + self.expression.to_string(level + 1)
        )

    def Generate(self, level=0):
        indentation = "  " * level
        variableName = self.identifier.Generate()
        expressionCode = self.expression.Generate()

        return f"{indentation}{variableName} = {expressionCode}\n"


class Assignment(Statement):
    def __init__(self, identifier, expression):
        super().__init__(NODE_TYPES.ASSIGNMENT)
        self.identifier = identifier
        self.expression = expression

    def to_string(self, level=0):
        return (
            "  " * level
            + f"Assign({self.identifier.token.value})\n"
            + self.expression.to_string(level + 1)
        )

    def Generate(self, level=0):
        indentation = "  " * level
        variableName = self.identifier.Generate()
        expressionCode = self.expression.Generate()

        return f"{indentation}{variableName} = {expressionCode}\n"


class PrintStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.PRINT)
        self.expression = expression

    def to_string(self, level=0):
        return "  " * level + "Print\n" + self.expression.to_string(level + 1)

    def Generate(self, level=0):
        indentation = "  " * level
        expressionCode = self.expression.Generate()

        if (
            hasattr(self.expression, "token")
            and self.expression.token.tag == TAGS.STRING.value
        ):
            return f'{indentation}print("{expressionCode}")\n'

        return f"{indentation}print({expressionCode})\n"


# ======================
# EXPRESSIONS
# ======================


class Identifier(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.IDENTIFIER)

    def to_string(self, level=0):
        return "  " * level + f"Id({self.token.value})"

    def Generate(self, level=0):
        return str(self.token.value)


class Literal(Expression):
    def __init__(self, token: Token):
        super().__init__(token, NODE_TYPES.LITERAL)

    def to_string(self, level=0):
        return "  " * level + f"Literal({self.token.value})"

    def Generate(self, level=0):
        value: str = str(self.token.value)

        if value == "true":
            return "True"
        if value == "false":
            return "False"

        return value


class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__(op, NODE_TYPES.BINARY)
        self.left = left
        self.right = right

    def to_string(self, level=0):
        return (
            "  " * level
            + f"Binary({self.token.value})\n"
            + self.left.to_string(level + 1)
            + "\n"
            + self.right.to_string(level + 1)
        )

    def Generate(self, level=0):
        leftHandCode = self.left.Generate()
        rightHandCode = self.right.Generate()
        operation = str(self.token.value)

        return f"{leftHandCode} {operation} {rightHandCode}"


class UnaryExpr(Expression):
    def __init__(self, op, expr):
        super().__init__(op, NODE_TYPES.EXPRESSION)
        self.expr = expr

    def to_string(self, level=0):
        return (
            "  " * level
            + f"Unary({self.token.value})\n"
            + self.expr.to_string(level + 1)
        )

    def Generate(self, level=0):
        return f"{self.token.value}{self.expr.Generate()}"


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

    def Generate(self, level=0):
        functionName = self.identifier.Generate()

        parameters = ", ".join(param.Generate() for param in self.params)

        return f"{functionName}({parameters})"


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

    def Generate(self, level=0):
        indentation = "  " * level
        functionName = self.identifier.Generate()

        parametersCode = ", ".join(param.Generate() for param in self.params)

        result = f"{indentation}def {functionName}({parametersCode}):\n"

        result += self.block.Generate(level + 1)
        return result


class WhileStatement(Statement):
    def __init__(self, condition, block):
        super().__init__(NODE_TYPES.WHILE)
        self.condition = condition
        self.block = block

    def to_string(self, level=0):
        return (
            "  " * level
            + "While\n"
            + self.condition.to_string(level + 1)
            + "\n"
            + self.block.to_string(level + 1)
        )

    def Generate(self, level=0):
        indentation = "  " * level
        condition = self.condition.Generate()

        result = f"{indentation}while {condition}:\n"

        result += self.block.Generate(level + 1)
        return result


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

    def Generate(self, level=0):
        indentation = "  " * level
        condition = self.condition.Generate()

        result = f"{indentation}if {condition}:\n"
        result += self.block.Generate(level + 1)

        if self.else_block:
            result += f"{indentation}else:\n"
            result += self.else_block.Generate(level + 1)

        return result


class ReturnStatement(Statement):
    def __init__(self, expression):
        super().__init__(NODE_TYPES.RETURN)
        self.expression = expression

    def to_string(self, level=0):
        return "  " * level + "Return\n" + self.expression.to_string(level + 1)

    def Generate(self, level=0):
        indentation = "  " * level
        expressionCode = self.expression.Generate()

        return f"{indentation}return {expressionCode}\n"


class FormalParam(Node):
    def __init__(self, identifier, type_token):
        super().__init__(NODE_TYPES.FORMAL_PARAM)
        self.identifier = identifier
        self.type = type_token

    def to_string(self, level=0):
        return "  " * level + f"Param({self.identifier.token.value}:{self.type.value})"

    def Generate(self, level=0):
        return self.identifier.Generate()
