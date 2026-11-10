import argparse
from pathlib import Path

from openleet.data import PROBLEMS_PATH


def main() -> None:
    """The `openleet` command; each subcommand imports only what it needs."""
    # Every command that reads or writes the problem list takes the same option, so a new
    # list can be staged (ingest --problems X, judge prepare --problems X) before it replaces
    # data/problems.json.
    problems = argparse.ArgumentParser(add_help=False)
    problems.add_argument(
        "--problems", type=Path, default=PROBLEMS_PATH, help=f"default: {PROBLEMS_PATH}"
    )
    parser = argparse.ArgumentParser(prog="openleet", description="OpenLeet data tools")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "ingest", parents=[problems], help="build the problem list from the source lists"
    )
    commands.add_parser(
        "check", parents=[problems], help="validate data/approaches.json against ASD-STE100 rules"
    )
    judge = commands.add_parser(
        "judge", parents=[problems], help="build the judge's specs and tests (data/judge)"
    )
    judge.add_argument(
        "stage",
        choices=[
            "prepare",
            "vote",
            "assemble",
            "stress",
            "final",
            "time",
            "limits",
            "all",
            "brief",
            "publish",
            "fetch",
            "migrate-corpus",
        ],
    )
    judge.add_argument(
        "args", nargs="*", help="brief: problems to describe; migrate-corpus: IN OUT"
    )
    smoke = commands.add_parser(
        "smoke", help="end-to-end judge and sandbox checks against a running server (HTTP only)"
    )
    smoke.add_argument("--base-url", default="http://localhost:8080")
    smoke.add_argument("--sample", type=int, default=30, help="problems to sample (default 30)")
    smoke.add_argument("--seed", type=int, help="sample seed (default: random, printed)")
    smoke.add_argument("--slow", type=int, default=2, help="stress problems given a slow variant")
    smoke.add_argument("--specs", type=Path, help="specs.json with the reference solutions")
    smoke.add_argument("--json", action="store_true", help="print the results as JSON")
    smoke.add_argument(
        "--allow-network",
        action="store_true",
        help="pass the network check anyway (the local Docker judge has a network)",
    )
    args = parser.parse_args()

    if args.command == "ingest":
        from openleet.ingest import ingest

        ingest(args.problems)
    elif args.command == "judge":
        from openleet.judging.cli import run

        run(args.stage, args.args, args.problems)
    elif args.command == "smoke":
        from openleet.judging import SPECS_PATH
        from openleet.smoke import smoke

        raise SystemExit(
            smoke(
                args.base_url,
                args.sample,
                args.seed,
                args.json,
                args.specs or SPECS_PATH,
                args.slow,
                args.allow_network,
            )
        )
    else:
        from openleet.approaches import check

        raise SystemExit(check(args.problems))
