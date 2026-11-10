import type { ReactNode } from "react";
import { ProblemHeader } from "@/components/problem-header";
import { ProblemStatement } from "@/components/problem-statement";
import { Segmented } from "@/components/segmented";
import type { AskedPeriod, Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/** The index-card surface. */
const CARD_SURFACE =
	"rounded-sm bg-card text-card-foreground shadow-[0_1px_0_var(--border),0_18px_40px_-24px_rgb(24_33_47/0.45)]";

/**
 * The study and code pages share this frame: a toolbar row of fixed height, then the card.
 * The row never wraps (it scrolls sideways on a narrow screen), so the card starts at the
 * same place on both pages and moving between them does not move it.
 */
export function ProblemPage({
	toolbar,
	children,
}: {
	toolbar: ReactNode;
	children: ReactNode;
}) {
	return (
		<div className="flex h-full min-h-0 flex-col gap-3">
			<div className="no-scrollbar flex h-8 shrink-0 items-center gap-2 overflow-x-auto overflow-y-hidden *:shrink-0">
				{toolbar}
			</div>
			{children}
		</div>
	);
}

/** Which pane a phone shows; wide screens show both. */
export type Pane = "problem" | "aside";

/**
 * The problem card: header, the statement on the left at the same width on every page, the
 * `aside` pane on the right, then `footer`. It fills the rest of the screen; on a phone the
 * two panes take turns, switched by `pane`.
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
	/** The aside pane's name, also its tab on a phone ("Guess", "Code"). */
	asideLabel: string;
	asideClassName?: string;
	pane: Pane;
	onPaneChange: (pane: Pane) => void;
	footer: ReactNode;
}) {
	return (
		<article
			aria-labelledby="problem-title"
			className={cn(
				"flex min-h-0 flex-1 flex-col overflow-hidden",
				CARD_SURFACE,
			)}
		>
			<ProblemHeader problem={problem} period={period}>
				{actions}
			</ProblemHeader>
			<Segmented
				label="Show"
				className="mx-4 mt-2 lg:hidden"
				value={pane}
				onChange={onPaneChange}
				options={[
					{ value: "problem", label: "Problem" },
					{ value: "aside", label: asideLabel },
				]}
			/>
			<div className="grid min-h-0 flex-1 grid-cols-1 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]">
				<section
					aria-label="Statement"
					className={cn(
						"flex min-h-0 flex-col px-4 py-3 sm:px-6",
						pane !== "problem" && "max-lg:hidden",
					)}
				>
					<ProblemStatement problem={problem} arrowKeys />
				</section>
				<section
					aria-label={asideLabel}
					className={cn(
						"flex min-h-0 flex-col lg:border-l lg:border-dashed",
						pane !== "aside" && "max-lg:hidden",
						asideClassName,
					)}
				>
					{aside}
				</section>
			</div>
			{footer}
		</article>
	);
}
