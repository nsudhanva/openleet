"""The Score of Students Solving Math Expression at the full 16 operands and 10^4 answers, so
recomputing every sub-expression's values without memoising is ~10^7 recursive calls."""

from math import prod

SEEDS = 2
OPS = 15
N = 10**4


def generate(rng):
    while True:
        digits = [rng.randint(0, 9) for _ in range(OPS + 1)]
        ops = [rng.choice("++*") for _ in range(OPS)]
        # hi[i][j]: the largest value any bracketing of operands i..j can take.
        m = OPS + 1
        hi = [[0] * m for _ in range(m)]
        for i in range(m - 1, -1, -1):
            hi[i][i] = digits[i]
            for j in range(i + 1, m):
                hi[i][j] = max(
                    hi[i][k] * hi[k + 1][j] if ops[k] == "*" else hi[i][k] + hi[k + 1][j]
                    for k in range(i, j)
                )
        s = str(digits[0]) + "".join(o + str(d) for o, d in zip(ops, digits[1:], strict=True))
        right = sum(prod(map(int, term.split("*"))) for term in s.split("+"))
        if hi[0][-1] <= 10**9 and right <= 1000:
            break
    answers = [rng.choice((right, rng.randint(0, 1000), rng.randint(0, 200))) for _ in range(N)]
    return {"s": s, "answers": answers}
