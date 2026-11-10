"""Test inputs from two places: the statement's examples (with their official outputs) and
LeetCodeDataset's `check` function (inputs only; its expected values are not trusted)."""

import ast
import html
import json
import re
from typing import Any

from openleet.judging.signature import parse

TAG = re.compile(r"<[^>]+>")
# "Input: ... Output: ..." up to the explanation, the next example or the end of the block.
EXAMPLE = re.compile(
    r"Input:?\s*(.*?)\s*Output:?\s*(.*?)\s*(?=Explanation|Example \d|Constraints|Follow|Note:|$)",
    re.S,
)
ASSIGNMENT = re.compile(r"(?:^|,\s*)([A-Za-z_]\w*)\s*=\s*")
NODE_HELPERS = ("list_node", "tree_node")


class Unparsable(ValueError):
    pass


def json_value(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise Unparsable(text[:80]) from error


def assignments(text: str) -> dict[str, Any]:
    """'nums = [2,7], target = 9' -> {'nums': [2, 7], 'target': 9}."""
    marks = list(ASSIGNMENT.finditer(text))
    if not marks or marks[0].start() != 0:
        raise Unparsable(text[:80])
    out = {}
    for mark, nxt in zip(marks, [*marks[1:], None], strict=True):
        out[mark.group(1)] = json_value(
            text[mark.end() : nxt.start() if nxt else len(text)].strip()
        )
    return out


def statement_examples(description: str | None) -> list[dict]:
    """[{'input': {...}, 'output': value}] for function problems, or
    [{'input': {'ops': [...], 'args': [...]}, 'output': [...]}] for design problems."""
    if not description:
        return []
    text = html.unescape(TAG.sub(" ", description)).replace("\xa0", " ")
    examples = []
    for raw_in, raw_out in EXAMPLE.findall(text):
        raw_in, raw_out = raw_in.strip(), raw_out.strip()
        try:
            if raw_in.startswith("["):
                ops, args = (json_value(line) for line in raw_in.splitlines() if line.strip())
                if not (ops and all(isinstance(op, str) for op in ops) and len(ops) == len(args)):
                    continue
                examples.append(
                    {
                        "input": {"ops": ops, "args": args},
                        "output": json_value(raw_out),
                        "design": True,
                    }
                )
            else:
                examples.append({"input": assignments(raw_in), "output": json_value(raw_out)})
        except Unparsable, ValueError:
            continue
    return examples


def literal(node: ast.expr) -> Any:
    """A dataset argument: a literal, or list_node([...]) / tree_node([...]) around one."""
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) in NODE_HELPERS:
        return literal(node.args[0]) if node.args else []
    return ast.literal_eval(node)


def dataset_inputs(check_source: str | None) -> list[dict]:
    """Keyword arguments of every `candidate(...)` call in LeetCodeDataset's check function."""
    if not check_source:
        return []
    tree = parse(check_source)
    if tree is None:
        return []
    inputs, seen = [], set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "candidate"):
            continue
        try:
            kwargs = {k.arg: literal(k.value) for k in node.keywords if k.arg}
        except ValueError, TypeError, SyntaxError, RecursionError:
            continue
        key = json.dumps(kwargs, sort_keys=True)
        if kwargs and key not in seen:
            seen.add(key)
            inputs.append(kwargs)
    return inputs
