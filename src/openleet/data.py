"""Where the data files live (paths are relative to the repo root) and the download cache."""

import shutil
import urllib.request
from pathlib import Path

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / ".cache"
PROBLEMS_PATH = DATA_DIR / "problems.json"
APPROACHES_PATH = DATA_DIR / "approaches.json"
DOWNLOAD_TIMEOUT_S = 60


def doocs_readme_path(problem_id: int) -> Path:
    """The cached doocs/leetcode README of a problem: statement, metadata and solutions."""
    return CACHE_DIR / "doocs" / f"{problem_id:04d}.md"


def download(url: str, path: Path) -> Path:
    """Downloads `url` to `path`; a partial download never takes the final name."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    with (
        urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT_S) as response,
        partial.open("wb") as out,
    ):
        shutil.copyfileobj(response, out)
    partial.replace(path)
    return path


def cached_download(url: str, path: Path) -> Path:
    """`path`, downloading `url` to it only if it is not there yet."""
    return path if path.exists() else download(url, path)
