"""Maximum Employees to Be Invited to a Meeting at n = 5 * 10^4: one big cycle and one mutual
pair fed by two long arms, with either the pair and its arms (cycle n/4) or the cycle (just over
n/2) the answer, so walking every employee to its cycle is ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    labels = list(range(N))
    rng.shuffle(labels)
    fav = [0] * N
    cycle = max(3, N // 4) if pick_shape(rng) == 0 else N // 2 + 2
    for i in range(cycle):
        fav[labels[i]] = labels[(i + 1) % cycle]
    a, b = cycle, cycle + 1
    fav[labels[a]], fav[labels[b]] = labels[b], labels[a]
    # Each side of the pair heads one long arm.
    half = cycle + 2 + (N - cycle - 2) // 2
    for i in range(cycle + 2, N):
        prev = a if i == cycle + 2 else b if i == half else i - 1
        fav[labels[i]] = labels[prev]
    return {"favorite": fav}
