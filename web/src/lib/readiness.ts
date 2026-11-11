import { percent } from "@/lib/format";
import type { Readiness } from "@/lib/types";

/**
 * What readiness covers, in words: "Ready for Google's 100 most-asked (6 months)", or, when
 * the 6-month list is too short, "Ready for Stripe's 12 most-asked (all time; 1 in 6 months)".
 * `owner` is the company's name, or null for any company.
 */
export function readinessLabel(owner: string | null, r: Readiness): string {
	const whose = owner === null ? "all companies'" : `${owner}'s`;
	if (!r.problems) return `${owner ?? "No company"} lists no problems yet`;
	const period =
		r.period === "6m" ? "6 months" : `all time; ${r.recent} in 6 months`;
	return `Ready for ${whose} ${r.problems} most-asked (${period})`;
}

/** The score as a whole percent, or "—" before there is anything to score. */
export function readinessText(r: Pick<Readiness, "score">): string {
	return r.score === null ? "—" : percent(r.score);
}
