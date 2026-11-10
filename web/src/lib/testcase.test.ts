import { describe, expect, it } from "vitest";
import { examplesToTestcase } from "@/lib/testcase";

describe("examplesToTestcase", () => {
	it("turns `name = value` lines into one value per line, case after case", () => {
		expect(
			examplesToTestcase([
				{ input: "nums = [2,7,11,15]\ntarget = 9", expected: "[0,1]" },
				{ input: 'nums = [3,3]\n\ns = "a = b"', expected: "[0,1]" },
			]),
		).toBe('[2,7,11,15]\n9\n[3,3]\n"a = b"');
	});

	it("is empty without examples", () => {
		expect(examplesToTestcase([])).toBe("");
	});
});
