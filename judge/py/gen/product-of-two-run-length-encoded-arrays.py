"""Product of Two Run-Length Encoded Arrays with 5000 runs of 8000 to 10^4 in the first array and
the same boundaries (some runs split in two) in the second, so expanding the ~4.5 * 10^7-element
arrays costs thousands of times walking the runs."""

SEEDS = 2
RUNS = 5000
FREQ = 10**4


def values(rng, n):
    out, last = [], 0
    for _ in range(n):
        last = rng.choice([x for x in (1, 2, 3) if x != last])
        out.append(last)
    return out


def generate(rng):
    first = [rng.randint(FREQ * 4 // 5, FREQ) for _ in range(RUNS)]
    second = []
    for f in first:
        if f > 1 and rng.random() < 0.3:
            cut = rng.randint(1, f - 1)
            second += [cut, f - cut]
        else:
            second.append(f)
    encoded1 = [[v, f] for v, f in zip(values(rng, len(first)), first, strict=True)]
    encoded2 = [[v, f] for v, f in zip(values(rng, len(second)), second, strict=True)]
    return {"encoded1": encoded1, "encoded2": encoded2}
