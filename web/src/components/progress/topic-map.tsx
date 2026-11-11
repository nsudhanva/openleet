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
import { MIN_TOPIC_CARDS, shownTopics } from "@/lib/insights";
import type { Plan } from "@/lib/plan";
import type { TopicRow } from "@/lib/types";

/**
 * The list's topics, most problems first: how many problems each has, how much of it you
 * covered on cards or in the judge, how often you named it on this list's cards, and what you
 * solved. Topics with fewer than three problems wait for "Show all". Practice opens a topic's
 * unsolved problems. Topics only, never which problem has which.
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
	const shown = shownTopics(topics, all);
	return (
		<Panel
			id="topic-map"
			title="Topic map"
			note={`Every topic of ${listName}, most problems first, and how much of it you covered with cards or in the judge.`}
			className="md:col-span-2 lg:col-span-3"
		>
			<Table className="table-fixed">
				<TableHeader>
					<TableRow>
						<TableHead className="w-auto">Topic</TableHead>
						<TableHead className="hidden w-20 text-right md:table-cell">
							Problems
						</TableHead>
						<TableHead
							className="w-[38%] sm:w-[24%]"
							title="Problems graded on a card or solved in the judge"
						>
							Covered
						</TableHead>
						<TableHead
							className="hidden w-32 text-right sm:table-cell"
							title={`Graded cards of this list with the topic that named it; shown from ${MIN_TOPIC_CARDS} cards`}
						>
							Named on cards
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
						const named = t.named === null ? "—" : `${t.named}/${t.graded}`;
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
										{t.named === null
											? `${t.solved} solved`
											: `named ${named} on cards · ${t.solved} solved`}
									</p>
								</TableCell>
								<TableCell className="hidden text-right tabular-nums md:table-cell">
									{t.problems}
								</TableCell>
								<TableCell>
									<div
										className="flex items-center gap-2"
										title={`${t.covered} of ${t.problems} graded or solved`}
									>
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
									{named}
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
			{(all || shown.length < topics.length) && (
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
