import type { SearchSchemaInput } from "@tanstack/react-router";
import {
	ASKED_PERIODS,
	type Asked,
	type AskedPeriod,
	type Company,
	type CompanyAsked,
	PERIOD_LABEL,
} from "@/lib/types";

/** The list every page starts on; the URL leaves `company` out for it. */
export const DEFAULT_COMPANY = "google";
/** Problems any listed company asked; ranked by the best frequency of any of them. */
export const ANY_COMPANY = "any";

/** The `company` search param, shared by every page (the root route keeps it). */
export type CompanySearch = { company: string };

const SLUG = /^[a-z0-9-]+$/;

/** A company slug from the URL; anything else means the default company. */
export function parseCompanySearch(
	search: Partial<CompanySearch> & SearchSchemaInput,
): CompanySearch {
	const company: unknown = search.company;
	return {
		company:
			typeof company === "string" && SLUG.test(company)
				? company
				: DEFAULT_COMPANY,
	};
}

/** The company's display name; an unknown slug shows as itself. */
export function companyName(companies: Company[], slug: string): string {
	if (slug === ANY_COMPANY) return "Any company";
	return companies.find((c) => c.slug === slug)?.name ?? slug;
}

/** "Meta: #1 in 6 months (frequency 100), #6 all time (frequency 92.9)". */
export function askedSummary(name: string, asked: CompanyAsked): string {
	const parts = ASKED_PERIODS.flatMap((period) => {
		const stat = asked[period];
		return stat
			? [`${rankLabel(stat.rank, period)} (frequency ${stat.frequency})`]
			: [];
	});
	return `${name}: ${parts.join(", ")}`;
}

/** "#3 in 6 months", "#12 all time". */
function rankLabel(rank: number, period: AskedPeriod): string {
	return period === "all"
		? `#${rank} all time`
		: `#${rank} in ${PERIOD_LABEL[period]}`;
}

/** One company that asked a problem, as the card's tags and table show it. */
export interface CompanyRanking {
	slug: string;
	name: string;
	asked: CompanyAsked;
	/** Its rank and frequency in the chosen period, else all time; null if it has neither. */
	stat: Asked | null;
	/** The period `stat` is for. */
	statPeriod: AskedPeriod;
}

/**
 * The companies that asked a problem, most relevant first: the selected one, then those
 * that asked it in `period` by frequency, then the rest by all-time frequency; ties keep
 * picker order. Slugs the picker does not know sort last among equals.
 */
export function rankCompanies(
	asked: Record<string, CompanyAsked>,
	companies: Company[],
	selected: string,
	period: AskedPeriod,
): CompanyRanking[] {
	const order = (slug: string) => {
		const i = companies.findIndex((c) => c.slug === slug);
		return i === -1 ? companies.length : i;
	};
	const rows = Object.entries(asked).map(([slug, stats]) => {
		const statPeriod: AskedPeriod = stats[period] ? period : "all";
		return {
			slug,
			name: companyName(companies, slug),
			asked: stats,
			stat: stats[statPeriod] ?? null,
			statPeriod,
		};
	});
	// Selected first, then this period's lists, then all time; frequency within each.
	const tier = (row: CompanyRanking) =>
		row.slug === selected ? 0 : row.statPeriod === period ? 1 : 2;
	return rows.sort(
		(a, b) =>
			tier(a) - tier(b) ||
			(b.stat?.frequency ?? 0) - (a.stat?.frequency ?? 0) ||
			order(a.slug) - order(b.slug),
	);
}
