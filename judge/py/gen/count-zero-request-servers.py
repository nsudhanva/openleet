"""Count Zero Request Servers with 3 * 10^4 logs and 3 * 10^4 queries whose windows of
x = 10^5 each hold about half the logs, so recounting each window costs ~5 * 10^8 steps."""

SEEDS = 2
N = 10**5
LOGS = 3 * 10**4
QUERIES = 3 * 10**4
X = 10**5


def generate(rng):
    servers = rng.randint(N // 10, N)
    logs = [[rng.randint(1, servers), rng.randint(1, 2 * X)] for _ in range(LOGS)]
    queries = [rng.randint(X + 1, 2 * X) for _ in range(QUERIES)]
    return {"n": servers, "logs": logs, "x": X, "queries": queries}
