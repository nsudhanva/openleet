"""Design A Leaderboard with the full 1000 calls over a few hundred players, resetting only
players on the board and asking top(K) with K up to the current player count."""

SEEDS = 2
CALLS = 1000


def generate(rng):
    ids = rng.sample(range(1, 10**4 + 1), rng.randint(50, 400))
    on_board = set()
    ops, args = ["Leaderboard"], [[]]
    for _ in range(CALLS):
        x = rng.random()
        if x < 0.6 or not on_board:
            pid = rng.choice(ids)
            on_board.add(pid)
            ops.append("addScore")
            args.append([pid, rng.randint(1, 100)])
        elif x < 0.75:
            pid = rng.choice(sorted(on_board))
            on_board.discard(pid)
            ops.append("reset")
            args.append([pid])
        else:
            ops.append("top")
            args.append([rng.randint(1, len(on_board))])
    return {"ops": ops, "args": args}
