"""Valid Parentheses at length 10^4: one deep nest of mixed brackets, a long valid random
sequence, or the same with one bracket type swapped at the end."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
PAIRS = ["()", "[]", "{}"]


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        opens = [rng.choice(PAIRS) for _ in range(N // 2)]
        s = "".join(p[0] for p in opens) + "".join(p[1] for p in reversed(opens))
    else:
        out, stack = [], []
        while len(out) + len(stack) < N:
            if stack and (rng.random() < 0.5 or len(out) + 2 * len(stack) >= N):
                out.append(stack.pop())
            else:
                p = rng.choice(PAIRS)
                out.append(p[0])
                stack.append(p[1])
        out.extend(reversed(stack))
        s = "".join(out)
        if shape == 2:
            i = rng.randrange(N - 20, N)
            swap = {"(": "[", ")": "]", "[": "{", "]": "}", "{": "(", "}": ")"}
            s = s[:i] + swap[s[i]] + s[i + 1 :]
    return {"s": s}
