import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.error.ErrorListener import ErrorListener
import re

from .MoldoLexer import MoldoLexer
from .MoldoParser import MoldoParser
from .MoldoParserVisitor import MoldoParserVisitor


class MyErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.critical_errors = []

        # This regex will precisely match the "extraneous input 'WHITESPACE_CHARS' expecting ..." messages.
        # \s matches any whitespace char, \u00A0 is non-breaking space.
        # The '...' part of the extraneous input is captured by [\s\u00A0]+
        self.ignorable_whitespace_regex = re.compile(
            r"extraneous input '[\s\u00A0]+' expecting {<EOF>, '<mblock', '<python', '<comment>'}"
        )

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Extract the actual message part after "msg: "
        message_content = msg  # msg is already just the core message string

        # If the message content exactly matches our ignorable pattern, DO NOTHING.
        if self.ignorable_whitespace_regex.fullmatch(message_content):
            return

        # For all other errors, consider them critical.
        full_error_message = f"Parser Error: line {line}:{column} msg: {msg}"
        self.critical_errors.append(full_error_message)
        # Print ONLY CRITICAL errors to stderr.
        print(full_error_message, file=sys.stderr)


class MoldoVisitorImpl(MoldoParserVisitor):
    def __init__(self):
        self.indent_level = 0

    def _indent_str(self):
        return "    " * self.indent_level

    def visitProgram(self, ctx: MoldoParser.ProgramContext):
        code_parts = []
        if ctx.element():
            for element_ctx in ctx.element():
                visited_element = self.visit(element_ctx)
                if (
                    isinstance(visited_element, str) and visited_element.strip()
                ):  # Only add if it has content
                    code_parts.append(visited_element)
        return "\n".join(code_parts)

    def visitElement(self, ctx: MoldoParser.ElementContext):
        if ctx.mblock_element():
            return self.visitMblock_element(ctx.mblock_element())
        elif ctx.python_element():
            return self.visitPython_element(ctx.python_element())
        elif ctx.moldo_comment_element():
            return self.visitMoldo_comment_element(ctx.moldo_comment_element())
        return ""

    def visitAttribute(self, ctx: MoldoParser.AttributeContext):
        name = ""
        value = ""
        if hasattr(ctx, "T_ID") and ctx.T_ID():
            name = ctx.T_ID().getText()

        if hasattr(ctx, "T_STRING") and ctx.T_STRING():
            value_token = ctx.T_STRING()
            value = value_token.getText()
            if len(value) >= 2:
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]
        return name, value

    def _process_mblock_content_as_code_lines(
        self, mblock_content_ctx: MoldoParser.Mblock_contentContext
    ):
        processed_lines = []
        if mblock_content_ctx and mblock_content_ctx.children:
            for child_ctx in mblock_content_ctx.children:
                if isinstance(child_ctx, MoldoParser.ElementContext):
                    nested_code_block = self.visit(child_ctx)
                    if isinstance(nested_code_block, str) and nested_code_block.strip():
                        processed_lines.append(nested_code_block)
                elif (
                    isinstance(child_ctx, TerminalNodeImpl)
                    and child_ctx.symbol.type == MoldoLexer.PCDATA
                ):
                    pcdata_text = child_ctx.getText()
                    if pcdata_text.strip():
                        for line in pcdata_text.splitlines():
                            stripped_line_content = line.strip()
                            if stripped_line_content:
                                processed_lines.append(
                                    self._indent_str() + stripped_line_content
                                )
        return processed_lines

    def visitMoldo_comment_element(self, ctx: MoldoParser.Moldo_comment_elementContext):
        comment_text_parts = []
        if ctx.comment_content_inner() and hasattr(
            ctx.comment_content_inner(), "COMMENT_TEXT_CONTENT"
        ):
            for ctc_node in ctx.comment_content_inner().COMMENT_TEXT_CONTENT():
                comment_text_parts.append(ctc_node.getText())

        full_comment_text = "".join(comment_text_parts)

        python_comment_lines = []
        if full_comment_text.strip():
            for line in full_comment_text.splitlines():
                python_comment_lines.append(self._indent_str() + "# " + line.strip())
            return "\n".join(python_comment_lines)
        else:
            return self._indent_str() + "# (empty Moldo comment)"

    def visitMblock_element(self, ctx: MoldoParser.Mblock_elementContext):
        attributes = {}
        if ctx.attribute():
            for attr_ctx in ctx.attribute():
                name, value = self.visitAttribute(attr_ctx)
                attributes[name] = value

        block_type = attributes.get("type")
        condition = attributes.get("condition")

        generated_code_lines = []
        current_mblock_content = ctx.mblock_content()

        if (
            block_type == "variable"
            or block_type == "call"
            or block_type == "highlight"
        ):
            code_lines = self._process_mblock_content_as_code_lines(
                current_mblock_content
            )
            generated_code_lines.extend(code_lines)

        elif block_type == "import":
            import_statement_parts = []

            if current_mblock_content and current_mblock_content.children:
                for child in current_mblock_content.children:
                    if (
                        isinstance(child, TerminalNodeImpl)
                        and child.symbol.type == MoldoLexer.PCDATA
                    ):
                        import_statement_parts.append(child.getText().strip())
            import_content = "".join(import_statement_parts)

            if import_content:
                for each_import_req in [
                    "import sys",
                    "sys.path.append('.')",
                ]:
                    generated_code_lines.append(
                        self._indent_str() + f"{each_import_req}"
                    )

                generated_code_lines.append(
                    self._indent_str() + f"import {import_content}"
                )

        elif block_type == "input":
            prompt_str_parts = []
            if current_mblock_content and current_mblock_content.children:
                for child in current_mblock_content.children:
                    if (
                        isinstance(child, TerminalNodeImpl)
                        and child.symbol.type == MoldoLexer.PCDATA
                    ):
                        prompt_str_parts.append(child.getText().strip())
            prompt = "".join(prompt_str_parts)
            generated_code_lines.append(self._indent_str() + f"input({repr(prompt)})")

        elif block_type == "print":
            expr_str_parts = []
            if current_mblock_content and current_mblock_content.children:
                for child in current_mblock_content.children:
                    if (
                        isinstance(child, TerminalNodeImpl)
                        and child.symbol.type == MoldoLexer.PCDATA
                    ):
                        expr_str_parts.append(child.getText())

            expression = "".join(expr_str_parts).strip()

            if expression:
                is_likely_python_string_literal = (
                    (expression.startswith('"') and expression.endswith('"'))
                    or (expression.startswith("'") and expression.endswith("'"))
                    or (expression.startswith('f"') and expression.endswith('"'))
                    or (expression.startswith("f'") and expression.endswith("'"))
                    or (expression.startswith('r"') and expression.endswith('"'))
                    or (expression.startswith("r'") and expression.endswith("'"))
                    or (expression.startswith('b"') and expression.endswith('"'))
                    or (expression.startswith("b'") and expression.endswith("'"))
                    or (expression.startswith('"""') and expression.endswith('"""'))
                    or (expression.startswith("'''") and expression.endswith("'''"))
                )

                is_identifier_path = (
                    all(
                        part.isidentifier()
                        or (part.endswith("()") and part[:-2].isidentifier())
                        for part in expression.split(".")
                    )
                    and expression
                )

                if is_likely_python_string_literal or is_identifier_path:
                    generated_code_lines.append(
                        self._indent_str() + f"print({expression})"
                    )
                else:
                    generated_code_lines.append(
                        self._indent_str() + f"print({repr(expression)})"
                    )
            else:
                generated_code_lines.append(self._indent_str() + "print()")

        elif block_type in ["if", "loop", "while"]:
            header = ""
            effective_condition = (
                condition
                if condition is not None
                else "False # Condition attribute was missing"
            )
            if block_type == "if":
                header = f"if {effective_condition}:"
            elif block_type == "loop":
                header = f"for {effective_condition}:"
            elif block_type == "while":
                header = f"while {effective_condition}:"

            generated_code_lines.append(self._indent_str() + header)

            self.indent_level += 1
            body_content_lines = []
            if current_mblock_content and current_mblock_content.children:
                for child_ctx in current_mblock_content.children:
                    visited_child_code = self.visit(child_ctx)
                    if (
                        isinstance(visited_child_code, str)
                        and visited_child_code.strip()
                    ):
                        body_content_lines.append(visited_child_code)

            if body_content_lines:
                generated_code_lines.extend(body_content_lines)
            else:
                generated_code_lines.append(self._indent_str() + "pass")
            self.indent_level -= 1

        else:
            comment_intro = f"# Fallback: Content for mblock "
            if block_type:
                comment_intro += f"type: {block_type}"
            else:
                comment_intro += "with no 'type' attribute"

            code_lines = self._process_mblock_content_as_code_lines(
                current_mblock_content
            )
            if code_lines:
                generated_code_lines.append(self._indent_str() + comment_intro)
                generated_code_lines.extend(code_lines)
            elif block_type or (
                current_mblock_content is None or not current_mblock_content.children
            ):
                generated_code_lines.append(
                    self._indent_str()
                    + f"# Encountered mblock ({block_type if block_type else 'no type'}) with no processable content and not explicitly handled."
                )

        final_code = "\n".join(
            line
            for line in generated_code_lines
            if line.strip()
            or line == self._indent_str() + "pass"
            or line.strip().startswith("#")
        )
        return final_code

    def visitPython_element(
        self, ctx: MoldoParser.Python_elementContext
    ):  # <<< PYTHON BLOCK INDENTATION "AS IS" (STRICT)
        base_indent_str = self._indent_str()
        py_content_ctx = ctx.python_content_text()

        if (
            py_content_ctx
            and hasattr(py_content_ctx, "PCDATA")
            and py_content_ctx.PCDATA()
        ):
            raw_python_code = py_content_ctx.PCDATA().getText()
            lines = raw_python_code.splitlines()

            if (
                not lines and not raw_python_code.strip()
            ):  # Truly empty or only whitespace PCDATA
                return base_indent_str + "pass"
            if (
                not any(line.strip() for line in lines) and raw_python_code.strip()
            ):  # PCDATA was just newlines
                return (
                    base_indent_str + "pass"
                )  # Or join of base_indent_str + rstripped lines if you want blank indented lines.
            if (
                not any(line.strip() for line in lines) and not raw_python_code.strip()
            ):  # PCDATA was just whitespace on one line
                return base_indent_str + "pass"

            # Prepend the current script indent to each line of the raw Python code.
            # The internal relative indentation of the PCDATA block is preserved by rstrip() only.
            final_output_lines = [(base_indent_str + line.rstrip()) for line in lines]

            return "\n".join(final_output_lines)
        else:
            return base_indent_str + "pass"


def cast(moldo_code_string: str) -> tuple[str, list]:
    input_stream = InputStream(moldo_code_string.strip())
    lexer = MoldoLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MoldoParser(token_stream)

    error_listener = MyErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    parse_tree = parser.program()

    visitor = MoldoVisitorImpl()
    python_code = visitor.visit(parse_tree)

    return python_code, error_listener.critical_errors
