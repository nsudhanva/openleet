import { ExternalLinkIcon } from "lucide-react";
import type { ReactNode } from "react";
import { CompanyTags } from "@/components/company-tags";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { PremiumBadge } from "@/components/premium-badge";
import { buttonVariants } from "@/components/ui/button";
import type { AskedPeriod, Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * The card's heading over the red rule: the title, then difficulty, company tags in the space
 * left (one line that never wraps), `children` (progress, actions) and the LeetCode link. From
 * `lg` it is one line, so the header keeps its height; below, the line goes under the title
 * and `children` wrap onto a line of their own when the tags would get too little room (on
 * the left on a phone, on the right from sm).
 */
export function ProblemHeader({
	problem,
	period,
	children,
}: {
	problem: Pick<
		Problem,
		"id" | "title" | "difficulty" | "premium" | "companies" | "url"
	>;
	/** The list whose ranks the company tags show. */
	period: AskedPeriod;
	children?: ReactNode;
}) {
	return (
		<header className="card-margin flex flex-col gap-1.5 px-4 pt-3 pb-2 sm:px-6 lg:flex-row lg:items-center lg:gap-3">
			<h1
				id="problem-title"
				className="text-xl leading-tight font-bold tracking-tight text-balance sm:text-2xl lg:max-w-1/2"
			>
				{problem.title}
			</h1>
			<div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted-foreground lg:flex-nowrap">
				<div className="flex h-7 min-w-0 flex-[1_1_12rem] items-center gap-2 sm:gap-3">
					<DifficultyBadge difficulty={problem.difficulty} />
					{problem.premium && <PremiumBadge />}
					<CompanyTags
						asked={problem.companies}
						period={period}
						className="flex-1"
					/>
				</div>
				<div className="flex min-h-7 flex-wrap items-center gap-x-2 gap-y-1 sm:ml-auto sm:justify-end sm:gap-x-3 lg:flex-nowrap lg:whitespace-nowrap">
					{children}
					<a
						href={problem.url}
						target="_blank"
						rel="noreferrer"
						className={cn(
							buttonVariants({ variant: "ghost", size: "xs" }),
							"shrink-0 text-muted-foreground",
						)}
					>
						<span className="sm:hidden">LC</span>
						<span className="max-sm:hidden">LeetCode</span> {problem.id}
						<ExternalLinkIcon data-icon="inline-end" />
					</a>
				</div>
			</div>
		</header>
	);
}
