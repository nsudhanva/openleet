import { createFileRoute, Link, useRouter } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { ConfirmClear } from "@/components/confirm-clear";
import { FitPages } from "@/components/fit-pages";
import { PageHeader } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { pageTitle, percent } from "@/lib/format";
import type { StudySet } from "@/lib/scheduler";
import type { DailyScore, Difficulty } from "@/lib/types";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/progress")({
	head: () => ({ meta: [{ title: pageTitle("Progress") }] }),
	loader: () => api.report(),
	component: Progress,
});

/** A titled block of the dashboard. */
function Panel({
	id,
	title,
	note,
	className,
	children,
}: {
	id: string;
	title: string;
	note?: string;
	className?: string;
	children: ReactNode;
}) {
	return (
		<section
			aria-labelledby={id}
			className={cn(
				"flex flex-col rounded-sm bg-card p-4 shadow-[0_1px_0_var(--border)] lg:min-h-0",
				className,
			)}
		>
			<h2 id={id} className="font-semibold tracking-tight">
				{title}
			</h2>
			{note && <p className="text-xs text-muted-foreground">{note}</p>}
			<div className="mt-3 flex min-h-0 flex-1 flex-col">{children}</div>
		</section>
	);
}

function Progress() {
	const { report, history } = Route.useLoaderData();
	const total = report.byDifficulty.reduce((sum, d) => sum + d.total, 0);

	return (
		<div className="flex min-h-0 flex-col lg:h-full">
			<PageHeader title="Progress" actions={<ResetAll />}>
				A background scorer recomputes this after every card and every 15
				minutes, so mastery fades when reviews get old.
			</PageHeader>

			{/* One screen on desktop; on a phone the panels stack at full height. */}
			<div className="grid gap-3 lg:min-h-0 lg:flex-1 lg:grid-cols-3">
				<Panel
					id="readiness"
					title="Readiness"
					note="Mastery of each problem, weighted by how often Google asks it."
				>
					<p className="text-6xl leading-none font-bold tracking-tighter tabular-nums">
						{percent(report.readiness, 1)}
					</p>
					<Trend history={history} />
					<dl className="mt-auto grid grid-cols-2 gap-x-4 gap-y-3 border-t pt-3">
						<Stat
							label="Graded at least once"
							value={`${Math.round(report.coverage * total)} of ${total}`}
						/>
						<Stat
							label="Topic accuracy, last 50"
							value={report.accuracy === null ? "—" : percent(report.accuracy)}
						/>
						<Stat label="Cards graded" value={String(report.graded)} />
						<Stat
							label="Day streak"
							value={`${report.streakDays} ${report.streakDays === 1 ? "day" : "days"}`}
						/>
					</dl>
				</Panel>

				<Panel
					id="sets"
					title="Study sets"
					note="Open a set to study only those cards."
				>
					<div className="flex flex-wrap gap-2">
						<SetLink
							set="due"
							label="Due for review"
							count={report.counts.due}
						/>
						<SetLink set="new" label="Not seen yet" count={report.counts.new} />
						<SetLink
							set="again"
							label="Visit again"
							count={report.counts.again}
						/>
						<SetLink
							set="less"
							label="Visit less often"
							count={report.counts.less}
						/>
						<SetLink set="missed" label="Missed topics" />
						<SetLink set="skipped" label="Skipped" />
					</div>
					<h3 className="mt-5 mb-2 font-semibold tracking-tight">
						By difficulty
					</h3>
					<ul>
						{report.byDifficulty.map((d) => (
							<Meter
								key={d.difficulty}
								label={d.difficulty}
								value={d.mastery}
								detail={`${d.seen} of ${d.total} graded`}
								to={{ set: "all", difficulty: d.difficulty }}
							/>
						))}
					</ul>
				</Panel>

				<Panel
					id="topics"
					title="Topics you miss most"
					note="How often you named a topic when it applied. Select one to drill it."
				>
					{report.topics.length ? (
						<FitPages className="h-72 lg:h-auto lg:flex-1">
							<ul>
								{report.topics.map((t) => (
									<Meter
										key={t.topic}
										label={t.topic}
										value={t.recall}
										detail={`${t.seen} ${t.seen === 1 ? "card" : "cards"}`}
										to={{ set: "all", topic: t.topic }}
									/>
								))}
							</ul>
						</FitPages>
					) : (
						<p className="text-sm text-muted-foreground">
							Grade a few cards to see which topics you miss.
						</p>
					)}
				</Panel>
			</div>
		</div>
	);
}

function Stat({ label, value }: { label: string; value: string }) {
	return (
		<div>
			<dt className="text-sm text-muted-foreground">{label}</dt>
			<dd className="text-xl font-semibold tabular-nums">{value}</dd>
		</div>
	);
}

function SetLink({
	set,
	label,
	count,
}: {
	set: StudySet;
	label: string;
	count?: number;
}) {
	return (
		<Link
			to="/"
			search={{ set }}
			className="rounded-full border bg-card px-3.5 py-1.5 text-sm hover:border-primary/60"
		>
			{label}
			{count !== undefined && (
				<span className="ml-2 font-semibold tabular-nums">{count}</span>
			)}
		</Link>
	);
}

function Meter({
	label,
	value,
	detail,
	to,
}: {
	label: string;
	value: number;
	detail: string;
	to: { set: StudySet; topic?: string; difficulty?: Difficulty };
}) {
	return (
		<li className="mb-3 break-inside-avoid">
			<Link to="/" search={to} className="group block">
				<div className="mb-1 flex items-baseline justify-between gap-4 text-sm">
					<span className="font-medium group-hover:text-primary group-hover:underline">
						{label}
					</span>
					<span className="text-muted-foreground tabular-nums">
						{percent(value)} <span className="text-xs">({detail})</span>
					</span>
				</div>
				<div className="h-2 overflow-hidden rounded-full bg-muted">
					<div
						className="h-full rounded-full bg-primary"
						style={{ width: percent(value) }}
					/>
				</div>
			</Link>
		</li>
	);
}

/** Daily readiness as a small line; needs two days of history. */
function Trend({ history }: { history: DailyScore[] }) {
	if (history.length < 2) {
		return (
			<p className="my-3 text-sm text-muted-foreground">
				A trend line appears after two days of practice.
			</p>
		);
	}
	const width = 320;
	const height = 56;
	const step = width / (history.length - 1);
	const points = history
		.map((d, i) => `${i * step},${height - d.readiness * height}`)
		.join(" ");
	return (
		<svg
			viewBox={`0 -2 ${width} ${height + 4}`}
			className="my-3 h-14 w-full text-primary"
			role="img"
			aria-label={`Readiness over ${history.length} days, from ${percent(history[0].readiness)} to ${percent(history.at(-1)?.readiness ?? 0)}`}
		>
			<polyline
				points={points}
				fill="none"
				stroke="currentColor"
				strokeWidth="2"
				strokeLinejoin="round"
				vectorEffect="non-scaling-stroke"
			/>
		</svg>
	);
}

function ResetAll() {
	const router = useRouter();
	return (
		<ConfirmClear
			trigger={<Button variant="destructive" />}
			title="Clear all progress?"
			description="This deletes every graded card, both lists and the score history. Your own answers stay."
			onClear={async () => {
				await api.clearProgress({ all: true });
				await router.invalidate();
			}}
		>
			Clear all progress
		</ConfirmClear>
	);
}
