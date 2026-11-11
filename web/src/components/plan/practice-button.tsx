import { useNavigate } from "@tanstack/react-router";
import { PlayIcon } from "lucide-react";
import { type ComponentProps, useState } from "react";
import { ICON_ON_PHONE } from "@/components/action-button";
import { remember } from "@/components/plan/plan-link";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { type Plan, planOf } from "@/lib/plan";
import { cn } from "@/lib/utils";

const LABEL = {
	idle: "Practice",
	busy: "Practice",
	empty: "Nothing left",
	failed: "Try again",
} as const;
type State = keyof typeof LABEL;

/**
 * Opens the first problem of `plan` on the code page, with the plan in its URL so Next goes
 * on from there, and remembers the plan. When nothing is left to do it says so instead.
 */
export function PracticeButton({
	plan,
	subject,
	iconOnPhone = false,
	className,
	children,
	...props
}: Omit<ComponentProps<typeof Button>, "onClick" | "aria-label"> & {
	plan: Plan;
	/** What it practices, for its accessible name when the text alone is not enough. */
	subject?: string;
	/** Only the icon on a phone (the text stays its accessible name), for a row of them. */
	iconOnPhone?: boolean;
}) {
	const navigate = useNavigate();
	// A result belongs to the plan it was for: with other filters the button is idle again.
	const key = JSON.stringify(plan);
	const [found, setFound] = useState<{ key: string; state: State }>();
	const state = found?.key === key ? found.state : "idle";
	const setState = (state: State) => setFound({ key, state });
	async function start() {
		setState("busy");
		try {
			const page = await api.next(plan);
			if (!page.next) return setState("empty");
			remember(plan);
			await navigate({
				to: "/code/$slug",
				params: { slug: page.next.slug },
				search: planOf(page.plan),
			});
		} catch (error) {
			console.error("Could not start the plan", error);
			setState("failed");
		}
	}
	const text =
		state === "idle" || state === "busy"
			? (children ?? LABEL.idle)
			: LABEL[state];
	return (
		<Button
			{...props}
			className={cn(iconOnPhone && ICON_ON_PHONE, className)}
			aria-label={
				subject && typeof text === "string" ? `${text}: ${subject}` : undefined
			}
			onClick={start}
			disabled={state === "busy" || state === "empty" || props.disabled}
		>
			<PlayIcon data-icon="inline-start" />
			<span aria-live="polite" className={cn(iconOnPhone && "max-sm:sr-only")}>
				{text}
			</span>
		</Button>
	);
}
