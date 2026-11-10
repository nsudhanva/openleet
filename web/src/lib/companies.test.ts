import { describe, expect, it } from "vitest";
import {
	askedSummary,
	companyName,
	parseCompanySearch,
	rankCompanies,
} from "@/lib/companies";

const companies = [
	{ slug: "google", name: "Google", problems: 3 },
	{ slug: "meta", name: "Meta", problems: 2 },
	{ slug: "amazon", name: "Amazon", problems: 1 },
];
const parse = (search: Record<string, unknown>) =>
	parseCompanySearch(search as Parameters<typeof parseCompanySearch>[0]);

describe("companies", () => {
	it("reads the company from the URL, Google by default", () => {
		expect(parse({})).toEqual({ company: "google" });
		expect(parse({ company: "meta" })).toEqual({ company: "meta" });
		expect(parse({ company: "any" })).toEqual({ company: "any" });
		expect(parse({ company: "<script>" })).toEqual({ company: "google" });
		expect(parse({ company: 3 })).toEqual({ company: "google" });
	});

	it("names companies, and an unknown slug as itself", () => {
		expect(companyName(companies, "meta")).toBe("Meta");
		expect(companyName(companies, "any")).toBe("Any company");
		expect(companyName(companies, "acme")).toBe("acme");
	});

	it("ranks a problem's companies: selected, then this period by frequency, then all time", () => {
		const ranked = rankCompanies(
			{
				acme: { "6m": { rank: 9, frequency: 40 } },
				amazon: { "6m": { rank: 2, frequency: 90 } },
				google: { all: { rank: 50, frequency: 20 } },
				meta: { "6m": { rank: 30, frequency: 10 } },
			},
			companies,
			"meta",
			"6m",
		);
		expect(ranked.map((r) => r.slug)).toEqual([
			"meta",
			"amazon",
			"acme",
			"google",
		]);
		expect(ranked[3]).toMatchObject({
			name: "Google",
			statPeriod: "all",
			stat: { rank: 50, frequency: 20 },
		});
	});

	it("summarizes ranks and frequencies, newest period first", () => {
		expect(
			askedSummary("Meta", {
				all: { rank: 6, frequency: 92.9 },
				"6m": { rank: 1, frequency: 100 },
			}),
		).toBe(
			"Meta: #1 in 6 months (frequency 100), #6 all time (frequency 92.9)",
		);
	});
});
