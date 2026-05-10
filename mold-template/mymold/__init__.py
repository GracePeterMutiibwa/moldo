# mymold — Moldo community mold
# Replace this file with your actual block implementations.
# Each function listed under pythonCall in moldo.json must be importable
# from this package (i.e. mymold.<function_name>).


def greet(name: str, style: str = "casual") -> None:
    """Print a greeting in the chosen style."""
    if style == "formal":
        print(f"Good day, {name}.")
    elif style == "shout":
        print(f"HEY {name.upper()}!!!")
    else:
        print(f"Hey, {name}!")


def reverse_text(text: str) -> str:
    """Return the input string reversed."""
    return text[::-1]
