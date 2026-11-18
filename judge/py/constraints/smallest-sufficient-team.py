"""Smallest Sufficient Team: required skills and the skills of each person."""


def _word(w: str) -> bool:
    return 1 <= len(w) <= 16 and w.isascii() and w.isalpha() and w.islower()


def check(req_skills: list[str], people: list[list[str]]) -> None:
    assert 1 <= len(req_skills) <= 16, "1 <= req_skills.length <= 16"
    assert all(_word(s) for s in req_skills), (
        "1 <= req_skills[i].length <= 16, lowercase English letters"
    )
    assert len(set(req_skills)) == len(req_skills), "all req_skills are unique"
    assert 1 <= len(people) <= 60, "1 <= people.length <= 60"
    assert all(len(p) <= 16 for p in people), "0 <= people[i].length <= 16"
    assert all(_word(s) for p in people for s in p), (
        "1 <= people[i][j].length <= 16, lowercase English letters"
    )
    assert all(len(set(p)) == len(p) for p in people), "all strings of people[i] are unique"
    req = set(req_skills)
    assert all(s in req for p in people for s in p), "every skill in people[i] is in req_skills"
    have = {s for p in people for s in p}
    assert have == req, "a sufficient team exists"
