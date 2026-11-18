"""Word Ladder: begin and end words plus a list of distinct same-length lowercase words."""


def check(beginWord: str, endWord: str, wordList: list[str]) -> None:
    n = len(beginWord)
    assert 1 <= n <= 10, "1 <= beginWord.length <= 10"
    assert len(endWord) == n, "endWord.length == beginWord.length"
    assert 1 <= len(wordList) <= 5000, "1 <= wordList.length <= 5000"
    assert all(len(w) == n for w in wordList), "wordList[i].length == beginWord.length"
    words = [beginWord, endWord, *wordList]
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "beginWord, endWord, and wordList[i] consist of lowercase English letters"
    )
    assert beginWord != endWord, "beginWord != endWord"
    assert len(set(wordList)) == len(wordList), "all the words in wordList are unique"
