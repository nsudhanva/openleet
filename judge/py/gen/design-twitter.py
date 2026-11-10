"""Design Twitter with 3 * 10^4 calls: 10^4 unique tweets spread over 500 users and dense
follow graphs, so each news feed merges many followees' timelines."""

SEEDS = 2
CALLS = 3 * 10**4
USERS = 500


def generate(rng):
    tweet_ids = rng.sample(range(10**4 + 1), 10**4 + 1)
    following = {u: set() for u in range(1, USERS + 1)}
    ops, args = ["Twitter"], [[]]
    posted = 0
    while len(ops) <= CALLS:
        x = rng.random()
        u = rng.randint(1, USERS)
        if x < 0.33 and posted < len(tweet_ids):
            ops.append("postTweet")
            args.append([u, tweet_ids[posted]])
            posted += 1
        elif x < 0.66:
            ops.append("getNewsFeed")
            args.append([u])
        elif x < 0.9:
            v = rng.randint(1, USERS)
            if v == u or v in following[u]:
                continue
            following[u].add(v)
            ops.append("follow")
            args.append([u, v])
        else:
            if not following[u]:
                continue
            v = rng.choice(sorted(following[u]))
            following[u].discard(v)
            ops.append("unfollow")
            args.append([u, v])
    return {"ops": ops, "args": args}
