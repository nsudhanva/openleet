import { notFound } from "@tanstack/react-router";
import type { CompanySearch } from "@/lib/companies";
import type { PlanSearch, ProblemsSearch, StudySearch } from "@/lib/schemas";
import type {
	AttemptInput,
	CodeInfo,
	Company,
	Difficulty,
	DraftVersions,
	NextPage,
	Period,
	ProblemRow,
	Readiness,
	Report,
	RunResult,
	SavedPlan,
	SearchHit,
	StudyCard,
	StudyDeck,
	Submission,
	SubmissionSummary,
	SubmitResult,
	TopicCount,
} from "@/lib/types";

/** A non-2xx answer from the API, carrying the server's `error` message. */
export class ApiError extends Error {
	constructor(
		readonly status: number,
		message: string,
	) {
		super(message);
		this.name = "ApiError";
	}
}

type Query = Record<string, string | number | boolean | undefined>;

interface Options {
	query?: Query;
	body?: unknown;
	signal?: AbortSignal;
	/** Lets the request finish after the page closes (draft saves). */
	keepalive?: boolean;
}

function urlOf(path: string, query: Query = {}): string {
	const params = new URLSearchParams();
	for (const [key, value] of Object.entries(query)) {
		if (value !== undefined) params.set(key, String(value));
	}
	const search = params.toString();
	return search ? `${path}?${search}` : path;
}

async function errorMessage(response: Response): Promise<string> {
	try {
		const body: unknown = await response.json();
		if (
			typeof body === "object" &&
			body !== null &&
			"error" in body &&
			typeof body.error === "string"
		)
			return body.error;
	} catch {
		// Not JSON (a proxy error page, for example): fall back to the status line.
	}
	return `${response.status} ${response.statusText}`.trim();
}

async function send(
	method: string,
	path: string,
	{ query, body, signal, keepalive }: Options = {},
): Promise<Response> {
	const response = await fetch(urlOf(path, query), {
		method,
		signal,
		keepalive,
		headers:
			body === undefined ? undefined : { "content-type": "application/json" },
		body: body === undefined ? undefined : JSON.stringify(body),
	});
	if (!response.ok)
		throw new ApiError(response.status, await errorMessage(response));
	return response;
}

/** A request whose answer is JSON of type T. */
async function json<T>(
	method: string,
	path: string,
	options?: Options,
): Promise<T> {
	return (await send(method, path, options)).json() as Promise<T>;
}

/** A request answered with 204 No Content. */
async function empty(
	method: string,
	path: string,
	options?: Options,
): Promise<void> {
	await send(method, path, options);
}

const problemPath = (base: string, slug: string) =>
	`${base}/${encodeURIComponent(slug)}`;

/** The company list is fixed for a build: fetched once per page load. */
let companies: Promise<Company[]> | undefined;

/** Topic counts depend only on the data and the list: fetched once per list and page load. */
const topicCounts = new Map<string, Promise<TopicCount[]>>();

/** The list GET /api/topics counts: its topics after the difficulty filter. */
export type TopicQuery = CompanySearch & {
	period: Period;
	difficulty?: Difficulty;
};

/** Typed client for the JSON API under /api (see the README's API table). */
export const api = {
	deck: (filter: StudySearch & CompanySearch, signal?: AbortSignal) =>
		json<StudyDeck>("GET", "/api/deck", { query: filter, signal }),
	/** Fetched once per page load; a failure gives an empty list and the next call retries. */
	companies: () => {
		companies ??= json<Company[]>("GET", "/api/companies").catch(
			(error: unknown) => {
				console.error("Could not load the companies", error);
				companies = undefined; // the next call retries
				return [];
			},
		);
		return companies;
	},
	recordAttempt: (attempt: AttemptInput) =>
		json<{ score: number | null }>("POST", "/api/attempts", { body: attempt }),
	/** Empty text deletes the note. */
	saveNote: (slug: string, text: string) =>
		json<{ note: string | null }>("PUT", "/api/notes", {
			body: { slug, text },
		}),
	clearProgress: (target: { slug: string } | { all: true }) =>
		empty("DELETE", "/api/progress", { query: target }),
	/** One list's problems that pass the filters, in its order (best match first with `q`). */
	problems: (list: CompanySearch & ProblemsSearch, signal?: AbortSignal) =>
		json<ProblemRow[]>("GET", "/api/problems", { query: list, signal }),
	/**
	 * The list's topics with their counts, most first. Shared and cached per list for the page
	 * load (callers drop answers they no longer need); a failure is not cached.
	 */
	topics: ({ company, period, difficulty }: TopicQuery) => {
		const query = { company, period, difficulty };
		const key = urlOf("", query);
		let request = topicCounts.get(key);
		if (!request) {
			request = json<TopicCount[]>("GET", "/api/topics", { query });
			topicCounts.set(key, request);
			request.catch(() => topicCounts.delete(key));
		}
		return request;
	},
	problem: (slug: string) =>
		json<StudyCard>("GET", problemPath("/api/problems", slug)),
	search: (q: string, limit: number, signal?: AbortSignal) =>
		json<SearchHit[]>("GET", "/api/search", { query: { q, limit }, signal }),
	/** The progress page: each figure says which list it covers. */
	report: (company: string) =>
		json<Report>("GET", "/api/report", { query: { company } }),
	readiness: (company: string) =>
		json<Readiness>("GET", "/api/readiness", { query: { company } }),

	code: (slug: string) => json<CodeInfo>("GET", problemPath("/api/code", slug)),
	/** Empty code deletes the draft. */
	saveDraft: (slug: string, code: string, keepalive = false) =>
		empty("PUT", "/api/drafts", { body: { slug, code }, keepalive }),
	/** Back to the starter; `code` (the editor's, '' for the starter) becomes the previous version. */
	resetDraft: (slug: string, code: string) =>
		json<DraftVersions>("POST", "/api/drafts/reset", { body: { slug, code } }),
	/** Brings the previous version back; `code` becomes the previous one, so it swaps. */
	restoreDraft: (slug: string, code: string) =>
		json<DraftVersions>("POST", "/api/drafts/restore", {
			body: { slug, code },
		}),
	/** Runs the examples, or `input` (one JSON value per line, per parameter) when given. */
	run: (slug: string, code: string, input?: string) =>
		json<RunResult>("POST", "/api/run", { body: { slug, code, input } }),
	submit: (slug: string, code: string) =>
		json<SubmitResult>("POST", "/api/submit", { body: { slug, code } }),
	submissions: (slug: string) =>
		json<SubmissionSummary[]>("GET", "/api/submissions", { query: { slug } }),
	submission: (id: number) => json<Submission>("GET", `/api/submissions/${id}`),

	/** The plan's next problem after `slug` (from the start without one), and the pivots. */
	next: (
		plan: CompanySearch & PlanSearch,
		slug?: string,
		signal?: AbortSignal,
	) => json<NextPage>("GET", "/api/next", { query: { ...plan, slug }, signal }),
	/** Pinned plans, then the recent ones. */
	plans: (signal?: AbortSignal) =>
		json<SavedPlan[]>("GET", "/api/plans", { signal }),
	/** Remembers that the plan was used (the same plan keeps its row). */
	rememberPlan: (plan: CompanySearch & PlanSearch) =>
		json<SavedPlan>("PUT", "/api/plans", { body: plan }),
	/** `name: null` drops the name, so the plan shows its label. */
	editPlan: (id: number, change: { name?: string | null; pinned?: boolean }) =>
		json<SavedPlan>("PATCH", `/api/plans/${id}`, { body: change }),
	deletePlan: (id: number) => empty("DELETE", `/api/plans/${id}`),
};

/** For route loaders: an unknown problem (404) shows the not-found page. */
export async function orNotFound<T>(request: Promise<T>): Promise<T> {
	try {
		return await request;
	} catch (error) {
		if (error instanceof ApiError && error.status === 404) throw notFound();
		throw error;
	}
}

/** A message for the user from anything a request can throw. */
export function messageOf(error: unknown): string {
	return error instanceof Error ? error.message : String(error);
}
