"""Largest Perimeter Triangle at n = 10^4 with values up to 10^6: random values, or a
Fibonacci-like run on top so the largest sides never form a triangle."""

SEEDS = 2
N = 10**4
LIMIT = 10**6


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, LIMIT) for _ in range(N)]
    else:
        fib = [1, 2]
        while fib[-1] + fib[-2] <= LIMIT:
            fib.append(fib[-1] + fib[-2])
        nums = [rng.randint(1, 3) for _ in range(N - len(fib))] + fib
        rng.shuffle(nums)
    return {"nums": nums}
