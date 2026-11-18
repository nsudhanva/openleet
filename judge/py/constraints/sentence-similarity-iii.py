"""Sentence Similarity III: two sentences of single-space separated words."""

import string


def check(sentence1: str, sentence2: str) -> None:
    ok = set(string.ascii_letters + " ")
    for s in (sentence1, sentence2):
        assert isinstance(s, str) and 1 <= len(s) <= 100, "1 <= sentence.length <= 100"
        assert set(s) <= ok, (
            "sentences consist of lowercase and uppercase English letters and spaces"
        )
        assert s == s.strip(" ") and "  " not in s, "words are separated by a single space"
