import { Link } from "@tanstack/react-router";
import {
	ArrowLeftIcon,
	CheckIcon,
	HistoryIcon,
	NotebookTextIcon,
	RotateCcwIcon,
} from "lucide-react";
import {
	type ComponentProps,
	lazy,
	type ReactNode,
	Suspense,
	useMemo,
	useRef,
	useState,
} from "react";
import { ActionButton } from "@/components/action-button";
import type { CodeEditorHandle } from "@/components/code/code-editor";
import { RunResultView, SubmitResultView } from "@/components/code/results";
import { SubmissionChart } from "@/components/code/submission-chart";
import { SubmissionList } from "@/components/code/submission-list";
import {
	type Pane,
	ProblemCard,
	ProblemPage,
} from "@/components/problem-frame";
import { Segmented } from "@/components/segmented";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useAfterPaint } from "@/hooks/use-after-paint";
import { type SaveStatus, useAutosave } from "@/hooks/use-autosave";
import { useCompanies, useCompany } from "@/hooks/use-companies";
import { useModKeys } from "@/hooks/use-hotkeys";
import { api, messageOf } from "@/lib/api";
import { companyName } from "@/lib/companies";
import { cpuTime } from "@/lib/format";
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

const CodeEditor = lazy(async () => ({
	default: (await import("@/components/code/code-editor")).CodeEditor,
}));

/**
 * CodeMirror is most of this page's code, so it loads once the statement is on screen; until
 * then an empty box of the same size holds its place.
 */
function DeferredCodeEditor(props: ComponentProps<typeof CodeEditor>) {
	const painted = useAfterPaint();
	const placeholder = <div className={props.className} />;
	if (!painted) return placeholder;
	return (
		<Suspense fallback={placeholder}>
			<CodeEditor {...props} />
		</Suspense>
	);
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

/** Restore's tooltip: what it brings back, by the first two lines the starter lacks. */
function restoreTitle(previous: string | null, starter: string): string {
	if (previous === null)
		return "Nothing to restore: Reset keeps your code here";
	const known = new Set(starter.split("\n").map((line) => line.trim()));
	const own = previous
		.split("\n")
		.map((line) => line.trim())
		.filter((line) => line && !known.has(line));
	const title = "Bring back your code from before the last reset";
	if (!own.length) return title;
	return [
		`${title}:`,
		...own.slice(0, 2),
		...(own.length > 2 ? ["…"] : []),
	].join("\n");
}

/** "3 examples · 34 hidden · 2 stress tests · 9630 ms CPU limit". */
function judgeSummary({
	examples,
	hidden,
	stress,
	timeLimitMs,
}: CodeInfo["judge"]): string {
	return [
		`${examples} examples`,
		`${hidden} hidden`,
		`${stress} stress tests`,
		...(timeLimitMs ? [`${cpuTime(timeLimitMs)} CPU limit`] : []),
	].join(" · ");
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

	const companies = useCompanies();
	const company = useCompany();
	const editor = useRef<CodeEditorHandle>(null);
	const source = useRef(code.draft ?? starter);
	// Code back at the starter is no draft at all: the API takes it as ''.
	const asDraft = (text: string) => (text === starter ? "" : text);
	const draft = useAutosave((text: string, keepalive) =>
		api.saveDraft(slug, asDraft(text), keepalive),
	);
	const [previous, setPrevious] = useState(code.previous);
	const [swapping, setSwapping] = useState(false);

	const examples = useMemo(
		() => examplesToTestcase(code.examples),
		[code.examples],
	);
	const [testcase, setTestcase] = useState(examples);
	const custom = testcase.trim() !== examples.trim();

	const [tab, setTab] = useState<Tab>("testcase");
	const [pane, setPane] = useState<Pane>("problem");
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

	/** Puts `code` in the editor as one undoable change, or keeps it for the editor to start with. */
	function replaceCode(code: string) {
		if (editor.current) {
			editor.current.setValue(code);
			editor.current.focus();
		} else edit(code);
	}

	async function judge(job: Job) {
		if (!supported || busy) return;
		setBusy(job);
		setTab("result");
		setPane("aside");
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
			replaceCode((await api.submission(id)).code);
		} catch (error) {
			setOutcome({ kind: "error", message: messageOf(error) });
			setTab("result");
		} finally {
			setOpening(null);
		}
	}

	/** Reset to the starter or Restore the previous version; the server keeps both. */
	async function swapVersion(action: "reset" | "restore") {
		setSwapping(true);
		try {
			// A pending save must land first, or it could overwrite the new version.
			await draft.flush();
			const current = asDraft(source.current);
			const next = await (action === "reset"
				? api.resetDraft(slug, current)
				: api.restoreDraft(slug, current));
			setPrevious(next.previous);
			// One undoable change, so ⌘Z still brings the replaced code back.
			replaceCode(next.code ?? starter);
		} catch (error) {
			setOutcome({ kind: "error", message: messageOf(error) });
			setTab("result");
		} finally {
			setSwapping(false);
		}
	}

	useModKeys({
		Enter: () => judge("run"),
		"Shift+Enter": () => judge("submit"),
	});

	return (
		<ProblemPage
			toolbar={
				<>
					<Link
						to="/"
						className={cn(
							buttonVariants({ variant: "ghost", size: "sm" }),
							"text-muted-foreground",
						)}
						title="Back to the study queue"
					>
						<ArrowLeftIcon data-icon="inline-start" />
						Study · {companyName(companies, company)}
					</Link>
					<span className="text-sm text-muted-foreground">
						Python 3{supported && ` · ${judgeSummary(code.judge)}`}
					</span>
				</>
			}
		>
			<ProblemCard
				problem={problem}
				actions={
					<>
						{solved && (
							<Badge className={cn("font-semibold", TONE.success)}>
								<CheckIcon className="sm:hidden" aria-hidden />
								<span className="max-sm:sr-only">Solved</span>
							</Badge>
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
							<span className="max-sm:sr-only">Card</span>
						</Link>
					</>
				}
				period="6m"
				pane={pane}
				onPaneChange={setPane}
				asideLabel="Code"
				aside={
					<>
						<DeferredCodeEditor
							ref={editor}
							initial={source.current}
							onChange={edit}
							label="Python 3 solution"
							className="min-h-0 flex-[3]"
						/>
						<div className="flex min-h-0 flex-[2] flex-col gap-2 border-t border-dashed px-4 py-2 sm:px-6">
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
									/>
								)}
								{tab === "result" && (
									<ResultPanel key={runs} busy={busy} outcome={outcome} />
								)}
								{tab === "submissions" && (
									<div className="space-y-2">
										<SubmissionChart
											submissions={submissions}
											timeLimitMs={code.judge.timeLimitMs}
											onOpen={openSubmission}
										/>
										<SubmissionList
											submissions={submissions}
											loading={opening}
											onOpen={openSubmission}
										/>
									</div>
								)}
							</div>
						</div>
					</>
				}
				footer={
					<footer className="flex flex-wrap items-center gap-2 border-t px-4 py-2 sm:px-6">
						<span className="text-xs text-muted-foreground" aria-live="polite">
							{SAVE_TEXT[draft.status]}
						</span>
						<Button
							variant="ghost"
							size="sm"
							disabled={!code.starter || swapping}
							onClick={() => swapVersion("reset")}
							title="Replace your code with the starter code; Restore previous brings it back"
						>
							<RotateCcwIcon data-icon="inline-start" />
							Reset
						</Button>
						<Button
							variant="ghost"
							size="sm"
							disabled={previous === null || swapping}
							onClick={() => swapVersion("restore")}
							title={restoreTitle(previous, starter)}
						>
							<HistoryIcon data-icon="inline-start" />
							Restore previous
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
				}
			/>
		</ProblemPage>
	);
}

function TestcasePanel({
	value,
	onChange,
	custom,
	onUseExamples,
}: {
	value: string;
	onChange: (value: string) => void;
	custom: boolean;
	onUseExamples: () => void;
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
