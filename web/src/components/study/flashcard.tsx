import { Link } from "@tanstack/react-router";
import {
	ArrowLeftIcon,
	CodeXmlIcon,
	LightbulbIcon,
	NotebookPenIcon,
	RotateCcwIcon,
	SkipForwardIcon,
} from "lucide-react";
import { useState } from "react";
import { ActionButton } from "@/components/action-button";
import { ConfirmClear } from "@/components/confirm-clear";
import { FitPages } from "@/components/fit-pages";
import { InlineCode } from "@/components/inline-code";
import { type Pane, ProblemCard } from "@/components/problem-frame";
import { Answer } from "@/components/study/answer";
import { CardHistory } from "@/components/study/card-history";
import { MyAnswer } from "@/components/study/my-answer";
import { TopicPicker } from "@/components/study/topic-picker";
import { Button, buttonVariants } from "@/components/ui/button";
import { useHotkeys } from "@/hooks/use-hotkeys";
import type { ListFilters } from "@/lib/schemas";
import { scoreTopics } from "@/lib/scorer";
import type { AskedPeriod, Grade, StudyCard } from "@/lib/types";
import { cn } from "@/lib/utils";

export interface Answered {
	grade: Grade;
	guessed: string[];
	hints: number;
}

const GRADE_ACTIONS: {
	grade: Exclude<Grade, "skip">;
	label: string;
	key: string;
	variant: "outline" | "default";
}[] = [
	{ grade: "again", label: "Visit again", key: "1", variant: "outline" },
	{ grade: "good", label: "Got it", key: "2", variant: "default" },
	{ grade: "less", label: "Visit less often", key: "3", variant: "outline" },
];

/**
 * One problem: the statement on the left, the guess, hint and answer on the right (one at a
 * time below `lg`), and a bar of actions under them. Remount it (key by slug) for a fresh
 * guess.
 */
export function Flashcard({
	card,
	period,
	list,
	topics,
	busy,
	canGoBack,
	onBack,
	onAnswer,
	onSaveNote,
	onClear,
}: {
	card: StudyCard;
	/** The list whose ranks the header shows. */
	period: AskedPeriod;
	/** The list and filters studied, which the code page's practice plan carries on. */
	list: ListFilters;
	topics: string[];
	busy: boolean;
	canGoBack: boolean;
	onBack: () => void;
	onAnswer: (answer: Answered) => void;
	/** Stores your answer and returns what was kept (null once deleted). */
	onSaveNote: (text: string) => Promise<string | null>;
	/** Deletes this problem's grades; your own answer stays. */
	onClear: () => Promise<void>;
}) {
	const { problem, approach, state } = card;
	const hints = approach?.hints ?? [];
	const [guessed, setGuessed] = useState<string[]>([]);
	const [hintsShown, setHintsShown] = useState(0);
	const [revealed, setRevealed] = useState(false);
	const [pane, setPane] = useState<Pane>("problem");
	const [note, setNote] = useState(card.note);
	const [editing, setEditing] = useState(false);

	const toggle = (topic: string) =>
		setGuessed((g) =>
			g.includes(topic) ? g.filter((t) => t !== topic) : [...g, topic],
		);
	const answer = (grade: Grade) =>
		!busy && onAnswer({ grade, guessed, hints: hintsShown });
	const showHint = () => {
		setHintsShown((n) => Math.min(n + 1, hints.length));
		setPane("aside");
	};
	const reveal = () => {
		setRevealed(true);
		setPane("aside");
	};
	const editNote = () => {
		setEditing(true);
		setPane("aside");
	};
	const saveNote = async (text: string) => {
		setNote(await onSaveNote(text));
		setEditing(false);
	};
	const back = () => {
		if (revealed) setRevealed(false);
		else if (canGoBack) onBack();
	};

	useHotkeys({
		b: back,
		m: editNote,
		...(revealed
			? Object.fromEntries(
					GRADE_ACTIONS.map((a) => [a.key, () => answer(a.grade)]),
				)
			: {
					Enter: reveal,
					s: () => answer("skip"),
					...(hintsShown < hints.length && { h: showHint }),
				}),
	});

	return (
		<ProblemCard
			problem={problem}
			period={period}
			actions={
				<>
					<CardHistory state={state} />
					{state && (
						<ConfirmClear
							trigger={
								<Button
									variant="ghost"
									size="icon-xs"
									aria-label="Clear progress for this problem"
									title="Clear progress"
								/>
							}
							title={`Clear progress for ${problem.title}?`}
							description="This deletes its grades and takes it off your lists. Your own answer stays."
							onClear={onClear}
						>
							<RotateCcwIcon />
						</ConfirmClear>
					)}
					<Link
						to="/code/$slug"
						params={{ slug: problem.slug }}
						search={list}
						className={cn(
							buttonVariants({ variant: "ghost", size: "xs" }),
							"text-muted-foreground",
						)}
						title="Solve it in Python"
					>
						<CodeXmlIcon data-icon="inline-start" />
						<span className="max-sm:sr-only">Code</span>
					</Link>
				</>
			}
			pane={pane}
			onPaneChange={setPane}
			asideLabel={revealed ? "Answer" : "Guess"}
			asideClassName="gap-3 px-4 py-3 sm:px-6"
			aside={
				<>
					{revealed ? (
						<FitPages>
							<Answer
								result={scoreTopics(guessed, problem.topics)}
								approach={approach}
							/>
						</FitPages>
					) : (
						<>
							<h2 className="font-semibold">Which topics does it use?</h2>
							<TopicPicker
								topics={topics}
								selected={guessed}
								onToggle={toggle}
							/>
							{hintsShown > 0 && (
								<ul className="space-y-1 rounded-md border border-warning/40 bg-warning-wash px-3 py-2 text-sm text-warning">
									{hints.slice(0, hintsShown).map((hint) => (
										<li key={hint} className="flex gap-2">
											<LightbulbIcon className="mt-0.5 size-4 shrink-0" />
											<span>
												<InlineCode text={hint} />
											</span>
										</li>
									))}
								</ul>
							)}
						</>
					)}
					<MyAnswer
						note={note}
						editing={editing}
						onEdit={editNote}
						onSave={saveNote}
						onCancel={() => setEditing(false)}
					/>
				</>
			}
			footer={
				<div className="flex items-center gap-1 sm:gap-2">
					<ActionButton
						variant="ghost"
						label="Back"
						shortcut="B"
						icon={<ArrowLeftIcon />}
						onClick={back}
						disabled={(!revealed && !canGoBack) || busy}
					/>
					<ActionButton
						variant="ghost"
						label="My answer"
						shortcut="M"
						icon={<NotebookPenIcon />}
						onClick={editNote}
						disabled={editing}
					/>
					{revealed ? (
						// On a phone the grades share the rest of the bar, their labels wrapping.
						<div className="ml-auto grid flex-1 grid-cols-3 gap-1 sm:flex sm:flex-none sm:gap-2">
							{GRADE_ACTIONS.map((a) => (
								<ActionButton
									key={a.grade}
									variant={a.variant}
									label={a.label}
									shortcut={a.key}
									disabled={busy}
									onClick={() => answer(a.grade)}
									className="max-sm:h-auto max-sm:min-h-10 max-sm:px-1 max-sm:leading-tight max-sm:whitespace-normal"
								/>
							))}
						</div>
					) : (
						<>
							<ActionButton
								variant="ghost"
								label="Skip"
								shortcut="S"
								icon={<SkipForwardIcon />}
								onClick={() => answer("skip")}
								disabled={busy}
							/>
							<ActionButton
								variant="outline"
								label={
									hints.length > 1
										? `Hint ${Math.min(hintsShown + 1, hints.length)} of ${hints.length}`
										: "Hint"
								}
								shortcut="H"
								icon={<LightbulbIcon />}
								onClick={showHint}
								disabled={hintsShown >= hints.length}
							/>
							<ActionButton
								className="ml-auto max-sm:flex-1"
								label="Show answer"
								shortcut="Enter"
								onClick={reveal}
							/>
						</>
					)}
				</div>
			}
		/>
	);
}
