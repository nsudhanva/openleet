"""The judge's test corpus as a DuckDB file (data/judge/tests.duckdb): its schema, writing it,
and converting a file of the older schema.

The server attaches the file read-only (server/src/db/corpus.rs). It reads `meta` first and
accepts SCHEMA_VERSION, or schema 0 (the layout before `meta`: tests(slug, idx, kind VARCHAR,
test, expected, expected_sha256), all nullable); it refuses anything else.
"""

from pathlib import Path

import duckdb

SCHEMA_VERSION = 1
TEST_KINDS = ("example", "hidden", "stress")

SCHEMA = f"""
CREATE TYPE test_kind AS ENUM {TEST_KINDS!r};
COMMENT ON TYPE test_kind IS 'example: shown above the editor and used by Run; hidden: run on '
    'Submit; stress: generated at judge time from a seed (judge/py/gen).';

CREATE TABLE tests (
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    idx USMALLINT NOT NULL,
    kind test_kind NOT NULL,
    test_case JSON NOT NULL USING COMPRESSION zstd,
    expected JSON USING COMPRESSION zstd,
    expected_sha256 VARCHAR CHECK (regexp_full_match(expected_sha256, '[0-9a-f]{{64}}')),
    CHECK ((expected IS NULL) <> (expected_sha256 IS NULL))
);
COMMENT ON TABLE tests IS 'Every test the judge runs, stored in (slug, idx) order so a lookup by '
    'slug reads one or two row groups (zone maps). Kept only when every qualified reference '
    'solution agrees (src/openleet/judging/assemble.py).';
COMMENT ON COLUMN tests.slug IS 'The problem (data/problems.json).';
COMMENT ON COLUMN tests.idx IS 'Position among the problem''s tests, from 0 with no gaps: '
    'examples, then hidden tests, then stress tests.';
COMMENT ON COLUMN tests.kind IS 'What the test is for (see the test_kind type).';
COMMENT ON COLUMN tests.test_case IS 'The test as the judge''s zygote takes it: '
    '{{"input": ...}} or a stress generator reference {{"gen", "seed", "sha"}}; canonical JSON.';
COMMENT ON COLUMN tests.expected IS 'The agreed answer as canonical JSON; NULL when only its '
    'digest is stored.';
COMMENT ON COLUMN tests.expected_sha256 IS 'For large exact stress answers instead of expected: '
    'the SHA-256 (hex) of the line the sandboxed child prints for the answer.';

CREATE TABLE meta (
    schema_version USMALLINT NOT NULL,
    built_at TIMESTAMPTZ NOT NULL,
    built_by VARCHAR NOT NULL CHECK (built_by <> ''),
    problem_count UINTEGER NOT NULL,
    test_count UINTEGER NOT NULL
);
COMMENT ON TABLE meta IS 'One row describing this file; the server checks it before reading tests.';
COMMENT ON COLUMN meta.schema_version IS 'The layout of this file (testdb.SCHEMA_VERSION).';
COMMENT ON COLUMN meta.built_at IS 'When the file was written.';
COMMENT ON COLUMN meta.built_by IS 'The command that wrote it.';
COMMENT ON COLUMN meta.problem_count IS 'Distinct slugs in tests.';
COMMENT ON COLUMN meta.test_count IS 'Rows in tests.';
"""

# Each version's tests as rows of the current table, from a database attached as `src`.
SOURCES = {
    0: "SELECT slug, idx, kind, test AS test_case, expected, expected_sha256 FROM src.tests",
    1: "SELECT slug, idx, kind, test_case, expected, expected_sha256 FROM src.tests",
}


def quoted(path: Path) -> str:
    """A path as a SQL string literal."""
    return "'" + str(path).replace("'", "''") + "'"


def version_of(con: duckdb.DuckDBPyConnection, database: str) -> int:
    """The schema version of an attached corpus (0 for the layout before `meta`)."""
    tables = {
        name
        for (name,) in con.execute(
            "SELECT table_name FROM duckdb_tables() WHERE database_name = ?", [database]
        ).fetchall()
    }
    if "meta" in tables:
        row = con.execute(f"SELECT max(schema_version) FROM {database}.meta").fetchone()
        return int(row[0]) if row and row[0] is not None else -1
    return 0 if tables == {"tests"} else -1


def write(path: Path, rows: str, built_by: str, attach: Path | None = None) -> None:
    """Writes a corpus to `path`, replacing it once complete. `rows` is a query yielding the
    tests table's columns by name; `attach` is a database it reads, attached as `src`."""
    partial = path.with_name(path.name + ".partial")
    partial.unlink(missing_ok=True)
    try:
        fill(partial, rows, built_by, attach)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    partial.replace(path)


def fill(path: Path, rows: str, built_by: str, attach: Path | None) -> None:
    """Creates the schema in a new file at `path` and fills it (see `write`)."""
    with duckdb.connect(str(path), config={"autoload_known_extensions": False}) as con:
        if attach is not None:
            con.execute(f"ATTACH {quoted(attach)} AS src (READ_ONLY)")
        con.execute(SCHEMA)
        # Sorted by slug so the server's lookups skip row groups that cannot contain it.
        con.execute(f"INSERT INTO tests BY NAME ({rows}) ORDER BY slug, idx")
        con.execute(
            """INSERT INTO meta SELECT ?, current_timestamp, ?, count(DISTINCT slug), count(*)
            FROM tests""",
            [SCHEMA_VERSION, built_by],
        )
        gaps = con.execute(
            """SELECT count(*) FROM (SELECT slug FROM tests GROUP BY slug
            HAVING min(idx) <> 0 OR max(idx) + 1 <> count(DISTINCT idx)
                OR count(*) <> count(DISTINCT idx))"""
        ).fetchone()
        if gaps and gaps[0]:
            raise SystemExit(f"{gaps[0]} problems' test indexes do not run 0, 1, 2, ...")
        if attach is not None:
            con.execute("DETACH src")
        con.execute("CHECKPOINT")


def write_jsonl(path: Path, staging: Path, built_by: str) -> None:
    """Writes a corpus from JSON lines, one object per test with the tests table's columns
    (kind and the JSON columns as text)."""
    columns = (
        "{slug: 'VARCHAR', idx: 'USMALLINT', kind: 'VARCHAR', test_case: 'VARCHAR',"
        " expected: 'VARCHAR', expected_sha256: 'VARCHAR'}"
    )
    write(path, f"FROM read_json({quoted(staging)}, columns = {columns})", built_by)


def summary(con: duckdb.DuckDBPyConnection, database: str) -> dict:
    """Counts and checks of an attached corpus, for comparing two files."""
    test_col = "test" if version_of(con, database) == 0 else "test_case"
    row = con.execute(
        f"""SELECT count(*), count(DISTINCT slug), count(DISTINCT (slug, idx)),
            count(*) FILTER (kind::VARCHAR = 'example'), count(*) FILTER (kind::VARCHAR = 'hidden'),
            count(*) FILTER (kind::VARCHAR = 'stress'), count(expected), count(expected_sha256),
            count(*) FILTER ((expected IS NULL) = (expected_sha256 IS NULL)),
            count(*) FILTER (slug IS NULL OR idx IS NULL OR kind IS NULL OR {test_col} IS NULL)
        FROM {database}.tests"""
    ).fetchone()
    assert row is not None
    names = [
        "rows",
        "problems",
        "distinct_keys",
        "example",
        "hidden",
        "stress",
        "with_expected",
        "with_sha256",
        "not_exactly_one_answer",
        "nulls_in_required",
    ]
    # Physical order: every row after the previous one in (slug, idx).
    unsorted = con.execute(
        f"""SELECT count(*) FROM (SELECT slug, idx, lag(slug) OVER w AS ps, lag(idx) OVER w AS pi
            FROM {database}.tests WINDOW w AS (ORDER BY rowid))
            WHERE ps IS NOT NULL AND (slug, idx) <= (ps, pi)"""
    ).fetchone()
    return dict(zip(names, row, strict=True)) | {"out_of_order": unsorted[0] if unsorted else -1}


def migrate(source: Path, target: Path) -> None:
    """`judge migrate-corpus IN OUT`: rewrites a corpus in the current schema, then checks
    that every test survived unchanged (text-identical test, expected and digest)."""
    if source.resolve() == target.resolve():
        raise SystemExit("IN and OUT must differ")
    with duckdb.connect(config={"autoload_known_extensions": False}) as con:
        con.execute(f"ATTACH {quoted(source)} AS src (READ_ONLY)")
        version = version_of(con, "src")
        con.execute("DETACH src")
    if version not in SOURCES:
        raise SystemExit(f"{source}: unknown corpus schema (version {version})")
    write(target, SOURCES[version], "openleet judge migrate-corpus", attach=source)

    with duckdb.connect(config={"autoload_known_extensions": False}) as con:
        con.execute(f"ATTACH {quoted(source)} AS src (READ_ONLY)")
        con.execute(f"ATTACH {quoted(target)} AS dst (READ_ONLY)")
        before, after = summary(con, "src"), summary(con, "dst")
        changed = con.execute(
            f"""SELECT count(*) FROM ({SOURCES[version]}) o FULL JOIN dst.tests n USING (slug, idx)
            WHERE o.kind IS DISTINCT FROM n.kind::VARCHAR
               OR o.test_case IS DISTINCT FROM n.test_case::VARCHAR
               OR o.expected IS DISTINCT FROM n.expected::VARCHAR
               OR o.expected_sha256 IS DISTINCT FROM n.expected_sha256"""
        ).fetchone()
        meta = con.execute(
            "SELECT * REPLACE (built_at::VARCHAR AS built_at) FROM dst.meta"
        ).fetchall()
    width = max(map(len, before))
    print(f"{'':{width}}  {'before':>9}  {'after':>9}")
    for name in before:
        print(f"{name:{width}}  {before[name]:>9}  {after[name]:>9}")
    print(f"rows that differ: {changed[0] if changed else '?'}")
    print(f"meta: {meta}")
    print(f"bytes: {source.stat().st_size} -> {target.stat().st_size}")
    if not changed or changed[0] or after["rows"] != before["rows"]:
        target.unlink()
        raise SystemExit("the converted corpus differs from its source; removed it")
