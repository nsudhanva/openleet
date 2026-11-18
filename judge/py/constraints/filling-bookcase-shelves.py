"""Filling Bookcase Shelves: [thickness, height] books and a shelf width."""


def check(books: list[list[int]], shelfWidth: int) -> None:
    assert 1 <= len(books) <= 1000, "1 <= books.length <= 1000"
    assert all(len(b) == 2 for b in books), "books[i].length == 2"
    assert 1 <= shelfWidth <= 1000, "shelfWidth <= 1000"
    assert all(1 <= t <= shelfWidth for t, _ in books), "1 <= thicknessi <= shelfWidth"
    assert all(1 <= h <= 1000 for _, h in books), "1 <= heighti <= 1000"
