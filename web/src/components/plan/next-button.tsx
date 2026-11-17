import { useNavigate } from "@tanstack/react-router";
import { ArrowRightIcon } from "lucide-react";
import { useState } from "react";
import { KeyHint } from "@/components/action-button";
import { remember } from "@/components/plan/plan-link";
import { Button } from "@/components/ui/button";
import { useHotkeys } from "@/hooks/use-hotkeys";
import { api } from "@/lib/api";
import { type Plan, planOf } from "@/lib/plan";
import { cn } from "@/lib/utils";

type State = "idle" | "finding" | "done" | "error";

const TITLE: Record<State, string> = {
	idle: "Skip to the plan's next problem",
	finding: "Finding the next problem…",
	done: "Nothing left in this plan",
	error: "Could not find the next problem; try again",
};

/**
 * Moves on to the plan's next problem, solved or not (N too). The next problem is asked for
 * on use, so the page loads nothing extra.
 */
export function NextButton({
	plan,
	slug,
	className,
}: {
	plan: Plan;
	slug: string;
	className?: string;
}) {
	const navigate = useNavigate();
	const [state, setState] = useState<State>("idle");

	async function skip() {
		if (state === "finding" || state === "done") return;
		setState("finding");
		try {
			const page = await api.next(plan, slug);
			if (!page.next) {
				setState("done");
				return;
			}
			const target = planOf(page.plan);
			remember(target);
			await navigate({
				to: "/code/$slug",
				params: { slug: page.next.slug },
				search: target,
			});
		} catch (error) {
			console.error("Could not find the next problem", error);
			setState("error");
		}
	}

	useHotkeys({ n: skip });

	return (
		<Button
			variant="ghost"
			size="xs"
			className={cn("shrink-0 text-muted-foreground", className)}
			title={TITLE[state]}
			disabled={state === "finding" || state === "done"}
			onClick={skip}
		>
			<span className="max-sm:sr-only">Next</span>
			<KeyHint>N</KeyHint>
			<ArrowRightIcon data-icon="inline-end" />
		</Button>
	);
}
