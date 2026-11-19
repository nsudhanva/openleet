import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { api } from "@/lib/api";
import type { Plan } from "@/lib/plan";

/**
 * Stores a plan the learner followed among the recent plans. A plan over one of your lists
 * is not stored: the list itself is kept.
 */
export async function savePlan(plan: Plan): Promise<void> {
	if (plan.list === undefined) await api.rememberPlan(plan);
}

/** Remembers a plan the learner followed; a failure only costs the recent list an entry. */
export function remember(plan: Plan) {
	savePlan(plan).catch((error: unknown) =>
		console.error("Could not save the plan", error),
	);
}

/** A link to a problem of a plan, on the code page with the plan, remembering the plan. */
export function PlanLink({
	plan,
	slug,
	className,
	title,
	"aria-label": ariaLabel,
	children,
}: {
	plan: Plan;
	slug: string;
	className?: string;
	title?: string;
	"aria-label"?: string;
	children: ReactNode;
}) {
	return (
		<Link
			to="/code/$slug"
			params={{ slug }}
			search={plan}
			onClick={() => remember(plan)}
			className={className}
			title={title}
			aria-label={ariaLabel}
		>
			{children}
		</Link>
	);
}
