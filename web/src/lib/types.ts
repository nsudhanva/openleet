/**
 * Shapes of data/problems.json and of the JSON API (server/, see the README's API table).
 * The server computes everything; the UI only renders these.
 */

export const DIFFICULTIES = ["Easy", "Medium", "Hard"] as const;
export type Difficulty = (typeof DIFFICULTIES)[number];

/** How recently a company asked a problem; each list is a subset of the next. */
export const ASKED_PERIODS = ["30d", "3m", "6m", "all"] as const;
export type AskedPeriod = (typeof ASKED_PERIODS)[number];

/** The problem lists: a company's periods, then the free LeetCode problems 1 to 1000. */
export const PERIODS = [...ASKED_PERIODS, "lc1000"] as const;
export type Period = (typeof PERIODS)[number];
export const PERIOD_LABEL: Record<Period, string> = {
	"30d": "30 days",
	"3m": "3 months",
	"6m": "6 months",
	all: "All time",
	lc1000: "LC 1–1000",
};
/** "in the last 6 months", "at any time": how a sentence names an asked period. */
export const PERIOD_PHRASE: Record<AskedPeriod, string> = {
	"30d": "in the last 30 days",
	"3m": "in the last 3 months",
	"6m": "in the last 6 months",
	all: "at any time",
};

export function isAskedPeriod(period: Period): period is AskedPeriod {
	return period !== "lc1000";
}

/** Position and frequency (0-100) of a problem in one period's list. */
export interface Asked {
	rank: number;
	frequency: number;
}

/** A company with problem lists, in the picker's order (GET /api/companies). */
export interface Company {
	slug: string;
	name: string;
	/** Problems it asked, all time. */
	problems: number;
}

/** One company's rank and frequency per period it asked a problem in. */
export type CompanyAsked = Partial<Record<AskedPeriod, Asked>>;

/** One problem of data/problems.json (built by `uv run google ingest`). */
export interface Problem {
	id: number;
	slug: string;
	title: string;
	difficulty: Difficulty;
	/** Every company that asked it, by slug; empty for a classic problem none of them asked. */
	companies: Record<string, CompanyAsked>;
	url: string;
	topics: string[];
	premium: boolean;
	/** Sanitized HTML statement (doocs/leetcode, CC BY-SA 4.0), premium problems included. */
	description: string;
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
const GRADES = ["again", "good", "less", "skip"] as const;
export type Grade = (typeof GRADES)[number];

export type CardList = "again" | "less";
type CardStatus = "new" | "due" | "later";

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

/**
 * One problem of a list (GET /api/problems?company=&period=&topic=&difficulty=&status=&order=
 * &q=), in the plan's order (best match first with `q`), with its progress. Topics stay off so browsing does not
 * spoil guesses.
 */
export interface ProblemRow
	extends Pick<Problem, "id" | "slug" | "title" | "difficulty" | "premium"> {
	/** Rank in the chosen list (LC 1–1000: the LeetCode number). */
	rank: number;
	/** Frequency (0-100) in the chosen list (LC 1–1000: the best of any company, or 0). */
	frequency: number;
	/** Slugs of every company that asked it in any period, in picker order. */
	companies: string[];
	status: CardStatus;
	list: CardList | null;
	reviews: number;
	lastScore: number | null;
	lastAt: number | null;
	due: number | null;
	/** With a search (`q`): the statement excerpt of a statement-only hit. */
	snippet?: string;
}

/** How many problems of a list carry one topic (GET /api/topics). */
export interface TopicCount {
	topic: string;
	problems: number;
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

/** How often you named a topic when it applied, over the cards that carry it. */
export interface TopicRecall {
	topic: string;
	recall: number;
	seen: number;
}

interface ScoreReport {
	computedAt: number;
	/** Mastery weighted by the company's 6-month frequency, 0..1. */
	readiness: number;
	/** Share of the company's 6-month problems graded at least once. */
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
	topics: TopicRecall[];
}

export interface DailyScore {
	day: string;
	readiness: number;
	coverage: number;
	accuracy: number | null;
}

/** The failed verdicts of some submissions, by kind. */
export interface Failures {
	wrongAnswer: number;
	timeLimitExceeded: number;
	memoryLimitExceeded: number;
	runtimeError: number;
	compileError: number;
	outputLimitExceeded: number;
}

/** Coding progress over the report's list. */
export interface Coding {
	byDifficulty: { difficulty: Difficulty; solved: number; total: number }[];
	/** Problems with any submission. */
	tried: number;
	/** Solved problems whose first submission was Accepted. */
	firstTry: number;
	submissions: number;
	failures: Failures;
}

/** A problem Accepted only after two or more failures, or a time limit. */
export interface ShakySolve
	extends Pick<Problem, "id" | "slug" | "title" | "difficulty"> {
	/** The failures before the first Accepted. */
	failures: Failures;
	/** When the first Accepted came, epoch milliseconds. */
	solvedAt: number;
}

/** One topic of the report's list and how much of it you covered. */
export interface TopicRow {
	topic: string;
	/** How much the company asks it: its frequency summed over the topic's problems. */
	weight: number;
	problems: number;
	/** Graded on a card or solved. */
	covered: number;
	solved: number;
	/** Flashcard topic accuracy; null before any card with it was graded. */
	recall: number | null;
}

/** A day with practice, in the server's time zone. */
export interface ActiveDay {
	/** "2026-11-10". */
	day: string;
	reviews: number;
	submissions: number;
}

/** The activity calendar: 26 weeks from `start` (a Monday) to `today`. */
export interface Activity {
	start: string;
	today: string;
	/** Only the days with practice. */
	days: ActiveDay[];
}

export interface Report {
	report: ScoreReport;
	history: DailyScore[];
	coding: Coding;
	/** The list's shaky solves, newest first. */
	shaky: ShakySolve[];
	shakyElsewhere: number;
	/** The list's topics, most asked first. */
	topicMap: TopicRow[];
	activity: Activity;
}

const VERDICTS = [
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
	/** The code Reset replaced, which Restore brings back. */
	previous: string | null;
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

/** The editor's code after Reset or Restore: `code` null means the starter. */
export interface DraftVersions {
	code: string | null;
	previous: string | null;
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
	/** How big the input is, as "nums: 100,000 items". */
	size: string | null;
}

/** The intended solution's complexity, such as "O(n)". */
export interface Complexity {
	time: string;
	space: string;
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
	/** Sent only with a result, since it gives part of the answer away. */
	intended: Complexity | null;
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

/** Which problems of a practice plan still count (lib/plan.ts has the labels). */
export const PLAN_STATUSES = ["unsolved", "untried", "shaky", "all"] as const;
export type PlanStatus = (typeof PLAN_STATUSES)[number];

/** The order a practice plan walks its problems in. */
export const PLAN_ORDERS = ["rank", "number", "easy-first", "random"] as const;
export type PlanOrder = (typeof PLAN_ORDERS)[number];

/**
 * A practice plan: a list, its filters, which problems still count and an order. Also the
 * code page's search params (with the root's `company`).
 */
export interface PlanView {
	company: string;
	period: Period;
	topic: string | null;
	difficulty: Difficulty | null;
	status: PlanStatus;
	order: PlanOrder;
	/** "Google · 6 months · Two Pointers · Unsolved". */
	label: string;
}

/** The problem a plan offers next. No topics: they would give the guess away. */
export interface NextProblem
	extends Pick<Problem, "id" | "slug" | "title" | "difficulty" | "premium"> {
	/** Rank in the plan's list. */
	rank: number;
}

/** Solved out of all the plan's problems, whatever its status. */
export interface PlanProgress {
	solved: number;
	total: number;
}

/** How a pivot differs from the plan it is offered from. */
export type PivotKind = "topic" | "list" | "harder" | "weakest";

/** Another plan offered after a solve. */
export interface Pivot {
	kind: PivotKind;
	plan: PlanView;
	next: NextProblem;
}

/** GET /api/next: a plan's next problem, its progress and, after a solve, the pivots. */
export interface NextPage {
	plan: PlanView;
	/** Null when the plan has no problem left to do. */
	next: NextProblem | null;
	progress: PlanProgress;
	pivots: Pivot[];
}

/** A practice plan the learner used (GET /api/plans): pinned, or recent. */
export interface SavedPlan {
	id: number;
	/** The learner's name; null shows the plan's label. */
	name: string | null;
	pinned: boolean;
	plan: PlanView;
	progress: PlanProgress;
	/** The first problem still to do; null when none is left. */
	next: NextProblem | null;
}
