import { FitPages } from "@/components/fit-pages";
import type { Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * A problem's statement fitted to its box: it shrinks, then pages (← → with `arrowKeys`).
 * Premium problems have no stored statement.
 */
export function ProblemStatement({
	problem,
	arrowKeys = false,
	className,
}: {
	problem: Pick<Problem, "description">;
	arrowKeys?: boolean;
	className?: string;
}) {
	if (!problem.description)
		return (
			<p className={cn("text-muted-foreground", className)}>
				This is a LeetCode Premium problem, so its statement is not stored here.
				Open it on LeetCode to read it.
			</p>
		);
	return (
		<FitPages
			arrowKeys={arrowKeys}
			className={cn("statement h-full", className)}
		>
			<div
				// biome-ignore lint/security/noDangerouslySetInnerHtml: statements are allowlist-sanitized at ingest (src/google/sanitize.py)
				dangerouslySetInnerHTML={{ __html: problem.description }}
			/>
		</FitPages>
	);
}
