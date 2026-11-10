import {
	defaultParseSearch,
	type SearchSchemaInput,
} from "@tanstack/react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { parseCompanySearch } from "@/lib/companies";
import cases from "@/lib/page-loads.json";
import {
	deckQuery,
	parseProblemsSearch,
	parseStudySearch,
	problemsQuery,
} from "@/lib/schemas";

afterEach(() => {
	vi.unstubAllGlobals();
});

/**
 * The requests a page's route loaders make first, from its URL: the root loader's, then the
 * page's (see routes/). Search params are parsed as the router does: its JSON-aware parse,
 * then each route's validateSearch over the params so far.
 */
async function pageLoads(page: string): Promise<string[]> {
	const urls: string[] = [];
	vi.stubGlobal("fetch", async (url: string) => {
		urls.push(url);
		return new Response("{}");
	});
	// A fresh client: it caches the company list for the page load.
	vi.resetModules();
	const { api } = await import("@/lib/api");

	const { pathname, search } = new URL(page, "https://openleet.test");
	const raw = defaultParseSearch(search) as SearchSchemaInput;
	const root = { ...raw, ...parseCompanySearch(raw) };
	await Promise.all([api.readiness(root.company), api.companies()]);
	const code = pathname.match(/^\/code\/([^/]+)$/);
	if (pathname === "/") {
		await api.deck(deckQuery({ ...root, ...parseStudySearch(root) }));
	} else if (pathname === "/problems") {
		await Promise.all([
			api.problems(problemsQuery({ ...root, ...parseProblemsSearch(root) })),
			api.plans(),
		]);
	} else if (pathname === "/progress") {
		await api.report(root.company);
	} else if (code) {
		const slug = decodeURIComponent(code[1]);
		await Promise.all([
			api.problem(slug),
			api.code(slug),
			api.submissions(slug),
		]);
	}
	return urls;
}

describe("page loads", () => {
	// The server preloads exactly these URLs (server/src/preload.rs tests the same cases), so
	// a change here must change both sides.
	it.each(cases)("$page", async ({ page, fetches }) => {
		expect(await pageLoads(page)).toEqual(fetches);
	});
});
