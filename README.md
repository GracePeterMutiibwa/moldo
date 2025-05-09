# Moldo

![Moldo](https://raw.githubusercontent.com/GracePeterMutiibwa/moldo/main/assets/moldo-var.png)

Moldo is a visual programming language with an XML-like syntax that compiles to Python. This document details the syntax structure and usage patterns for Moldo code.

## Installation

```bash

pip install moldo

```

## Quick Start

## 1. Basic Structure

Moldo code consists of blocks represented by XML-like tags. Each block represents a programming concept or operation.

### 1.1 Block Syntax

The basic block structure is:

```xml
<mblock type="blockType">content</mblock>
```

Where:

- `blockType` defines the operation or concept.
- `content` contains the code or data for that block (often PCDATA or nested blocks).

### 1.2 Block Attributes

Blocks can have additional attributes:

```xml
<mblock type="blockType" attribute1="value1" attribute2="value2">content</mblock>
```

Common attributes include:

- `condition`: Used for loop and if-statement conditions. Attribute values can use single or double quotes.

## 2. Core Block Types

### 2.1 Variable Declaration and Assignment

Used to declare variables or assign values. The content is Python assignment code.

```xml
<mblock type="variable">variableName = value</mblock>
```

**Example:**

```xml
<mblock type="variable">counter = 0</mblock>
<mblock type="variable">name = "Alice"</mblock>
<mblock type="variable">numbers =</mblock>
<mblock type="variable">result = x * y</mblock>
```

**Note:** Literal `<` or `>` characters are not allowed directly in this blocks if they are not escaped unless they are within a Python string literal.

For example, `my_html = "<p>Hello</p>"` is invalid because of the raw `<` and `>`.

It should be `my_html = '"<p>Hello</p>"'` or `my_html = '''<p>Hello</p>'''` if the Python code itself is defining a string containing HTML.

### 2.2 Input

Prompts the user for input. The PCDATA content is the prompt message. The result is typically assigned to a variable using a subsequent "variable" block.

```xml
<mblock type="input">Prompt message for the user</mblock>
```

**Example:**
To get input and store it:

```xml
<mblock type="variable">user_name = input("Enter your name: ")</mblock>
<mblock type="variable">age_str = input('How old are you? ')</mblock>
```

A direct input block (value often lost if not assigned):

```xml
<mblock type="input">Press Enter to continue...</mblock>
```

This will translate to: `input('Press Enter to continue...')`

### 2.3 Output/Print

Prints expressions or text to the console.

```xml
<mblock type="print">expression_or_text</mblock>
```

**Behavior:**

- If `expression_or_text` is a valid Python string literal (e.g., `"Hello"`, `'World'`, `f"Name: {name}"`), it's printed directly.
- If `expression_or_text` is a valid Python identifier (e.g., `my_variable`, `object.attribute`), it's printed directly.
- Otherwise (e.g., plain text like `Hello World`, or a complex expression like `x + y` that isn't an f-string), it will be treated as a literal string and Python's `repr()` will be used to ensure it's quoted for the `print()` function. To print the _result_ of an expression like `x + y`, use an f-string: `<mblock type="print">f"{x + y}"</mblock>` or assign it to a variable first.

**Example:**

```xml
<comment>Printing plain text (will be repr'd)</comment>
<mblock type="print">Hello, Moldo World!</mblock>

<comment>Printing an existing Python string literal</comment>
<mblock type="print">"This is already a string."</mblock>

<comment>Printing an f-string</comment>
<mblock type="variable">name = "Moldo"</mblock>
<mblock type="print">f"Hello, {name}!"</mblock>

<comment>Printing a variable's value</comment>
<mblock type="variable">count = 100</mblock>
<mblock type="print">count</mblock>

<comment>Printing the literal string 'x + y' (gets repr'd)</comment>
<mblock type="print">x + y</mblock>

<comment>Printing the result of x + y</comment>
<mblock type="variable">x = 5</mblock>
<mblock type="variable">y = 3</mblock>
<mblock type="print">f"{x + y}"</mblock>

<comment>Empty print block for a newline</comment>
<mblock type="print"></mblock>
```

## 2.4 Highlight Blocks

The `highlight` block type is intended for code that might interact with a "Moldo Bridge" for visual programming aspects like highlighting execution steps. Its PCDATA content is treated as direct Python code lines, similar to `variable` or `call` blocks.

```xml
<mblock type="highlight">
moldoBridge.highlight(1, 'nodes-meta')
</mblock>
```

## 3. Control Flow

### 3.1 Conditional Statements (If Statement)

Executes blocks of code based on a condition. The condition is a Python boolean expression.

```xml
<mblock type="if" condition="boolean_expression">
    <!-- Nested blocks -->
</mblock>
```

**Example:**

```xml
<mblock type="variable">age = 20</mblock>
<mblock type="if" condition="age >= 18">
    <mblock type="print">'You are an adult.'</mblock>
    <mblock type="if" condition="age > 65">
        <mblock type="print">'You are a senior citizen.'</mblock>
    </mblock>
</mblock>
<mblock type="if" condition="age < 18">
    <mblock type="print">'You are a minor.'</mblock>
</mblock>
```

### 3.2 Loops

#### For Loop

Iterates over a sequence. The condition is a Python `for` loop header (e.g., `item in iterable`).

```xml
<mblock type="loop" condition="iterator in iterable">
    <!-- Nested blocks -->
</mblock>
```

**Example:**

```xml
<mblock type="loop" condition="i in range(3)">
    <mblock type="print">f"Current value: {i}"</mblock>
</mblock>

<mblock type="variable">my_list = ["a", "b", "c"]</mblock>
<mblock type="loop" condition="char in my_list">
    <mblock type="print">char</mblock>
</mblock>
```

#### While Loop

Executes blocks as long as a condition is true.

```xml
<mblock type="while" condition="boolean_expression">
    <!-- Nested blocks -->
</mblock>
```

**Example:**

```xml
<mblock type="variable">counter = 0</mblock>
<mblock type="while" condition="counter < 3">
    <mblock type="print">f"Counter is {counter}"</mblock>
    <mblock type="variable">counter += 1</mblock>
</mblock>
```

## 4. Functions and Modules

### 4.1 Importing Modules

The content of the `import blocks` is the module name or `module as alias`.

```xml
<mblock type="import">math</mblock>

<mblock type="import">os.path as osp</mblock>
```

### 4.2 Calling Functions

Function calls are typically part of "variable" blocks (for assignment) or "print" blocks (to print results), or "call" blocks (if the function is called for its side effects and its return value is not immediately used).

```xml
<mblock type="variable">result = my_function(arg1, arg2)</mblock>

<mblock type="print">another_function()</mblock>
```

Please note how the content of Python blocks for the function call is structured;

```xml
<mblock type="call">do_something_for_effect()</mblock>
```

**Example:**

```xml
<mblock type="import">math</mblock>
<mblock type="variable">square_root_of_25 = math.sqrt(25)</mblock>
<mblock type="print">square_root_of_25</mblock>
<mblock type="call">print("Effect call")</mblock>
```

### 4.3 Defining Functions

Functions are defined using the `<python>` block (see Section 7.1) or in separate `.py` files and then imported.

## 5. Data Structures

Data structures like lists and dictionaries are typically created within "variable" blocks.

### 5.1 Lists

```xml
<mblock type="variable">my_list = [item1, item2, item3]</mblock>
<mblock type="variable">numbers =</mblock>
<mblock type="variable">names = ["Alice", "Bob", "Charlie"]</mblock>
```

Accessing items (PCDATA is Python code):

```xml
<mblock type="variable">first_number = numbers</mblock>
<mblock type="print">names</mblock>
```

### 5.2 Dictionaries

```xml
<mblock type="variable">my_dict = {"key1": "value1", "key2": 123}</mblock>
<mblock type="variable">student = {"name": "Alice", "age": 20, "grades":}</mblock>
```

Accessing items:

```xml
<mblock type="variable">student_name = student["name"]</mblock>
<mblock type="print">f"Student Age: {student['age']}"</mblock>
```

## 6. Comments

Moldo supports block-style comments using `<comment>` tags. The content of these comments is translated into Python `#` style comments. These comments can span multiple lines.

```xml
<comment>This is a Moldo comment.
It can span multiple lines.
Literal < and > characters are allowed here (as long as they don't form a nested </comment> tag prematurely).
</comment>
<mblock type="print">'Code after comment'</mblock>
<mblock type="variable">x = 1</mblock> <comment>This is an inline-style Moldo comment</comment>
```

**Output Python:**

```python
# This is a Moldo comment.
# It can span multiple lines.
# Literal < and > characters are allowed here (as long as they don't form a nested </comment> tag prematurely).
print('Code after comment')
x = 1 # This is an inline-style Moldo comment
```

**Note:** Moldo `<comment>` tags should not be placed _inside_ the PCDATA content of a `<python>` block. Use Python's native `#` comments within `<python>` blocks.

## 7. Python Integration

### 7.1 Inline Python (`<python>` block)

For complex operations, defining functions, or code that doesn't have a dedicated Moldo block, you can use the `<python>` block. The content of this block is treated as raw Python code. Its internal indentation is preserved exactly as written, and the entire block is then indented according to its position in the Moldo structure.

```xml
<python>
# This is Python code
import random

def generate_random_number(min_val, max_val):
    # This comment is a Python comment
    return random.randint(min_val, max_val)

my_num = generate_random_number(1, 100)
</python>
<mblock type="print">f"My random number from python block: {my_num}"</mblock>
```

## 8. Advanced Features

### 8.1 Block Nesting

Blocks can be nested to create complex structures. `mblock_content` allows for `element`s, which include `mblock_element`, `python_element`, and `moldo_comment_element`.

```xml
<mblock type="loop" condition="i in range(2)">
    <mblock type="print">f"Outer loop: {i}"</mblock>
    <comment>Inside outer loop</comment>
    <mblock type="loop" condition="j in range(2)">
        <mblock type="print">f"  Inner loop: {j}"</mblock>
        <mblock type="variable">product = i * j</mblock>
        <mblock type="print">f"  Product: {product}"</mblock>
    </mblock>
</mblock>
```

## 8.2 Creating Custom Functions

To create functions that can be used in Moldo, use the `@moldo_function` decorator:

```python

from moldo.decorators import moldo_function

@moldo_function(reference_name="add")
def add_numbers(a: float, b: float) -> float:
	"""Add two numbers together."""

	return a + b

```

Currently, the above structure can only be used in moldo files;

## 9. Command Line Interface

The `moldo` command provides several options:

```bash
moldo compile <input_file> -o <output_file> # Compile Moldo code to Python

python snippets/cnr.py <input_file> # Compile and run Moldo code run file is included in the snippets

moldo --help # Show help message

moldo serve # starts a fast api server for the compiler accessible via /compile, default address is 127.0.0.1:8000

```

## 10. Code Examples (Summary)

### 10.1 Hello World

```xml
<comment>A simple Hello World program</comment>
<mblock type="print">Hello, Moldo World!</mblock>
```

### 10.2 Basic Calculator (Illustrative)

```xml
<mblock type="variable">num1_str = input("Enter first number: ")</mblock>
<mblock type="variable">num2_str = input("Enter second number: ")</mblock>
<mblock type="variable">op_str = input("Enter operation (+, -, *, /): ")</mblock>

<mblock type="variable">num1 = float(num1_str)</mblock>
<mblock type="variable">num2 = float(num2_str)</mblock>
<mblock type="variable">result = "Invalid operation"</mblock>

<mblock type="if" condition='op_str == "+"'>
    <mblock type="variable">result = num1 + num2</mblock>
</mblock>
<mblock type="if" condition='op_str == "-"'>
    <mblock type="variable">result = num1 - num2</mblock>
</mblock>
<mblock type="if" condition='op_str == "*"'>
    <mblock type="variable">result = num1 * num2</mblock>
</mblock>
<mblock type="if" condition='op_str == "/"'>
    <mblock type="if" condition="num2 != 0">
        <mblock type="variable">result = num1 / num2</mblock>
    </mblock>
    <mblock type="if" condition="num2 == 0">
        <mblock type="variable">result = "Error: Division by zero"</mblock>
    </mblock>
</mblock>
<mblock type="print">f"Result: {result}"</mblock>
```

## 11. Best Practices

1.  Use `<comment>...</comment>` for documenting Moldo code.

2.  Only Use Python's `#` comments for comments _within_ `<python>` blocks.

3.  Maintain clear visual indentation in your Moldo code for readability, even though the compiler primarily relies on block structure rather than visual Pythonic indentation for Moldo itself.

4.  Note that the code within `<python>` blocks, however, _must_ have correct Python indentation, thats what the compiler expects

5.  For `print` blocks, if you want to print the result of a complex expression, use f-strings (e.g., `<mblock type="print">f"{expression_result}"</mblock>`) or assign the result to a variable and print the variable.

6.  Plain text or expressions not directly identifiable as Python string literals or simple identifiers will be treated as literal strings to be printed.

7.  Content in most `mblock` types (like "variable", "print", "import") cannot contain raw unescaped `<` or `>` characters as they delimit tags.

8.  These characters are allowed in attribute string values and within the content of `<comment>` blocks.

## Contributing

Contributions are welcome Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/GracePeterMutiibwa/moldo/main/LICENSE.txt) file for details.

## Author

- **Mutiibwa Grace Peter**
  - [GitHub](https://github.com/GracePeterMutiibwa)
  - [Website](https://www.gracepeter.space)

## Acknowledgments

- ANTLR4 for the parsing infrastructure

- Python community for inspiration and tools
