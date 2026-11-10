import { describe, expect, it } from "vitest";
import {
	activityLevel,
	activitySummary,
	calendarWeeks,
	dayLabel,
	failureSummary,
	failureTotal,
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
			"4 reviews and 7 submissions on 2 days in the last 26 weeks. Busiest: Tue 10 Nov 2026 (10).",
		);
		expect(activitySummary({ ...activity, days: [] })).toBe(
			"No practice in the last 26 weeks yet.",
		);
		expect(dayLabel("2026-03-01")).toBe("Sun 1 Mar 2026");
	});
});
