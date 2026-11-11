"""Find Longest Self-Contained Substring at length 2 * 10^4: a boundary letter at both ends and
in the middle ties the 20 mixed letters to the whole string, so only short one-letter blocks
qualify and checking substrings, longest first, is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    letters = list("abcdefghijklmnopqrstuvwxyz")
    rng.shuffle(letters)
    edge, mixed, solo = letters[0], letters[1:21], letters[21:]
    runs = [[c] * rng.randint(50, 400) for c in solo]
    body = [rng.choice(mixed) for _ in range(N - 5 - sum(map(len, runs)))]
    # The middle copies of the edge letter stop any span of mixed letters from avoiding both ends.
    for _ in range(3):
        body.insert(rng.randrange(len(body) // 4, 3 * len(body) // 4), edge)
    for run in runs:
        # Each solo letter is one run, never inside or beside another run.
        i = rng.randrange(1, len(body))
        while body[i - 1] in solo or body[i] in solo:
            i = rng.randrange(1, len(body))
        body[i:i] = run
    return {"s": edge + "".join(body) + edge}
