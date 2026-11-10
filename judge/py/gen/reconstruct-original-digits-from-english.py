"""Reconstruct Original Digits at length near 10^5: shuffled letters of digit words, built from
a real multiset of digits so the input is valid."""

SEEDS = 2
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def generate(rng):
    weights = [rng.random() for _ in range(10)]
    if rng.random() < 0.5:
        weights = [w if i in (1, 3, 5, 7, 9) else w / 50 for i, w in enumerate(weights)]
    letters = []
    while True:
        d = rng.choices(range(10), weights)[0]
        if len(letters) + len(WORDS[d]) > 10**5:
            break
        letters.extend(WORDS[d])
    rng.shuffle(letters)
    return {"s": "".join(letters)}
