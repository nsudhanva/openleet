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
    args = parser.parse_args()

    if args.command == "ingest":
        from openleet.ingest import ingest

        ingest(args.problems)
    elif args.command == "judge":
        from openleet.judging.cli import run

        run(args.stage, args.args, args.problems)
    else:
        from openleet.approaches import check

        raise SystemExit(check(args.problems))
