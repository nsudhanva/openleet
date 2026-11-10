import { describe, expect, it } from "vitest";
import { percent } from "@/lib/format";

describe("percent", () => {
	it("rounds to the given digits", () => {
		expect(percent(0)).toBe("0%");
		expect(percent(0.426)).toBe("43%");
		expect(percent(0.4256, 1)).toBe("42.6%");
		expect(percent(1)).toBe("100%");
		expect(percent(1, 1)).toBe("100.0%");
	});

	it("never shows a little progress as none", () => {
		// Easy mastery with 1 of 252 graded; readiness 0.02%.
		expect(percent(0.00077)).toBe("<1%");
		expect(percent(0.0002, 1)).toBe("<0.1%");
		expect(percent(0.0049)).toBe("<1%");
		expect(percent(0.005)).toBe("1%");
		expect(percent(0.0004, 1)).toBe("<0.1%");
		expect(percent(0.0006, 1)).toBe("0.1%");
	});

	it("never shows almost all as all", () => {
		expect(percent(0.996)).toBe(">99%");
		expect(percent(0.9996, 1)).toBe(">99.9%");
		expect(percent(0.994)).toBe("99%");
	});
});
