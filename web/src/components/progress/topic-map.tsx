import { Link } from "@tanstack/react-router";
import { useState } from "react";
import { PracticeButton } from "@/components/plan/practice-button";
import { Panel } from "@/components/progress/panel";
import { ProgressBar } from "@/components/progress-bar";
import { Button } from "@/components/ui/button";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import { percent } from "@/lib/format";
import type { Plan } from "@/lib/plan";
import type { TopicRow } from "@/lib/types";

/** Topics listed before "Show all". */
const SHOWN = 10;

/**
 * Every topic of the list, most asked first: how much the company asks it (relative to the
 * most asked), how much of it you covered on cards or in the judge, your flashcard accuracy
 * on it, and what you solved. Practice opens its unsolved problems. Topics only, never which
 * problem has which.
 */
export function TopicMap({
	topics,
	list,
	listName,
}: {
	topics: TopicRow[];
	/** The list's plan; each topic narrows it. */
	list: Plan;
	listName: string;
}) {
	const [all, setAll] = useState(false);
	const shown = all ? topics : topics.slice(0, SHOWN);
	const most = topics[0]?.weight || 1;
	return (
		<Panel
			id="topic-map"
			title="Topic map"
			note={`Every topic of ${listName}, most asked first, and how much of it you covered with cards or in the judge.`}
			className="md:col-span-2 lg:col-span-3"
		>
			<Table className="table-fixed">
				<TableHeader>
					<TableRow>
						<TableHead className="w-auto">Topic</TableHead>
						<TableHead className="hidden w-[18%] md:table-cell">
							Asked
						</TableHead>
						<TableHead className="w-[38%] sm:w-[24%]">Covered</TableHead>
						<TableHead className="hidden w-24 text-right sm:table-cell">
							Cards
						</TableHead>
						<TableHead className="hidden w-20 text-right sm:table-cell">
							Solved
						</TableHead>
						<TableHead className="w-12 sm:w-32">
							<span className="sr-only">Practice</span>
						</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					{shown.map((t) => {
						const cards = t.recall === null ? "—" : percent(t.recall);
						return (
							<TableRow key={t.topic}>
								<TableCell className="whitespace-normal">
									<Link
										to="/"
										search={{ set: "all", topic: t.topic }}
										className="font-medium hover:text-primary hover:underline"
										title={`Study ${t.topic} cards`}
									>
										{t.topic}
									</Link>
									<p className="text-xs text-muted-foreground sm:hidden">
										{cards} on cards · {t.solved} solved
									</p>
								</TableCell>
								<TableCell className="hidden md:table-cell">
									<ProgressBar value={t.weight / most} className="h-1.5" />
									<span className="sr-only">
										{percent(t.weight / most)} of the most asked topic
									</span>
								</TableCell>
								<TableCell>
									<div className="flex items-center gap-2">
										<ProgressBar
											value={t.covered / t.problems}
											className="h-1.5 flex-1"
										/>
										<span className="shrink-0 text-xs text-muted-foreground tabular-nums">
											{t.covered}/{t.problems}
										</span>
									</div>
								</TableCell>
								<TableCell className="hidden text-right tabular-nums sm:table-cell">
									{cards}
								</TableCell>
								<TableCell className="hidden text-right tabular-nums sm:table-cell">
									{t.solved}
								</TableCell>
								<TableCell className="text-right">
									<PracticeButton
										plan={{ ...list, topic: t.topic, status: "unsolved" }}
										variant="outline"
										size="xs"
										subject={t.topic}
										iconOnPhone
									/>
								</TableCell>
							</TableRow>
						);
					})}
				</TableBody>
			</Table>
			{topics.length > SHOWN && (
				<Button
					variant="link"
					size="xs"
					className="mt-2 self-start px-0"
					onClick={() => setAll((a) => !a)}
				>
					{all ? "Show fewer" : `Show all ${topics.length} topics`}
				</Button>
			)}
		</Panel>
	);
}
