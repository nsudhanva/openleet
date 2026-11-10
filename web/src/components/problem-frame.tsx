import { type ReactNode, useEffect, useRef } from "react";
import { ProblemHeader } from "@/components/problem-header";
import { ProblemStatement } from "@/components/problem-statement";
import { Segmented } from "@/components/segmented";
import type { AskedPeriod, Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/** The sticky site header's height (h-12), which covers the top of the page. */
const HEADER_PX = 48;

/** The index-card surface. */
const CARD_SURFACE =
	"rounded-sm bg-card text-card-foreground shadow-[0_1px_0_var(--border),0_18px_40px_-24px_rgb(24_33_47/0.45)]";

/**
 * The study and code pages share this frame: a toolbar, then the card. On a `fit:` screen the
 * toolbar is one row of fixed height that never wraps (it scrolls sideways if it must), so
 * the card starts at the same place on both pages and moving between them does not move it.
 * Elsewhere its items wrap, two to a row on a phone (`max-sm:col-span-2` for a whole row).
 */
export function ProblemPage({
	toolbar,
	children,
}: {
	toolbar: ReactNode;
	children: ReactNode;
}) {
	return (
		<div className="flex flex-col gap-3 fit:h-full fit:min-h-0">
			<div className="grid grid-cols-2 items-center gap-2 sm:flex sm:flex-wrap fit:no-scrollbar fit:h-8 fit:shrink-0 fit:flex-nowrap fit:overflow-x-auto fit:overflow-y-hidden fit:*:shrink-0">
				{toolbar}
			</div>
			{children}
		</div>
	);
}

/** Which pane shows below `lg`; wider screens show both. */
export type Pane = "problem" | "aside";

/**
 * The problem card: header, the statement on the left at the same width on every page, the
 * `aside` pane on the right, then the `footer` bar. On a `fit:` screen it fills the rest of
 * the screen; elsewhere it is as tall as its content and the footer sticks to the bottom of
 * the screen. Below `lg` the two panes take turns, switched by `pane`.
 */
export function ProblemCard({
	problem,
	period,
	actions,
	aside,
	asideLabel,
	asideClassName,
	pane,
	onPaneChange,
	footer,
}: {
	problem: Problem;
	/** The list whose ranks the header shows. */
	period: AskedPeriod;
	/** Header extras: progress, links, badges. */
	actions?: ReactNode;
	aside: ReactNode;
	/** The aside pane's name, also its tab below `lg` ("Guess", "Code"). */
	asideLabel: string;
	asideClassName?: string;
	pane: Pane;
	onPaneChange: (pane: Pane) => void;
	footer: ReactNode;
}) {
	const panes = useRef<HTMLDivElement>(null);
	const shownPane = useRef(pane);
	// A pane switched by an action (Show answer, Run) shows from its top, not from wherever
	// the page had scrolled to in the other one.
	useEffect(() => {
		if (shownPane.current === pane) return;
		shownPane.current = pane;
		const element = panes.current;
		if (element && element.getBoundingClientRect().top < HEADER_PX)
			element.scrollIntoView({ block: "start" });
	}, [pane]);

	return (
		<article
			aria-labelledby="problem-title"
			className={cn(
				"flex flex-col fit:min-h-0 fit:flex-1 fit:overflow-hidden",
				CARD_SURFACE,
			)}
		>
			<ProblemHeader problem={problem} period={period}>
				{actions}
			</ProblemHeader>
			<div
				ref={panes}
				className="flex scroll-mt-14 flex-col fit:min-h-0 fit:flex-1"
			>
				<Segmented
					label="Show"
					className="mx-4 mt-3 grid grid-cols-2 sm:mx-6 sm:flex lg:hidden"
					itemClassName="sm:min-w-24"
					value={pane}
					onChange={onPaneChange}
					options={[
						{ value: "problem", label: "Problem" },
						{ value: "aside", label: asideLabel },
					]}
				/>
				<div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] fit:min-h-0 fit:flex-1">
					<section
						aria-label="Statement"
						className={cn(
							"flex min-w-0 flex-col px-4 py-3 sm:px-6 fit:min-h-0",
							pane !== "problem" && "max-lg:hidden",
						)}
					>
						<ProblemStatement problem={problem} arrowKeys />
					</section>
					<section
						aria-label={asideLabel}
						className={cn(
							"flex min-w-0 flex-col lg:border-l lg:border-dashed fit:min-h-0",
							pane !== "aside" && "max-lg:hidden",
							asideClassName,
						)}
					>
						{aside}
					</section>
				</div>
			</div>
			<footer className="sticky bottom-0 z-10 rounded-b-sm border-t bg-card px-3 py-2 shadow-[0_-10px_20px_-18px_rgb(24_33_47/0.5)] sm:px-6 fit:static fit:shadow-none">
				{footer}
			</footer>
		</article>
	);
}
