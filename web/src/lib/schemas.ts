import type { SearchSchemaInput } from "@tanstack/react-router";
import { type CompanySearch, parseCompanySearch } from "@/lib/companies";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import {
	DIFFICULTIES,
	type Difficulty,
	PERIODS,
	type Period,
	PLAN_ORDERS,
	PLAN_STATUSES,
	type PlanOrder,
	type PlanStatus,
} from "@/lib/types";

/**
 * The URL is the single source of truth for every filter: each page parses its search params
 * here (the root route parses `company`, see lib/companies.ts), and leaves defaults out of the
 * URL with `stripSearchParams`.
 */

/** Longest search query kept; the rest is cut off. */
export const MAX_QUERY = 200;
/** Longest topic name kept; longer ones are not topics. */
const MAX_TOPIC = 100;

/** Filters over one problem list, shared by the study page and the problem table. */
export type ListFilters = {
	period: Period;
	/** A topic by name, such as "Dynamic Programming". */
	topic?: string;
	difficulty?: Difficulty;
};

/** Search params of the study page, which are also the query of GET /api/deck. */
// Types, not interfaces, so they fit the API client's query record.
export type StudySearch = ListFilters & {
	set: StudySet;
	/** Show this problem instead of the next one in the queue. */
	slug?: string;
};

/**
 * Search params of the problem table: the list's filters, which problems to show and in which
 * order (left out: every problem, in list order), and a search within it.
 */
export type ProblemsSearch = ListFilters & {
	/** Only these problems; left out, every one ("all" is never in the URL). */
	status?: Exclude<PlanStatus, "all">;
	/** Left out, list order ("rank"). */
	order?: Exclude<PlanOrder, "rank">;
	/** Free-text search: number, title, topic or statement. */
	q?: string;
};

/**
 * Search params of the code page: the practice plan whose next problem it offers after a
 * solve (with the root's `company`). Links from the study page and the problem table carry
 * the list the learner came from.
 */
export type PlanSearch = ListFilters & {
	status: PlanStatus;
	order: PlanOrder;
};

export const STUDY_DEFAULTS = { set: "smart", period: "6m" } as const;
export const PROBLEMS_DEFAULTS = { period: "6m" } as const;
export const PLAN_DEFAULTS = {
	period: "6m",
	status: "unsolved",
	order: "rank",
} as const;

const SET_KEYS = Object.keys(STUDY_SETS) as StudySet[];

function oneOf<T extends string>(
	values: readonly T[],
	value: unknown,
): T | undefined {
	return values.find((v) => v === value);
}

/**
 * Trimmed, non-empty text of at most `max` characters. The router reads `?q=42` as the number
 * 42, so finite numbers count as their text.
 */
function text(value: unknown, max = Number.POSITIVE_INFINITY) {
	const raw =
		typeof value === "number" && Number.isFinite(value) ? String(value) : value;
	if (typeof raw !== "string") return undefined;
	const trimmed = raw.trim().slice(0, max).trim();
	return trimmed || undefined;
}

/** Drops undefined keys, so the URL carries only what was chosen. */
function compact<T extends object>(parsed: T): T {
	for (const key of Object.keys(parsed) as (keyof T)[]) {
		if (parsed[key] === undefined) delete parsed[key];
	}
	return parsed;
}

function parseListFilters(raw: Record<string, unknown>): ListFilters {
	return {
		period: oneOf(PERIODS, raw.period) ?? STUDY_DEFAULTS.period,
		topic: text(raw.topic, MAX_TOPIC),
		difficulty: oneOf(DIFFICULTIES, raw.difficulty),
	};
}

/**
 * Parses the study page's search params: an invalid set or period falls back to the
 * default, any other invalid param is dropped. Links may leave out any of them.
 */
export function parseStudySearch(
	search: Partial<StudySearch> & SearchSchemaInput,
): StudySearch {
	// Typed for links; from the URL any value can be anything.
	const raw: Record<string, unknown> = search;
	return compact({
		set: oneOf(SET_KEYS, raw.set) ?? STUDY_DEFAULTS.set,
		...parseListFilters(raw),
		slug: text(raw.slug),
	});
}

const TABLE_STATUSES = PLAN_STATUSES.filter((s) => s !== "all");
const TABLE_ORDERS = PLAN_ORDERS.filter((o) => o !== "rank");

/** Parses the problem table's search params, like {@link parseStudySearch}. */
export function parseProblemsSearch(
	search: Partial<ProblemsSearch> & SearchSchemaInput,
): ProblemsSearch {
	const raw: Record<string, unknown> = search;
	return compact({
		...parseListFilters(raw),
		status: oneOf(TABLE_STATUSES, raw.status),
		order: oneOf(TABLE_ORDERS, raw.order),
		q: text(raw.q, MAX_QUERY),
	});
}

/** Parses the code page's plan, like {@link parseStudySearch}. */
export function parsePlanSearch(
	search: Partial<PlanSearch> & SearchSchemaInput,
): PlanSearch {
	const raw: Record<string, unknown> = search;
	return compact({
		...parseListFilters(raw),
		status: oneOf(PLAN_STATUSES, raw.status) ?? PLAN_DEFAULTS.status,
		order: oneOf(PLAN_ORDERS, raw.order) ?? PLAN_DEFAULTS.order,
	});
}

/*
 * The queries the page loaders send: only the validated filters (the router's search object
 * also keeps the URL's other and invalid params), in a fixed order, so the same filters give
 * the same URL. The server preloads these URLs when it serves the page (server/src/preload.rs;
 * lib/page-loads.json holds the cases both sides are tested against).
 */

/** GET /api/deck's query on the study page. */
export function deckQuery(search: object): StudySearch & CompanySearch {
	const raw = search as SearchSchemaInput;
	const { company } = parseCompanySearch(raw);
	const { set, period, topic, difficulty, slug } = parseStudySearch(raw);
	return { company, set, period, topic, difficulty, slug };
}

/** GET /api/problems's query on the problem table. */
export function problemsQuery(search: object): ProblemsSearch & CompanySearch {
	const raw = search as SearchSchemaInput;
	const { company } = parseCompanySearch(raw);
	const { period, topic, difficulty, status, order, q } =
		parseProblemsSearch(raw);
	return { company, period, topic, difficulty, status, order, q };
}

/** A plan as GET /api/next and PUT /api/plans take it. */
export function planQuery(search: object): PlanSearch & CompanySearch {
	const raw = search as SearchSchemaInput;
	const { company } = parseCompanySearch(raw);
	const { period, topic, difficulty, status, order } = parsePlanSearch(raw);
	return { company, period, topic, difficulty, status, order };
}
