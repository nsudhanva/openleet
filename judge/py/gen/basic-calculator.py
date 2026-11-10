"""Basic Calculator at ~3 * 10^5 characters: a right-nested chain of 'a - (b - (c - ...))' about
7 * 10^4 levels deep (recursion worst case), or a long random expression with nested groups,
unary minus after '(' and random spaces."""

SEEDS = 3
BUDGET = 3 * 10**5 - 10


def _deep(rng):
    depth = (BUDGET - 4) // 6
    parts = []
    for _ in range(depth):
        parts.append(f"{rng.randint(0, 9)} {rng.choice('+-')} (")
    return "".join(parts) + str(rng.randint(0, 9)) + ")" * depth


def _random(rng):
    out = []
    size = 0
    open_parens = 0

    def emit(tok):
        nonlocal size
        out.append(tok)
        size += len(tok)

    def space():
        if rng.random() < 0.3:
            emit(" ")

    at_expr_start = True
    while True:
        # Term position: maybe unary minus at the start of an expression, then a term.
        if at_expr_start and rng.random() < 0.3:
            emit("-")
            space()
        if size < BUDGET - 4 * open_parens - 200 and rng.random() < 0.3:
            emit("(")
            space()
            open_parens += 1
            at_expr_start = True
            continue
        emit(str(rng.randint(0, 1000)))
        space()
        at_expr_start = False
        # After a term: close some groups, then stop or continue with an operator.
        while open_parens and rng.random() < 0.3:
            emit(")")
            space()
            open_parens -= 1
        if size >= BUDGET - 4 * open_parens - 200:
            break
        emit(rng.choice("+-"))
        space()
    out.append(")" * open_parens)
    return "".join(out).strip()


def generate(rng):
    s = _deep(rng) if rng.random() < 0.4 else _random(rng)
    return {"s": s}
