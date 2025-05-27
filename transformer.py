import re

class CppTransformer:
    

    
    def transform(self, code: str) -> str:
        if not code or not isinstance(code, str):
            raise ValueError("Input code must be a non-empty string")

       
        code = re.sub(r'#include\s*<stdio.h>', '#include <iostream>', code)
        if 'using namespace std;' not in code:
            code = re.sub(r'(#include\s*<[^>]+>)', r'\1\nusing namespace std;', code, count=1)

        code = re.sub(
            r'printf\("([^"]+)%d\\n",\s*(\w+)\);',
            r'cout << "\1" << \2 << endl;',
            code
        )
       
        code = re.sub(
            r'printf\("([^"]+)%d",\s*(\w+)\);',
            r'cout << "\1" << \2;',
            code
        )
        
        code = re.sub(
            r'printf\("([^"]*)\\n"\);',
            r'cout << "\1" << endl;',
            code
        )
       
        code = re.sub(
            r'printf\("([^"]*)"\);',
            r'cout << "\1";',
            code
        )

       
        code = re.sub(r'scanf\("([^"]+)",\s*([^)]+)\);', self._replace_scanf, code)

      
        code = re.sub(
            r'(\w+)\s*=\s*\(int\s*\*\)\s*malloc\(([^)]+)\);',
            r'\1 = new int[\2];',
            code
        )

       
        code = re.sub(
            r'free\((\w+)\);',
            r'delete[] \1;',
            code
        )

        
        code = re.sub(r'\bNULL\b', 'nullptr', code)

        
        code = re.sub(
            r'struct\s+(\w+)\s*\{([^}]+)\};',
            r'class \1 {\npublic:\n\2\n};',
            code,
            flags=re.MULTILINE
        )

       
        code = re.sub(
            r'class\s+(\w+)\s*\{([^}]+)\};',
            lambda m: f'class {m.group(1)} {{\npublic:\n{m.group(2)}\n}}',
            code,
            flags=re.MULTILINE
        )

      
        code = re.sub(
            r'for\s*\(\s*int\s+(\w+)\s*=\s*0;',
            r'for (int \1 = 0;',
            code
        )

       
        code = re.sub(
            r'for\s*\(\s*(\w+)\s*=\s*([^;]+);\s*([^;]+);\s*([^)]+)\)',
            r'for (\1 = \2; \3; \4)',
            code
        )

        
        code = re.sub(r'while\s*\(', 'while (', code)



       
        code = re.sub(r'\n{3,}', '\n\n', code)

       
        code = '\n'.join(line.rstrip() for line in code.splitlines())

        return code

    def _replace_scanf(self, match):
        
        format_str = match.group(1)
        vars_str = match.group(2)
        vars_list = [v.strip().lstrip('&') for v in vars_str.split(',')]
        return 'cin >> ' + ' >> '.join(vars_list) + ';'



if __name__ == "__main__":
    test_c_code = '''
#include <stdio.h>

int main() {
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);

    if (num % 2 == 0) {
        printf("The number %d is even.\n", num);
    } else {
        printf("The number %d is odd.\n", num);
    }

    return 0;
}
    '''

    transformer = CppTransformer()
    cpp_code = transformer.transform(test_c_code)
    print(cpp_code)
