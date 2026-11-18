"""Most Common Word: a paragraph of letters, spaces and punctuation, and banned words."""

import re
import string
from collections import Counter


def check(paragraph: str, banned: list[str]) -> None:
    assert 1 <= len(paragraph) <= 1000, "1 <= paragraph.length <= 1000"
    allowed = set(string.ascii_letters + " !?',;.")
    assert all(c in allowed for c in paragraph), (
        "paragraph consists of English letters, space, or one of !?',;."
    )
    assert 0 <= len(banned) <= 100, "0 <= banned.length <= 100"
    assert all(1 <= len(b) <= 10 for b in banned), "1 <= banned[i].length <= 10"
    assert all(b.isascii() and b.isalpha() and b.islower() for b in banned), (
        "banned[i] consists of only lowercase English letters"
    )
    words = re.findall(r"[a-z]+", paragraph.lower())
    counts = Counter(w for w in words if w not in set(banned))
    assert counts, "at least one word is not banned"
    top = counts.most_common(2)
    assert len(top) == 1 or top[0][1] > top[1][1], "the answer is unique"
