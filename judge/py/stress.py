"""Runs the stress-test generators (gen/<slug>.py) through the zygote: each seed's input is
made exactly as the judge will make it, then every reference that passed the problem's other
tests answers it. openleet.judging.assemble keeps the seeds they all agree on.

Usage (inside the judge image, as root, without network):
    python stress.py WORK_DIR SPECS_JSON RESULTS_DIR [JOBS]
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from random import Random

import vote
from zygote import GEN_DIR, generator, input_sha

# Reference solutions get far more time than submissions: their times set the limits.
LIMITS = {**vote.LIMITS, "cpu_s": 120}


def stress(slug: str, item: dict, entry: dict, results_dir: Path) -> None:
    gen = generator(slug)
    seeds = list(range(getattr(gen, "SEEDS", 3)))
    shas = [input_sha(gen.generate(Random(seed))) for seed in seeds]
    tests = [{"gen": slug, "seed": seed, "sha": sha} for seed, sha in zip(seeds, shas, strict=True)]
    codes = {name: item["voters"][name] for name in entry["voters"]}
    voters = vote.ballots(entry["spec"], codes, tests, LIMITS)
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
