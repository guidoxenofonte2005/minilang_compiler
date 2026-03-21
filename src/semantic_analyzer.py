from symtable import SymTable, Symbol
from globals import TAGS, REL_OPS, ADD_OPS, MUL_OPS


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymTable()
        self.current_function = None
        self.has_Return = False


    def analyze(self, ast):
        self.visit(ast)


    def visit(self, node):
        method_name = f"_visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self._generic_visit)
        return method(node)

    def _generic_visit(self, node):
        raise SemanticError(f"No visit method for {node.__class__.__name__}")

    # ================= Sistema de tipos =================

    def _map_type(self, type_token):
        value = type_token.value

        if value == "int":
            return "int"
        if value == "real":
            return "real"
        if value == "bool":
            return "bool"
        if value == "void":
            return "void"

        raise SemanticError(f"Tipo desconhecido: {value}")

    # ================= BLOCK =================

    def _visit_Block(self, node):
        saved = self.symbol_table
        self.symbol_table = SymTable(previousScope=saved)

        for stmt in node.statements:
            self.visit(stmt)

        self.symbol_table = saved

    # ================= DECLARATIONS =================

    def _visit_VariableDeclaration(self, node):
        name = node.identifier.token.value
        var_type = self._map_type(node.type)

        if not self.symbol_table.insert(name, Symbol(name, var_type)):
            raise SemanticError(f"Variável '{name}' já declarada no escopo")

        expr_type = self.visit(node.expression)

        if expr_type != var_type:
            raise SemanticError(
                f"Tipo incompatível em declaração de '{name}': "
                f"{var_type} != {expr_type}"
            )

    def _visit_Assignment(self, node):
        name = node.identifier.token.value

        symbol = self.symbol_table.findSymbol(name)
        if symbol is None:
            raise SemanticError(f"Variável '{name}' não declarada")

        expr_type = self.visit(node.expression)

        if symbol.type != expr_type:
            raise SemanticError(
                f"Tipo incompatível em atribuição '{name}': "
                f"{symbol.type} != {expr_type}"
            )

    # ================= EXPRESSIONS =================

    def _visit_Identifier(self, node):
        name = node.token.value

        symbol = self.symbol_table.findSymbol(name)
        if symbol is None:
            raise SemanticError(f"Variável '{name}' não declarada")

        return symbol.type

    def _visit_Literal(self, node):
        tag = node.token.tag

        if tag == TAGS.INTEGER.value:
            return "int"

        if tag in (TAGS.TRUE.value, TAGS.FALSE.value):
            return "bool"

        if tag == TAGS.STRING.value:
            return "string"

        raise SemanticError("Literal desconhecido")

    def _visit_BinaryExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        op = node.token.tag

        # ARITMÉTICOS (+, -, *, /)
        if op in ADD_OPS or op in MUL_OPS:
            if left_type != right_type:
                raise SemanticError("Tipos incompatíveis em operação")

            if left_type not in ("int", "real", "bool", "void"):
                raise SemanticError("Operação aritmética inválida")

            return left_type

        # RELACIONAIS (>, <, ==, etc)
        if op in REL_OPS:
            if left_type != right_type:
                raise SemanticError("Comparação com tipos diferentes")

            return "bool"

        raise SemanticError("Operador desconhecido")

    def _visit_UnaryExpr(self, node):
        expr_type = self.visit(node.expr)
        op = node.token.tag

        if op == TAGS.NOT.value:
            if expr_type != "bool":
                raise SemanticError("NOT espera booleano")
            return "bool"

        if op in (TAGS.PLUS.value, TAGS.MINUS.value):
            if expr_type not in ("int", "real", "bool", "void"):
                raise SemanticError("Operador unário inválido")
            return expr_type

        raise SemanticError("Operador unário desconhecido")

    # ================= CONTROL =================

    def _visit_IfStatement(self, node):
        cond_type = self.visit(node.condition)

        if cond_type != "bool":
            raise SemanticError("IF espera condição booleana")

        self.visit(node.block)

        if node.else_block:
            self.visit(node.else_block)

    def _visit_WhileStatement(self, node):
        cond_type = self.visit(node.condition)

        if cond_type != "bool":
            raise SemanticError("WHILE espera condição booleana")

        self.visit(node.block)

    # ================= FUNCTIONS =================

    def _visit_FunctionDecl(self, node):
        name = node.identifier.token.value

        param_types = []
        for param in node.params:
            param_types.append(self._map_type(param.type))

        return_type = self._map_type(node.return_type)

        # registra função com assinatura
        if not self.symbol_table.insert(
            name,
            Symbol(name, "function", param_types, return_type)
        ):
            raise SemanticError(f"Função '{name}' já declarada")

        # novo escopo
        saved = self.symbol_table
        self.symbol_table = SymTable(previousScope=saved)

        self.current_function = node

        # inserir parâmetros no escopo
        for param in node.params:
            pname = param.identifier.token.value
            ptype = self._map_type(param.type)

            if not self.symbol_table.insert(pname, Symbol(pname, ptype)):
                raise SemanticError(f"Parâmetro '{pname}' duplicado")

        self.visit(node.block)

        if return_type != "void" and not self.has_Return:
            raise SemanticError(f"Função '{name}' deve retornar um valor")

        self.symbol_table = saved
        self.current_function = None
        self.has_Return = False

    def _visit_FunctionCall(self, node):
        name = node.identifier.token.value

        symbol = self.symbol_table.findSymbol(name)
        if symbol is None:
            raise SemanticError(f"Função '{name}' não declarada")

        if symbol.type != "function":
            raise SemanticError(f"'{name}' não é uma função")

        # validar quantidade
        if len(node.params) != len(symbol.params):
            raise SemanticError(
                f"Função '{name}' espera {len(symbol.params)} argumentos, "
                f"mas recebeu {len(node.params)}"
            )

        # validar tipos
        for i, param in enumerate(node.params):
            arg_type = self.visit(param)
            expected_type = symbol.params[i]

            if arg_type != expected_type:
                raise SemanticError(
                    f"Argumento {i+1} da função '{name}' esperado {expected_type}, "
                    f"recebido {arg_type}"
                )

        return symbol.return_type

    def _visit_ReturnStatement(self, node):
        if self.current_function is None:
            raise SemanticError("'return' fora de função")

        self.has_Return = True

        expr_type = self.visit(node.expression)

        expected_type = self._map_type(self.current_function.return_type)

        if expr_type != expected_type:
            raise SemanticError(
                f"Tipo de retorno incompatível: esperado {expected_type}, recebido {expr_type}"
            )

        return expr_type

    # ================= PRINT =================

    def _visit_PrintStatement(self, node):
        self.visit(node.expression)