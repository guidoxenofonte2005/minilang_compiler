from lexer import Lexer


def test_lexer_scan():
    with open("test/codigo_teste_vars.mini") as file:
        lex = Lexer(file)

        while lex._current_position < len(lex._source_code):
            print(lex.scan_file())
        
        print(lex.token_table)

if __name__ == "__main__":
    test_lexer_scan()