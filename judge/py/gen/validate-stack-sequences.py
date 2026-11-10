"""Validate Stack Sequences at the maximum 1000 elements: popped order produced by a real
push/pop run (true), its reverse-ish variant, or a random permutation (almost surely false)."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    pushed = rng.sample(range(1001), N)
    if shape == 2:
        popped = pushed[:]
        rng.shuffle(popped)
        return {"pushed": pushed, "popped": popped}
    popped, stack, i = [], [], 0
    while len(popped) < N:
        if i < N and (not stack or rng.random() < (0.5 if shape == 0 else 0.9)):
            stack.append(pushed[i])
            i += 1
        else:
            popped.append(stack.pop())
    if shape == 1:
        # Swap two adjacent pops late in the sequence: usually breaks validity.
        j = rng.randrange(N - 50, N - 1)
        popped[j], popped[j + 1] = popped[j + 1], popped[j]
    return {"pushed": pushed, "popped": popped}
