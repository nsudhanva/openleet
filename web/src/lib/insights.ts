import { count } from "@/lib/format";
import type { ActiveDay, Activity, Failures } from "@/lib/types";

/** The failed verdicts, most telling first, with what the page calls them. */
export const FAILURE_KINDS: {
	key: keyof Failures;
	label: string;
	/** "2 wrong answers": the singular and the plural. */
	noun: [string, string];
}[] = [
	{
		key: "wrongAnswer",
		label: "Wrong answer",
		noun: ["wrong answer", "wrong answers"],
	},
	{
		key: "timeLimitExceeded",
		label: "Time limit",
		noun: ["time limit", "time limits"],
	},
	{
		key: "memoryLimitExceeded",
		label: "Memory limit",
		noun: ["memory limit", "memory limits"],
	},
	{
		key: "runtimeError",
		label: "Runtime error",
		noun: ["runtime error", "runtime errors"],
	},
	{
		key: "compileError",
		label: "Compile error",
		noun: ["compile error", "compile errors"],
	},
	{
		key: "outputLimitExceeded",
		label: "Output limit",
		noun: ["output limit", "output limits"],
	},
];

/** All the failures counted. */
export function failureTotal(failures: Failures): number {
	return FAILURE_KINDS.reduce((sum, kind) => sum + failures[kind.key], 0);
}

/** "2 wrong answers, 1 time limit": the failures there were, most telling first. */
export function failureSummary(failures: Failures): string {
	return FAILURE_KINDS.filter((kind) => failures[kind.key] > 0)
		.map((kind) => {
			const n = failures[kind.key];
			return `${n} ${kind.noun[n === 1 ? 0 : 1]}`;
		})
		.join(", ");
}

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = [
	"Jan",
	"Feb",
	"Mar",
	"Apr",
	"May",
	"Jun",
	"Jul",
	"Aug",
	"Sep",
	"Oct",
	"Nov",
	"Dec",
];
const DAY_MS = 86_400_000;

/** A "2026-11-10" day as UTC midnight milliseconds, so arithmetic ignores time zones. */
function dayMs(day: string): number {
	const [y, m, d] = day.split("-").map(Number);
	return Date.UTC(y, m - 1, d);
}

function dayKey(ms: number): string {
	return new Date(ms).toISOString().slice(0, 10);
}

/** "Tue 10 Nov 2026". Written out, not Intl: a formatter costs the first render. */
export function dayLabel(day: string): string {
	const date = new Date(dayMs(day));
	return `${WEEKDAYS[date.getUTCDay()]} ${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]} ${date.getUTCFullYear()}`;
}

/** The shades of the calendar, by the day's reviews and submissions together. */
export const ACTIVITY_LEVELS = [1, 3, 6, 10] as const;

/** 0 for no practice, then 1 to 4 at 1, 3, 6 and 10 or more. */
export function activityLevel(total: number): number {
	return ACTIVITY_LEVELS.filter((least) => total >= least).length;
}

/** One cell of the calendar. */
export interface CalendarDay extends ActiveDay {
	level: number;
	/** "Tue 10 Nov 2026: 3 reviews, 1 submission". */
	label: string;
}

/**
 * The calendar's weeks, Monday first, from `start` to `today` (the last week ends at today),
 * and the month each week starts, for its labels.
 */
export function calendarWeeks(activity: Activity): {
	weeks: CalendarDay[][];
	months: (string | null)[];
} {
	const byDay = new Map(activity.days.map((d) => [d.day, d]));
	const end = dayMs(activity.today);
	const weeks: CalendarDay[][] = [];
	const months: (string | null)[] = [];
	let lastMonth = -1;
	for (let week = dayMs(activity.start); week <= end; week += 7 * DAY_MS) {
		const days: CalendarDay[] = [];
		for (let at = week; at < week + 7 * DAY_MS && at <= end; at += DAY_MS) {
			const day = dayKey(at);
			const { reviews = 0, submissions = 0 } = byDay.get(day) ?? {};
			days.push({
				day,
				reviews,
				submissions,
				level: activityLevel(reviews + submissions),
				label: `${dayLabel(day)}: ${count(reviews, "review")}, ${count(submissions, "submission")}`,
			});
		}
		const month = new Date(week).getUTCMonth();
		months.push(month === lastMonth ? null : MONTHS[month]);
		lastMonth = month;
		weeks.push(days);
	}
	// A partial first month whose label would run into the next one's goes unlabeled.
	const next = months.findIndex((m, i) => i > 0 && m !== null);
	if (next > 0 && next < 3) months[0] = null;
	return { weeks, months };
}

/** The calendar in words: totals, active days and the busiest day. */
export function activitySummary(activity: Activity): string {
	const reviews = activity.days.reduce((sum, d) => sum + d.reviews, 0);
	const submissions = activity.days.reduce((sum, d) => sum + d.submissions, 0);
	if (!activity.days.length) return "No practice in the last 26 weeks yet.";
	const busiest = activity.days.reduce((best, d) =>
		d.reviews + d.submissions > best.reviews + best.submissions ? d : best,
	);
	return `${count(reviews, "review")} and ${count(submissions, "submission")} on ${count(activity.days.length, "day")} in the last 26 weeks. Busiest: ${dayLabel(busiest.day)}, with ${count(busiest.reviews, "review")} and ${count(busiest.submissions, "submission")}.`;
}

/** "10 Nov": a day as the trend's axis names it. */
export function shortDay(day: string): string {
	const date = new Date(dayMs(day));
	return `${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]}`;
}

/** First-try solves are a share only from this many solves; fewer show as counts. */
export const FIRST_TRY_MIN = 10;

/** "3 of 10", with "30%" once there are enough solves for a share to mean something. */
export function firstTryText(
	firstTry: number,
	solved: number,
): { value: string; detail?: string } {
	if (!solved) return { value: "—" };
	const value = `${firstTry} of ${solved}`;
	return solved < FIRST_TRY_MIN
		? { value }
		: { value, detail: `${Math.round((firstTry / solved) * 100)}%` };
}

/** A topic is rated on cards from this many graded cards with it (the server's rule). */
export const MIN_TOPIC_CARDS = 5;

/** The topic map leaves topics with fewer problems than this for "Show all". */
export const TOPIC_MIN_PROBLEMS = 3;
/** And lists at most this many until then. */
export const TOPICS_SHOWN = 10;

/** The topic map's rows: all of them, or the first few with enough problems to matter. */
export function shownTopics<T extends { problems: number }>(
	topics: T[],
	all: boolean,
): T[] {
	return all
		? topics
		: topics
				.filter((t) => t.problems >= TOPIC_MIN_PROBLEMS)
				.slice(0, TOPICS_SHOWN);
}

/** A trend chart's value axis: its range and its ticks, all whole percents. */
export interface TrendScale {
	lo: number;
	hi: number;
	ticks: number[];
}

/** Tick steps tried, smallest first, as shares. */
const TICK_STEPS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.25];
/** Most gaps between ticks. */
const MAX_TICK_GAPS = 4;

/**
 * The value axis for a readiness trend: the smallest even step that spans the values in at
 * most four gaps, from a multiple of it below the lowest value to one above the highest,
 * within 0 to 100%. A flat line still gets one step of range.
 */
export function trendScale(values: number[]): TrendScale {
	const min = Math.min(...values);
	const max = Math.max(...values);
	const step =
		TICK_STEPS.find(
			(s) =>
				Math.ceil(max / s - 1e-9) - Math.floor(min / s + 1e-9) <= MAX_TICK_GAPS,
		) ?? 0.25;
	let lo = Math.floor(min / step + 1e-9) * step;
	let hi = Math.ceil(max / step - 1e-9) * step;
	if (hi - lo < step / 2) {
		if (hi + step <= 1 + 1e-9) hi += step;
		else lo -= step;
	}
	const ticks: number[] = [];
	for (let t = lo; t <= hi + 1e-9; t += step)
		ticks.push(Math.round(t * 100) / 100);
	return { lo: ticks[0], hi: ticks.at(-1) ?? hi, ticks };
}

/** Days between two "2026-11-10" days. */
export function daysBetween(from: string, to: string): number {
	return Math.round((dayMs(to) - dayMs(from)) / DAY_MS);
}
