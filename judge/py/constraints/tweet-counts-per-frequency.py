"""Tweet Counts Per Frequency: a TweetCounts call sequence."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "TweetCounts" and args[0] == [], "constructor takes no arguments"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls in total"
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "recordTweet":
            assert len(a) == 2, "recordTweet(tweetName, time)"
            assert isinstance(a[0], str), "tweetName is a string"
            assert 0 <= a[1] <= 10**9, "0 <= time <= 10^9"
        else:
            assert op == "getTweetCountsPerFrequency", "only the two documented calls"
            assert len(a) == 4, "getTweetCountsPerFrequency(freq, tweetName, startTime, endTime)"
            assert a[0] in ("minute", "hour", "day"), "freq is minute, hour or day"
            assert isinstance(a[1], str), "tweetName is a string"
            assert 0 <= a[2] <= 10**9 and 0 <= a[3] <= 10**9, "0 <= startTime, endTime <= 10^9"
            assert 0 <= a[3] - a[2] <= 10**4, "0 <= endTime - startTime <= 10^4"
