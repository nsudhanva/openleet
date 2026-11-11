"""Next Greater Node in Linked List at n = 10^4 non-increasing values with runs of equal ones,
so almost no node has a larger one after it and scanning ahead from each node is ~5 * 10^7
steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    vals = sorted((rng.randint(1, 10**9) for _ in range(N)), reverse=True)
    for i in range(0, N - 10, 40):
        vals[i + 1 : i + 10] = [vals[i]] * 9
    vals[-1] = rng.randint(1, 10**9)
    return {"head": vals}
