"""Walking Robot Simulation II on a 100 x 100 grid at 10^4 calls, 9000 of them steps of nearly
10^5 cells (one short of a whole number of laps), so walking each step cell by cell is ~9 *
10^8 moves."""

SEEDS = 2
SIDE = 100
CALLS = 10**4


def generate(rng):
    lap = 4 * (SIDE - 1)
    most = (10**5 + 1) // lap - 1  # the most laps that still leave room for lap - 1 more cells
    ops, args = ["Robot"], [[SIDE, SIDE]]
    for _ in range(CALLS):
        if rng.random() < 0.9:
            ops.append("step")
            args.append([lap * rng.randint(most - 20, most) + lap - 1])
        else:
            ops.append(rng.choice(["getPos", "getDir"]))
            args.append([])
    return {"ops": ops, "args": args}
