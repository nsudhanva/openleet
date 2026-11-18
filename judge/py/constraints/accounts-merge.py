"""Accounts Merge: accounts as [name, email, ...] lists."""


def check(accounts: list[list[str]]) -> None:
    assert 1 <= len(accounts) <= 1000, "1 <= accounts.length <= 1000"
    assert all(isinstance(a, list) for a in accounts), "accounts[i] is a list"
    assert all(2 <= len(a) <= 10 for a in accounts), "2 <= accounts[i].length <= 10"
    assert all(isinstance(s, str) for a in accounts for s in a), "accounts[i][j] is a string"
    assert all(1 <= len(s) <= 30 for a in accounts for s in a), "1 <= accounts[i][j].length <= 30"
    assert all(a[0].isascii() and a[0].isalpha() for a in accounts), (
        "accounts[i][0] consists of English letters"
    )
    for a in accounts:
        for e in a[1:]:
            local, at, domain = e.partition("@")
            assert at and local and domain and "@" not in domain, (
                "accounts[i][j] (for j > 0) is a valid email"
            )
