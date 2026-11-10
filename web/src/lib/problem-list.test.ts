import { describe, expect, it } from "vitest";
import { askedIn, inList } from "@/lib/problem-list";

const rows = [
	{ id: 42, premium: false, asked: { "6m": { rank: 2, frequency: 50 } } },
	{
		id: 1,
		premium: false,
		asked: {
			"30d": { rank: 1, frequency: 90 },
			"6m": { rank: 1, frequency: 80 },
		},
	},
	{ id: 7, premium: false, asked: {} },
	{ id: 9, premium: true, asked: {} },
	{ id: 2001, premium: false, asked: { "6m": { rank: 3, frequency: 10 } } },
];
const ids = (list: { id: number }[]) => list.map((r) => r.id);

describe("problem lists", () => {
	it("keeps Google's periods in rank order", () => {
		expect(ids(inList(rows, "6m"))).toEqual([1, 42, 2001]);
		expect(ids(inList(rows, "30d"))).toEqual([1]);
	});

	it("lists free problems 1 to 1000 by number, asked by Google or not", () => {
		expect(ids(inList(rows, "lc1000"))).toEqual([1, 7, 42]);
	});

	it("shows the 6-month rank in LC 1–1000 and nothing for a classic problem", () => {
		expect(askedIn(rows[0], "lc1000")?.rank).toBe(2);
		expect(askedIn(rows[0], "30d")).toBeUndefined();
		expect(askedIn(rows[2], "lc1000")).toBeUndefined();
	});
});
