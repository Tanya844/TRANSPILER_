#!/usr/bin/env python3
"""
C to C++ Transpiler - Tokenizer Module
This module is responsible for breaking down C code into tokens.
"""

import re

class Token:
    """Represents a single token in the C code"""
    
    def __init__(self, type, value, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Tokenizer:
    """
    Converts raw C code into a list of tokens 
    for the parser to process
    """
    
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        # Remove comments before tokenizing
        self.clean_code()
    
    def clean_code(self):
        """Remove comments from the code"""
        # Remove multiline comments /* ... */
        self.code = re.sub(r'/\*.*?\*/', '', self.code, flags=re.DOTALL)
        # Remove single line comments // ...
        self.code = re.sub(r'//.*?$', '', self.code, flags=re.MULTILINE)
    
    def tokenize(self):
        """Convert the code into a list of tokens"""
        tokens = []
        
        # Define token patterns
        token_specs = [
            ('INCLUDE',       r'#include\s*[<"].*?[>"]'),
            ('PRAGMA',        r'#pragma.*?$'),
            ('DEFINE',        r'#define.*?$'),
            ('IFDEF',         r'#ifdef.*?$'),
            ('IFNDEF',        r'#ifndef.*?$'),
            ('ENDIF',         r'#endif.*?$'),
            ('KEYWORD',       r'\b(int|char|float|double|struct|union|void|if|else|for|while|return|switch|case|break|continue|const|typedef|extern|static|auto|register)\b'),
            ('IDENTIFIER',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER',        r'\b\d+(\.\d*)?\b'),
            ('STRING',        r'"(\\.|[^"\\])*"'),
            ('CHAR',          r"'(\\.|[^'\\])'"),
            ('OPERATOR',      r'[+\-*/=%&|^~!<>]=?|&&|\|\||\+\+|--'),
            ('PUNCTUATION',   r'[(){}[\];,:]'),
            ('WHITESPACE',    r'\s+'),
        ]
        
        # Compile all patterns
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        token_pattern = re.compile(token_regex)
        
        # Find all tokens
        matches = token_pattern.finditer(self.code)
        
        for match in matches:
            token_type = match.lastgroup
            token_value = match.group()
            
            # Skip whitespace but update line/column
            if token_type == 'WHITESPACE':
                newlines = token_value.count('\n')
                if newlines > 0:
                    self.line += newlines
                    self.column = len(token_value) - token_value.rfind('\n')
                else:
                    self.column += len(token_value)
                continue
            
            tokens.append(Token(token_type, token_value, self.line, self.column))
            
            # Update position
            self.column += len(token_value)
        
        return tokens

# Simple test if this module is run directly
if __name__ == "__main__":
    test_code = """
    #include <stdio.h>
    
    /* This is a multi-line comment
       that should be removed */
    
    int main() {
        // This is a single line comment
        printf("Hello, World!\\n");
        return 0;
    }
    """
    
    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()
    
    for token in tokens:
        print(token)