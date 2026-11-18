"""Invalid Transactions: strings "name,time,amount,city"."""


def check(transactions: list[str]) -> None:
    assert isinstance(transactions, list), "transactions is a list"
    assert len(transactions) <= 1000, "transactions.length <= 1000"
    for t in transactions:
        assert isinstance(t, str), "each transaction is a string"
        parts = t.split(",")
        assert len(parts) == 4, 'form "{name},{time},{amount},{city}"'
        name, time, amount, city = parts
        for w in (name, city):
            assert 1 <= len(w) <= 10, "name and city have length 1..10"
            assert all("a" <= c <= "z" for c in w), "name and city are lowercase English letters"
        assert time.isascii() and time.isdigit(), "time consists of digits"
        assert 0 <= int(time) <= 1000, "time is an integer in [0, 1000]"
        assert amount.isascii() and amount.isdigit(), "amount consists of digits"
        assert 0 <= int(amount) <= 2000, "amount is an integer in [0, 2000]"
