# This parser is stolen almost in its entirety from Jay Conrod.

# I still don't want you to sue me.

from WalText2i.expr_api.AST import *
from WalText2i.expr_api.parser_combinators import *
from WalText2i.expr_api.lexer import *
from functools import reduce


def keyword(kw, tag):
    return Reserved(kw, tag)

num = Tag(NUM) ^ (lambda i: complex(float(i), 0))
inum = Tag(INUM) ^ (lambda i: complex(0, float(i[:-1])))
id = Tag(NAME)


def aexp_value():
    return num ^ (lambda i: NumExp(i)) | \
           inum ^ (lambda i: InumExp(i)) | \
           id ^ (lambda v: VarExp(v))


def aexp_negative():
    return (keyword('-', OP) + Lazy(aexp_term)) ^ (lambda parsed: UnopAexp(parsed[1], '-'))


def aexp_conjugate():
    return (keyword('$', OP) + Lazy(aexp_term)) ^ (lambda parsed: UnopAexp(parsed[1], '$'))


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def aexp_group():
    return keyword('(', PAREN) + Lazy(parsetoks) + keyword(')', PAREN) ^ process_group


def aexp_term():
    return aexp_value() |\
           aexp_group() |\
           aexp_negative() |\
           aexp_conjugate()


def process_binop(op):
    return lambda l, r: BinopAexp(l, r, op)


def any_operator_in_list(ops):
    op_parsers = [keyword(op[0], OP) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

aexp_precedence_levels = [
    [('..', 'l')],
    [('~', 'l')],
    [('*', 'l'), ('/', 'l'), ('%', 'l')],
    [('+', 'l'), ('-', 'l')],
]


def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level[0])
    return parser


def parsetoks():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)


def parser():
    return Phrase(parsetoks())


def parse_tokens(tokens):
    ast = parser()(tokens, 0)
    return ast


def parse(script):
    parsed = parse_tokens(lex(script))
    print(parsed)
    return parsed

if __name__ == '__main__':
    print(parse(input()))