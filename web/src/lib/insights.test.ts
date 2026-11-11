import { describe, expect, it } from "vitest";
import {
	activityLevel,
	activitySummary,
	calendarWeeks,
	dayLabel,
	daysBetween,
	failureSummary,
	failureTotal,
	firstTryText,
	shortDay,
	shownTopics,
	trendScale,
} from "@/lib/insights";
import type { Activity, Failures } from "@/lib/types";

const none: Failures = {
	wrongAnswer: 0,
	timeLimitExceeded: 0,
	memoryLimitExceeded: 0,
	runtimeError: 0,
	compileError: 0,
	outputLimitExceeded: 0,
};

describe("failures", () => {
	it("sum and say what failed, most telling first", () => {
		const failures = { ...none, wrongAnswer: 2, timeLimitExceeded: 1 };
		expect(failureTotal(failures)).toBe(3);
		expect(failureSummary(failures)).toBe("2 wrong answers, 1 time limit");
		expect(failureSummary({ ...none, runtimeError: 1 })).toBe(
			"1 runtime error",
		);
		expect(failureSummary(none)).toBe("");
	});
});

describe("the activity calendar", () => {
	// 2026-11-10 is a Tuesday; 26 weeks back from its week's Monday (9 Nov).
	const activity: Activity = {
		start: "2026-05-18",
		today: "2026-11-10",
		days: [
			{ day: "2026-05-18", reviews: 1, submissions: 0 },
			{ day: "2026-11-10", reviews: 3, submissions: 7 },
		],
	};

	it("lays out 26 weeks of days, Monday first, ending today", () => {
		const { weeks, months } = calendarWeeks(activity);
		expect(weeks).toHaveLength(26);
		expect(weeks[0]).toHaveLength(7);
		expect(weeks.at(-1)?.map((d) => d.day)).toEqual([
			"2026-11-09",
			"2026-11-10",
		]);
		expect(weeks[0][0]).toMatchObject({ day: "2026-05-18", level: 1 });
		expect(weeks.at(-1)?.[1]).toMatchObject({
			reviews: 3,
			submissions: 7,
			level: 4,
		});
		expect(weeks.at(-1)?.[1].label).toBe(
			"Tue 10 Nov 2026: 3 reviews, 7 submissions",
		);
		// A month label where a month's first week starts, none in between; May's two weeks
		// leave no room for its label before June's.
		expect(months[0]).toBeNull();
		expect(months[2]).toBe("Jun");
		expect(months.filter(Boolean)).toEqual([
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
		]);
	});

	it("shades by the day's total and says it in words", () => {
		expect([0, 1, 2, 3, 5, 6, 9, 10, 40].map(activityLevel)).toEqual([
			0, 1, 1, 2, 2, 3, 3, 4, 4,
		]);
		expect(activitySummary(activity)).toBe(
			"4 reviews and 7 submissions on 2 days in the last 26 weeks. Busiest: Tue 10 Nov 2026, with 3 reviews and 7 submissions.",
		);
		expect(activitySummary({ ...activity, days: [] })).toBe(
			"No practice in the last 26 weeks yet.",
		);
		expect(dayLabel("2026-03-01")).toBe("Sun 1 Mar 2026");
	});
});

describe("first-try solves", () => {
	it("are counts until ten solves, then also a share", () => {
		expect(firstTryText(0, 0)).toEqual({ value: "—" });
		// 1 of 1 is no 100%.
		expect(firstTryText(1, 1)).toEqual({ value: "1 of 1" });
		expect(firstTryText(3, 9)).toEqual({ value: "3 of 9" });
		expect(firstTryText(3, 10)).toEqual({ value: "3 of 10", detail: "30%" });
	});
});

describe("the topic map", () => {
	const topic = (problems: number) => ({ topic: `t${problems}`, problems });

	it("leaves topics with fewer than three problems for Show all", () => {
		const topics = [5, 4, 3, 2, 1].map(topic);
		expect(shownTopics(topics, false).map((t) => t.problems)).toEqual([
			5, 4, 3,
		]);
		expect(shownTopics(topics, true)).toEqual(topics);
		// A tiny list may have none to show until Show all.
		expect(shownTopics([topic(1)], false)).toEqual([]);
	});

	it("shows at most ten until Show all", () => {
		const topics = Array.from({ length: 14 }, () => topic(9));
		expect(shownTopics(topics, false)).toHaveLength(10);
	});
});

describe("the trend's axes", () => {
	it("scale to the values in even steps of whole percents", () => {
		// Steps of 1, 2 or 5 points would need more than four gaps from 12% to 31%.
		expect(trendScale([0.12, 0.31])).toEqual({
			lo: 0.1,
			hi: 0.4,
			ticks: [0.1, 0.2, 0.3, 0.4],
		});
		expect(trendScale([0.421, 0.437])).toEqual({
			lo: 0.42,
			hi: 0.44,
			ticks: [0.42, 0.43, 0.44],
		});
		// The full range takes the widest step.
		expect(trendScale([0, 1]).ticks).toEqual([0, 0.25, 0.5, 0.75, 1]);
	});

	it("give a flat line a step of range, inside 0 to 100%", () => {
		expect(trendScale([0.3, 0.3])).toEqual({
			lo: 0.3,
			hi: 0.31,
			ticks: [0.3, 0.31],
		});
		expect(trendScale([0, 0]).ticks).toEqual([0, 0.01]);
		expect(trendScale([1, 1]).ticks).toEqual([0.99, 1]);
	});

	it("name days and count between them across months", () => {
		expect(shortDay("2026-11-10")).toBe("10 Nov");
		expect(daysBetween("2026-10-30", "2026-11-02")).toBe(3);
		expect(daysBetween("2026-03-07", "2026-03-09")).toBe(2);
	});
});
