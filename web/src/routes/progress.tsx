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
import { TrendChart } from "@/components/progress/trend-chart";
import { ProgressBar } from "@/components/progress-bar";
import { Button } from "@/components/ui/button";
import { useCompanies } from "@/hooks/use-companies";
import { api } from "@/lib/api";
import { ANY_COMPANY, companyName } from "@/lib/companies";
import { pageTitle, percent } from "@/lib/format";
import { MIN_TOPIC_CARDS } from "@/lib/insights";
import type { Plan } from "@/lib/plan";
import { readinessLabel, readinessText } from "@/lib/readiness";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import type { Difficulty, TopicRecall } from "@/lib/types";

export const Route = createFileRoute("/progress")({
	head: () => ({ meta: [{ title: pageTitle("Progress") }] }),
	loaderDeps: ({ search: { company } }) => ({ company }),
	loader: ({ deps: { company } }) => api.report(company),
	component: Progress,
});

function Progress() {
	const { report, coding, shaky, shakyElsewhere, topicMap, activity } =
		Route.useLoaderData();
	const { company } = Route.useSearch();
	const navigate = Route.useNavigate();
	const name = companyName(useCompanies(), company);
	const owner = company === ANY_COMPANY ? null : name;
	const { readiness } = report;
	const total = report.byDifficulty.reduce((sum, d) => sum + d.total, 0);
	const seen = report.byDifficulty.reduce((sum, d) => sum + d.seen, 0);
	// The 6-month list as a plan: what Practice opens from here.
	const list: Plan = {
		company,
		period: "6m",
		status: "unsolved",
		order: "rank",
	};
	const listName =
		owner === null ? "every company's 6-month list" : `${owner}'s 6-month list`;
	const asker = owner ?? "any company";

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
				Each panel says which problems it counts: the most-asked ones for
				readiness, the 6-month list, or every card and submission.
			</PageHeader>

			{/* Three to a row from lg, two from md; on a phone they stack. The page scrolls. */}
			<div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
				<Panel
					id="readiness"
					title="Readiness"
					note={readinessLabel(owner, readiness)}
				>
					<p className="text-6xl leading-none font-bold tracking-tighter tabular-nums">
						{readinessText(readiness)}
					</p>
					{readiness.score === null && readiness.problems > 0 && (
						<p className="mt-2 text-sm">
							Grade a card or submit a solution for one of these problems to
							start.
						</p>
					)}
					<p className="mt-2 text-xs text-muted-foreground">
						Each problem counts by how often {asker} asks it: 60% for solving it
						cleanly in the judge (half for a shaky solve), 40% for a card graded
						“Got it” or “Visit less often” that is not overdue (half when
						overdue by less than its interval).
					</p>
					<div className="my-3">
						<TrendChart trend={report.trend} />
					</div>
					<dl className="mt-auto grid grid-cols-2 gap-x-4 gap-y-3 border-t pt-3">
						<Stat
							label="Solved cleanly"
							value={`${readiness.solved} of ${readiness.problems}`}
							detail={readiness.shaky ? `${readiness.shaky} shaky` : undefined}
						/>
						<Stat
							label="Cards up to date"
							value={`${readiness.cards} of ${readiness.problems}`}
							detail={
								readiness.fading ? `${readiness.fading} overdue` : undefined
							}
						/>
					</dl>
				</Panel>

				<Panel
					id="sets"
					title="Study sets"
					note={`Cards of ${listName}. Open a set to study only those cards.`}
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
						<SetLink set="missed" label={STUDY_SETS.missed} />
						<SetLink set="skipped" label="Skipped" />
					</div>
					<h3 className="mt-5 mb-2 font-semibold tracking-tight">
						Cards by difficulty
					</h3>
					<ul>
						{report.byDifficulty.map((d) => (
							<Meter
								key={d.difficulty}
								label={d.difficulty}
								value={d.total ? d.seen / d.total : 0}
								text={`${d.seen} of ${d.total} reviewed`}
								to={{ set: "all", difficulty: d.difficulty }}
							/>
						))}
					</ul>
					<dl className="mt-auto border-t pt-3">
						<Stat label="Graded at least once" value={`${seen} of ${total}`} />
					</dl>
				</Panel>

				<Panel
					id="topics"
					title="Topics you name least"
					note="On every card you graded, on any list: how often you named a topic when it applied, less half for each wrong guess of it. Rated from 5 graded cards; listed under 60%. Select one to drill it."
					className="md:max-lg:col-span-2"
				>
					{report.topics.length ? (
						<TopicMeters topics={report.topics} />
					) : (
						<EmptyNote>
							{report.graded < MIN_TOPIC_CARDS
								? `Grade ${MIN_TOPIC_CARDS}+ cards on a topic to rate it.`
								: `No topic with ${MIN_TOPIC_CARDS} or more graded cards scores under 60%.`}
						</EmptyNote>
					)}
					<dl className="mt-auto grid grid-cols-2 gap-x-4 gap-y-3 border-t pt-3">
						<Stat
							label="Topic guess score, last 50 cards"
							value={report.accuracy === null ? "—" : percent(report.accuracy)}
						/>
						<Stat label="Grades given" value={String(report.graded)} />
					</dl>
				</Panel>

				<CodingPanel coding={coding} list={list} listName={listName} />
				<ShakyPanel
					shaky={shaky}
					elsewhere={shakyElsewhere}
					plan={{ ...list, status: "shaky" }}
				/>
				<ActivityPanel activity={activity} streakDays={report.streakDays} />
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
						value={t.score}
						text={`${percent(t.score)} (named ${t.named} of ${t.seen})`}
						to={{ set: "all", topic: t.topic }}
					/>
				))}
			</ul>
			{shown.length < topics.length && (
				<Button
					variant="outline"
					size="sm"
					className="mb-3 self-start"
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

/** A labelled bar that opens its cards; `text` says what the bar shows. */
function Meter({
	label,
	value,
	text,
	to,
}: {
	label: string;
	value: number;
	text: string;
	to: { set: StudySet; topic?: string; difficulty?: Difficulty };
}) {
	return (
		<li className="mb-3 break-inside-avoid">
			<Link to="/" search={to} className="group block">
				<div className="mb-1 flex items-baseline justify-between gap-4 text-sm">
					<span className="font-medium group-hover:text-primary group-hover:underline">
						{label}
					</span>
					<span className="text-muted-foreground tabular-nums">{text}</span>
				</div>
				<ProgressBar value={value} />
			</Link>
		</li>
	);
}

function ResetAll() {
	const router = useRouter();
	return (
		<ConfirmClear
			trigger={<Button variant="destructive" />}
			title="Clear all progress?"
			description="This deletes every graded card and both lists. Your own answers, code and submissions stay."
			onClear={async () => {
				await api.clearProgress({ all: true });
				await router.invalidate();
			}}
		>
			Clear all progress
		</ConfirmClear>
	);
}
