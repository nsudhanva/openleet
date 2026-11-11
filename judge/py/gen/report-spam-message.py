"""Report Spam Message at 10^4 message words and 10^4 banned words over a three-letter alphabet,
the only banned message words at the end, so a banned list scanned per word costs ~10^8 string
comparisons."""

SEEDS = 2
N = 10**4
M = 10**4


def word(rng):
    return "".join(rng.choice("abc") for _ in range(rng.randint(12, 15)))


def generate(rng):
    banned = set()
    while len(banned) < M:
        banned.add(word(rng))
    banned_list = sorted(banned)
    rng.shuffle(banned_list)
    message = []
    while len(message) < N - 2:
        w = word(rng)
        if w not in banned:
            message.append(w)
    hits = 2 if rng.random() < 0.5 else 1
    message += rng.sample(banned_list, hits)
    if hits == 1:
        message.insert(N - 2, message[0])
    return {"message": message, "bannedWords": banned_list}
