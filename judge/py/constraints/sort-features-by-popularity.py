"""Sort Features by Popularity: feature names and space-separated responses."""


def _lower(s: str) -> bool:
    return all("a" <= c <= "z" for c in s)


def check(features: list[str], responses: list[str]) -> None:
    assert 1 <= len(features) <= 10**4, "1 <= features.length <= 10^4"
    assert all(isinstance(f, str) and 1 <= len(f) <= 10 for f in features), (
        "1 <= features[i].length <= 10"
    )
    assert all(_lower(f) for f in features), "features[i] consists of lowercase letters"
    assert len(set(features)) == len(features), "features contains no duplicates"
    assert 1 <= len(responses) <= 100, "1 <= responses.length <= 10^2"
    assert all(isinstance(r, str) and 1 <= len(r) <= 1000 for r in responses), (
        "1 <= responses[i].length <= 10^3"
    )
    assert all(_lower(r.replace(" ", "")) for r in responses), (
        "responses[i] consists of lowercase letters and spaces"
    )
    assert all("  " not in r for r in responses), "responses[i] contains no two consecutive spaces"
    assert all(r == r.strip(" ") for r in responses), (
        "responses[i] has no leading or trailing spaces"
    )
