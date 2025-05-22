import re


KEYWORDS = {'int', 'float', 'char', 'return', 'if', 'else', 'while', 'for', 'main'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||'}
DELIMITERS = {'(', ')', '{', '}', '[', ']', ';', ','}
PREPROCESSORS = {'#include', '#define'}

patterns = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('PREPROCESSOR', r'#\w+'),
    ('STRING', r'"[^"\n]*"'),
    ('CHAR', r"'[^'\n]'"),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('ID', r'[A-Za-z_]\w*'),
    ('OP', r'==|!=|<=|>=|&&|\|\||[+\-*/=<>]'),
    ('DELIM', r'[()\[\]{};,]'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('UNKNOWN', r'.'),
]


all_patterns = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
regex = re.compile(all_patterns)


def tokenize(code):
    tokens = []
    line = 1

    for match in regex.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'NEWLINE':
            line += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'ID':
            if value in KEYWORDS:
                tokens.append((line, 'KEYWORD', value))
            else:
                tokens.append((line, 'IDENTIFIER', value))
        elif kind == 'OP':
            if value in OPERATORS:
                tokens.append((line, 'OPERATOR', value))
            else:
                tokens.append((line, 'UNKNOWN', value))
        elif kind == 'DELIM':
            tokens.append((line, 'DELIMITER', value))
        elif kind == 'PREPROCESSOR':
            if value in PREPROCESSORS:
                tokens.append((line, 'PREPROCESSOR', value))
            else:
                tokens.append((line, 'UNKNOWN', value))
        else:
            tokens.append((line, kind, value))

    tokens.append((line, 'EOF', ''))
    return tokens


def show(tokens):
    for line, type_, value in tokens:
        print(f"Line {line:3}: {type_:12} -> {value}")


if __name__ == "__main__":
    code = '''
    #include <stdio.h>
    int main() {
        int x = 10;
        float y = 3.14;
        char c = 'A';
        char str[] = "Hello";
        if (x > 5 && y < 10) {
            return 0;
        }
    }
    '''
    result = tokenize(code)
    show(result)
