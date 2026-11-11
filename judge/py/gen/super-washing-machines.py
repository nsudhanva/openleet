"""Super Washing Machines at the maximum n = 10^4 with loads up to 10^5, always solvable: one
end piled up, a random spread or a few piles in the middle, so the answer is large and
recomputing both side sums for each machine is quadratic."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
TOP = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        machines = [0] * N
        machines[rng.choice([0, N - 1])] = TOP  # 10 per machine after balancing
    elif shape == 1:
        machines = [rng.randint(0, TOP) for _ in range(N)]
    else:
        machines = [rng.randint(0, 3) for _ in range(N)]
        for i in rng.sample(range(N // 3, 2 * N // 3), 5):
            machines[i] = rng.randint(TOP // 2, TOP)
    # Take the remainder off the fullest machines so the total divides evenly.
    excess = sum(machines) % N
    for i in sorted(range(N), key=lambda j: -machines[j]):
        take = min(excess, machines[i])
        machines[i] -= take
        excess -= take
        if not excess:
            break
    return {"machines": machines}
