import sys

class Compiler:
    def __init__(self, fileName: str) -> None:
        self.file = fileName
    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errado")
        sys.exit(1)

    try:
        with open(sys.argv[1]) as file:
            # TODO: LEXER -> PARSER
            print(file.read())
    except FileNotFoundError:
        print(f"Arquivo {sys.argv[1]} não encontrado")
    except SyntaxError:
        pass