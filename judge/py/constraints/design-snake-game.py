"""Design Snake Game: SnakeGame calls."""


def _shape(ops, args, ctor, ctor_arity, sig):
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == ctor, "first operation is the constructor"
    assert all(isinstance(a, list) for a in args), "each args[i] is a list"
    assert len(args[0]) == ctor_arity, "constructor argument count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in sig, "known method name"
        assert len(a) == sig[op], "argument count of " + op


def check(ops: list[str], args: list[list]) -> None:
    _shape(ops, args, "SnakeGame", 3, {"move": 1})
    from collections import deque

    width, height, food = args[0]
    assert isinstance(width, int) and 1 <= width <= 10**4, "1 <= width <= 10^4"
    assert isinstance(height, int) and 1 <= height <= 10**4, "1 <= height <= 10^4"
    assert isinstance(food, list) and 1 <= len(food) <= 50, "1 <= food.length <= 50"
    assert all(isinstance(f, list) and len(f) == 2 for f in food), "food[i].length == 2"
    assert all(0 <= r < height and 0 <= c < width for r, c in food), (
        "0 <= ri < height, 0 <= ci < width"
    )
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to move"
    assert all(isinstance(a[0], str) and a[0] in ("U", "D", "L", "R") for a in args[1:]), (
        "direction is 'U', 'D', 'L', or 'R'"
    )
    delta = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    body = deque([(0, 0)])
    occupied = {(0, 0)}
    nxt = 0
    assert tuple(food[0]) not in occupied, "food does not appear on a block occupied by the snake"
    for a in args[1:]:
        dr, dc = delta[a[0]]
        r, c = body[-1][0] + dr, body[-1][1] + dc
        if not (0 <= r < height and 0 <= c < width):
            break
        eating = nxt < len(food) and (r, c) == tuple(food[nxt])
        if not eating:
            occupied.discard(body.popleft())
        if (r, c) in occupied:
            break
        body.append((r, c))
        occupied.add((r, c))
        if eating:
            nxt += 1
            if nxt < len(food):
                assert tuple(food[nxt]) not in occupied, (
                    "food does not appear on a block occupied by the snake"
                )
