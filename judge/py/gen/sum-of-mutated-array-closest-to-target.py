"""Sum of Mutated Array Closest to Target at n = 5000: tiny values plus one or two near 10^5, with
the target putting the best cap past 3 * 10^4, so trying caps upward and summing the array for
each is ~2 * 10^8 steps."""

SEEDS = 2
N = 5000


def generate(rng):
    big = rng.randint(1, 2)
    arr = [rng.randint(1, 5) for _ in range(N - big)]
    arr += [rng.randint(9 * 10**4, 10**5) for _ in range(big)]
    rng.shuffle(arr)
    cap = rng.randint(3 * 10**4, (10**5 - 3 * N) // big)
    return {"arr": arr, "target": sum(min(x, cap) for x in arr) + rng.randint(0, big)}
