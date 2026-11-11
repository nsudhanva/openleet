"""nums of 10^5 small values whose only balanced index (or the place it just misses) sits mid-array
behind a run of ones, so a scan from either end recomputing each index's sum or product costs
~5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    # Left of `mid` sums to p; right of it is ones then p (or p - 1, giving -1). Going left the
    # suffix sum falls and the product only grows, so no other index balances, and the product
    # stays below the sum until `mid`, so a right-to-left scan cannot stop early.
    balanced = rng.getrandbits(1)
    mid = rng.randint(N * 2 // 5, N * 3 // 5)
    left = [rng.randint(1, 3) for _ in range(mid)]
    p = sum(left)
    last = p if balanced else p - 1
    return {"nums": [*left, rng.randint(2, 9), *[1] * (N - mid - 2), last]}
