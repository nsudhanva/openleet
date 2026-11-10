"""Longest Valid Parentheses at length 3 * 10^4: random parentheses, deeply nested balanced
blocks, or "()" repeated with a few breaks."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = rng.choice(["random", "nested", "pairs"])
    if shape == "random":
        s = "".join(rng.choice("()") for _ in range(N))
    elif shape == "nested":
        depth = rng.randint(N // 4, N // 2)
        s = ")" + "(" * depth + ")" * depth
        s += "".join(rng.choice("()") for _ in range(N - len(s)))
    else:
        chars = list("()" * (N // 2))
        for i in rng.sample(range(N), 5):
            chars[i] = ")" if chars[i] == "(" else "("
        s = "".join(chars)
    return {"s": s}
