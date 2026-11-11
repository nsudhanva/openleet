"""Longest Uploaded Prefix at n = 3 * 10^4 videos and 4.5 * 10^4 calls: the first half of the videos
goes up first, then each remaining upload is followed by a longest() call, so recounting the
prefix from 1 per query is >= 2 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    first = list(range(1, N // 2 + 1))
    rest = list(range(N // 2 + 1, N + 1))
    rng.shuffle(first)
    rng.shuffle(rest)
    ops, args = ["LUPrefix"], [[N]]
    for video in first:
        ops.append("upload")
        args.append([video])
    for video in rest:
        ops += ["longest", "upload"]
        args += [[], [video]]
    ops.append("longest")
    args.append([])
    return {"ops": ops, "args": args}
