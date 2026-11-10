import { Link } from "@tanstack/react-router";
import { NotebookTextIcon, RotateCcwIcon } from "lucide-react";
import { type ReactNode, useMemo, useRef, useState } from "react";
import { ActionButton } from "@/components/action-button";
import {
	CodeEditor,
	type CodeEditorHandle,
} from "@/components/code/code-editor";
import { RunResultView, SubmitResultView } from "@/components/code/results";
import { SubmissionList } from "@/components/code/submission-list";
import { CARD_SURFACE, ProblemHeader } from "@/components/problem-header";
import { ProblemStatement } from "@/components/problem-statement";
import { Segmented } from "@/components/segmented";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { type SaveStatus, useAutosave } from "@/hooks/use-autosave";
import { useModKeys } from "@/hooks/use-hotkeys";
import { api, messageOf } from "@/lib/api";
import { examplesToTestcase } from "@/lib/testcase";
import { TONE } from "@/lib/tones";
import type {
	CodeInfo,
	RunResult,
	StudyCard,
	SubmissionSummary,
	SubmitResult,
} from "@/lib/types";
import { cn } from "@/lib/utils";

export interface CodePageData {
	card: StudyCard;
	code: CodeInfo;
	submissions: SubmissionSummary[];
}

type Tab = "testcase" | "result" | "submissions";
type Job = "run" | "submit";
type Outcome =
	| { kind: "run"; result: RunResult }
	| { kind: "submit"; result: SubmitResult }
	| { kind: "error"; message: string };

const TABS: { value: Tab; label: string }[] = [
	{ value: "testcase", label: "Testcase" },
	{ value: "result", label: "Result" },
	{ value: "submissions", label: "Submissions" },
];

const SAVE_TEXT: Record<SaveStatus, string> = {
	idle: "",
	pending: "Saving draft…",
	saving: "Saving draft…",
	saved: "Draft saved",
	failed: "Draft not saved",
};

function judgeSummary({
	examples,
	hidden,
	stress,
	timeLimitMs,
}: CodeInfo["judge"]) {
	const limit = timeLimitMs ? `, ${timeLimitMs} ms CPU limit` : "";
	return `Submit runs ${examples} examples, ${hidden} hidden and ${stress} stress tests${limit}.`;
}

/**
 * Solve one problem in Python: the statement on the left, the editor with its test case,
 * results and submissions on the right (stacked on a phone). The draft saves itself.
 * Remount it (key by slug) for another problem.
 */
export function CodePage({ card, code, submissions: initial }: CodePageData) {
	const { problem } = card;
	const { slug } = problem;
	const starter = code.starter ?? "";
	const supported = code.judge.supported;

	const editor = useRef<CodeEditorHandle>(null);
	const source = useRef(code.draft ?? starter);
	const draft = useAutosave((text: string, keepalive) =>
		// Code back at the starter is no draft at all.
		api.saveDraft(slug, text === starter ? "" : text, keepalive),
	);

	const examples = useMemo(
		() => examplesToTestcase(code.examples),
		[code.examples],
	);
	const [testcase, setTestcase] = useState(examples);
	const custom = testcase.trim() !== examples.trim();

	const [tab, setTab] = useState<Tab>("testcase");
	const [busy, setBusy] = useState<Job | null>(null);
	const [outcome, setOutcome] = useState<Outcome | null>(null);
	const [runs, setRuns] = useState(0);
	const [solved, setSolved] = useState(code.solved);
	const [submissions, setSubmissions] = useState(initial);
	const [opening, setOpening] = useState<number | null>(null);

	function edit(text: string) {
		source.current = text;
		draft.schedule(text);
	}

	async function judge(job: Job) {
		if (!supported || busy) return;
		setBusy(job);
		setTab("result");
		try {
			if (job === "run") {
				const input = custom ? testcase : undefined;
				const result = await api.run(slug, source.current, input);
				setOutcome({ kind: "run", result });
			} else {
				const result = await api.submit(slug, source.current);
				setOutcome({ kind: "submit", result });
				if (result.verdict === "accepted") setSolved(true);
				api
					.submissions(slug)
					.then(setSubmissions, (error: unknown) =>
						console.error("Could not reload submissions", error),
					);
			}
		} catch (error) {
			setOutcome({ kind: "error", message: messageOf(error) });
		} finally {
			setRuns((n) => n + 1);
			setBusy(null);
		}
	}

	async function openSubmission(id: number) {
		setOpening(id);
		try {
			editor.current?.setValue((await api.submission(id)).code);
			editor.current?.focus();
		} catch (error) {
			setOutcome({ kind: "error", message: messageOf(error) });
			setTab("result");
		} finally {
			setOpening(null);
		}
	}

	useModKeys({
		Enter: () => judge("run"),
		"Shift+Enter": () => judge("submit"),
	});

	return (
		<article
			aria-labelledby="problem-title"
			className={cn(
				"flex min-h-0 flex-col lg:h-full lg:overflow-hidden",
				CARD_SURFACE,
			)}
		>
			<ProblemHeader problem={problem}>
				{solved && (
					<Badge className={cn("font-semibold", TONE.success)}>Solved</Badge>
				)}
				<Link
					to="/"
					search={{ set: "all", slug }}
					className={cn(
						buttonVariants({ variant: "ghost", size: "xs" }),
						"text-muted-foreground",
					)}
					title="Back to the flashcard"
				>
					<NotebookTextIcon data-icon="inline-start" />
					Card
				</Link>
			</ProblemHeader>

			<div className="grid min-h-0 flex-1 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)]">
				<section
					aria-label="Statement"
					className="flex h-[60dvh] min-h-0 flex-col px-4 py-3 sm:px-6 lg:h-auto"
				>
					<ProblemStatement problem={problem} arrowKeys />
				</section>

				<section
					aria-label="Solution"
					className="flex min-h-0 flex-col border-t border-dashed lg:border-t-0 lg:border-l"
				>
					<CodeEditor
						ref={editor}
						initial={source.current}
						onChange={edit}
						label="Python 3 solution"
						className="h-[55dvh] min-h-0 lg:h-auto lg:flex-[3]"
					/>
					<div className="flex h-96 min-h-0 flex-col gap-2 border-t border-dashed px-4 py-2 sm:px-6 lg:h-auto lg:flex-[2]">
						<Segmented
							label="Panel"
							value={tab}
							options={TABS}
							onChange={setTab}
						/>
						{!supported && (
							<p
								role="note"
								className="rounded-md border border-warning/40 bg-warning-wash px-3 py-2 text-sm text-warning"
							>
								Run and Submit are off for this problem
								{code.judge.reason ? `: ${code.judge.reason}` : "."}
							</p>
						)}
						<div className="min-h-0 flex-1 overflow-y-auto">
							{tab === "testcase" && (
								<TestcasePanel
									value={testcase}
									onChange={setTestcase}
									custom={custom}
									onUseExamples={() => setTestcase(examples)}
									summary={supported ? judgeSummary(code.judge) : null}
								/>
							)}
							{tab === "result" && (
								<ResultPanel key={runs} busy={busy} outcome={outcome} />
							)}
							{tab === "submissions" && (
								<SubmissionList
									submissions={submissions}
									loading={opening}
									onOpen={openSubmission}
								/>
							)}
						</div>
					</div>
				</section>
			</div>

			<footer className="flex flex-wrap items-center gap-2 border-t px-4 py-2 sm:px-6">
				<span className="text-xs font-medium text-muted-foreground">
					Python 3
				</span>
				<span className="text-xs text-muted-foreground" aria-live="polite">
					{SAVE_TEXT[draft.status]}
				</span>
				<Button
					variant="ghost"
					size="sm"
					disabled={!code.starter}
					onClick={() => editor.current?.setValue(starter)}
					title="Replace your code with the starter code (⌘Z undoes it)"
				>
					<RotateCcwIcon data-icon="inline-start" />
					Reset to starter
				</Button>
				<div className="ml-auto flex gap-2">
					<ActionButton
						variant="outline"
						label={busy === "run" ? "Running…" : "Run"}
						shortcut="⌘↵"
						disabled={!supported || busy !== null}
						onClick={() => judge("run")}
					/>
					<ActionButton
						label={busy === "submit" ? "Submitting…" : "Submit"}
						shortcut="⌘⇧↵"
						disabled={!supported || busy !== null}
						onClick={() => judge("submit")}
					/>
				</div>
			</footer>
		</article>
	);
}

function TestcasePanel({
	value,
	onChange,
	custom,
	onUseExamples,
	summary,
}: {
	value: string;
	onChange: (value: string) => void;
	custom: boolean;
	onUseExamples: () => void;
	summary: string | null;
}) {
	return (
		<div className="flex h-full min-h-40 flex-col gap-1.5">
			<p className="flex flex-wrap items-center gap-x-2 text-xs text-muted-foreground">
				One JSON value per line, one line per parameter; put more cases after
				it. Run uses these lines.
				{custom && (
					<Button
						variant="link"
						size="xs"
						className="h-auto px-0"
						onClick={onUseExamples}
					>
						Use the examples again
					</Button>
				)}
			</p>
			<Textarea
				aria-label="Test case input"
				value={value}
				spellCheck={false}
				onChange={(event) => onChange(event.target.value)}
				className="min-h-0 flex-1 resize-none bg-transparent font-mono text-xs [field-sizing:fixed] md:text-xs"
			/>
			{summary && <p className="text-xs text-muted-foreground">{summary}</p>}
		</div>
	);
}

function ResultPanel({
	busy,
	outcome,
}: {
	busy: Job | null;
	outcome: Outcome | null;
}): ReactNode {
	if (busy)
		return (
			<p className="text-sm text-muted-foreground" aria-live="polite">
				{busy === "run" ? "Running your code…" : "Judging every test…"}
			</p>
		);
	if (!outcome)
		return (
			<p className="text-sm text-muted-foreground">
				Run your code to see its output here.
			</p>
		);
	switch (outcome.kind) {
		case "run":
			return <RunResultView result={outcome.result} />;
		case "submit":
			return <SubmitResultView result={outcome.result} />;
		case "error":
			return (
				<p role="alert" className="text-sm text-destructive">
					{outcome.message}
				</p>
			);
	}
}
