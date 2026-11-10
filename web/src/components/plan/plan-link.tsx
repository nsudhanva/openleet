import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { api } from "@/lib/api";
import { type Plan, planOf } from "@/lib/plan";
import type { PlanView } from "@/lib/types";

/** Remembers a plan the learner followed; a failure only costs the recent list an entry. */
export function remember(plan: Plan) {
	api
		.rememberPlan(plan)
		.catch((error: unknown) => console.error("Could not save the plan", error));
}

/** A link to a plan's next problem, remembering the plan when followed. */
export function PlanLink({
	view,
	slug,
	className,
	title,
	children,
}: {
	view: PlanView;
	slug: string;
	className?: string;
	title?: string;
	children: ReactNode;
}) {
	const plan = planOf(view);
	return (
		<Link
			to="/code/$slug"
			params={{ slug }}
			search={plan}
			onClick={() => remember(plan)}
			className={className}
			title={title}
		>
			{children}
		</Link>
	);
}
