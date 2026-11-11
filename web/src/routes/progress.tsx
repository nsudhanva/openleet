import { createFileRoute, Link, useRouter } from "@tanstack/react-router";
import { useState } from "react";
import { CompanyPicker } from "@/components/company-picker";
import { ConfirmClear } from "@/components/confirm-clear";
import { PageHeader } from "@/components/page-header";
import { ActivityPanel } from "@/components/progress/activity-panel";
import { CodingPanel } from "@/components/progress/coding-panel";
import { EmptyNote, Panel, Stat } from "@/components/progress/panel";
import { ShakyPanel } from "@/components/progress/shaky-panel";
import { TopicMap } from "@/components/progress/topic-map";
import { ProgressBar } from "@/components/progress-bar";
import { Button } from "@/components/ui/button";
import { useCompanies } from "@/hooks/use-companies";
import { api } from "@/lib/api";
import { ANY_COMPANY, companyName } from "@/lib/companies";
import { count, pageTitle, percent } from "@/lib/format";
import type { Plan } from "@/lib/plan";
import type { StudySet } from "@/lib/scheduler";
import type { DailyScore, Difficulty, TopicRecall } from "@/lib/types";

export const Route = createFileRoute("/progress")({
	head: () => ({ meta: [{ title: pageTitle("Progress") }] }),
	loaderDeps: ({ search: { company } }) => ({ company }),
	loader: ({ deps: { company } }) => api.report(company),
	component: Progress,
});

function Progress() {
	const { report, history, coding, shaky, shakyElsewhere, topicMap, activity } =
		Route.useLoaderData();
	const { company } = Route.useSearch();
	const navigate = Route.useNavigate();
	const name = companyName(useCompanies(), company);
	const total = report.byDifficulty.reduce((sum, d) => sum + d.total, 0);
	// The list readiness covers, as a plan: what Practice opens from here.
	const list: Plan = {
		company,
		period: "6m",
		status: "unsolved",
		order: "rank",
	};
	const listName =
		company === ANY_COMPANY
			? "every company's 6-month list"
			: `${name}'s 6-month list`;

	return (
		<div className="flex flex-col">
			<PageHeader
				title="Progress"
				actions={
					<div className="grid grid-cols-2 gap-2 sm:flex sm:items-center">
						<CompanyPicker
							value={company}
							onChange={(next) =>
								navigate({ search: (prev) => ({ ...prev, company: next }) })
							}
						/>
						<ResetAll />
					</div>
				}
			>
				A background scorer recomputes this after every card and every 15
				minutes, so mastery fades when reviews get old.
			</PageHeader>

			{/* Three to a row from lg, two from md; on a phone they stack. The page scrolls. */}
			<div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
				<Panel
					id="readiness"
					title="Readiness"
					note={
						company === ANY_COMPANY
							? "Mastery of each problem, weighted by how often the companies ask it, over the last 6 months."
							: `Mastery of each problem ${name} asked in the last 6 months, weighted by how often it asks it.`
					}
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
						<Stat label="Day streak" value={count(report.streakDays, "day")} />
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
					className="md:max-lg:col-span-2"
				>
					{report.topics.length ? (
						<TopicMeters topics={report.topics} />
					) : (
						<EmptyNote>
							Grade a few cards to see which topics you miss.
						</EmptyNote>
					)}
				</Panel>

				<CodingPanel coding={coding} list={list} listName={listName} />
				<ShakyPanel
					shaky={shaky}
					elsewhere={shakyElsewhere}
					plan={{ ...list, status: "shaky" }}
				/>
				<ActivityPanel activity={activity} />
				<TopicMap topics={topicMap} list={list} listName={listName} />
			</div>
		</div>
	);
}

/** Topics listed before "Show all". */
const TOPICS_SHOWN = 8;

function TopicMeters({ topics }: { topics: TopicRecall[] }) {
	const [all, setAll] = useState(false);
	const shown = all ? topics : topics.slice(0, TOPICS_SHOWN);
	return (
		<>
			<ul>
				{shown.map((t) => (
					<Meter
						key={t.topic}
						label={t.topic}
						value={t.recall}
						detail={count(t.seen, "card")}
						to={{ set: "all", topic: t.topic }}
					/>
				))}
			</ul>
			{shown.length < topics.length && (
				<Button
					variant="outline"
					size="sm"
					className="self-start"
					onClick={() => setAll(true)}
				>
					Show all {topics.length} topics
				</Button>
			)}
		</>
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
				<ProgressBar value={value} />
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
