import { describe, expect, it } from "vitest";
import { parseStudySearch } from "@/lib/schemas";

/** Search params straight from a URL, which can hold anything. */
const parse = (search: Record<string, unknown>) =>
	parseStudySearch(search as Parameters<typeof parseStudySearch>[0]);

describe("parseStudySearch", () => {
	it("fills in the default set and period", () => {
		expect(parse({})).toEqual({ set: "smart", period: "6m" });
	});

	it("keeps valid params", () => {
		const search = {
			set: "all",
			period: "lc1000",
			topic: "Graph Theory",
			difficulty: "Hard",
			slug: "two-sum",
		} as const;
		expect(parse(search)).toEqual(search);
	});

	it("falls back or drops invalid params", () => {
		expect(
			parse({
				set: "nope",
				period: 3,
				topic: 7,
				difficulty: "Impossible",
				slug: null,
			}),
		).toEqual({ set: "smart", period: "6m" });
	});
});
