import {
	type Asked,
	isAskedPeriod,
	type Period,
	type Problem,
} from "@/lib/types";

type Listed = Pick<Problem, "id" | "asked" | "premium">;

/** The highest LeetCode number in the classic list. */
const LC_MAX = 1000;

/**
 * The problems in one list, in its order: Google's periods by rank, LC 1–1000 (free
 * problems only) by LeetCode number.
 */
export function inList<T extends Listed>(rows: T[], period: Period): T[] {
	if (!isAskedPeriod(period))
		return rows
			.filter((r) => r.id <= LC_MAX && !r.premium)
			.sort((a, b) => a.id - b.id);
	return rows
		.filter((r) => r.asked[period])
		.sort(
			(a, b) => (a.asked[period]?.rank ?? 0) - (b.asked[period]?.rank ?? 0),
		);
}

/**
 * Google's rank and frequency to show for a row: the period's own, or the 6-month one in
 * LC 1–1000. Undefined for a classic problem Google did not ask.
 */
export function askedIn(row: Listed, period: Period): Asked | undefined {
	return row.asked[isAskedPeriod(period) ? period : "6m"];
}
