import { describe, expect, it } from "vitest";
import { readinessLabel, readinessText } from "@/lib/readiness";
import type { Readiness } from "@/lib/types";

const google: Readiness = {
	score: 0.4249,
	period: "6m",
	problems: 100,
	recent: 312,
	solved: 30,
	shaky: 2,
	cards: 40,
	fading: 5,
};

describe("readiness", () => {
	it("names the list it covers", () => {
		expect(readinessLabel("Google", google)).toBe(
			"Ready for Google's 100 most-asked (6 months)",
		);
		expect(readinessLabel(null, google)).toBe(
			"Ready for all companies' 100 most-asked (6 months)",
		);
	});

	it("says when a short 6-month list gave way to all time", () => {
		const stripe = { ...google, period: "all", problems: 12, recent: 1 };
		expect(readinessLabel("Stripe", stripe as Readiness)).toBe(
			"Ready for Stripe's 12 most-asked (all time; 1 in 6 months)",
		);
		expect(readinessLabel("X", { ...google, problems: 0, recent: 0 })).toBe(
			"X lists no problems yet",
		);
	});

	it("is a whole percent, or a dash before there is anything to score", () => {
		expect(readinessText(google)).toBe("42%");
		expect(readinessText({ score: 0 })).toBe("0%");
		expect(readinessText({ score: null })).toBe("—");
	});
});
