"""Step 1: one work item per problem in data/.cache/judge/work/, built from the sources only."""

import json
import re
import shutil
from pathlib import Path

from openleet.data import PROBLEMS_PATH
from openleet.judging import WORK_ITEMS_DIR, unsupported
from openleet.judging.examples import dataset_inputs, statement_examples
from openleet.judging.signature import design_spec, function_spec, starter_code
from openleet.judging.sources import sources_for
from openleet.sanitize import html_text

ADAPTER_BY_SLUG = {
    "linked-list-cycle": "cycle",
    "linked-list-cycle-ii": "cycle",
    "intersection-of-two-linked-lists": "intersection",
    "delete-node-in-a-linked-list": "delete_node",
    "copy-list-with-random-pointer": "random_list",
    "clone-graph": "graph",
    "populating-next-right-pointers-in-each-node": "next_pointer",
    "populating-next-right-pointers-in-each-node-ii": "next_pointer",
}
# Extra input names an adapter consumes beyond the method's parameters.
ADAPTER_INPUTS = {
    "cycle": {"pos"},
    "intersection": {"intersectVal", "listA", "listB", "skipA", "skipB"},
    "delete_node": {"node"},
}
UNSUPPORTED_TOPICS = {
    "Database": "SQL and Pandas problems are not judged yet.",
    "Concurrency": "Concurrency problems are not judged yet.",
    "Interactive": "Interactive problems are not judged yet.",
    "Randomized": "Problems with random answers are not judged yet.",
}
ANY_ORDER = re.compile(r"\bany order\b", re.I)


def adapter_for(slug: str, spec: dict, examples: list[dict]) -> str | None:
    if slug in ADAPTER_BY_SLUG:
        return ADAPTER_BY_SLUG[slug]
    if "n-ary-tree" in slug:
        return "nary"
    returns_node = spec["kind"] == "function" and "TreeNode" in spec["returns"]
    if returns_node and examples and not any(isinstance(e["output"], list) for e in examples):
        return "node_value"
    return None


def find_spec(examples: list[dict], codes: list[str], entry: str | None) -> dict | None:
    """The spec read from the first of `codes` that yields one."""
    if examples and all(e.get("design") for e in examples):
        cls = examples[0]["input"]["ops"][0]
        ops = {op for e in examples for op in e["input"]["ops"][1:]}
        return next((s for c in codes if (s := design_spec(c, cls, ops))), None)
    method = entry.rsplit(".", 1)[-1] if entry else None
    names = set().union(*(e["input"] for e in examples if not e.get("design"))) or None
    return next((s for c in codes if (s := function_spec(c, method, names))), None)


def work_item(problem: dict) -> dict:
    slug = problem["slug"]
    base = {"slug": slug, "id": problem["id"]}
    for topic, reason in UNSUPPORTED_TOPICS.items():
        if topic in problem["topics"]:
            return base | unsupported(reason)
    found = sources_for(problem["id"], slug)
    if not found.voters:
        return base | unsupported("No reference Python solution to check answers against.")
    examples = statement_examples(problem["description"])
    codes = [c for c in (found.starter, *found.voters.values()) if c]
    spec = find_spec(examples, codes, found.entry_point)
    if spec is None:
        return base | unsupported("Could not read the problem's Python signature.")
    if adapter := adapter_for(slug, spec, examples):
        spec["adapter"] = adapter
    if spec["kind"] == "function":
        known = {p["name"] for p in spec["params"]} | ADAPTER_INPUTS.get(adapter or "", set())
        if any(set(e["input"]) - known for e in examples):
            return base | unsupported("The examples use inputs the signature does not take.")
        inputs = [i for i in dataset_inputs(found.dataset_test) if set(i) <= known]
    else:
        inputs = []
    return base | {
        "supported": True,
        "spec": spec,
        "starter": found.starter or starter_code(spec),
        "examples": examples,
        "inputs": inputs,
        "voters": found.voters,
        "anyOrder": bool(ANY_ORDER.search(html_text(problem["description"] or ""))),
    }


def prepare(problems_path: Path = PROBLEMS_PATH) -> None:
    problems = json.loads(problems_path.read_text())["problems"]
    shutil.rmtree(WORK_ITEMS_DIR, ignore_errors=True)
    WORK_ITEMS_DIR.mkdir(parents=True)
    supported = 0
    for problem in problems:
        item = work_item(problem)
        supported += item["supported"]
        (WORK_ITEMS_DIR / f"{problem['slug']}.json").write_text(json.dumps(item))
    print(f"Prepared {len(problems)} problems, {supported} with a readable signature")
