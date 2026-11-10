import { describe, expect, it } from "vitest";
import {
	type Plan,
	pivotText,
	planChipLabel,
	planOf,
	progressShare,
	progressText,
	tablePlan,
} from "@/lib/plan";
import {
	parsePlanSearch,
	parseProblemsSearch,
	planQuery,
	problemsQuery,
} from "@/lib/schemas";
import type { PlanView } from "@/lib/types";

const names: Record<string, string> = { google: "Google", meta: "Meta" };
const companyName = (slug: string) => names[slug] ?? slug;

describe("plan search params", () => {
	it("default to the unsolved problems of the list in rank order", () => {
		expect(parsePlanSearch({} as never)).toEqual({
			period: "6m",
			status: "unsolved",
			order: "rank",
		});
		expect(planQuery({})).toEqual({
			company: "google",
			period: "6m",
			topic: undefined,
			difficulty: undefined,
			status: "unsolved",
			order: "rank",
		});
	});

	it("keep valid values and drop the rest, like the other filters", () => {
		expect(
			parsePlanSearch({
				period: "lc1000",
				topic: "  Trie ",
				difficulty: "Hard",
				status: "all",
				order: "easy-first",
			} as never),
		).toEqual({
			period: "lc1000",
			topic: "Trie",
			difficulty: "Hard",
			status: "all",
			order: "easy-first",
		});
		expect(
			parsePlanSearch({
				status: "solved",
				order: 3,
				difficulty: "hard",
			} as never),
		).toEqual({ period: "6m", status: "unsolved", order: "rank" });
		// Extra params (the study page's set, a search) are not part of a plan.
		expect(
			planQuery({ company: "meta", set: "due", q: "x", order: "random" }),
		).toEqual({
			company: "meta",
			period: "6m",
			topic: undefined,
			difficulty: undefined,
			status: "unsolved",
			order: "random",
		});
	});

	it("leave the problem table's defaults out of its query", () => {
		// The table shows every problem in list order unless a status or order is chosen.
		expect(
			parseProblemsSearch({ status: "all", order: "rank" } as never),
		).toEqual({ period: "6m" });
		const query = problemsQuery({ status: "untried", order: "number" });
		expect([query.status, query.order]).toEqual(["untried", "number"]);
	});

	it("turn the table's filters into its plan", () => {
		expect(
			tablePlan({ company: "meta", period: "3m", topic: "Graph" }),
		).toEqual({
			company: "meta",
			period: "3m",
			topic: "Graph",
			difficulty: undefined,
			status: "unsolved",
			order: "rank",
		});
		expect(
			tablePlan({
				company: "any",
				period: "6m",
				status: "untried",
				order: "random",
			}),
		).toMatchObject({ status: "untried", order: "random" });
	});
});

const plan: Plan = {
	company: "google",
	period: "6m",
	status: "unsolved",
	order: "rank",
};

describe("plan labels", () => {
	it("name the plan in a few words, defaults left out", () => {
		expect(planChipLabel(plan, companyName)).toBe("Google · 6m · Unsolved");
		expect(
			planChipLabel(
				{
					...plan,
					company: "meta",
					period: "all",
					topic: "Two Pointers",
					difficulty: "Medium",
					status: "all",
					order: "random",
				},
				companyName,
			),
		).toBe("Meta · All time · Two Pointers · Medium · All problems · Shuffled");
		// LC 1–1000 is the same list for every company.
		expect(planChipLabel({ ...plan, period: "lc1000" }, companyName)).toBe(
			"LC 1–1000 · Unsolved",
		);
	});

	it("rebuild a plan the server sent", () => {
		const view: PlanView = {
			company: "meta",
			period: "3m",
			topic: null,
			difficulty: "Hard",
			status: "untried",
			order: "number",
			label: "Meta · 3 months · Hard · Untried · By number",
		};
		expect(planOf(view)).toEqual({
			company: "meta",
			period: "3m",
			topic: undefined,
			difficulty: "Hard",
			status: "untried",
			order: "number",
		});
	});
});

describe("the next panel's text", () => {
	it("says how much of the plan is solved", () => {
		expect(progressText({ solved: 12, total: 48 })).toBe("12 of 48 solved");
		expect(progressText({ solved: 48, total: 48 })).toBe("All 48 solved");
		expect(progressText({ solved: 0, total: 0 })).toBe("0 of 0 solved");
		expect(progressShare({ solved: 12, total: 48 })).toBe(0.25);
		expect(progressShare({ solved: 0, total: 0 })).toBe(0);
	});

	it("names what each pivot changes, never the next problem's topics", () => {
		const view = (
			topic: string | null,
			difficulty: PlanView["difficulty"],
		) => ({
			...planOf({ ...plan, topic, difficulty, label: "" } as PlanView),
			topic,
			difficulty,
			label: "",
		});
		expect(pivotText({ kind: "topic", plan: view("Hash Table", null) })).toBe(
			"Topic: Hash Table",
		);
		expect(pivotText({ kind: "list", plan: view(null, null) })).toBe(
			"Whole list",
		);
		expect(pivotText({ kind: "harder", plan: view(null, "Medium") })).toBe(
			"Harder: Medium",
		);
		expect(pivotText({ kind: "weakest", plan: view("Graph", null) })).toBe(
			"Weakest: Graph",
		);
	});
});
