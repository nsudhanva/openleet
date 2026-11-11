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
	return `${count(reviews, "review")} and ${count(submissions, "submission")} on ${count(activity.days.length, "day")} in the last 26 weeks. Busiest: ${dayLabel(busiest.day)} (${busiest.reviews + busiest.submissions}).`;
}
