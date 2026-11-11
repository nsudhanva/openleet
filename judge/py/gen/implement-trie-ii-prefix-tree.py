"""Trie II at the maximum 3 * 10^4 calls: 1.5 * 10^4 inserts of mostly distinct short words over
a four-letter alphabet, then prefix counts, equal counts and erases, so counting a prefix by
scanning the stored words costs ~1.5 * 10^4 steps per call, ~2 * 10^8 in all."""

from _shapes import random_string

SEEDS = 2
CALLS = 3 * 10**4
FILL = 15000
ALPHA = "abcd"


def generate(rng):
    ops, args = ["Trie"], [[]]
    words = []
    for _ in range(FILL):
        w = random_string(rng, ALPHA, rng.randint(7, 9))
        words.append(w)
        ops.append("insert")
        args.append([w])
    for _ in range(CALLS - FILL):
        r = rng.random()
        if r < 0.8 or not words:
            ops.append("countWordsStartingWith")
            args.append([random_string(rng, ALPHA, rng.randint(1, 4))])
        elif r < 0.9:
            ops.append("countWordsEqualTo")
            w = rng.choice(words) if rng.random() < 0.5 else random_string(rng, ALPHA, 8)
            args.append([w])
        else:
            i = rng.randrange(len(words))
            words[i], words[-1] = words[-1], words[i]
            ops.append("erase")
            args.append([words.pop()])
    return {"ops": ops, "args": args}
