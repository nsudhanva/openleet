"""Queue Reconstruction at n = 2000, built from a real queue (so it is reconstructable), with
many repeated heights to stress tie handling."""

SEEDS = 2
N = 2000


def generate(rng):
    top = rng.choice([20, 10**6])
    queue = [rng.randint(0, top) for _ in range(N)]
    people = []
    for i, h in enumerate(queue):
        k = sum(1 for j in range(i) if queue[j] >= h)
        people.append([h, k])
    rng.shuffle(people)
    return {"people": people}
