import { isNotFound } from "@tanstack/react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, api, orNotFound } from "@/lib/api";

function answer(status: number, body?: unknown, statusText = "") {
	const fetch = vi.fn(
		async (_url: string, _init?: RequestInit) =>
			new Response(body === undefined ? null : JSON.stringify(body), {
				status,
				statusText,
			}),
	);
	vi.stubGlobal("fetch", fetch);
	return fetch;
}

afterEach(() => {
	vi.unstubAllGlobals();
});

describe("api client", () => {
	it("sends the query, skipping unset filters, and parses JSON", async () => {
		const fetch = answer(200, { card: null, remaining: 0, topics: [] });
		const deck = await api.deck({ set: "again", period: "lc1000" });
		expect(deck.remaining).toBe(0);
		expect(fetch.mock.calls[0][0]).toBe("/api/deck?set=again&period=lc1000");
	});

	it("sends JSON bodies and accepts 204 No Content", async () => {
		const fetch = answer(204);
		await expect(api.saveDraft("two-sum", "pass")).resolves.toBeUndefined();
		const [url, init] = fetch.mock.calls[0];
		expect(url).toBe("/api/drafts");
		expect(init).toMatchObject({
			method: "PUT",
			headers: { "content-type": "application/json" },
			body: JSON.stringify({ slug: "two-sum", code: "pass" }),
		});
	});

	it("throws the server's error message with the status", async () => {
		answer(503, { error: "The judge is busy" });
		const error = await api.run("two-sum", "pass").catch((e: unknown) => e);
		expect(error).toBeInstanceOf(ApiError);
		expect(error).toMatchObject({ status: 503, message: "The judge is busy" });
	});

	it("falls back to the status line when the body is not JSON", async () => {
		vi.stubGlobal(
			"fetch",
			vi.fn(
				async () =>
					new Response("<h1>Bad gateway</h1>", {
						status: 502,
						statusText: "Bad Gateway",
					}),
			),
		);
		await expect(api.problems()).rejects.toThrow("502 Bad Gateway");
	});

	it("turns a 404 into the router's not-found in loaders", async () => {
		answer(404, { error: "Unknown problem: nope" });
		const error = await orNotFound(api.problem("nope")).catch(
			(e: unknown) => e,
		);
		expect(isNotFound(error)).toBe(true);
		answer(500, { error: "boom" });
		await expect(orNotFound(api.problem("x"))).rejects.toThrow("boom");
	});

	it("encodes slugs and clears everything with all=true", async () => {
		const fetch = answer(204);
		await api.clearProgress({ all: true });
		expect(fetch.mock.calls[0][0]).toBe("/api/progress?all=true");
		answer(200, {});
		await api.code("a/b");
		expect(vi.mocked(globalThis.fetch).mock.calls[0][0]).toBe(
			"/api/code/a%2Fb",
		);
	});
});
