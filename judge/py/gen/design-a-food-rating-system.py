"""Food Rating System with 1.5 * 10^4 foods, nine in ten of one cuisine, and 1.5 * 10^4 calls: half
highestRated, and most changes lower the cuisine's current top food, so scanning a cuisine's foods
per query, or only when its top food drops, costs ~10^8 steps."""

import heapq

SEEDS = 2
N = 15000
CALLS = 15000


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    foods = set()
    while len(foods) < N:
        foods.add("".join(rng.choices(letters, k=rng.randint(6, 10))))
    foods = sorted(foods)
    rng.shuffle(foods)
    kinds = ["".join(rng.choices(letters, k=rng.randint(1, 10))) for _ in range(2)]
    while kinds[1] == kinds[0]:
        kinds[1] = "".join(rng.choices(letters, k=rng.randint(1, 10)))
    # Ratings from a narrow band in one seed, so ties between foods are common.
    band = rng.choice((10**3, 10**8))
    cuisines = [kinds[0] if rng.random() < 0.9 else kinds[1] for _ in range(N)]
    ratings = [rng.randint(1, band) for _ in range(N)]
    rating = dict(zip(foods, ratings, strict=True))
    # Each cuisine's foods by (-rating, name); stale entries are skipped when they reach the top.
    heaps = {kind: [] for kind in kinds}
    for food, kind, r in zip(foods, cuisines, ratings, strict=True):
        heaps[kind].append((-r, food))
    for heap in heaps.values():
        heapq.heapify(heap)
    cuisine_of = dict(zip(foods, cuisines, strict=True))

    def top(kind):
        heap = heaps[kind]
        while -heap[0][0] != rating[heap[0][1]]:
            heapq.heappop(heap)
        return heap[0][1]

    ops, args = ["FoodRatings"], [[foods, cuisines, ratings]]
    for _ in range(CALLS):
        if rng.random() < 0.5:
            food = top(kinds[0]) if rng.random() < 0.8 else rng.choice(foods)
            old = rating[food]
            new = (
                rng.randint(1, old - 1)
                if old > 1 and food == top(kinds[0])
                else rng.randint(1, band)
            )
            rating[food] = new
            heapq.heappush(heaps[cuisine_of[food]], (-new, food))
            ops.append("changeRating")
            args.append([food, new])
        else:
            ops.append("highestRated")
            args.append([kinds[0] if rng.random() < 0.9 else kinds[1]])
    return {"ops": ops, "args": args}
