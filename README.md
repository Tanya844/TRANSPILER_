# C to C++ Transpiler

A Python-based tool that automatically converts C code to equivalent C++ code.

## Overview

This transpiler transforms C source code into modern C++ by converting syntax, libraries, and idioms to their C++ equivalents. It's designed to help developers migrate legacy C code to C++ with minimal manual intervention.

## Features

- Converts C standard headers to their C++ equivalents (e.g., `stdio.h` → `iostream` and `cstdio`)
- Replaces C-style I/O functions (`printf`/`scanf`) with C++ streams (`cout`/`cin`)
- Transforms C memory management (`malloc`/`free`) to C++ (`new`/`delete`)
- Adds C++ namespace usage (`using namespace std;`)
- Handles newlines in output statements appropriately
- Preserves code functionality while making it more C++-like

## Project Structure

- `main.py`: Entry point and orchestrator for the transpilation process
- `tokenizer.py`: Breaks down C code into individual tokens for analysis
- `parser.py`: Converts tokens into an Abstract Syntax Tree (AST)
- `transformer.py`: Transforms C constructs to their C++ equivalents

## Installation

No additional dependencies are required beyond a standard Python installation (Python 3.6+).

1. Clone this repository or download the files
2. Ensure all files are in the same directory
3. Make the Python files executable (optional, for Unix-like systems):
   ```bash
   chmod +x main.py tokenizer.py parser.py transformer.py
   ```

## Usage

### Basic Usage

```bash
python main.py input.c [output.cpp]
```

If no output file is specified, the transpiler will create one with the same base name as the input file but with a `.cpp` extension.

### Examples

Converting a single file:

```bash
python main.py hello.c
```

Specifying an output file:

```bash
python main.py source.c converted.cpp
```

## Example Conversion

### Input (C code):

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    printf("Enter number of elements: ");
    scanf("%d", &n);

    int* arr = (int*)malloc(n * sizeof(int));

    for(int i = 0; i < n; i++) {
        printf("Enter element %d: ", i+1);
        scanf("%d", &arr[i]);
    }

    printf("You entered:\n");
    for(int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    free(arr);
    return 0;
}
```

### Output (C++ code):

```cpp
#include <iostream>
#include <cstdio>
#include <cstdlib>

using namespace std;

int main() {
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    int* arr = new int[n];

    for(int i = 0; i < n; i++) {
        cout << "Enter element " << i+1 << ": ";
        cin >> arr[i];
    }

    cout << "You entered:" << endl;
    for(int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    delete[] arr;
    return 0;
}
```

## Current Implementation Details

The transpiler works in two modes:

1. **Quick Transform Mode (Default)**: Uses regex-based transformation for direct code conversion without full parsing. This works well for most basic C code.

2. **AST-based Transform Mode (Partial Implementation)**: Parses code into an abstract syntax tree for more accurate transformations. This mode is not fully implemented yet but provides the foundation for handling more complex C code in the future.

## Limitations

- Handles only a subset of C language constructs
- May not preserve all comments or formatting
- Complex expressions might require manual adjustment after conversion
- Not all C libraries and functions have direct C++ equivalents
- Preprocessor directives may need manual refinement

## Future Improvements

- Complete the AST-based transformation pipeline
- Add support for more C constructs and libraries
- Improve preservation of comments and code formatting
- Handle complex expressions and statements more accurately
- Support C99 and C11 features
- Add configuration options for different C++ standards (C++11, C++14, C++17, etc.)

## Contributing

Contributions are welcome! Areas where help is particularly needed:

- Expanding the token patterns to cover more C syntax
- Enhancing the parser to build a more complete AST
- Adding more transformation rules in the transformer module
- Improving documentation and examples

## License

This project is open source and available under the MIT License.

## Acknowledgments

This transpiler is designed for educational and practical purposes to assist in the migration of C code to C++.
