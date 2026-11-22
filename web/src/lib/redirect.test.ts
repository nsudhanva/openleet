import { describe, expect, it } from "vitest";
import { safeRedirect } from "@/lib/redirect";

describe("the page to go back to after signing in", () => {
	const origin = "https://openleet.test";
	it("keeps a page of this site", () => {
		expect(safeRedirect("/progress?company=meta#x", origin)).toBe(
			"/progress?company=meta#x",
		);
		expect(safeRedirect("/code/two-sum", origin)).toBe("/code/two-sum");
	});

	it("sends anything that leaves the site home", () => {
		for (const value of [
			"https://evil.example",
			"//evil.example",
			"/\t/evil.example",
			"/\n/evil.example",
			"/\\evil.example",
			"\\/evil.example",
			"javascript:alert(1)",
			42,
			undefined,
		])
			expect(safeRedirect(value, origin)).toBe("/");
	});
});
