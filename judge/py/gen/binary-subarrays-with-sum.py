"""Binary Subarrays With Sum at n = 3 * 10^4: mostly zeros with goal 0 or 1 (counts near 4.5 *
10^8, punishing enumeration), or random bits with a mid-range goal."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = rng.choice(["zeros", "sparse", "random"])
    if shape == "zeros":
        nums = [0] * N
        goal = 0
    elif shape == "sparse":
        nums = [1 if rng.random() < 0.001 else 0 for _ in range(N)]
        goal = rng.choice([0, 1, 2])
    else:
        nums = [rng.randint(0, 1) for _ in range(N)]
        goal = rng.randint(0, sum(nums) // 2)
    return {"nums": nums, "goal": goal}
