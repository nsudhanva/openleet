"""Count the Number of Inversions at n = 30 with a few prefix requirements taken from a random
permutation, so building permutations one by one is hopeless while the DP is 30 x 400."""

SEEDS = 2
N = 30
CNT = 400


def generate(rng):
    perm = list(range(N))
    rng.shuffle(perm)
    while sum(perm[i] > perm[j] for j in range(N) for i in range(j)) > CNT:
        rng.shuffle(perm)
    ends = sorted({N - 1, *rng.sample(range(N - 1), rng.randint(0, 3))})
    requirements = []
    for end in ends:
        cnt = sum(perm[i] > perm[j] for j in range(end + 1) for i in range(j))
        requirements.append([end, cnt])
    rng.shuffle(requirements)
    return {"n": N, "requirements": requirements}
