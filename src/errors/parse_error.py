class ParseError(Exception):
    def __init__(self, error_message: str = "Erro de sintaxe"):
        self.msg = error_message
        super().__init__(self.msg)