import type { CompanySearch } from "@/lib/companies";
import {
	PLAN_DEFAULTS,
	type PlanSearch,
	type ProblemsSearch,
} from "@/lib/schemas";
import type {
	Period,
	Pivot,
	PlanOrder,
	PlanProgress,
	PlanStatus,
	PlanView,
} from "@/lib/types";

/** What each status keeps, as the plan controls name it. */
export const STATUS_LABEL: Record<PlanStatus, string> = {
	unsolved: "Unsolved",
	untried: "Untried",
	all: "All problems",
};

export const ORDER_LABEL: Record<PlanOrder, string> = {
	rank: "By rank",
	number: "By number",
	"easy-first": "Easy first",
	random: "Shuffled",
};

/** Periods as short as a chip needs them. */
const PERIOD_SHORT: Record<Period, string> = {
	"30d": "30d",
	"3m": "3m",
	"6m": "6m",
	all: "All time",
	lc1000: "LC 1–1000",
};

/** A plan as one value: the code page's search params with the root's company. */
export type Plan = CompanySearch & PlanSearch;

/**
 * "Google · 6m · Two Pointers · Unsolved": the plan chip's label, defaults (rank order, any
 * difficulty) left out. `companyName` names a company slug.
 */
export function planChipLabel(
	plan: Plan,
	companyName: (slug: string) => string,
): string {
	return [
		plan.period === "lc1000" ? undefined : companyName(plan.company),
		PERIOD_SHORT[plan.period],
		plan.topic,
		plan.difficulty,
		STATUS_LABEL[plan.status],
		plan.order === PLAN_DEFAULTS.order ? undefined : ORDER_LABEL[plan.order],
	]
		.filter(Boolean)
		.join(" · ");
}

/** The search params that rebuild a plan the server sent, for a link. */
export function planOf(view: PlanView): Plan {
	return {
		company: view.company,
		period: view.period,
		topic: view.topic ?? undefined,
		difficulty: view.difficulty ?? undefined,
		status: view.status,
		order: view.order,
	};
}

/**
 * The plan of the problem table's filters: its status when one is chosen (the table's "all"
 * is the plan's default, unsolved) and its order.
 */
export function tablePlan(search: CompanySearch & ProblemsSearch): Plan {
	return {
		company: search.company,
		period: search.period,
		topic: search.topic,
		difficulty: search.difficulty,
		status: search.status ?? PLAN_DEFAULTS.status,
		order: search.order ?? PLAN_DEFAULTS.order,
	};
}

/** "12 of 48 solved", or "All 48 solved" when nothing is left. */
export function progressText({ solved, total }: PlanProgress): string {
	if (total > 0 && solved >= total) return `All ${total} solved`;
	return `${solved} of ${total} solved`;
}

/** Solved as a share of the plan, 0 to 1 (0 for an empty plan). */
export function progressShare({ solved, total }: PlanProgress): number {
	return total > 0 ? Math.min(1, solved / total) : 0;
}

/**
 * A pivot's button text: what changes ("Topic: Hash Table", "Whole list", "Harder: Medium",
 * "Weakest: Graph Theory"). Only the solved problem's topics and the learner's own weakest
 * topic are named, never the next problem's.
 */
export function pivotText({
	kind,
	plan,
}: Pick<Pivot, "kind" | "plan">): string {
	switch (kind) {
		case "topic":
			return `Topic: ${plan.topic}`;
		case "list":
			return "Whole list";
		case "harder":
			return `Harder: ${plan.difficulty}`;
		case "weakest":
			return `Weakest: ${plan.topic}`;
	}
}
