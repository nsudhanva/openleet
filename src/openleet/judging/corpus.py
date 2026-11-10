"""`judge publish` and `judge fetch`: data/judge/tests.duckdb is too big for git, so it lives
as an asset of the GitHub release `corpus`; data/judge/corpus.json (in git) names the asset
and its SHA-256."""

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from openleet.data import download
from openleet.judging import JUDGE_DIR, TESTS_PATH

REPO = "nsudhanva/openleet"
RELEASE = "corpus"
CORPUS_PATH = JUDGE_DIR / "corpus.json"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as data:
        while chunk := data.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def gh(*args: str, **options: Any) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args, "--repo", REPO], **options)


def publish() -> None:
    """Uploads tests.duckdb under a content-addressed name and records it in corpus.json."""
    digest = sha256_of(TESTS_PATH)
    asset = f"tests-{digest[:12]}.duckdb"
    if gh("release", "view", RELEASE, capture_output=True).returncode != 0:
        notes = "The judge's test corpus (data/judge/tests.duckdb); see data/judge/corpus.json."
        create = ("release", "create", RELEASE, "--prerelease", "--title", "Judge corpus")
        gh(*create, "--notes", notes, check=True)
    # gh names an asset after its file, so upload a copy that carries the asset name.
    with tempfile.TemporaryDirectory() as tmp:
        named = Path(tmp) / asset
        shutil.copyfile(TESTS_PATH, named)
        gh("release", "upload", RELEASE, str(named), "--clobber", check=True)
    corpus = {"asset": asset, "sha256": digest, "bytes": TESTS_PATH.stat().st_size}
    CORPUS_PATH.write_text(json.dumps(corpus, indent=1) + "\n")
    print(f"Published {asset} ({corpus['bytes']} bytes); commit {CORPUS_PATH}")


def fetch() -> None:
    """Downloads the corpus named in corpus.json unless tests.duckdb already matches it."""
    corpus = json.loads(CORPUS_PATH.read_text())
    if TESTS_PATH.exists() and sha256_of(TESTS_PATH) == corpus["sha256"]:
        print(f"{TESTS_PATH} is up to date")
        return
    url = f"https://github.com/{REPO}/releases/download/{RELEASE}/{corpus['asset']}"
    fetched = download(url, TESTS_PATH.with_name(corpus["asset"]))
    if (actual := sha256_of(fetched)) != corpus["sha256"]:
        fetched.unlink()
        raise SystemExit(f"{url}: SHA-256 {actual}, expected {corpus['sha256']}")
    fetched.replace(TESTS_PATH)
    print(f"Fetched {corpus['asset']} -> {TESTS_PATH}")
