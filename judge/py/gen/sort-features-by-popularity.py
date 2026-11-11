"""Sort Features by Popularity with 10^4 features and 100 responses of ~1,000 characters, so
splitting every response again for every feature is 10^6 splits of ~200 words."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
FEATURES = 10**4
RESPONSES = 100
LENGTH = 1000
POPULAR = 300


def generate(rng):
    pool = set()
    while len(pool) < FEATURES:
        pool.add(random_string(rng, ascii_lowercase, rng.randint(1, 10)))
    features = sorted(pool)
    rng.shuffle(features)
    # A few hundred popular features recur across responses; the rest show up rarely or never.
    popular = rng.sample(features, POPULAR)
    responses = []
    for _ in range(RESPONSES):
        words, size = [], -1
        while True:
            if rng.random() < 0.6:
                word = rng.choice(popular)
            elif rng.random() < 0.5:
                word = rng.choice(features)
            else:
                word = random_string(rng, ascii_lowercase, rng.randint(1, 10))
            if size + 1 + len(word) > LENGTH:
                break
            words.append(word)
            size += 1 + len(word)
        responses.append(" ".join(words))
    return {"features": features, "responses": responses}
