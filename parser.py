#!/usr/bin/env python3
"""
C to C++ Transpiler - Parser Module
This module converts tokens into an Abstract Syntax Tree (AST).
"""

class ASTNode:
    """Base class for all AST nodes"""
    
    def __init__(self, node_type):
        self.type = node_type
        
    def __repr__(self):
        return f"{self.type}"

class ProgramNode(ASTNode):
    """Root node of the AST representing the entire program"""
    
    def __init__(self):
        super().__init__("Program")
        self.includes = []
        self.defines = []
        self.typedefs = []
        self.declarations = []
        self.functions = []
    
    def __repr__(self):
        return f"Program(includes={len(self.includes)}, functions={len(self.functions)})"

class IncludeNode(ASTNode):
    """Represents a #include directive"""
    
    def __init__(self, header):
        super().__init__("Include")
        self.header = header
    
    def __repr__(self):
        return f"Include({self.header})"

class FunctionNode(ASTNode):
    """Represents a function definition"""
    
    def __init__(self, name, return_type):
        super().__init__("Function")
        self.name = name
        self.return_type = return_type
        self.parameters = []
        self.body = []
    
    def __repr__(self):
        return f"Function({self.name})"

class CParser:
    """
    Parser for C code. Takes tokens and produces an AST.
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
    
    def parse(self):
        """
        Convert tokens into an AST structure.
        For now, this is a simplified version focused on includes and basic structures.
        """
        # Create root node
        program = ProgramNode()
        
        # Process tokens to build the AST
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            
            if token.type == 'INCLUDE':
                # Process include directives
                program.includes.append(IncludeNode(token.value))
                self.current_token_index += 1
            elif token.type == 'DEFINE':
                # Process #define directives
                program.defines.append(token.value)
                self.current_token_index += 1
            else:
                # Skip other tokens for now
                # A complete parser would process all C constructs here
                self.current_token_index += 1
        
        # In a real parser, we would process all constructs including
        # functions, declarations, statements, etc.
        
        return program

# Simple test if this module is run directly
if __name__ == "__main__":
    from tokenizer import Tokenizer
    
    test_code = """
    #include <stdio.h>
    #define MAX_SIZE 100
    
    int main() {
        printf("Hello, World!\\n");
        return 0;
    }
    """
    
    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()
    
    parser = CParser(tokens)
    ast = parser.parse()
    
    print(ast)
    for include in ast.includes:
        print(include)