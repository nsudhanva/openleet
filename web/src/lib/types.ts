/**
 * Shapes of data/problems.json and of the JSON API (server/, see the README's API table).
 * The server computes everything; the UI only renders these.
 */

export const DIFFICULTIES = ["Easy", "Medium", "Hard"] as const;
export type Difficulty = (typeof DIFFICULTIES)[number];

/** How recently Google asked a problem; each list is a subset of the next. */
export const ASKED_PERIODS = ["30d", "3m", "6m"] as const;
export type AskedPeriod = (typeof ASKED_PERIODS)[number];

/** The problem lists: Google's three periods, then the free LeetCode problems 1 to 1000. */
export const PERIODS = [...ASKED_PERIODS, "lc1000"] as const;
export type Period = (typeof PERIODS)[number];
export const PERIOD_LABEL: Record<Period, string> = {
	"30d": "30 days",
	"3m": "3 months",
	"6m": "6 months",
	lc1000: "LC 1–1000",
};

export function isAskedPeriod(period: Period): period is AskedPeriod {
	return period !== "lc1000";
}

/** Position and frequency (0-100) of a problem in one period's list. */
export interface Asked {
	rank: number;
	frequency: number;
}

/** One row of data/problems.json (built by `uv run google ingest`). */
export interface Problem {
	id: number;
	slug: string;
	title: string;
	difficulty: Difficulty;
	/** Google's lists; empty for a classic problem Google did not ask. */
	asked: Partial<Record<AskedPeriod, Asked>>;
	url: string;
	topics: string[];
	premium: boolean;
	/** Sanitized HTML statement; null for premium problems. */
	description: string | null;
}

/** One entry of data/approaches.json, written in ASD-STE100 Simplified Technical English. */
export interface Approach {
	insight: string;
	steps: string[];
	time: string;
	space: string;
	/** Nudges shown one at a time before the answer; they never name the technique. */
	hints: string[];
}

/**
 * What the learner did with a card. "again" adds it to the visit-again list, "less" to the
 * visit-less-often list, "good" clears both, and "skip" defers it without a grade.
 */
export const GRADES = ["again", "good", "less", "skip"] as const;
export type Grade = (typeof GRADES)[number];

export type CardList = "again" | "less";
export type CardStatus = "new" | "due" | "later";

/** A card's Leitner state, replayed by the server from the attempt log. */
export interface CardState {
	box: number;
	due: number;
	list: CardList | null;
	reviews: number;
	lastAt: number;
	lastScore: number | null;
	lastGrade: Grade;
}

// ---- Study ----

export interface StudyCard {
	problem: Problem;
	approach: Approach | null;
	state: CardState | null;
	/** Your own answer, or null when you have not written one. */
	note: string | null;
}

export interface StudyDeck {
	card: StudyCard | null;
	/** Cards left in the chosen set, including this one. */
	remaining: number;
	/** Every topic, most common first, for the guess picker. */
	topics: string[];
}

export interface AttemptInput {
	slug: string;
	grade: Grade;
	guessed: string[];
	hints: number;
}

/** Every problem with its progress. Topics stay off so browsing does not spoil guesses. */
export interface ProblemRow
	extends Pick<
		Problem,
		"id" | "slug" | "title" | "difficulty" | "asked" | "premium"
	> {
	status: CardStatus;
	list: CardList | null;
	reviews: number;
	lastScore: number | null;
	lastAt: number | null;
	due: number | null;
}

/** Where a search hit matched, strongest first. */
export type SearchField =
	| "number"
	| "title"
	| "difficulty"
	| "topic"
	| "statement";

export interface SearchHit {
	slug: string;
	id: number;
	rank: number;
	title: string;
	difficulty: Difficulty;
	field: SearchField;
	/** Statement excerpt around the match, for statement-only hits. */
	snippet: string | null;
}

// ---- Progress ----

export interface ScoreReport {
	computedAt: number;
	/** Mastery weighted by 6-month Google frequency, 0..1. */
	readiness: number;
	/** Share of Google problems graded at least once. */
	coverage: number;
	/** Mean topic score over the last 50 graded attempts. */
	accuracy: number | null;
	graded: number;
	streakDays: number;
	counts: { due: number; new: number; again: number; less: number };
	byDifficulty: {
		difficulty: Difficulty;
		mastery: number;
		seen: number;
		total: number;
	}[];
	/** Recall per topic: how often you named it when it applied. Weakest first. */
	topics: { topic: string; recall: number; seen: number }[];
}

export interface DailyScore {
	day: string;
	readiness: number;
	coverage: number;
	accuracy: number | null;
}

export interface Report {
	report: ScoreReport;
	history: DailyScore[];
}

// ---- Code ----

export const VERDICTS = [
	"accepted",
	"wrong_answer",
	"time_limit_exceeded",
	"memory_limit_exceeded",
	"runtime_error",
	"compile_error",
	"output_limit_exceeded",
	"internal_error",
	// Run only: custom input with no reference answer, so nothing to compare against.
	"finished",
] as const;
export type Verdict = (typeof VERDICTS)[number];

export interface CodeExample {
	/** One `name = value` line per parameter. */
	input: string;
	expected: string;
}

export interface CodeInfo {
	slug: string;
	starter: string | null;
	draft: string | null;
	judge: {
		supported: boolean;
		reason: string | null;
		examples: number;
		hidden: number;
		stress: number;
		timeLimitMs: number | null;
	};
	examples: CodeExample[];
	solved: boolean;
}

export interface RunCase {
	input: string;
	output: string | null;
	expected: string | null;
	stdout: string;
	ok: boolean | null;
}

export interface RunResult {
	verdict: Verdict;
	cases: RunCase[];
	cpuMs: number;
	/** Traceback or compiler message for runtime and compile errors. */
	error: string | null;
}

export type TestKind = "example" | "hidden" | "stress";

export interface FailingCase extends Omit<RunCase, "ok"> {
	kind: TestKind;
}

export interface SubmitResult {
	id: number;
	verdict: Verdict;
	passed: number;
	total: number;
	cpuMs: number;
	limitMs: number;
	error: string | null;
	failing: FailingCase | null;
}

export interface SubmissionSummary {
	id: number;
	/** Epoch milliseconds. */
	at: number;
	verdict: Verdict;
	passed: number;
	total: number;
	cpuMs: number;
}

export interface Submission extends SubmissionSummary {
	code: string;
}
