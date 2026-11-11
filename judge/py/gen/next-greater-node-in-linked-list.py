"""Next Greater Node in Linked List at n = 10^4: non-increasing values with runs of equal ones,
then a spike between 0.6 n and 0.95 n and a larger last value, so every node has a larger one
only far ahead and scanning ahead from each node is ~3 * 10^7 to 5 * 10^7 steps per seed."""

SEEDS = 4
N = 10**4


def generate(rng):
    vals = sorted((rng.randint(1, 4 * 10**8) for _ in range(N)), reverse=True)
    for i in range(0, N - 10, 40):
        vals[i + 1 : i + 10] = [vals[i]] * 9
    vals[rng.randint(N * 6 // 10, N * 95 // 100)] = rng.randint(5 * 10**8, 6 * 10**8)
    vals[-1] = rng.randint(7 * 10**8, 10**9)
    return {"head": vals}
