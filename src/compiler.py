import sys

from lexer import Lexer
import globals
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

class Compiler:
    def __init__(self, fileName: str) -> None:
        with open(fileName) as file:
            globals.global_lexer = Lexer(file)
            globals.global_parser = Parser(globals.global_lexer)

            ast = globals.global_parser.start()

            print(ast.to_string())

            globals.global_semantic_analyzer = SemanticAnalyzer()
            globals.global_semantic_analyzer.analyze(ast)
            
            finalCode = globals.global_parser.Generate()

            with open("compiled_exit.py", "w") as exitFile:
                exitFile.write(finalCode)


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
