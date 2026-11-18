"""Maximum Points You Can Obtain from Cards: card points and the number of cards to take."""


def check(cardPoints: list[int], k: int) -> None:
    assert 1 <= len(cardPoints) <= 10**5, "1 <= cardPoints.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in cardPoints), "1 <= cardPoints[i] <= 10^4"
    assert 1 <= k <= len(cardPoints), "1 <= k <= cardPoints.length"
