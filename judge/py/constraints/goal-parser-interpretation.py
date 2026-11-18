"""Goal Parser Interpretation: a string made of "G", "()" and "(al)"."""

import re


def check(command: str) -> None:
    assert 1 <= len(command) <= 100, "1 <= command.length <= 100"
    assert re.fullmatch(r"(G|\(\)|\(al\))+", command), (
        'command consists of "G", "()", and/or "(al)"'
    )
