"""Maximum Number of Robots Within Budget with 5 * 10^4 robots whose charge times strictly fall and
a budget that admits windows of about 2 * 10^4, so growing a window from every start, or rescanning
the window when its maximum leaves, is quadratic."""

SEEDS = 2
N = 5 * 10**4
WINDOW = 2 * 10**4


def generate(rng):
    charge = [10**5 - 2 * i for i in range(N)]
    running = [rng.randint(1, 10**5) for _ in range(N)]
    budget = 10**5 + WINDOW * WINDOW * 5 * 10**4 + rng.randint(0, 10**9)
    return {"chargeTimes": charge, "runningCosts": running, "budget": budget}
