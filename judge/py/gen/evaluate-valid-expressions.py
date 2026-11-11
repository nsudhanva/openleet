"""Evaluate Valid Expressions at length ~10^5: one chain of ~10^4 nested operations, so a parser
that scans for each operation's top-level comma is ~5 * 10^8 steps."""

SEEDS = 2
N = 10**5
CAP = 10**15


def generate(rng):
    value = rng.randint(-1000, 1000)
    core = str(value)
    pre, post, length = [], [], len(core)
    while True:
        b = rng.randint(-1000, 1000)
        op = rng.choice(["add", "sub", "mul", "div"])
        # The chain so far is the first operand or the second, at random.
        first = rng.random() < 0.5
        if op == "div":
            if first:
                # Only divisors that leave an exact quotient.
                b = rng.choice([d for d in (1, -1, 2, -2, 3, -3) if value % d == 0])
            else:
                op = "mul"
        new = {"add": value + b, "sub": value - b, "mul": value * b}.get(op)
        if op == "sub" and not first:
            new = b - value
        if op == "div":
            new = value // b
        if abs(new) > CAP:
            op, new = "add", value + b
        piece_left, piece_right = (op + "(", f",{b})") if first else (f"{op}({b},", ")")
        length += len(piece_left) + len(piece_right)
        if length > N:
            break
        pre.append(piece_left)
        post.append(piece_right)
        value = new
    return {"expression": "".join(reversed(pre)) + core + "".join(post)}
