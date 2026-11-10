"""Super Washing Machines at n = 10^4 with loads up to 10^5: everything piled on one end, or
a random spread whose total divides evenly (with one unsolvable case)."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        machines = [0] * N
        machines[rng.choice([0, N - 1])] = 10**5  # 10 per machine after balancing
    elif shape == 1:
        machines = [rng.randint(0, 10**5) for _ in range(N)]
        excess = sum(machines) % N
        i = 0
        while excess:
            take = min(excess, machines[i])
            machines[i] -= take
            excess -= take
            i += 1
    else:
        machines = [rng.randint(0, 10**5) for _ in range(N)]
        if sum(machines) % N == 0:
            machines[0] = machines[0] + 1 if machines[0] < 10**5 else machines[0] - 1
    return {"machines": machines}
