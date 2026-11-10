"""Evaluate Reverse Polish Notation with ~10^4 tokens: every operand pushed first (a 5000-deep
stack), or operands and operators interleaved; every intermediate result stays a 32-bit
integer and no division is by zero."""

SEEDS = 2
NUMS = 5000
LO, HI = -(2**31), 2**31 - 1


def apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if b == 0:
        return None
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def generate(rng):
    deep = rng.random() < 0.5
    tokens, stack, left = [], [], NUMS
    while left or len(stack) > 1:
        push = left and (len(stack) < 2 or (not deep and rng.random() < 0.5) or deep)
        if push:
            v = rng.randint(-200, 200)
            tokens.append(str(v))
            stack.append(v)
            left -= 1
            continue
        b, a = stack.pop(), stack.pop()
        ops = ["+", "-", "*", "/"]
        rng.shuffle(ops)
        for op in ops:
            r = apply(op, a, b)
            if r is not None and LO <= r <= HI:
                break
        tokens.append(op)
        stack.append(r)
    return {"tokens": tokens}
