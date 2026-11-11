"""Sender With Largest Word Count over 10^4 messages from ~10^4 distinct senders, so summing every
message per sender is ~10^8 comparisons."""

SEEDS = 2
N = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def name(rng, size):
    return "".join(rng.choice(LETTERS) for _ in range(size))


def generate(rng):
    names = set()
    while len(names) < N * 9 // 10:
        names.add(name(rng, rng.randint(1, 10)))
    names = sorted(names)
    rng.shuffle(names)
    senders = [names[i] if i < len(names) else rng.choice(names) for i in range(N)]
    rng.shuffle(senders)
    messages = [
        " ".join(name(rng, rng.randint(1, 4)) for _ in range(rng.randint(1, 5))) for _ in range(N)
    ]
    return {"messages": messages, "senders": senders}
