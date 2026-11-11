"""Report Spam Message at 2 * 10^4 message words and 2 * 10^4 banned words over a three-letter
alphabet: either two banned message words, at the very first and last positions, or exactly one,
at a random position. A scan can neither stop early nor start from the end, so a banned list
scanned per word costs ~4 * 10^8 string comparisons."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
M = 2 * 10**4


def word(rng):
    return "".join(rng.choice("abc") for _ in range(rng.randint(12, 15)))


def generate(rng):
    banned = set()
    while len(banned) < M:
        banned.add(word(rng))
    banned_list = sorted(banned)
    rng.shuffle(banned_list)
    message = []
    while len(message) < N:
        w = word(rng)
        if w not in banned:
            message.append(w)
    if pick_shape(rng) == 0:
        if rng.random() < 0.5:
            first, last = rng.sample(banned_list, 2)
        else:
            first = last = rng.choice(banned_list)
        message[0], message[-1] = first, last
    else:
        message[rng.randrange(N)] = rng.choice(banned_list)
    return {"message": message, "bannedWords": banned_list}
