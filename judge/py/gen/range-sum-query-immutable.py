"""Range Sum Query with 10^4 values and 10^4 mostly wide ranges, so summing each range
directly is quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    ops, args = ["NumArray"], [[nums]]
    for _ in range(10**4):
        left = rng.randrange(N // 10)
        right = rng.randrange(N - N // 10, N)
        if rng.random() < 0.2:
            left, right = sorted((rng.randrange(N), rng.randrange(N)))
        ops.append("sumRange")
        args.append([left, right])
    return {"ops": ops, "args": args}
