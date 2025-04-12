#!/usr/bin/env python3
"""
C to C++ Transpiler - Transformer Module
This module takes an AST or C code and transforms it to C++.
"""

import re

class CppTransformer:
    """
    Transform C AST or code to C++ equivalent
    """
    
    def __init__(self, ast):
        self.ast = ast
        
    def transform(self):
        """
        Transform AST to C++ code.
        This would be a complex implementation walking the AST.
        """
        # For a full implementation, we'd convert each AST node
        # to its C++ equivalent here
        
        # Since our parser is simplified, using the quick transform for now
        return "// Full AST transform not implemented yet"
    
    def quick_transform(self, c_code):
        """
        Quick transformation using regex patterns.
        This bypasses the AST for simpler conversions.
        """
        cpp_code = c_code
        
        # 1. Replace C headers with C++ equivalents
        header_mappings = {
            r'#include\s*<stdio.h>': '#include <iostream>\n#include <cstdio>',
            r'#include\s*<stdlib.h>': '#include <cstdlib>',
            r'#include\s*<string.h>': '#include <cstring>\n#include <string>',
            r'#include\s*<math.h>': '#include <cmath>',
            r'#include\s*<time.h>': '#include <ctime>',
            r'#include\s*<assert.h>': '#include <cassert>',
            r'#include\s*<ctype.h>': '#include <cctype>',
            r'#include\s*<errno.h>': '#include <cerrno>',
            r'#include\s*<float.h>': '#include <cfloat>',
            r'#include\s*<limits.h>': '#include <climits>',
            r'#include\s*<locale.h>': '#include <clocale>',
            r'#include\s*<setjmp.h>': '#include <csetjmp>',
            r'#include\s*<signal.h>': '#include <csignal>',
            r'#include\s*<stdarg.h>': '#include <cstdarg>',
            r'#include\s*<stddef.h>': '#include <cstddef>',
        }
        
        for c_header, cpp_header in header_mappings.items():
            cpp_code = re.sub(c_header, cpp_header, cpp_code)
        
        # 2. Add using namespace std; after includes if iostream is included
        if re.search(r'#include\s*<iostream>', cpp_code):
            # Find the position after all includes
            includes_pattern = r'#include\s*<[^>]+>'
            last_include = None
            for match in re.finditer(includes_pattern, cpp_code):
                last_include = match
            
            if last_include:
                insert_pos = last_include.end()
                cpp_code = cpp_code[:insert_pos] + '\n\nusing namespace std;' + cpp_code[insert_pos:]
        
        # 3. Replace printf/scanf with cout/cin
        # Find printf statements
        printf_pattern = r'printf\s*\(\s*"([^"]*)"\s*(?:,\s*([^)]*))?\s*\)'
        
        def replace_printf(match):
            format_str = match.group(1)
            args = match.group(2)
            
            if not args:  # Simple case with no arguments
                return f'cout << "{format_str}"'
            
            # Handle format specifiers and arguments
            # This is simplified and doesn't handle all printf format specifiers
            parts = []
            
            # Split the format string at format specifiers
            format_parts = re.split(r'(%[diouxXfFeEgGaAcsp])', format_str)
            
            if len(format_parts) > 1:
                # There are format specifiers
                args_list = [arg.strip() for arg in args.split(',')]
                arg_index = 0
                
                result = "cout"
                for part in format_parts:
                    if part.startswith('%') and len(part) > 1:
                        # This is a format specifier
                        if arg_index < len(args_list):
                            result += f" << {args_list[arg_index]}"
                            arg_index += 1
                    else:
                        if part:  # Skip empty parts
                            result += f" << \"{part}\""
                
                return result
            else:
                # Just a string with arguments not used as format specifiers
                return f'cout << "{format_str}" << {args}'
        
        cpp_code = re.sub(printf_pattern, replace_printf, cpp_code)
        
        # Replace scanf with cin
        scanf_pattern = r'scanf\s*\(\s*"([^"]*)"\s*,\s*([^)]*)\s*\)'
        
        def replace_scanf(match):
            format_str = match.group(1)
            args = match.group(2)
            
            args_list = [arg.strip() for arg in args.split(',')]
            result = "cin"
            
            for arg in args_list:
                # Remove & from variable references
                if arg.startswith('&'):
                    arg = arg[1:]
                result += f" >> {arg}"
            
            return result
        
        cpp_code = re.sub(scanf_pattern, replace_scanf, cpp_code)
        
        # 4. Replace malloc/free with new/delete
        malloc_pattern = r'(\w+)\s*=\s*\(\s*(\w+\s*\*)\s*\)\s*malloc\s*\(\s*(\w+)\s*\*\s*sizeof\s*\(\s*(\w+)\s*\)\s*\)'
        cpp_code = re.sub(malloc_pattern, r'\1 = new \4[\3]', cpp_code)
        
        free_pattern = r'free\s*\(\s*(\w+)\s*\)'
        cpp_code = re.sub(free_pattern, r'delete[] \1', cpp_code)
        
        # 5. Add endl after \n in cout statements
        newline_in_cout = r'cout\s*<<\s*"([^"]*\\n[^"]*)"'
        
        def replace_newline_in_cout(match):
            text = match.group(1)
            text = text.replace('\\n', '" << endl << "')
            if text.endswith('" << endl << "'):
                text = text[:-13] + '"'  # Remove trailing empty string
                return f'cout << "{text}" << endl'
            return f'cout << "{text}"'
        
        cpp_code = re.sub(newline_in_cout, replace_newline_in_cout, cpp_code)
        
        # Final cleanup: Replace multiple consecutive newlines with at most two
        cpp_code = re.sub(r'\n{3,}', '\n\n', cpp_code)
        
        return cpp_code

# Simple test if this module is run directly
if __name__ == "__main__":
    test_code = """
    #include <stdio.h>

int main() {
    int num1, num2, sum;

    printf("Enter first number: ");
    scanf("%d", &num1);

    printf("Enter second number: ");
    scanf("%d", &num2);

    sum = num1 + num2;

    printf("Sum = %d\n", sum);

    return 0;
}

    """
    
    transformer = CppTransformer(None)
    cpp_code = transformer.quick_transform(test_code)
    
    print(cpp_code)