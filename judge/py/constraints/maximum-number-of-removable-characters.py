"""Maximum Number of Removable Characters: strings s and p and distinct removable indices."""


def check(s: str, p: str, removable: list[int]) -> None:
    assert 1 <= len(p) <= len(s) <= 10**5, "1 <= p.length <= s.length <= 10^5"
    assert all(0 <= i < len(s) for i in removable), "0 <= removable[i] < s.length"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert all("a" <= c <= "z" for c in p), "p consists of lowercase English letters"
    assert len(set(removable)) == len(removable), "the elements in removable are distinct"
    it = iter(s)
    assert all(c in it for c in p), "p is a subsequence of s"
