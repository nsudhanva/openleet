"""Time Needed to Buy Tickets at the maximum 100 people with up to 100 tickets each."""

SEEDS = 2
N = 100


def generate(rng):
    tickets = [rng.randint(1, 100) for _ in range(N)]
    return {"tickets": tickets, "k": rng.randrange(N)}
