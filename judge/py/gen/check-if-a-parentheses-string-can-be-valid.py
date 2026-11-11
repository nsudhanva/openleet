"""Check if a Parentheses String Can Be Valid at n = 2 * 10^4: a valid string with most positions
unlocked and rewritten at random, so the answer is true only after the whole string is read and
tracking every reachable balance is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    s, depth = [], 0
    for i in range(N):
        if depth == N - i or (depth and rng.random() < 0.5):
            s.append(")")
            depth -= 1
        else:
            s.append("(")
            depth += 1
    locked = "".join("1" if rng.random() < 0.3 else "0" for _ in range(N))
    # Unlocked characters may become anything, so the answer stays true while s itself is not
    # valid and no "is it already valid" shortcut applies.
    s = [c if lock == "1" else rng.choice("()") for c, lock in zip(s, locked, strict=True)]
    return {"s": "".join(s), "locked": locked}
