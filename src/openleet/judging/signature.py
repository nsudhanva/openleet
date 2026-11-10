"""Problem specs (see judge/py/harness.py) and LeetCode-style starter code, read from Python
source with `ast`; nothing is executed."""

import ast
import warnings

NODE_TYPES = ("ListNode", "TreeNode")
NODE_COMMENTS = {
    "ListNode": (
        "# Definition for singly-linked list.\n"
        "# class ListNode:\n"
        "#     def __init__(self, val=0, next=None):\n"
        "#         self.val = val\n"
        "#         self.next = next\n"
    ),
    "TreeNode": (
        "# Definition for a binary tree node.\n"
        "# class TreeNode:\n"
        "#     def __init__(self, val=0, left=None, right=None):\n"
        "#         self.val = val\n"
        "#         self.left = left\n"
        "#         self.right = right\n"
    ),
}


def type_text(annotation: ast.expr | None) -> str:
    return ast.unparse(annotation).replace("'", "").replace('"', "") if annotation else "Any"


def public_methods(cls: ast.ClassDef) -> list[ast.FunctionDef]:
    return [
        f
        for f in cls.body
        if isinstance(f, ast.FunctionDef) and (not f.name.startswith("_") or f.name == "__init__")
    ]


def params_of(fn: ast.FunctionDef) -> list[dict]:
    return [{"name": a.arg, "type": type_text(a.annotation)} for a in fn.args.args[1:]]


def parse(code: str) -> ast.Module | None:
    """Python source as a tree; None when it does not parse. Old escape sequences in
    third-party code are not our concern, so their warnings are silenced."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            return ast.parse(code)
    except SyntaxError:
        return None


def classes(code: str) -> dict[str, ast.ClassDef]:
    tree = parse(code)
    if tree is None:
        return {}
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def function_spec(code: str, method: str | None, arg_names: set[str] | None) -> dict | None:
    """Spec of `class Solution`'s entry method: the named one, else the one whose parameters
    match the example inputs, else the only public one."""
    solution = classes(code).get("Solution")
    if solution is None:
        return None
    candidates = [f for f in public_methods(solution) if f.name != "__init__"]
    if method:
        candidates = [f for f in candidates if f.name == method]
    elif arg_names and len(candidates) > 1:
        candidates = [f for f in candidates if {p["name"] for p in params_of(f)} <= arg_names]
    if len(candidates) != 1:
        return None
    fn = candidates[0]
    return {
        "kind": "function",
        "cls": "Solution",
        "method": fn.name,
        "params": params_of(fn),
        "returns": type_text(fn.returns) if fn.returns else "Any",
    }


def design_spec(code: str, class_name: str, ops: set[str]) -> dict | None:
    """Spec of a design class: its constructor and the methods the examples call (helper
    methods of a reference solution are not part of the problem)."""
    cls = classes(code).get(class_name)
    if cls is None:
        return None
    methods = {
        f.name: {
            "params": [p["type"] for p in params_of(f)],
            "names": [p["name"] for p in params_of(f)],
            "returns": type_text(f.returns) if f.returns else "Any",
        }
        for f in public_methods(cls)
        if f.name == "__init__" or f.name in ops
    }
    if not ops <= set(methods):
        return None
    return {"kind": "design", "cls": class_name, "methods": methods}


def starter_code(spec: dict) -> str:
    """LeetCode's Python 3 template for a spec: signatures with empty bodies."""
    used = str(spec)
    header = "".join(NODE_COMMENTS[t] + "\n" for t in NODE_TYPES if t in used)
    if spec["kind"] == "function":
        args = "".join(f", {p['name']}: {p['type']}" for p in spec["params"])
        return (
            f"{header}class Solution:\n"
            f"    def {spec['method']}(self{args}) -> {spec['returns']}:\n        "
        )
    lines = [f"{header}class {spec['cls']}:\n"]
    for name, info in spec["methods"].items():
        args = "".join(f", {n}: {t}" for n, t in zip(info["names"], info["params"], strict=True))
        returns = "" if name == "__init__" else f" -> {info['returns']}"
        lines.append(f"\n    def {name}(self{args}){returns}:\n        \n")
    return "".join(lines)
