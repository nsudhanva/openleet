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
import re
from collections import deque
from collections.abc import Callable
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


# ---------------------------------------------------------------------------------------------
# Linked lists and trees in LeetCode's JSON form


def to_list_node(values: list | None) -> ListNode | None:
    head = tail = None
    for value in values or []:
        node = ListNode(value)
        if tail is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head


def from_list_node(head: ListNode | None) -> list:
    values = []
    while head is not None:
        values.append(head.val)
        if len(values) > MAX_LIST:
            raise ValueError("Output linked list has a cycle")
        head = head.next
    return values


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


# ---------------------------------------------------------------------------------------------
# Generic, type-driven conversion


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
        if value != value or value in (float("inf"), float("-inf")):
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


# ---------------------------------------------------------------------------------------------
# Special cases, chosen per problem by spec["adapter"]


class Call:
    """How one test calls a function-kind solution: positional args and how to read the result."""

    def __init__(self, args: list, read: Callable[[Any], Any]):
        self.args = args
        self.read = read


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
    for a, b in itertools.pairwise(nodes):
        a.next = b
    if nodes and pos is not None and pos >= 0:
        nodes[-1].next = nodes[pos]
    index = {id(n): i for i, n in enumerate(nodes)}

    def read(result: Any) -> Any:
        if isinstance(result, ListNode):
            return index.get(id(result), -2)
        return encode(result, spec["returns"])

    return Call([nodes[0] if nodes else None], read)


def node_value_call(spec: dict, data: dict) -> Call:
    """Answers that are one tree node (lowest common ancestor): LeetCode prints its value."""
    call = generic_call(spec, data)
    return Call(call.args, lambda result: None if result is None else result.val)


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
    for chain in (a + shared, b + shared):
        for x, y in itertools.pairwise(chain):
            x.next = y
    head_a = (a + shared)[0] if a + shared else None
    head_b = (b + shared)[0] if b + shared else None
    return Call([head_a, head_b], lambda result: None if result is None else result.val)


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
    for i, (_, r) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        nodes[i].random = nodes[r] if r is not None else None
    originals = {id(n) for n in nodes}

    def read(result: Any) -> Any:
        out, seen, node = [], [], result
        while node is not None:
            if id(node) in originals:
                raise ValueError("The copy reuses nodes of the original list")
            seen.append(node)
            node = node.next
            if len(seen) > MAX_LIST:
                raise ValueError("Output linked list has a cycle")
        index = {id(n): i for i, n in enumerate(seen)}
        for n in seen:
            out.append([n.val, None if n.random is None else index.get(id(n.random))])
        return out

    return Call([nodes[0] if nodes else None], read)


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
    cls = namespace.get(spec["cls"])
    if cls is None:
        raise NameError(f"class {spec['cls']} is not defined")
    method = getattr(cls(), spec["method"], None)
    if method is None:
        raise AttributeError(f"{spec['cls']} has no method {spec['method']}")
    return prepared.read(method(*prepared.args))


def run_design(namespace: dict, spec: dict, data: dict) -> list:
    ops, args = data["ops"], data["args"]
    cls = namespace.get(spec["cls"])
    if cls is None:
        raise NameError(f"class {spec['cls']} is not defined")
    methods = spec.get("methods", {})
    obj = cls(*decode_args(args[0], methods.get("__init__", {}).get("params", [])))
    out: list = [None]
    for op, op_args in zip(ops[1:], args[1:], strict=True):
        info = methods.get(op, {})
        result = getattr(obj, op)(*decode_args(op_args, info.get("params", [])))
        out.append(encode(result, info.get("returns")))
    return out


def decode_args(values: list, types: list[str]) -> list:
    """Design-problem arguments; without known types they pass through as JSON values."""
    if len(types) != len(values):
        return values
    return [decode(v, t) for v, t in zip(values, types, strict=True)]


def dumps(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
