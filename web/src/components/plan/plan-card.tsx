import { Link } from "@tanstack/react-router";
import { ListIcon } from "lucide-react";
import type { ReactNode } from "react";
import { PlanLink } from "@/components/plan/plan-link";
import { ProgressBar } from "@/components/progress-bar";
import { buttonVariants } from "@/components/ui/button";
import { planOf, problemsOf, progressShare } from "@/lib/plan";
import type { NextProblem, PlanProgress, PlanView } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * One saved plan or one of your lists, as a card: `title`, the progress, Problems (the
 * plan's problems in the table), Continue (to the next problem, with the plan in the link)
 * and `menu`.
 */
export function PlanCard({
	title,
	plan,
	progress,
	next,
	menu,
}: {
	title: ReactNode;
	plan: PlanView;
	progress: PlanProgress;
	next: NextProblem | null;
	menu: ReactNode;
}) {
	const { solved, total } = progress;
	const search = planOf(plan);
	return (
		<li className="flex min-w-0 items-center gap-2 rounded-sm bg-card py-2 pr-1.5 pl-3 shadow-[0_1px_0_var(--border)]">
			<div className="min-w-0 flex-1">
				{title}
				<div className="mt-1 flex items-center gap-2">
					<ProgressBar
						value={progressShare(progress)}
						className="h-1.5 flex-1"
					/>
					<span className="shrink-0 text-xs text-muted-foreground tabular-nums">
						{solved} of {total}
					</span>
				</div>
			</div>
			<Link
				to="/problems"
				search={problemsOf(search)}
				className={cn(
					buttonVariants({ variant: "ghost", size: "sm" }),
					"shrink-0 text-muted-foreground",
				)}
				title="Show its problems"
			>
				<ListIcon data-icon="inline-start" />
				<span className="max-sm:sr-only">Problems</span>
			</Link>
			{next ? (
				<PlanLink
					plan={search}
					slug={next.slug}
					title={`Next: ${next.title}`}
					className={cn(
						buttonVariants({ variant: "outline", size: "sm" }),
						"shrink-0 bg-card",
					)}
				>
					Continue
				</PlanLink>
			) : (
				<span
					className={cn(
						"shrink-0 px-2 text-xs",
						total ? "text-success" : "text-muted-foreground",
					)}
				>
					{total ? "All solved" : "Empty"}
				</span>
			)}
			{menu}
		</li>
	);
}
