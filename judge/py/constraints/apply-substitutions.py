"""Apply Substitutions: replacement [key, value] pairs and a text of placeholders."""

import re


def check(replacements: list[list[str]], text: str) -> None:
    assert isinstance(replacements, list) and isinstance(text, str), "types"
    n = len(replacements)
    assert 1 <= n <= 10, "1 <= replacements.length <= 10"
    assert all(isinstance(r, list) and len(r) == 2 for r in replacements), (
        "each replacement is [key, value]"
    )
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in replacements), (
        "key and value are strings"
    )
    keys = [k for k, _ in replacements]
    assert all(len(k) == 1 and "A" <= k <= "Z" for k in keys), (
        "key is a single uppercase English letter"
    )
    assert all(1 <= len(v) <= 8 for _, v in replacements), (
        "value is a non-empty string of at most 8 characters"
    )
    assert len(set(keys)) == n, "all replacement keys are unique"
    assert len(text) == 4 * n - 1, "text.length == 4 * replacements.length - 1"
    parts = text.split("_")
    assert len(parts) == n, "text is placeholders separated by underscores"
    keyset = set(keys)
    assert {p[1:2] for p in parts} == keyset, "text concatenates every key placeholder once"
    for p in parts:
        assert len(p) == 3 and p[0] == "%" and p[2] == "%", "text is made of %<key>% placeholders"
        assert p[1] in keyset, "every placeholder in text corresponds to a key"
    deps: dict[str, list[str]] = {}
    for k, v in replacements:
        deps[k] = re.findall(r"%([A-Z])%", v)
        assert all(d in keyset for d in deps[k]), (
            "every placeholder in a value corresponds to a key"
        )
    state = dict.fromkeys(keys, 0)
    for start in keys:
        if state[start]:
            continue
        stack = [(start, iter(deps[start]))]
        state[start] = 1
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[node] = 2
                stack.pop()
                continue
            assert state[nxt] != 1, "no cyclic dependencies between replacement keys"
            if state[nxt] == 0:
                state[nxt] = 1
                stack.append((nxt, iter(deps[nxt])))
