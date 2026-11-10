"""Turns LeetCode-style JSON test input into Python objects, calls a solution, and turns the
result back into JSON. Shared by the judge's zygote and by the offline test builder, so a
submission and the reference solutions are always run the same way.

A problem's `spec` (built offline, stored with its tests):
    kind     "function" (class Solution with one method) or "design" (a class driven by
             LeetCode's ["Ctor", "op", ...] / [[args], ...] lists)
    cls      class name ("Solution" for function problems)
    method   method name (function problems)
    params   [{"name": "nums", "type": "List[int]"}, ...] in signature order
    returns  return type text; "None" means the method mutates its first parameter
    methods  design problems: {"op": {"params": [...types], "returns": type}}
    adapter  optional name of a special case in ADAPTERS (cycles, node references, ...)
"""

import itertools
import json
import math
import re
from collections import deque
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from prelude import ListNode, Node, TreeNode

# Longest linked list we follow when serializing; longer means a cycle in the output.
MAX_LIST = 2_000_000
OPTIONAL = re.compile(r"^Optional\[(.*)\]$")
LIST_OF = re.compile(r"^List\[(.*)\]$")


class HarnessError(Exception):
    """The test input does not fit the problem's signature (a bad test, not a bad solution)."""


def bare(type_: str) -> str:
    """'Optional[ListNode]' -> 'ListNode'; quotes from forward references are dropped."""
    type_ = type_.replace("'", "").replace('"', "").replace(" ", "")
    while match := OPTIONAL.match(type_):
        type_ = match.group(1)
    return type_


def element(type_: str) -> str | None:
    """'List[TreeNode]' -> 'TreeNode'; None when the type is not a list."""
    match = LIST_OF.match(bare(type_))
    return bare(match.group(1)) if match else None


def link(nodes: list) -> Any:
    """Chains `nodes` through `.next` and returns the head (None for no nodes)."""
    for a, b in itertools.pairwise(nodes):
        a.next = b
    return nodes[0] if nodes else None


def walk(head: Any) -> Iterator[Any]:
    """The nodes of a solution's linked list; raises once it is too long to be acyclic."""
    count = 0
    while head is not None:
        yield head
        count += 1
        if count > MAX_LIST:
            raise ValueError("Output linked list has a cycle")
        head = head.next


def to_list_node(values: list | None) -> ListNode | None:
    return link([ListNode(v) for v in values or []])


def from_list_node(head: ListNode | None) -> list:
    return [node.val for node in walk(head)]


def to_tree(values: list | None, node_type: type = TreeNode) -> TreeNode | None:
    if not values or values[0] is None:
        return None
    root = node_type(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = node_type(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def from_tree(root: Any) -> list:
    values: list = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
        if len(values) > 4 * MAX_LIST:
            raise ValueError("Output tree has a cycle")
    while values and values[-1] is None:
        values.pop()
    return values


def find_node(root: Any, value: Any) -> Any:
    """The tree node holding `value` (LeetCode passes node arguments by value)."""
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            continue
        if node.val == value:
            return node
        queue.extend((node.left, node.right))
    raise HarnessError(f"No node with value {value!r} in the tree")


def decode(value: Any, type_: str) -> Any:
    kind = bare(type_)
    if kind == "ListNode":
        return to_list_node(value)
    if kind == "TreeNode":
        return to_tree(value)
    inner = element(type_)
    if inner in ("ListNode", "TreeNode") or (inner and element(inner)):
        return [decode(v, inner) for v in value]
    return value


def encode(value: Any, type_: str | None = None) -> Any:
    """JSON-ready form of a result, coerced to the declared type the way LeetCode prints it."""
    kind = bare(type_) if type_ else None
    # LeetCode prints an empty list or tree as [].
    if value is None and kind in ("ListNode", "TreeNode"):
        return []
    if isinstance(value, ListNode):
        return from_list_node(value)
    if isinstance(value, (TreeNode, Node)) and hasattr(value, "left"):
        return from_tree(value)
    if isinstance(value, bool):
        return value
    if kind == "bool" and isinstance(value, int):
        return bool(value)
    if isinstance(value, float):
        if kind == "int" and value.is_integer():
            return int(value)
        if not math.isfinite(value):
            return str(value)
        return value
    if isinstance(value, (list, tuple)):
        inner = element(type_) if type_ else None
        return [encode(v, inner) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(encode(v) for v in value)
    if value is None or isinstance(value, (int, str)):
        return value
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    raise TypeError(f"Cannot print a {type(value).__name__} result")


@dataclass(slots=True)
class Call:
    """How one test calls a function-kind solution: positional args and how to read the result."""

    args: list
    read: Callable[[Any], Any]


def node_value(node: Any) -> Any:
    """An answer that is one node, printed as LeetCode does: its value."""
    return None if node is None else node.val


def generic_call(spec: dict, data: dict) -> Call:
    params = spec["params"]
    missing = [p["name"] for p in params if p["name"] not in data]
    if missing:
        raise HarnessError(f"Test input lacks {missing}")
    args = []
    for p in params:
        raw = data[p["name"]]
        kind = bare(p["type"])
        # A node argument given as a plain value names a node of the first tree argument.
        if kind == "TreeNode" and not isinstance(raw, list) and args and raw is not None:
            args.append(find_node(args[0], raw))
        else:
            args.append(decode(raw, p["type"]))
    returns = spec["returns"]
    if bare(returns) == "None":
        first, first_type = args[0], params[0]["type"]
        return Call(args, lambda _result: encode(first, first_type))
    return Call(args, lambda result: encode(result, returns))


def cycle_call(spec: dict, data: dict) -> Call:
    """Linked List Cycle I/II: `pos` links the tail back; the answer is a node or a bool."""
    values, pos = data["head"], data.get("pos", -1)
    nodes = [ListNode(v) for v in values]
    head = link(nodes)
    if nodes and pos is not None and pos >= 0:
        nodes[-1].next = nodes[pos]
    index = {id(n): i for i, n in enumerate(nodes)}

    def read(result: Any) -> Any:
        if isinstance(result, ListNode):
            return index.get(id(result), -2)
        return encode(result, spec["returns"])

    return Call([head], read)


def node_value_call(spec: dict, data: dict) -> Call:
    """Answers that are one tree node (lowest common ancestor): LeetCode prints its value."""
    return Call(generic_call(spec, data).args, node_value)


def intersection_call(spec: dict, data: dict) -> Call:
    """Intersection of Two Linked Lists: both lists share the tail from skipA / skipB on."""
    list_a, list_b = data["listA"], data["listB"]
    skip_a, skip_b = data["skipA"], data["skipB"]
    a = [ListNode(v) for v in list_a[:skip_a]]
    b = [ListNode(v) for v in list_b[:skip_b]]
    shared = [ListNode(v) for v in list_a[skip_a:]] if data["intersectVal"] else []
    if not data["intersectVal"]:
        a += [ListNode(v) for v in list_a[skip_a:]]
        b += [ListNode(v) for v in list_b[skip_b:]]
    return Call([link(a + shared), link(b + shared)], node_value)


def delete_node_call(spec: dict, data: dict) -> Call:
    """Delete Node in a Linked List: called with the node only; the answer is the whole list."""
    head = to_list_node(data["head"])
    node = head
    while node is not None and node.val != data["node"]:
        node = node.next
    if node is None:
        raise HarnessError("Node to delete is not in the list")
    return Call([node], lambda _result: from_list_node(head))


def random_list_call(spec: dict, data: dict) -> Call:
    """Copy List with Random Pointer: [[val, random_index], ...] in and out."""
    pairs = data["head"]
    nodes = [Node(v) for v, _ in pairs]
    head = link(nodes)
    for node, (_, r) in zip(nodes, pairs, strict=True):
        node.random = nodes[r] if r is not None else None
    originals = {id(n) for n in nodes}

    def read(result: Any) -> Any:
        seen = []
        for node in walk(result):
            if id(node) in originals:
                raise ValueError("The copy reuses nodes of the original list")
            seen.append(node)
        index = {id(n): i for i, n in enumerate(seen)}
        return [[n.val, None if n.random is None else index.get(id(n.random))] for n in seen]

    return Call([head], read)


def graph_call(spec: dict, data: dict) -> Call:
    """Clone Graph: adjacency list of nodes 1..n in and out; the copy must be new nodes."""
    adj = data["adjList"]
    nodes = [Node(i + 1) for i in range(len(adj))]
    for node, neighbors in zip(nodes, adj, strict=True):
        node.neighbors = [nodes[j - 1] for j in neighbors]
    originals = {id(n) for n in nodes}

    def read(result: Any) -> Any:
        if result is None:
            return []
        found, queue = {result.val: result}, deque([result])
        while queue:
            node = queue.popleft()
            if id(node) in originals:
                raise ValueError("The clone reuses nodes of the original graph")
            for nb in node.neighbors:
                if nb.val not in found:
                    found[nb.val] = nb
                    queue.append(nb)
        return [[nb.val for nb in found[v].neighbors] for v in sorted(found)]

    return Call([nodes[0] if nodes else None], read)


def nary_tree(values: list | None) -> Node | None:
    """LeetCode's N-ary level order: children groups separated by null."""
    if not values:
        return None
    root = Node(values[0], children=[])
    queue, i = deque([root]), 2
    while queue and i <= len(values):
        node = queue.popleft()
        while i < len(values) and values[i] is not None:
            child = Node(values[i], children=[])
            node.children.append(child)
            queue.append(child)
            i += 1
        i += 1
    return root


def nary_call(spec: dict, data: dict) -> Call:
    root = nary_tree(data["root"])
    extra = [decode(data[p["name"]], p["type"]) for p in spec["params"][1:]]
    return Call([root, *extra], lambda result: encode(result, spec["returns"]))


def next_pointer_call(spec: dict, data: dict) -> Call:
    """Populating Next Right Pointers: the answer is each level, then '#'."""
    root = to_tree(data["root"], Node)

    def read(result: Any) -> Any:
        out, start = [], result
        while start is not None:
            node, first_child = start, None
            while node is not None:
                out.append(node.val)
                first_child = first_child or node.left or node.right
                node = node.next
            out.append("#")
            start = first_child
        return out

    return Call([root], read)


ADAPTERS: dict[str, Callable[[dict, dict], Call]] = {
    "cycle": cycle_call,
    "node_value": node_value_call,
    "intersection": intersection_call,
    "delete_node": delete_node_call,
    "random_list": random_list_call,
    "graph": graph_call,
    "nary": nary_call,
    "next_pointer": next_pointer_call,
}


def prepare(spec: dict, data: dict) -> Any:
    """Everything a test needs before the solution runs; built before the sandbox forks so
    input conversion never counts toward the solution's time."""
    if spec["kind"] == "design":
        return data
    adapter = ADAPTERS.get(spec.get("adapter") or "", generic_call)
    return adapter(spec, data)


def run(namespace: dict, spec: dict, prepared: Any) -> Any:
    """Runs one prepared test against the code already executed into `namespace`."""
    if spec["kind"] == "design":
        return run_design(namespace, spec, prepared)
    method = getattr(solution_class(namespace, spec)(), spec["method"], None)
    if method is None:
        raise AttributeError(f"{spec['cls']} has no method {spec['method']}")
    return prepared.read(method(*prepared.args))


def run_design(namespace: dict, spec: dict, data: dict) -> list:
    ops, args = data["ops"], data["args"]
    methods = spec.get("methods", {})
    cls = solution_class(namespace, spec)
    obj = cls(*decode_args(args[0], methods.get("__init__", {}).get("params", [])))
    out: list = [None]
    for op, op_args in zip(ops[1:], args[1:], strict=True):
        info = methods.get(op, {})
        result = getattr(obj, op)(*decode_args(op_args, info.get("params", [])))
        out.append(encode(result, info.get("returns")))
    return out


def solution_class(namespace: dict, spec: dict) -> Any:
    """The class the spec names, as the solution defined it."""
    cls = namespace.get(spec["cls"])
    if cls is None:
        raise NameError(f"class {spec['cls']} is not defined")
    return cls


def decode_args(values: list, types: list[str]) -> list:
    """Design-problem arguments; without known types they pass through as JSON values."""
    if len(types) != len(values):
        return values
    return [decode(v, t) for v, t in zip(values, types, strict=True)]


def dumps(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
