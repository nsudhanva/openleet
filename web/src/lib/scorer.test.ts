import { describe, expect, it } from "vitest";
import { scoreTopics } from "@/lib/scorer";

describe("scoreTopics", () => {
	it("scores a topic guess with F1", () => {
		expect(scoreTopics(["Array", "Graph"], ["Array", "Hash Table"])).toEqual({
			hits: ["Array"],
			missed: ["Hash Table"],
			extra: ["Graph"],
			score: 0.5,
		});
	});

	it("scores an empty guess against no topics as zero", () => {
		expect(scoreTopics([], []).score).toBe(0);
	});
});
