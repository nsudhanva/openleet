"""Verify Preorder Serialization near 10^4 chars: a valid serialization of a random or
left-deep tree, with an extra or missing '#' at the very end."""

SEEDS = 3
LIMIT = 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    deep = rng.random() < 0.5
    tokens, size, slots = [], -1, 1  # size counts the joined string (commas included)
    while slots:
        # A new number opens one extra slot; every open slot still needs at least "#,".
        room = size + 4 + 2 * (slots + 1) + 4 <= LIMIT
        if room and (deep or slots < 30 or rng.random() < 0.5):
            tokens.append(str(rng.randint(0, 100)))
            slots += 1
        else:
            tokens.append("#")
            slots -= 1
        size += len(tokens[-1]) + 1
    if shape == 1:
        tokens.append("#")
    elif shape == 2:
        tokens.pop()
    return {"preorder": ",".join(tokens)}
