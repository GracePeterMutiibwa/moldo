"""
Convert an exported Moldo flow JSON to runnable Python source code.

Public API:
    python_source = compile_flow(flow_json: dict) -> str

Algorithm:
    Iterative DFS using an explicit stack so recursion depth never depends
    on how deeply the flow graph is nested.

Stack item shapes:
    ('node',   node_dict)  -- visit this flow node and expand it onto the stack
    ('emit',   code_line)  -- write this line at the current indentation level
    ('indent', )           -- step one indentation level in  (4 spaces)
    ('dedent', )           -- step one indentation level out (4 spaces)
"""

import json

PYTHON_CAST_FOR_TYPE = {
    "int": "int",
    "float": "float",
    "bool": "bool",
    "text": "str",
    "str": "str",
}


def _build_print_call(message: str) -> str:
    """Messages with {variable} placeholders become f-strings."""
    if "{" in message and "}" in message:
        return f'print(f"{message}")'
    return f'print("{message}")'


def _build_condition_right_side(condition_meta: dict) -> str:
    """Return the right-hand side of a conditional as a Python token."""
    use_variable = condition_meta.get("useVariable", False)
    right_var = condition_meta.get("rightVar") or ""
    right_value = str(condition_meta.get("rightValue", ""))

    if use_variable and right_var:
        return right_var

    try:
        float(right_value)
        return right_value  # numeric literal, no quotes
    except (ValueError, TypeError):
        return f'"{right_value}"'  # string literal, quoted


def compile_flow(flow_json: dict) -> str:
    """
    Convert an exported Moldo flow JSON to a Python source string.

    Prints the incoming JSON and the generated Python to stdout so you can
    verify both sides without opening any files.

    Parameters
    ----------
    flow_json : dict
        The full exported JSON as produced by mflow-editor's export feature.

    Returns
    -------
    str
        Valid Python source code that implements the same logic as the flow.
    """

    # print("json input")
    # print(json.dumps(flow_json, indent=2))
    # print()

    # Build a lookup from nodeId to visualState settings so community-block
    # nodes can recover their manifest even when it is absent from flowObject.meta.
    visual_settings_by_node_id: dict[str, dict] = {}
    for vs_node in flow_json.get("visualState", {}).get("nodes", []):
        node_id = vs_node.get("id", "")
        if node_id:
            visual_settings_by_node_id[node_id] = vs_node.get("settings", {})

    first_node = flow_json["flowObject"]["start"]

    generated_lines: list[str] = []
    needed_imports: list[str] = []
    current_indent: int = 0

    # Iterative DFS stack
    # items are processed LIFO (last appended = first popped)
    dfs_stack: list[tuple] = [("node", first_node)]

    while dfs_stack:
        stack_item = dfs_stack.pop()
        action = stack_item[0]

        if action == "emit":
            code_line: str = stack_item[1]
            generated_lines.append("    " * current_indent + code_line)

        elif action == "indent":
            current_indent += 1

        elif action == "dedent":
            current_indent = max(0, current_indent - 1)

        elif action == "node":
            node: dict = stack_item[1]
            if node is None:
                continue

            node_type: str = node.get("type", "")
            meta: dict = node.get("meta", {})
            next_node = node.get("next")

            if node_type == "termination":
                continue

            elif node_type == "declaration":
                # Push next_node first so it lives deep in the stack and runs
                # only after all variable assignments have been emitted.
                if next_node:
                    dfs_stack.append(("node", next_node))
                # Push in reverse so the first variable pops first.
                for var_name, default_value in reversed(list(meta.items())):
                    dfs_stack.append(("emit", f"{var_name} = {repr(default_value)}"))

            elif node_type == "output":
                if next_node:
                    dfs_stack.append(("node", next_node))
                message: str = meta.get("message", "")
                dfs_stack.append(("emit", _build_print_call(message)))

            elif node_type == "input":
                if next_node:
                    dfs_stack.append(("node", next_node))
                target_variable: str = meta.get("selectedVariable", "_inp")
                variable_type: str = meta.get("variableType", "text").lower()
                prompt_message: str = meta.get("displayMessage", "Enter value:")
                cast_function: str = PYTHON_CAST_FOR_TYPE.get(variable_type, "str")
                dfs_stack.append(
                    ("emit", f'{target_variable} = {cast_function}(input("{prompt_message}"))')
                )

            elif node_type == "community-block":
                if next_node:
                    dfs_stack.append(("node", next_node))

                mold_name: str = meta.get("moldName", "")
                block_id: str = meta.get("blockId", "")
                params: dict = meta.get("params", {})

                # Manifest may only exist in visualState, not in flowObject.meta
                node_id = node.get("nodeId", "")
                vs_settings = visual_settings_by_node_id.get(node_id, {})
                manifest: dict = meta.get("manifest") or vs_settings.get("manifest") or {}
                if not params:
                    params = vs_settings.get("params", {})

                python_call: str = manifest.get("pythonCall") or f"{mold_name}.{block_id}"
                module_name: str = python_call.rsplit(".", 1)[0]

                if module_name not in needed_imports:
                    needed_imports.append(module_name)

                # When we have a manifest, use its declared output slot ids.
                # When we don't, fall back to a convention: any param whose value
                # does NOT start with '@' is an output variable name (not an input).
                manifest_outputs: list = manifest.get("outputs", [])
                if manifest_outputs:
                    output_slot_ids: set[str] = {out["id"] for out in manifest_outputs}
                else:
                    output_slot_ids = {k for k, v in params.items() if not str(v).startswith("@")}

                call_arguments: list[str] = []
                for param_key, param_value in params.items():
                    if param_key in output_slot_ids:
                        continue
                    str_value = str(param_value)
                    if str_value.startswith("@"):
                        arg_expression = str_value[1:]  # @varName -> varName
                    else:
                        arg_expression = repr(param_value)
                    call_arguments.append(f"{param_key}={arg_expression}")

                call_expression: str = f'{python_call}({", ".join(call_arguments)})'

                output_variable_names: list[str] = []
                if manifest_outputs:
                    for output_slot in manifest_outputs:
                        assigned_var = str(params.get(output_slot["id"], "")).strip()
                        if assigned_var:
                            output_variable_names.append(assigned_var)
                else:
                    for param_key, param_value in params.items():
                        str_value = str(param_value).strip()
                        if param_key in output_slot_ids and str_value:
                            output_variable_names.append(str_value)

                if output_variable_names:
                    lhs = ", ".join(output_variable_names)
                    dfs_stack.append(("emit", f"{lhs} = {call_expression}"))
                else:
                    dfs_stack.append(("emit", call_expression))

            elif node_type == "loop":
                iteration_count: int = meta.get("iterations", 1)
                loop_body_node: dict = meta.get("body")

                if next_node:
                    dfs_stack.append(("node", next_node))

                # Push in reverse execution order (LIFO): for-header runs first
                dfs_stack.append(("dedent",))
                if loop_body_node:
                    dfs_stack.append(("node", loop_body_node))
                dfs_stack.append(("indent",))
                dfs_stack.append(("emit", f"for _loop_i in range({iteration_count}):"))

            elif node_type == "decision":
                conditional_nodes: list = meta.get("decisions", [])

                if next_node:
                    dfs_stack.append(("node", next_node))

                # Iterate in reverse so the FIRST conditional ends up on TOP of the
                # stack (last pushed = first popped = first emitted).
                for push_index, conditional_node in enumerate(reversed(conditional_nodes)):
                    condition_meta: dict = conditional_node.get("meta", {})
                    branch_body = conditional_node.get("next")

                    left_var: str = condition_meta.get("leftVar", "")
                    operator: str = condition_meta.get("operator", "==")
                    right_side: str = _build_condition_right_side(condition_meta)
                    condition: str = f"{left_var} {operator} {right_side}"

                    actual_index = len(conditional_nodes) - 1 - push_index
                    keyword = "if" if actual_index == 0 else "elif"

                    dfs_stack.append(("dedent",))
                    if branch_body:
                        dfs_stack.append(("node", branch_body))
                    dfs_stack.append(("indent",))
                    dfs_stack.append(("emit", f"{keyword} {condition}:"))

    import_lines: list[str] = [f"import {mod}" for mod in needed_imports]
    blank_separator = [""] if import_lines else []
    all_lines = import_lines + blank_separator + generated_lines

    python_source: str = "\n".join(all_lines)

    # print("Generated Python Code")
    # print(python_source)
    # print()

    return python_source
