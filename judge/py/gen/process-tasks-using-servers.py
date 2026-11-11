"""Process Tasks Using Servers at the maximum 2 * 10^5 servers and 2 * 10^5 tasks lasting up to
2 * 10^5 seconds, so about half the servers are busy and scanning or shifting them for each task
does ~10^10 steps."""

SEEDS = 2
N = 2 * 10**5
M = 2 * 10**5


def generate(rng):
    servers = [rng.randint(1, 2 * 10**5) for _ in range(N)]
    tasks = [rng.randint(1, N) for _ in range(M)]
    return {"servers": servers, "tasks": tasks}
