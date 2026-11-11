"""Minimum Cost to Change the Final Value of Expression nested 24000 parentheses deep (length
96001), to the left, to the right, or to the left as an all-zero AND chain, so finding each
group's closing parenthesis by scanning is quadratic."""

from _shapes import pick_shape

SEEDS = 3
DEPTH = 24000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 1:
        # 0&(1|(0&(...(1)...)))
        parts = [rng.choice("01") + rng.choice("&|") + "(" for _ in range(DEPTH)]
        parts += [rng.choice("01"), ")" * DEPTH]
    else:
        # ((((0&1)|0)&1)...), or ((((0&0)&0)&0)...) whose flip costs 2
        parts = ["(" * DEPTH, "0" if shape == 2 else rng.choice("01")]
        for _ in range(DEPTH):
            parts.append(("&0" if shape == 2 else rng.choice("&|") + rng.choice("01")) + ")")
    return {"expression": "".join(parts)}
