"""Maximum Number of Books You Can Take: book counts per shelf."""


def check(books: list[int]) -> None:
    assert 1 <= len(books) <= 10**5, "1 <= books.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in books), "0 <= books[i] <= 10^5"
