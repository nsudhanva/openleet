import { useState } from "react";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { PlanLink } from "@/components/plan/plan-link";
import { PracticeButton } from "@/components/plan/practice-button";
import { EmptyNote, Panel } from "@/components/progress/panel";
import { Button } from "@/components/ui/button";
import { count, timeFrom } from "@/lib/format";
import { failureSummary } from "@/lib/insights";
import type { Plan } from "@/lib/plan";
import type { ShakySolve } from "@/lib/types";

/** Shaky solves listed before "Show all". */
const SHOWN = 5;

/**
 * The problems Accepted only after failing (two or more real failures, or a time limit) and
 * not solved cleanly again on a later day, newest first, each opening its code page with the
 * shaky plan, so Next goes on to the rest.
 */
export function ShakyPanel({
	shaky,
	elsewhere,
	plan,
}: {
	shaky: ShakySolve[];
	elsewhere: number;
	/** The list's shaky plan. */
	plan: Plan;
}) {
	const [all, setAll] = useState(false);
	const shown = all ? shaky : shaky.slice(0, SHOWN);
	return (
		<Panel
			id="shaky"
			title="Shaky solves"
			note="Accepted only after two or more failed tries, or a time limit. One leaves the list once you solve it again on a later day with no failed try since your last Accepted."
			action={
				shaky.length > 0 && (
					<PracticeButton plan={plan} size="sm" variant="outline">
						Practice these
					</PracticeButton>
				)
			}
		>
			{shaky.length ? (
				<ul className="-mt-1 divide-y">
					{shown.map((s) => (
						<li key={s.slug} className="py-2">
							<div className="flex items-center gap-2">
								<PlanLink
									plan={plan}
									slug={s.slug}
									className="min-w-0 truncate text-sm font-medium hover:text-primary hover:underline"
								>
									{s.title}
								</PlanLink>
								<DifficultyBadge difficulty={s.difficulty} />
							</div>
							<p className="text-xs text-muted-foreground">
								{failureSummary(s.failures)} before Accepted ·{" "}
								{timeFrom(s.solvedAt)}
							</p>
						</li>
					))}
				</ul>
			) : (
				<EmptyNote>
					None yet. A problem lands here when it took two or more wrong answers,
					crashes or limits, or any time limit, before it passed.
				</EmptyNote>
			)}
			<div className="mt-auto flex flex-wrap items-center gap-x-3 pt-2">
				{shaky.length > SHOWN && (
					<Button
						variant="link"
						size="xs"
						className="px-0"
						onClick={() => setAll((a) => !a)}
					>
						{all ? "Show fewer" : `Show all ${shaky.length}`}
					</Button>
				)}
				{elsewhere > 0 && (
					<p className="text-xs text-muted-foreground">
						{count(elsewhere, "more shaky solve")} outside this list.
					</p>
				)}
			</div>
		</Panel>
	);
}
