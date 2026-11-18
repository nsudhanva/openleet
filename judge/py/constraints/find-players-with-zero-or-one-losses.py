"""Find Players With Zero or One Losses: a list of [winner, loser] matches."""


def check(matches: list[list[int]]) -> None:
    assert 1 <= len(matches) <= 10**5, "1 <= matches.length <= 10^5"
    assert all(len(m) == 2 for m in matches), "matches[i].length == 2"
    assert all(1 <= w <= 10**5 and 1 <= lo <= 10**5 for w, lo in matches), (
        "1 <= winneri, loseri <= 10^5"
    )
    assert all(w != lo for w, lo in matches), "winneri != loseri"
    assert len({(w, lo) for w, lo in matches}) == len(matches), "all matches[i] are unique"
