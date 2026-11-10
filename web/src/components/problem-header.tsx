import { ExternalLinkIcon } from "lucide-react";
import type { ReactNode } from "react";
import { AskedBadges } from "@/components/asked-badges";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { buttonVariants } from "@/components/ui/button";
import type { Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * The card's heading over the red rule: title, difficulty, Google ranks, then `children`
 * (progress, actions) and the LeetCode link.
 */
export function ProblemHeader({
	problem,
	children,
}: {
	problem: Pick<Problem, "id" | "title" | "difficulty" | "asked" | "url">;
	children?: ReactNode;
}) {
	return (
		<header className="card-margin flex flex-wrap items-center gap-x-3 gap-y-1 px-4 pt-3 pb-2 sm:px-6">
			<h1
				id="problem-title"
				className="mr-auto text-xl leading-tight font-bold tracking-tight sm:text-2xl"
			>
				{problem.title}
			</h1>
			<div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted-foreground">
				<DifficultyBadge difficulty={problem.difficulty} />
				<AskedBadges asked={problem.asked} />
				{children}
				<a
					href={problem.url}
					target="_blank"
					rel="noreferrer"
					className={cn(
						buttonVariants({ variant: "ghost", size: "xs" }),
						"text-muted-foreground",
					)}
				>
					LeetCode {problem.id}
					<ExternalLinkIcon data-icon="inline-end" />
				</a>
			</div>
		</header>
	);
}

/** The index-card surface shared by the study card and the code page. */
export const CARD_SURFACE =
	"rounded-sm bg-card text-card-foreground shadow-[0_1px_0_var(--border),0_18px_40px_-24px_rgb(24_33_47/0.45)]";
