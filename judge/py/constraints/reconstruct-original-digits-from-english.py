"""Reconstruct Original Digits from English: a scrambled concatenation of digit words."""

from collections import Counter

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
ORDER = [
    (0, "z"),
    (2, "w"),
    (4, "u"),
    (6, "x"),
    (8, "g"),
    (3, "h"),
    (5, "f"),
    (7, "s"),
    (1, "o"),
    (9, "i"),
]


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "egfihonsrutwvxz" for c in s), (
        "s[i] is one of the characters e,g,f,i,h,o,n,s,r,u,t,w,v,x,z"
    )
    cnt = Counter(s)
    for d, key in ORDER:
        k = cnt[key]
        if k:
            for c in WORDS[d]:
                cnt[c] -= k
    assert all(v == 0 for v in cnt.values()), "s is guaranteed to be valid"
