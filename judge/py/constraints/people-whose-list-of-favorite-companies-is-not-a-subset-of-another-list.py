"""People Whose List of Favorite Companies Is Not a Subset of Another List: lists of company
names."""

import re


def check(favoriteCompanies: list[list[str]]) -> None:
    assert 1 <= len(favoriteCompanies) <= 100, "1 <= favoriteCompanies.length <= 100"
    assert all(isinstance(lst, list) for lst in favoriteCompanies), "favoriteCompanies[i] is a list"
    assert all(1 <= len(lst) <= 500 for lst in favoriteCompanies), (
        "1 <= favoriteCompanies[i].length <= 500"
    )
    assert all(
        isinstance(s, str) and 1 <= len(s) <= 20 for lst in favoriteCompanies for s in lst
    ), "1 <= favoriteCompanies[i][j].length <= 20"
    assert all(re.fullmatch(r"[a-z]+", s) for lst in favoriteCompanies for s in lst), (
        "strings are lowercase English letters only"
    )
    assert all(len(set(lst)) == len(lst) for lst in favoriteCompanies), (
        "strings in favoriteCompanies[i] are distinct"
    )
    sets = {frozenset(lst) for lst in favoriteCompanies}
    assert len(sets) == len(favoriteCompanies), "all lists of favorite companies are distinct"
