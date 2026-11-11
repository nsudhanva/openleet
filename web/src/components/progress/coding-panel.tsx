import { PracticeButton } from "@/components/plan/practice-button";
import { EmptyNote, Panel, Stat } from "@/components/progress/panel";
import { ProgressBar } from "@/components/progress-bar";
import { FAILURE_KINDS, failureTotal, firstTryText } from "@/lib/insights";
import type { Plan } from "@/lib/plan";
import type { Coding, Failures } from "@/lib/types";

/** A color per failure kind, from the theme; the legend names each with its count. */
const FAILURE_COLOR: Record<keyof Failures, string> = {
	wrongAnswer: "bg-destructive",
	timeLimitExceeded: "bg-warning",
	memoryLimitExceeded: "bg-[var(--syntax-function)]",
	runtimeError: "bg-[var(--syntax-type)]",
	compileError: "bg-muted-foreground",
	outputLimitExceeded: "bg-primary",
};

/** The failed verdicts as one stacked bar, with a legend that carries the numbers. */
function FailureMix({ failures }: { failures: Failures }) {
	const total = failureTotal(failures);
	if (!total)
		return (
			<EmptyNote>
				No failed submissions before a solve: every try passed.
			</EmptyNote>
		);
	const kinds = FAILURE_KINDS.filter((k) => failures[k.key] > 0);
	return (
		<div className="space-y-2">
			<div aria-hidden className="flex h-2.5 overflow-hidden rounded-full">
				{kinds.map((k) => (
					<div
						key={k.key}
						className={FAILURE_COLOR[k.key]}
						style={{ width: `${(failures[k.key] / total) * 100}%` }}
					/>
				))}
			</div>
			<ul className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
				{kinds.map((k) => (
					<li key={k.key} className="flex items-center gap-1.5">
						<span
							aria-hidden
							className={`size-2.5 rounded-full ${FAILURE_COLOR[k.key]}`}
						/>
						{k.label}
						<span className="font-semibold tabular-nums">
							{failures[k.key]}
						</span>
					</li>
				))}
			</ul>
		</div>
	);
}

/**
 * Coding over the list: solved per difficulty, how many solves came before any wrong answer,
 * limit or crash, and what failed on the way to each solve. About understanding, not speed:
 * no CPU times.
 */
export function CodingPanel({
	coding,
	list,
	listName,
}: {
	coding: Coding;
	/** The list's plan, to start practicing it. */
	list: Plan;
	listName: string;
}) {
	const solved = coding.byDifficulty.reduce((sum, d) => sum + d.solved, 0);
	const total = coding.byDifficulty.reduce((sum, d) => sum + d.total, 0);
	const firstTry = firstTryText(coding.firstTry, solved);
	const failed = failureTotal(coding.failures);
	return (
		<Panel
			id="coding"
			title="Coding"
			note={`Problems of ${listName} you solved in the judge.`}
		>
			<ul className="space-y-2.5">
				{coding.byDifficulty.map((d) => (
					<li key={d.difficulty}>
						<div className="mb-1 flex items-baseline justify-between gap-4 text-sm">
							<span className="font-medium">{d.difficulty}</span>
							<span className="text-muted-foreground tabular-nums">
								{d.solved} of {d.total} solved
							</span>
						</div>
						<ProgressBar value={d.total ? d.solved / d.total : 0} />
					</li>
				))}
			</ul>
			<dl className="mt-4 grid grid-cols-2 gap-x-4 gap-y-3 border-t pt-3">
				<Stat label="Solved" value={`${solved} of ${total}`} />
				<Stat label="Solved on the first try" {...firstTry} />
			</dl>
			<p className="mt-1 text-xs text-muted-foreground">
				First try: no wrong answer, limit or crash before Accepted. Compile
				errors do not count.
			</p>
			<h3 className="mt-4 mb-2 text-sm font-semibold">
				Failed submissions before a solve
				{failed > 0 && (
					<span className="ml-1.5 font-normal text-muted-foreground tabular-nums">
						({failed})
					</span>
				)}
			</h3>
			{coding.tried ? (
				<FailureMix failures={coding.failures} />
			) : (
				<div className="space-y-2">
					<EmptyNote>
						Submit a solution on a problem's code page to see what passed and
						what failed, and why.
					</EmptyNote>
					<PracticeButton plan={list} variant="outline" size="sm">
						Start with the first unsolved
					</PracticeButton>
				</div>
			)}
		</Panel>
	);
}
