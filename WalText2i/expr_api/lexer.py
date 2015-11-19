from WalText2i.expr_api.UtopiaLexer import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support

# Tags
NUM = 'NUMBER'
INUM = 'IMAGINARY NUMBER'
OP = 'OP'
PAREN = 'PAREN'
NAME = 'NAME'


def lex(exp):  # Lex a single line
    lexr = lexer([])  # Create a Lexer object

    lexr.add_token_expr(r'^[\s]', None)
    lexr.add_token_expr(r'^[0-9]+i', INUM)
    lexr.add_token_expr(r'^[0-9]+', NUM)
    lexr.add_token_expr(r'^[()]', PAREN)
    lexr.add_token_expr(r'^[^a-zA-Z0-9_()]+', OP)
    lexr.add_token_expr(r'^[a-zA-Z_]+', NAME)

    ret = lexr.lex(exp)
    print(ret)
    return ret

if __name__ == '__main__':
    print(lex(input()))