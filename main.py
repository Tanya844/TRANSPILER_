#!/usr/bin/env python3
"""
C to C++ Transpiler - Main Module
This is the entry point for the transpiler that connects all components.
"""

import sys
import os
from tokenizer import Tokenizer
from parser import CParser
from transformer import CppTransformer

def transpile_code(c_code):
    """
    Process raw C code and convert it to C++
    """
    # Step 1: Tokenize the C code
    tokenizer = Tokenizer(c_code)
    tokens = tokenizer.tokenize()
    
    # Step 2: Parse the tokens into an AST
    parser = CParser(tokens)
    ast = parser.parse()
    
    # Step 3: Transform AST to C++ code
    transformer = CppTransformer(ast)
    cpp_code = transformer.transform()
    
    return cpp_code

def process_file(input_file, output_file=None):
    """
    Read C file, process it, and write C++ output
    """
    if not output_file:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}.cpp"
    
    

def main():
    """
    Process command line arguments and execute transpilation
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.c> [output_file.cpp]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_file(input_file, output_file)

# For simple cases without proper parsing
def quick_transpile(input_file, output_file=None):
    """
    Quick transpile using only the transformer for simple conversions
    This bypasses the tokenizer and parser for quick results
    """
    if not output_file:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}.cpp"
    
    

if __name__ == "__main__":
    # For now, we'll use the quick transpile method, 
    # as the full parsing system is more complex
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.c> [output_file.cpp]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        quick_transpile(input_file, output_file)
