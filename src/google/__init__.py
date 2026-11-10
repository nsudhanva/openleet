import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="google", description="LeetCode flashcard data tools")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("ingest", help="build data/problems.json from the source lists")
    commands.add_parser("check", help="validate data/approaches.json against ASD-STE100 rules")
    judge = commands.add_parser("judge", help="build the judge's specs and tests (data/judge)")
    judge.add_argument(
        "stage", choices=["prepare", "vote", "assemble", "stress", "final", "brief", "all"]
    )
    judge.add_argument("slugs", nargs="*", help="brief: problems to describe")
    args = parser.parse_args()

    if args.command == "ingest":
        from google.ingest import ingest

        ingest()
    elif args.command == "judge":
        from google.judging.cli import run

        run(args.stage, args.slugs)
    else:
        from google.approaches import check

        raise SystemExit(check())
