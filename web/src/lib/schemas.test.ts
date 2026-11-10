import { describe, expect, it } from "vitest";
import {
	MAX_QUERY,
	parseProblemsSearch,
	parseStudySearch,
} from "@/lib/schemas";

/** Search params straight from a URL, which can hold anything. */
const study = (search: Record<string, unknown>) =>
	parseStudySearch(search as Parameters<typeof parseStudySearch>[0]);
const problems = (search: Record<string, unknown>) =>
	parseProblemsSearch(search as Parameters<typeof parseProblemsSearch>[0]);

describe("parseStudySearch", () => {
	it("fills in the default set and period", () => {
		expect(study({})).toEqual({ set: "smart", period: "6m" });
	});

	it("keeps valid params", () => {
		const search = {
			set: "all",
			period: "lc1000",
			topic: "Graph Theory",
			difficulty: "Hard",
			slug: "two-sum",
		} as const;
		expect(study(search)).toEqual(search);
	});

	it("falls back or drops invalid params", () => {
		expect(
			study({
				set: "nope",
				period: 3,
				topic: 7,
				difficulty: "Impossible",
				slug: null,
			}),
		).toEqual({ set: "smart", period: "6m", topic: "7" });
	});

	it("drops blank and overlong topics, and trims the rest", () => {
		expect(study({ topic: "   " })).toEqual({ set: "smart", period: "6m" });
		expect(study({ topic: "  Tree " }).topic).toBe("Tree");
		expect(study({ topic: "x".repeat(150) }).topic).toHaveLength(100);
		expect(study({ topic: ["Tree"] }).topic).toBeUndefined();
	});
});

describe("parseProblemsSearch", () => {
	it("defaults the period and leaves every filter out", () => {
		expect(problems({})).toEqual({ period: "6m" });
	});

	it("keeps the list's filters and the search", () => {
		const search = {
			period: "all",
			topic: "Dynamic Programming",
			difficulty: "Medium",
			q: "two sum",
		} as const;
		expect(problems(search)).toEqual(search);
	});

	it("reads a numeric query as its text, and drops blank or invalid ones", () => {
		expect(problems({ q: 42 })).toEqual({ period: "6m", q: "42" });
		expect(problems({ q: "  " })).toEqual({ period: "6m" });
		expect(problems({ q: Number.NaN })).toEqual({ period: "6m" });
		expect(problems({ q: { a: 1 } })).toEqual({ period: "6m" });
	});

	it("caps the query and ignores study-only params", () => {
		expect(problems({ q: "a".repeat(500) }).q).toHaveLength(MAX_QUERY);
		expect(
			problems({ set: "due", slug: "two-sum", difficulty: "Easy" }),
		).toEqual({ period: "6m", difficulty: "Easy" });
	});
});
