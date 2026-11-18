"""Best Time to Buy and Sell Stock with Transaction Fee: daily prices and a fee."""


def check(prices: list[int], fee: int) -> None:
    assert isinstance(fee, int), "fee is an integer"
    assert 1 <= len(prices) <= 5 * 10**4, "1 <= prices.length <= 5 * 10^4"
    assert all(1 <= p < 5 * 10**4 for p in prices), "1 <= prices[i] < 5 * 10^4"
    assert 0 <= fee < 5 * 10**4, "0 <= fee < 5 * 10^4"
