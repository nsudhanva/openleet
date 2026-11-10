"""`uv run google judge prepare|vote|assemble|all`."""

import os
import subprocess

from google.judging import HARNESS_DIR, SPECS_PATH, WORK_DIR
from google.judging.assemble import assemble
from google.judging.brief import brief
from google.judging.prepare import prepare

# The judge's own runtime, so references run exactly as submissions will.
IMAGE = "google-judge-dev"
IMAGE_RECIPE = (
    "FROM python:3.15-slim\n"
    "RUN pip install --no-cache-dir --root-user-action=ignore sortedcontainers==2.4.0\n"
)


def vote() -> None:
    """Runs the references in a container without network, as root so the sandbox can drop
    to its own user. Problems already voted on are skipped; delete results/ to redo them."""
    subprocess.run(
        ["docker", "build", "-q", "-t", IMAGE, "-"], input=IMAGE_RECIPE.encode(), check=True
    )
    results = WORK_DIR / "results"
    results.mkdir(parents=True, exist_ok=True)
    jobs = str(os.cpu_count() or 1)
    subprocess.run(
        [
            "docker", "run", "--rm", "--network", "none",
            "-v", f"{HARNESS_DIR.resolve()}:/judge:ro",
            "-v", f"{(WORK_DIR / 'work').resolve()}:/work:ro",
            "-v", f"{results.resolve()}:/results",
            IMAGE, "python", "/judge/vote.py", "/work", "/results", jobs,
        ],
        check=True,
    )  # fmt: skip


def stress() -> None:
    """Runs the stress generators in judge/py/gen and the references on what they make.
    Needs specs.json from a first assemble (it names each problem's qualified references)."""
    results = WORK_DIR / "stress"
    results.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "docker", "run", "--rm", "--network", "none",
            "-v", f"{HARNESS_DIR.resolve()}:/judge:ro",
            "-v", f"{(WORK_DIR / 'work').resolve()}:/work:ro",
            "-v", f"{SPECS_PATH.resolve()}:/specs.json:ro",
            "-v", f"{results.resolve()}:/results",
            IMAGE, "python", "/judge/stress.py", "/work", "/specs.json", "/results",
            str(os.cpu_count() or 1),
        ],
        check=True,
    )  # fmt: skip


def run(stage: str, slugs: list[str]) -> None:
    if stage == "brief":
        brief(slugs)
        return
    stages = {
        "prepare": prepare,
        "vote": vote,
        "assemble": assemble,
        "stress": stress,
        "final": assemble,
    }
    for name in stages if stage == "all" else [stage]:
        stages[name]()
