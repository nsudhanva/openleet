"""`uv run openleet judge <stage>`: the stages of the pipeline in openleet.judging."""

import os
import subprocess
from pathlib import Path

from openleet.judging import HARNESS_DIR, RESULTS_DIR, SPECS_PATH, STRESS_DIR, WORK_ITEMS_DIR
from openleet.judging.assemble import assemble
from openleet.judging.brief import brief
from openleet.judging.corpus import fetch, publish
from openleet.judging.prepare import prepare
from openleet.judging.testdb import migrate

# The stages `judge all` runs, in order.
PIPELINE = ("prepare", "vote", "assemble", "stress", "final")
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


def migrate_corpus(paths: list[str]) -> None:
    """Converts a corpus file to the current schema (see testdb.migrate)."""
    if len(paths) != 2:
        raise SystemExit("usage: openleet judge migrate-corpus IN OUT")
    migrate(Path(paths[0]), Path(paths[1]))


def run(stage: str, args: list[str], problems_path: Path) -> None:
    stages = {
        "prepare": lambda: prepare(problems_path),
        "vote": vote,
        "assemble": assemble,
        "stress": stress,
        "final": assemble,
        "brief": lambda: brief(args, problems_path),
        "publish": publish,
        "fetch": fetch,
        "migrate-corpus": lambda: migrate_corpus(args),
    }
    for name in PIPELINE if stage == "all" else [stage]:
        stages[name]()
