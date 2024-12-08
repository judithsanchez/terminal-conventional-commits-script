# Python Beginner's Guide

## Variables, Functions, and Conditionals

### Defining Functions
Functions in Python allow you to encapsulate reusable blocks of code. Here's a simple example of a function that greets a person by their name:

```python
def greet(name: str) -> None:
    """Function to greet a person with their name."""
    print(f"Hello, {name}!")

# Calling the function
greet("Alice")
```

### Lambda Functions
Lambda functions, also known as anonymous functions, are small functions defined without a name. They are useful for short-term tasks where a full function definition would be unnecessary.

```python
# A lambda function to add two numbers
add = lambda a: int, b: int: a + b

result = add(3, 4)
print(result)  # Output: 7
```

**Note:** Python does not support direct return type annotations for lambda functions. To specify types, use comments or type hints in context.

### Variable Handling
Unlike JavaScript, Python does not have block-scoped variable declarations like `let` and `const`. Variables in Python are dynamically typed and can be reassigned at any time.

- Use **naming conventions** (e.g., all uppercase letters) to indicate that a variable is a constant, though this is not enforced by the language.
- Example:

```python
PI = 3.14159  # Constant by convention
radius = 5
circumference = 2 * PI * radius
```

### Conditional Statements
Conditional statements in Python allow you to execute different blocks of code based on conditions. Here’s an example of a function that checks if a number is positive, negative, or zero:

```python
def check_number(num: int) -> None:
    """Function to check if a number is positive, negative, or zero."""
    if num > 0:
        print("The number is positive.")
    elif num < 0:
        print("The number is negative.")
    else:
        print("The number is zero.")

# Using the function
check_number(10)
check_number(-5)
check_number(0)
```

