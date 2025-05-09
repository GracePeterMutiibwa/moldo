# Moldo Code Snippets

This folder contains various code examples for the Moldo visual programming language.

## Programs

1. **hello_world.moldo**: A simple "Hello, World!" program
2. **name_input.moldo**: Takes a name as input and displays a greeting
3. **grade_calculator.moldo**: Calculates a letter grade based on a numeric score
4. **temperature_converter.moldo**: Converts between Celsius and Fahrenheit temperatures
5. **calculator.moldo**: A simple calculator that performs basic arithmetic operations
6. **student_records.moldo**: Manages student records and computes grade averages

## Running the Programs

### Moldo Compilation and Execution

To compile a Moldo program to Python:

```bash
moldo compile program_name.moldo -o program_name.py
```

To run a compiled program:

```bash
python program_name.py
```

Or to compile and run in one step:

```bash
moldo run program_name.moldo
```

### Python Modules

Some programs depend on Python modules:

- **math_functions.py**: Contains basic arithmetic functions
- **temperature_utils.py**: Contains temperature conversion functions

## Example Usage

```bash
# Hello World
moldo run snippets/hello_world.moldo

# Name Input
moldo run snippets/name_input.moldo

# Grade Calculator
moldo run snippets/grade_calculator.moldo

# Temperature Converter
moldo run snippets/temperature_converter.moldo

# Calculator
moldo run snippets/calculator.moldo

# Student Records
python snippets/student_records.py
```
