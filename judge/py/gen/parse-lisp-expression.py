"""Parse Lisp Expression near the 2000-character limit: legal nested let/add/mult with
shadowed variables, built bottom-up so every intermediate value stays far inside 32 bits."""

SEEDS = 3
NAMES = ["x", "y", "z", "a1", "b2", "cc", "v9"]
BOUND = 10**6


def atom(rng, scope):
    if scope and rng.random() < 0.6:
        name = rng.choice(sorted(scope))
        return name, scope[name]
    v = rng.randint(-20, 20)
    return str(v), v


def gen(rng, scope, budget, deep):
    if budget < 25:
        return atom(rng, scope)
    kind = rng.choice(["let", "let", "add", "mult"])
    if kind == "let":
        inner = dict(scope)
        parts = []
        pairs = rng.randint(1, 3)
        share = (budget - 10) // (pairs + 1)
        for _ in range(pairs):
            name = rng.choice(NAMES)
            s, v = gen(rng, inner, share, deep)
            inner[name] = v
            parts.append(f"{name} {s}")
        s, v = gen(rng, inner, share, deep)
        return f"(let {' '.join(parts)} {s})", v
    if deep:
        first = rng.random() < 0.5
        b1, b2 = (budget - 10, 0) if first else (0, budget - 10)
    else:
        cut = rng.randint(0, budget - 10)
        b1, b2 = cut, budget - 10 - cut
    s1, v1 = gen(rng, scope, b1, deep)
    s2, v2 = gen(rng, scope, b2, deep)
    if kind == "mult" and abs(v1 * v2) <= BOUND:
        return f"(mult {s1} {s2})", v1 * v2
    if abs(v1 + v2) <= BOUND:
        return f"(add {s1} {s2})", v1 + v2
    return s1, v1


def generate(rng):
    deep = rng.random() < 0.4
    best = "(add 1 2)"
    for _ in range(40):
        s, _ = gen(rng, {}, rng.randint(2000, 4000), deep)
        if len(best) < len(s) <= 2000 and s.startswith("("):
            best = s
    return {"expression": best}
