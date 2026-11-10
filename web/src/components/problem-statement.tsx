import { FitPages } from "@/components/fit-pages";
import type { Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * A problem's statement fitted to its box: it shrinks, then pages (← → with `arrowKeys`).
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
	return (
		<FitPages
			arrowKeys={arrowKeys}
			className={cn("statement h-full", className)}
		>
			<div
				// biome-ignore lint/security/noDangerouslySetInnerHtml: statements are allowlist-sanitized at ingest (src/openleet/sanitize.py)
				dangerouslySetInnerHTML={{ __html: problem.description }}
			/>
		</FitPages>
	);
}
