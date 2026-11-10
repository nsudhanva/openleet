"""`uv run openleet judge <stage>`: the stages of the pipeline in openleet.judging."""

import os
import subprocess
from pathlib import Path

from openleet.judging import HARNESS_DIR, RESULTS_DIR, SPECS_PATH, STRESS_DIR, WORK_ITEMS_DIR
from openleet.judging.assemble import assemble
from openleet.judging.brief import brief
from openleet.judging.prepare import prepare

# The judge's own runtime, so references run exactly as submissions will.
IMAGE = "openleet-judge-dev"
IMAGE_RECIPE = (
    "FROM python:3.15-slim\n"
    "RUN pip install --no-cache-dir --root-user-action=ignore sortedcontainers==2.4.0\n"
)


def run_in_sandbox(script: str, args: list[str], mounts: dict[Path, str]) -> None:
    """Runs judge/py/<script> in the judge image without network, as root so the sandbox can
    drop to its own user. `mounts` maps host paths to container paths (append ":ro" for
    read-only); the harness is mounted at /judge. The job count goes last."""
    subprocess.run(
        ["docker", "build", "-q", "-t", IMAGE, "-"], input=IMAGE_RECIPE.encode(), check=True
    )
    volumes = [
        arg
        for host, target in {HARNESS_DIR: "/judge:ro", **mounts}.items()
        for arg in ("-v", f"{host.resolve()}:{target}")
    ]
    subprocess.run(
        [
            "docker", "run", "--rm", "--network", "none", *volumes,
            IMAGE, "python", f"/judge/{script}", *args, str(os.cpu_count() or 1),
        ],
        check=True,
    )  # fmt: skip


def vote() -> None:
    """Runs every reference on every input. Problems already voted on are skipped; delete
    their results to redo them."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_in_sandbox(
        "vote.py",
        ["/work", "/results"],
        {WORK_ITEMS_DIR: "/work:ro", RESULTS_DIR: "/results"},
    )


def stress() -> None:
    """Runs the stress generators in judge/py/gen and the references on what they make.
    Needs specs.json from a first assemble (it names each problem's qualified references)."""
    STRESS_DIR.mkdir(parents=True, exist_ok=True)
    run_in_sandbox(
        "stress.py",
        ["/work", "/specs.json", "/results"],
        {WORK_ITEMS_DIR: "/work:ro", SPECS_PATH: "/specs.json:ro", STRESS_DIR: "/results"},
    )


def run(stage: str, slugs: list[str], problems_path: Path) -> None:
    if stage == "brief":
        brief(slugs, problems_path)
        return
    stages = {
        "prepare": lambda: prepare(problems_path),
        "vote": vote,
        "assemble": assemble,
        "stress": stress,
        "final": assemble,
    }
    for name in stages if stage == "all" else [stage]:
        stages[name]()
