"""Maximum Sum Obtained of Any Permutation at n = 10^5 with 10^5 requests, long ranges so
per-request counting does ~10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [rng.randint(0, 10**5) for _ in range(N)]
    requests = []
    wide = rng.random() < 0.5
    for _ in range(N):
        if wide:
            a = rng.randint(0, N // 10)
            b = rng.randint(N - N // 10, N - 1)
        else:
            a = rng.randint(0, N - 1)
            b = rng.randint(a, N - 1)
        requests.append([a, b])
    return {"nums": nums, "requests": requests}
