"""Maximum Number of Weeks for Which You Can Work with 200 projects of up to 10^6 milestones, one
seed with a project larger than all the rest, so simulating the weeks cannot finish."""

SEEDS = 2
N = 200


def generate(rng):
    milestones = [rng.randint(1, 10**6) for _ in range(N)]
    if rng.random() < 0.5:
        milestones[rng.randrange(N)] = min(10**9, sum(milestones) + rng.randint(2, 10**6))
    return {"milestones": milestones}
