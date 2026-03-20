from lexer import Lexer
from parser import Parser
from errors.parse_error import ParseError


def test_parser():
    try:
        with open("test/codigo_teste.mini") as file:
            lexer = Lexer(file)
            parser = Parser(lexer)

            ast = parser.start()

            print("✅ Parsing concluído com sucesso!")
            print(ast.to_string())

    except ParseError as e:
        print(f"❌ Erro de parsing: {e}")

    except Exception as e:
        print(f"❌ Erro geral: {e}")


if __name__ == "__main__":
    test_parser()