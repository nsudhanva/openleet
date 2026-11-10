"""Best Time to Buy and Sell Stock V at n = 1000 and k up to 500, prices up to 10^9 (profits
exceed 32 bits), so the O(n * k) DP runs at full size."""

SEEDS = 3
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(1, 10**9) for _ in range(N)]
    else:
        prices = [
            rng.randint(1, 10**3) if i % 2 == 0 else rng.randint(10**9 - 10**3, 10**9)
            for i in range(N)
        ]
    return {"prices": prices, "k": rng.choice([N // 2, rng.randint(1, N // 2)])}
