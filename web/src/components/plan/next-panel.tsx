import { useNavigate } from "@tanstack/react-router";
import { ArrowRightIcon } from "lucide-react";
import { useEffect, useEffectEvent, useState } from "react";
import { KeyHint } from "@/components/action-button";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { PlanLink, remember } from "@/components/plan/plan-link";
import { ProgressBar } from "@/components/progress-bar";
import { buttonVariants } from "@/components/ui/button";
import { useHotkeys } from "@/hooks/use-hotkeys";
import { api } from "@/lib/api";
import {
	type Plan,
	pivotText,
	planOf,
	progressShare,
	progressText,
} from "@/lib/plan";
import type { NextPage } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * Shown under an accepted submission: the plan's next problem (N follows it) with how much of
 * the plan is solved, and other plans to switch to. It never moves on by itself. The next
 * problem's topics are never shown; the pivots may name the solved problem's.
 */
export function NextPanel({ plan, slug }: { plan: Plan; slug: string }) {
	const [page, setPage] = useState<NextPage | "error" | null>(null);
	const navigate = useNavigate();
	const key = JSON.stringify(plan);
	const load = useEffectEvent((signal: AbortSignal) =>
		api.next(plan, slug, signal),
	);
	// biome-ignore lint/correctness/useExhaustiveDependencies: asks again when the plan changes
	useEffect(() => {
		const controller = new AbortController();
		load(controller.signal).then(setPage, (error: unknown) => {
			if (controller.signal.aborted) return;
			console.error("Could not find the next problem", error);
			setPage("error");
		});
		return () => controller.abort();
	}, [key]);

	const ready = page !== null && page !== "error" ? page : null;
	const next = ready?.next;
	useHotkeys(
		ready && next
			? {
					n: () => {
						const target = planOf(ready.plan);
						remember(target);
						navigate({
							to: "/code/$slug",
							params: { slug: next.slug },
							search: target,
						});
					},
				}
			: {},
	);

	return (
		<section
			aria-labelledby="next-heading"
			aria-busy={page === null}
			className="space-y-2.5 rounded-md border border-dashed border-primary/40 p-3"
		>
			<div className="flex flex-wrap items-baseline justify-between gap-x-3">
				<h3 id="next-heading" className="text-sm font-semibold">
					Next in your plan
				</h3>
				{ready && (
					<span className="text-xs text-muted-foreground tabular-nums">
						{progressText(ready.progress)}
					</span>
				)}
			</div>
			{page === null && (
				<p className="text-sm text-muted-foreground">
					Finding the next problem…
				</p>
			)}
			{page === "error" && (
				<p role="alert" className="text-sm text-destructive">
					Could not find the next problem.
				</p>
			)}
			{ready && (
				<>
					<ProgressBar value={progressShare(ready.progress)} />
					<p className="truncate text-xs text-muted-foreground">
						{ready.plan.label}
					</p>
					{next ? (
						<PlanLink
							view={ready.plan}
							slug={next.slug}
							className={cn(
								buttonVariants({ size: "lg" }),
								"h-auto min-h-10 w-full justify-start py-1.5 whitespace-normal",
							)}
						>
							<span className="min-w-0 flex-1 text-left">
								Next: <span className="font-semibold">{next.title}</span>
							</span>
							<DifficultyBadge difficulty={next.difficulty} />
							<KeyHint className="bg-primary-foreground/15 text-primary-foreground">
								N
							</KeyHint>
							<ArrowRightIcon aria-hidden />
						</PlanLink>
					) : (
						<p className="text-sm">
							{progressText(ready.progress)}: nothing left in this plan.
							{ready.pivots.length > 0 && " Try another:"}
						</p>
					)}
					{ready.pivots.length > 0 && (
						<div className="space-y-1.5">
							{next && (
								<p className="text-xs text-muted-foreground">Or switch to</p>
							)}
							<ul aria-label="Other plans" className="flex flex-wrap gap-1.5">
								{ready.pivots.map((pivot) => (
									<li key={`${pivot.kind}:${pivot.plan.label}`}>
										<PlanLink
											view={pivot.plan}
											slug={pivot.next.slug}
											title={`${pivot.plan.label}. Next: ${pivot.next.title}`}
											className={cn(
												buttonVariants({ variant: "outline", size: "sm" }),
												"bg-card",
											)}
										>
											{pivotText(pivot)}
										</PlanLink>
									</li>
								))}
							</ul>
						</div>
					)}
				</>
			)}
		</section>
	);
}
