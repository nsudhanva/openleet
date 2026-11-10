import type { CodeExample } from "@/lib/types";

const ASSIGNMENT = /^\s*[A-Za-z_]\w*\s*=\s*/;

/**
 * The examples in LeetCode's "Testcase" format: one JSON value per line, one line per
 * parameter in signature order, cases one after another. `nums = [1,2]` becomes `[1,2]`.
 */
export function examplesToTestcase(examples: CodeExample[]): string {
	return examples
		.flatMap((example) =>
			example.input
				.split("\n")
				.filter((line) => line.trim())
				.map((line) => line.replace(ASSIGNMENT, "").trim()),
		)
		.join("\n");
}
