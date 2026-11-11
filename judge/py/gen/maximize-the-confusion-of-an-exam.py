"""Maximize the Confusion of an Exam at n = 3 * 10^4 random answers with k in [n / 8, n / 4], so
windows span ~2k and growing one from every start for both letters is ~5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    key = "".join(rng.choice("TF") for _ in range(N))
    return {"answerKey": key, "k": rng.randint(N // 8, N // 4)}
