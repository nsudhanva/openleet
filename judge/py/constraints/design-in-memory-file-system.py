"""Design In-Memory File System: FileSystem calls."""


def _shape(ops, args, ctor, ctor_arity, sig):
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == ctor, "first operation is the constructor"
    assert all(isinstance(a, list) for a in args), "each args[i] is a list"
    assert len(args[0]) == ctor_arity, "constructor argument count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in sig, "known method name"
        assert len(a) == sig[op], "argument count of " + op


def check(ops: list[str], args: list[list]) -> None:
    _shape(
        ops,
        args,
        "FileSystem",
        0,
        {"ls": 1, "mkdir": 1, "addContentToFile": 2, "readContentFromFile": 1},
    )
    assert len(ops) - 1 <= 300, "at most 300 calls"
    root = {}

    def parts(p):
        assert isinstance(p, str) and 1 <= len(p) <= 100, "1 <= path.length <= 100"
        assert p[0] == "/", "paths begin with '/'"
        if p == "/":
            return []
        assert not p.endswith("/"), "paths do not end with '/' except the root"
        segs = p[1:].split("/")
        assert all(s and all("a" <= c <= "z" for c in s) for s in segs), (
            "names are lowercase letters"
        )
        return segs

    def walk(segs):
        node = root
        for s in segs:
            assert isinstance(node, dict), "a path does not pass through a file"
            assert s in node, "operations refer to existing paths"
            node = node[s]
        return node

    for op, a in zip(ops[1:], args[1:], strict=True):
        segs = parts(a[0])
        if op == "ls":
            walk(segs)
        elif op == "mkdir":
            node = root
            for s in segs:
                assert isinstance(node, dict), "a name is not both a file and a directory"
                node = node.setdefault(s, {})
            assert isinstance(node, dict), "a name is not both a file and a directory"
        elif op == "addContentToFile":
            assert segs, "a file path is not the root"
            assert isinstance(a[1], str) and 1 <= len(a[1]) <= 50, "1 <= content.length <= 50"
            parent = walk(segs[:-1])
            assert isinstance(parent, dict), "the parent directory exists"
            assert not isinstance(parent.get(segs[-1]), dict), (
                "a name is not both a file and a directory"
            )
            parent[segs[-1]] = "f"
        else:
            assert walk(segs) == "f", "readContentFromFile refers to an existing file"
