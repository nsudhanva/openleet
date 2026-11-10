"""UTF-8 Validation at 2 * 10^4 bytes: a long valid stream of 1-4 byte characters, the same
with one byte corrupted or truncated near the end."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def char(rng):
    width = rng.randint(1, 4)
    if width == 1:
        return [rng.randint(0, 0x7F)]
    lead = {2: (0xC0, 0xDF), 3: (0xE0, 0xEF), 4: (0xF0, 0xF7)}[width]
    return [rng.randint(*lead)] + [rng.randint(0x80, 0xBF) for _ in range(width - 1)]


def generate(rng):
    shape = pick_shape(rng)
    data = []
    while True:
        c = char(rng)
        if len(data) + len(c) > N:
            break
        data.extend(c)
    if shape == 1:
        i = rng.randrange(len(data) - 50, len(data))
        data[i] = rng.choice([0xF8, 0xFF, 0x80, 0xC0, 0x41])
    elif shape == 2:
        while data and data[-1] < 0xC0:
            data.pop()
        if data:
            data.pop()
        data.append(rng.choice([0xC2, 0xE2, 0xF0]))  # a lead byte with nothing after
    return {"data": data}
