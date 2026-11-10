"""Runs the stress-test generators (gen/<slug>.py) through the zygote: each seed's input is
made exactly as the judge will make it, then every reference that passed the problem's other
tests answers it. openleet.judging.assemble keeps the seeds they all agree on.

Usage (inside the judge image, as root, without network):
    python stress.py WORK_DIR SPECS_JSON RESULTS_DIR [JOBS]
"""

import hashlib
import importlib.util
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).parent))

import harness
from vote import outcomes, zygote

GEN_DIR = Path(__file__).with_name("gen")
sys.path.append(str(GEN_DIR))  # generators import _shapes
# Reference solutions get far more time than submissions: their times set the limits.
LIMITS = {"cpu_s": 120, "as_mb": 3072, "out_bytes": 512 << 20, "stdout_bytes": 0}


def module(slug: str):
    spec = importlib.util.spec_from_file_location(f"gen_{slug}", GEN_DIR / f"{slug}.py")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def stress(slug: str, item: dict, entry: dict, results_dir: Path) -> None:
    gen = module(slug)
    seeds = list(range(getattr(gen, "SEEDS", 3)))
    tests, shas = [], []
    for seed in seeds:
        data = gen.generate(Random(seed))
        shas.append(hashlib.sha256(harness.dumps(data).encode()).hexdigest())
        tests.append({"gen": slug, "seed": seed, "sha": shas[-1]})
    voters = {}
    for name in entry["voters"]:
        job = {
            "spec": entry["spec"],
            "code": item["voters"][name],
            "tests": tests,
            "limits": LIMITS,
            "keep_going": True,
        }
        try:
            results, cpu, error = outcomes(zygote().run(job), len(tests))
        except (RuntimeError, OSError, ValueError) as failure:
            results, cpu, error = [None] * len(tests), 0, repr(failure)
        voters[name] = {"results": results, "cpuMs": cpu, "error": error}
    out = {"slug": slug, "seeds": seeds, "shas": shas, "voters": voters}
    (results_dir / f"{slug}.json").write_text(json.dumps(out))


def main() -> None:
    work, specs_path, results = (Path(a) for a in sys.argv[1:4])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count() or 1
    results.mkdir(parents=True, exist_ok=True)
    specs = json.loads(specs_path.read_text())
    slugs = sorted(
        p.stem
        for p in GEN_DIR.glob("*.py")
        if specs.get(p.stem, {}).get("supported") and not (results / f"{p.stem}.json").exists()
    )
    print(f"Stress-testing {len(slugs)} problems with {jobs} workers", flush=True)

    def one(slug: str) -> None:
        item = json.loads((work / f"{slug}.json").read_text())
        try:
            stress(slug, item, specs[slug], results)
        except Exception as error:
            print(f"  {slug}: {type(error).__name__}: {error}", flush=True)

    with ThreadPoolExecutor(jobs) as pool:
        list(pool.map(one, slugs))


if __name__ == "__main__":
    main()
