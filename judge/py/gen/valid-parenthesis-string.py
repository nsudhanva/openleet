"""Valid Parenthesis String at the maximum length 100, heavy with '*' and false only because
of the last characters, so trying the three meanings of each star searches exponentially many
prefixes before failing."""

SEEDS = 2
N = 100


def generate(rng):
    if rng.random() < 0.5:
        # Mostly stars, never more ')' than '(' and '*' so far, then one '(' nothing can close.
        s, most = [], 0
        for _ in range(N - 1):
            c = rng.choice("***()")
            if c == ")" and most == 0:
                c = "*"
            most += -1 if c == ")" else 1
            s.append(c)
        s.append("(")
    else:
        # '(' and '*' up front, one ')' too many at the back.
        head = N // 2 - 1
        s = [rng.choice("(**") for _ in range(head)] + [")"] * (N - head)
    return {"s": "".join(s)}
