"""Range Sum Query Mutable with 3 * 10^4 values and 3 * 10^4 interleaved updates and wide
range sums, so neither a plain prefix array nor direct summing is fast enough."""

SEEDS = 2
N = 3 * 10**4
CALLS = 3 * 10**4


def generate(rng):
    nums = [rng.randint(-100, 100) for _ in range(N)]
    ops, args = ["NumArray"], [[nums]]
    for _ in range(CALLS):
        if rng.random() < 0.5:
            ops.append("update")
            args.append([rng.randrange(N), rng.randint(-100, 100)])
        else:
            left = rng.randrange(N // 10)
            right = rng.randrange(N - N // 10, N)
            ops.append("sumRange")
            args.append([left, right])
    return {"ops": ops, "args": args}
