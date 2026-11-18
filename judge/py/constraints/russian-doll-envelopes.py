"""Russian Doll Envelopes: a list of [width, height] pairs."""


def check(envelopes: list[list[int]]) -> None:
    assert 1 <= len(envelopes) <= 10**5, "1 <= envelopes.length <= 10^5"
    assert all(len(e) == 2 for e in envelopes), "envelopes[i].length == 2"
    assert all(1 <= v <= 10**5 for e in envelopes for v in e), "1 <= wi, hi <= 10^5"
