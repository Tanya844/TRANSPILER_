def create_program():
    return {
        'type': 'Program',
        'includes': [],
        'defines': [],
        'functions': []
    }

def create_include(header):
    return {
        'type': 'Include',
        'header': header
    }

def create_function(name, return_type):
    return {
        'type': 'Function',
        'name': name,
        'return_type': return_type,
        'params': [],
        'body': []
    }

def create_variable_declaration(var_type, var_name):
    return {
        'type': 'Variable',
        'var_type': var_type,
        'var_name': var_name
    }

def create_return_statement(value):
    return {
        'type': 'Return',
        'value': value
    }

def parse(tokens):
    i = 0
    program = create_program()

    while i < len(tokens):
        tok_type, _, value = tokens[i]

       
        if value.startswith("#include"):
            parts = value.split()
            if len(parts) > 1:
                program['includes'].append(create_include(parts[1]))
            i += 1


        elif value.startswith("#define"):
            program['defines'].append(value)
            i += 1

      
        elif value in ("int", "void", "float", "char"):  
            
            if i + 2 < len(tokens) and tokens[i + 2][2] == '(':
                return_type = value
                func_name = tokens[i + 1][2]
                i += 3  
                params = []

                while tokens[i][2] != ')':
                    if tokens[i][2] in ('int', 'char', 'float', 'double'):
                        param_type = tokens[i][2]
                        param_name = tokens[i + 1][2]
                        params.append({'type': param_type, 'name': param_name})
                        i += 2
                    elif tokens[i][2] == ',':
                        i += 1
                    else:
                        i += 1
                i += 1  
                while tokens[i][2] != '{':
                    i += 1
                i += 1  

                function = create_function(func_name, return_type)
                function['params'] = params

               
                while tokens[i][2] != '}':
                    tok = tokens[i]
                    if tok[2] in ('int', 'char', 'float', 'double'):
                       
                        var_type = tok[2]
                        var_name = tokens[i + 1][2]
                        function['body'].append(create_variable_declaration(var_type, var_name))
                        i += 3  
                    elif tok[2] == 'return':
                        ret_val = tokens[i + 1][2]
                        function['body'].append(create_return_statement(ret_val))
                        i += 3
                    else:
                        i += 1

                i += 1 
                program['functions'].append(function)
            else:
                i += 1
        else:
            i += 1

    return program
