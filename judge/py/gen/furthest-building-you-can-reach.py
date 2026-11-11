"""10^5 buildings rising in long runs of ~10^5 climbs that shrink, each at most the smallest so
far, with just enough bricks and ladders to reach 90 to 95% of the way, so keeping the climbs in
a sorted list costs ~5 * 10^9 element moves and re-sorting them at every building far more."""

SEEDS = 2
N = 10**5
LIMIT = 10**6
TOP = 15000


def generate(rng):
    # Climbs fall from TOP to about 1, so each lands near the front of a sorted list. Heights rise
    # until the next climb would pass LIMIT, then drop back to 1.
    heights, climbs = [1], []
    total = N - 1 - 800  # ~750 drops
    for i in range(total):
        d = max(1, TOP - i * TOP // total - rng.randint(0, 3))
        if heights[-1] + d > LIMIT:
            heights.append(1)
            if len(heights) == N:
                break
        heights.append(heights[-1] + d)
        climbs.append(d)
        if len(heights) == N:
            break
    while len(heights) < N:
        heights.append(heights[-1])
    # Ladders take the largest climbs among the first 90-95%; bricks pay for exactly the rest.
    reach = rng.randint(len(climbs) * 9 // 10, len(climbs) * 19 // 20)
    ladders = rng.randint(100, 2000)
    first = sorted(climbs[:reach])
    return {"heights": heights, "bricks": sum(first[: len(first) - ladders]), "ladders": ladders}
