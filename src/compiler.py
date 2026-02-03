import sys

from lexer import Lexer


class Compiler:
    def __init__(self, fileName: str) -> None:
        with open(fileName) as file:
            self.lexer = Lexer(file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USO CORRETO: python src/compiler.py nome_do_arquivo")
        sys.exit(1)

    try:
        Compiler(sys.argv[1])
    except FileNotFoundError:
        print(f"Arquivo {sys.argv[1]} não encontrado")
    except SyntaxError:
        print("Erro de sintaxe encontrado")
