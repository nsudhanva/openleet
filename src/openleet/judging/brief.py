"""`uv run openleet judge brief [slugs...]`: what a stress-generator author needs per problem
(signature, constraints, one example), compact enough to read hundreds at once. Without slugs
it lists every judged problem that has no generator yet."""

import json
import re
from pathlib import Path

from openleet.judging import HARNESS_DIR, SPECS_PATH, WORK_ITEMS_DIR
from openleet.sanitize import html_text

SUP = re.compile(r"<sup>(.*?)</sup>")
CONSTRAINTS = re.compile(r"Constraints:(.*?)(?=Follow[- ]up|Note:|$)", re.S)
FOLLOW_UP = re.compile(r"Follow[- ]up:?(.*?)(?:\n\n|$)", re.S)


def signature(spec: dict) -> str:
    if spec["kind"] == "design":

        def args(m: dict) -> str:
            return ", ".join(f"{n}: {t}" for n, t in zip(m["names"], m["params"], strict=True))

        methods = ", ".join(f"{name}({args(m)})" for name, m in spec["methods"].items())
        return f"design class {spec['cls']}: {methods}"
    params = ", ".join(f"{p['name']}: {p['type']}" for p in spec["params"])
    adapter = f"  [adapter {spec['adapter']}]" if spec.get("adapter") else ""
    return f"{spec['method']}({params}) -> {spec['returns']}{adapter}"


def brief(slugs: list[str], problems_path: Path) -> None:
    problems = {p["slug"]: p for p in json.loads(problems_path.read_text())["problems"]}
    specs = json.loads(SPECS_PATH.read_text())
    if not slugs:
        done = {p.stem for p in (HARNESS_DIR / "gen").glob("*.py")}
        slugs = sorted(s for s, e in specs.items() if e["supported"] and s not in done)
    for slug in slugs:
        entry, problem = specs[slug], problems[slug]
        # 10<sup>4</sup> reads as 10^4; tags vanish so `<code>n</code>` keeps its spacing.
        body = html_text(SUP.sub(r"^\1", problem["description"] or ""), tag_sep="")
        constraints = CONSTRAINTS.search(body)
        follow = FOLLOW_UP.search(body)
        work = json.loads((WORK_ITEMS_DIR / f"{slug}.json").read_text())
        example = work["examples"][0]["input"] if work["examples"] else None
        print(f"### {slug}  (#{problem['id']} {problem['title']}, {problem['difficulty']})")
        print(f"signature: {signature(entry['spec'])}")
        lines = constraints.group(1).split("\n") if constraints else []
        print("constraints: " + " | ".join(line.strip() for line in lines if line.strip()))
        if follow:
            print(f"follow-up: {' '.join(follow.group(1).split())}")
        print(f"example input: {json.dumps(example)[:300]}")
        print()
