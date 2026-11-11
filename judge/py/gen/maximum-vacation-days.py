"""Maximum Vacation Days at n = k = 20 with dense flights, so following every flight choice week
by week without memoising explores ~10^25 schedules."""

SEEDS = 2
N = 20
K = 20


def generate(rng):
    flights = [[int(i != j and rng.random() < 0.7) for j in range(N)] for i in range(N)]
    days = [[rng.randint(0, 7) for _ in range(K)] for _ in range(N)]
    return {"flights": flights, "days": days}
