"""Generate Tag for Video Caption: a caption of English letters and spaces."""


def check(caption: str) -> None:
    assert 1 <= len(caption) <= 150, "1 <= caption.length <= 150"
    assert all(c == " " or ("a" <= c <= "z") or ("A" <= c <= "Z") for c in caption), (
        "caption consists only of English letters and ' '"
    )
