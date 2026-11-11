"""Strings Differ by One Character with 2 * 10^4 five-letter words whose last letter is a
checksum, so no two differ in one place (or only the last two do): comparing every pair is
~2 * 10^8 pair checks."""

from string import ascii_lowercase

SEEDS = 2
COUNT = 2 * 10**4
LENGTH = 5


def generate(rng):
    # The first draw picks the answer, so seeds 0 and 1 take different branches.
    twin = rng.random() < 0.5
    pool = set()
    while len(pool) < COUNT:
        head = [rng.randrange(26) for _ in range(LENGTH - 1)]
        word = [*head, sum(head) % 26]
        pool.add("".join(ascii_lowercase[x] for x in word))
    words = sorted(pool)
    rng.shuffle(words)
    if twin:
        # Swap the last word for one that differs from its neighbour in a single place.
        last = words[-2]
        i = rng.randrange(LENGTH)
        c = rng.choice([x for x in ascii_lowercase if x != last[i]])
        words[-1] = last[:i] + c + last[i + 1 :]
    return {"dict": words}
