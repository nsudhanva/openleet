"""Lexicographically Minimum String After Removing Stars at the maximum length 10^5, letters first
and stars mostly after them, so scanning the kept letters for the smallest per star costs ~10^9
steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    head = N // 2 + rng.randint(0, N // 10)
    out = [rng.choice(letters) for _ in range(head)]
    avail = head
    while len(out) < N:
        if avail and rng.random() < 0.9:
            out.append("*")
            avail -= 1
        else:
            out.append(rng.choice(letters))
            avail += 1
    return {"s": "".join(out)}
