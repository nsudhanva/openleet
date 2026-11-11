"""`judge publish` and `judge fetch`: data/judge/tests.duckdb is too big for git, so it lives
as an asset of the GitHub release `corpus`; data/judge/corpus.json (in git) names the repository
that holds it, the asset and its SHA-256. A fork downloads its upstream's corpus until it
publishes its own."""

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from openleet.data import download
from openleet.judging import JUDGE_DIR, TESTS_PATH

RELEASE = "corpus"
CORPUS_PATH = JUDGE_DIR / "corpus.json"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as data:
        while chunk := data.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def gh(repo: str, *args: str, **options: Any) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args, "--repo", repo], **options)


def current_repo() -> str:
    """The checkout's GitHub repository (owner/name), as gh resolves it from the git remote."""
    view = ("gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
    return subprocess.run(view, capture_output=True, text=True, check=True).stdout.strip()


def publish() -> None:
    """Uploads tests.duckdb under a content-addressed name to this checkout's repository and
    records it in corpus.json."""
    repo = current_repo()
    digest = sha256_of(TESTS_PATH)
    asset = f"tests-{digest[:12]}.duckdb"
    if gh(repo, "release", "view", RELEASE, capture_output=True).returncode != 0:
        notes = "The judge's test corpus (data/judge/tests.duckdb); see data/judge/corpus.json."
        create = ("release", "create", RELEASE, "--prerelease", "--title", "Judge corpus")
        gh(repo, *create, "--notes", notes, check=True)
    # gh names an asset after its file, so upload a copy that carries the asset name.
    with tempfile.TemporaryDirectory() as tmp:
        named = Path(tmp) / asset
        shutil.copyfile(TESTS_PATH, named)
        gh(repo, "release", "upload", RELEASE, str(named), "--clobber", check=True)
    size = TESTS_PATH.stat().st_size
    corpus = {"repository": repo, "asset": asset, "sha256": digest, "bytes": size}
    CORPUS_PATH.write_text(json.dumps(corpus, indent=1) + "\n")
    print(f"Published {asset} ({size} bytes) to {repo}; commit {CORPUS_PATH}")


def fetch() -> None:
    """Downloads the corpus named in corpus.json unless tests.duckdb already matches it."""
    corpus = json.loads(CORPUS_PATH.read_text())
    if TESTS_PATH.exists() and sha256_of(TESTS_PATH) == corpus["sha256"]:
        print(f"{TESTS_PATH} is up to date")
        return
    repo, asset = corpus["repository"], corpus["asset"]
    url = f"https://github.com/{repo}/releases/download/{RELEASE}/{asset}"
    fetched = download(url, TESTS_PATH.with_name(asset))
    if (actual := sha256_of(fetched)) != corpus["sha256"]:
        fetched.unlink()
        raise SystemExit(f"{url}: SHA-256 {actual}, expected {corpus['sha256']}")
    fetched.replace(TESTS_PATH)
    print(f"Fetched {asset} -> {TESTS_PATH}")
