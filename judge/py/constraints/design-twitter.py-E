"""Design Twitter: postTweet/getNewsFeed/follow/unfollow calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert args[0] == [], "Twitter()"
    assert len(ops) - 1 <= 3 * 10**4, "at most 3 * 10^4 calls"
    tweets = set()
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert all(isinstance(x, int) for x in a), "integer arguments"
        if op == "postTweet":
            assert len(a) == 2, "postTweet(userId, tweetId)"
            assert 1 <= a[0] <= 500, "1 <= userId <= 500"
            assert 0 <= a[1] <= 10**4, "0 <= tweetId <= 10^4"
            assert a[1] not in tweets, "all tweets have unique IDs"
            tweets.add(a[1])
        elif op == "getNewsFeed":
            assert len(a) == 1 and 1 <= a[0] <= 500, "1 <= userId <= 500"
        elif op in ("follow", "unfollow"):
            assert len(a) == 2, f"{op}(followerId, followeeId)"
            assert 1 <= a[0] <= 500 and 1 <= a[1] <= 500, "1 <= followerId, followeeId <= 500"
            assert op == "unfollow" or a[0] != a[1], "a user cannot follow himself"
        else:
            raise AssertionError("unknown operation")
