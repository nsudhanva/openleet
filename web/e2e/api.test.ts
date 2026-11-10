import { describe, expect, inject, it } from "vitest";

const base = inject("baseUrl");

async function api(path: string, init?: RequestInit) {
	const response = await fetch(`${base}${path}`, init);
	const text = await response.text();
	return { status: response.status, body: text ? JSON.parse(text) : null };
}

function send(method: string, path: string, body: unknown) {
	return api(path, {
		method,
		headers: { "content-type": "application/json" },
		body: JSON.stringify(body),
	});
}

// One shared database: the tests run in order and build on each other.
describe("HTTP API, end to end", () => {
	it("searches by number, title and statement, and rejects a missing query", async () => {
		expect((await api("/api/search?q=lc%2042")).body[0].slug).toBe(
			"trapping-rain-water",
		);
		expect((await api("/api/search?q=two%20sum")).body[0].slug).toBe("two-sum");
		const statement = await api("/api/search?q=prerequisites&limit=5");
		expect(statement.body.map((h: { slug: string }) => h.slug)).toContain(
			"course-schedule",
		);
		expect((await api("/api/search")).status).toBe(400);
	});

	it("lists every problem without topics, and serves one full card", async () => {
		const list = await api("/api/problems");
		// 793 Google problems, then the free LeetCode 1–1000 problems Google did not ask.
		expect(list.body).toHaveLength(1175);
		expect(list.body.at(-1).asked).toEqual({});
		expect(list.body[0]).not.toHaveProperty("topics");

		const card = await api("/api/problems/two-sum");
		expect(card.body.problem.topics).toEqual(["Array", "Hash Table"]);
		expect(card.body.approach.hints.length).toBeGreaterThan(0);
		expect(card.body.state).toBeNull();
		expect((await api("/api/problems/not-a-problem")).status).toBe(404);
	});

	it("deals the most frequent new card first, ignoring an unknown pinned slug", async () => {
		const deck = await api("/api/deck");
		expect(deck.body.card.problem.slug).toBe("two-sum");
		expect(deck.body.remaining).toBe(793);
		expect(deck.body.topics.length).toBeGreaterThan(100);
		const recent = await api("/api/deck?period=30d");
		expect(recent.body.remaining).toBe(154);
		expect(recent.body.card.problem.asked["30d"].rank).toBe(1);
		const classic = await api("/api/deck?period=lc1000");
		expect(classic.body.card.problem.id).toBe(1);
		const stale = await api("/api/deck?slug=no-longer-listed");
		expect(stale.body.card.problem.slug).toBe("two-sum");
	});

	it("records grades, validates input, and moves cards between sets", async () => {
		const graded = await send("POST", "/api/attempts", {
			slug: "two-sum",
			grade: "good",
			guessed: ["Array", "Hash Table"],
			hints: 1,
		});
		expect(graded).toEqual({ status: 201, body: { score: 1 } });

		expect(
			(await send("POST", "/api/attempts", { slug: "two-sum", grade: "x" }))
				.status,
		).toBe(400);
		expect(
			(await send("POST", "/api/attempts", { slug: "nope", grade: "good" }))
				.status,
		).toBe(404);
		const badJson = await api("/api/attempts", { method: "POST", body: "{" });
		expect(badJson.status).toBe(400);

		expect((await api("/api/deck")).body.card.problem.slug).toBe(
			"add-two-numbers",
		);
		expect((await api("/api/deck?set=again")).body.card).toBeNull();
		await send("POST", "/api/attempts", {
			slug: "add-two-numbers",
			grade: "again",
		});
		const again = await api("/api/deck?set=again");
		expect(again.body.card.problem.slug).toBe("add-two-numbers");
		expect(again.body.card.state.list).toBe("again");
	});

	it("reports the score the background scorer computes", async () => {
		const { body } = await api("/api/report");
		expect(body.report.graded).toBe(2);
		expect(body.report.counts.again).toBe(1);
		expect(body.report.readiness).toBeGreaterThan(0);
		expect(body.history).toHaveLength(1);
	});

	it("saves your own answer on the card, and deletes it with empty text", async () => {
		const note = (body: unknown) => send("PUT", "/api/notes", body);
		expect(
			await note({ slug: "two-sum", text: "  Map value to index.  " }),
		).toEqual({ status: 200, body: { note: "Map value to index." } });
		expect((await api("/api/problems/two-sum")).body.note).toBe(
			"Map value to index.",
		);
		expect((await api("/api/problems/add-two-numbers")).body.note).toBeNull();
		expect((await note({ slug: "two-sum" })).status).toBe(400);
		expect((await note({ slug: "nope", text: "x" })).status).toBe(404);
	});

	it("clears one problem, refuses an unclear target, then clears everything", async () => {
		const del = (query: string) =>
			api(`/api/progress${query}`, { method: "DELETE" });
		expect((await del("?slug=two-sum")).status).toBe(204);
		const cleared = await api("/api/problems/two-sum");
		expect(cleared.body.state).toBeNull();
		expect(cleared.body.note).toBe("Map value to index.");
		expect((await del("")).status).toBe(400);
		expect((await del("?Slug=add-two-numbers")).status).toBe(400);
		expect((await api("/api/report")).body.report.graded).toBe(1);
		expect((await del("?all=true")).status).toBe(204);
		expect((await api("/api/report")).body.report.graded).toBe(0);

		await send("PUT", "/api/notes", { slug: "two-sum", text: " " });
		expect((await api("/api/problems/two-sum")).body.note).toBeNull();
	});

	it("serves the single-page app for any page", async () => {
		for (const path of ["/", "/problems", "/code/two-sum"]) {
			const html = await (await fetch(`${base}${path}`)).text();
			expect(html).toContain('<div id="app">');
		}
	});
});
