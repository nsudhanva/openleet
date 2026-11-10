"""Allowlist HTML sanitizer for problem statements, so the web app can render them as-is, and
plain-text extraction for parsing them."""

import re
from html import escape, unescape
from html.parser import HTMLParser

ALLOWED_TAGS = frozenset(
    {
        "p",
        "pre",
        "code",
        "strong",
        "b",
        "em",
        "i",
        "u",
        "sup",
        "sub",
        "ul",
        "ol",
        "li",
        "br",
        "hr",
        "img",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "span",
        "div",
        "blockquote",
    }
)
VOID_TAGS = frozenset({"br", "hr", "img"})
DROP_CONTENT_TAGS = frozenset({"script", "style", "iframe", "object"})
ALLOWED_ATTRS = {"img": frozenset({"src", "alt"})}
TAG = re.compile(r"<[^>]+>")


class _Sanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.dropping = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in DROP_CONTENT_TAGS:
            self.dropping += 1
        if self.dropping or tag not in ALLOWED_TAGS:
            return
        allowed = ALLOWED_ATTRS.get(tag, frozenset())
        kept = "".join(
            f' {name}="{escape(value)}"'
            for name, value in attrs
            if name in allowed and value is not None and _safe_attr(name, value)
        )
        self.out.append(f"<{tag}{kept}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in DROP_CONTENT_TAGS:
            self.dropping = max(0, self.dropping - 1)
            return
        if not self.dropping and tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.out.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if not self.dropping:
            self.out.append(escape(data, quote=False))


def _safe_attr(name: str, value: str) -> bool:
    return name != "src" or value.startswith("https://")


def sanitize_html(raw: str) -> str:
    """`raw` with only allowlisted tags and attributes; script and style content dropped."""
    parser = _Sanitizer()
    parser.feed(raw)
    parser.close()
    return "".join(parser.out).strip()


def html_text(html: str, tag_sep: str = " ") -> str:
    """The text of an HTML fragment: tags become `tag_sep`, entities and no-break spaces are
    decoded."""
    return unescape(TAG.sub(tag_sep, html)).replace("\xa0", " ")
