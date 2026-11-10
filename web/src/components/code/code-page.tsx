import { getRouteApi, Link } from "@tanstack/react-router";
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
import { ActionButton, ICON_ON_PHONE } from "@/components/action-button";
import type { CodeEditorHandle } from "@/components/code/code-editor";
import { RunResultView, SubmitResultView } from "@/components/code/results";
import { SubmissionChart } from "@/components/code/submission-chart";
import { SubmissionList } from "@/components/code/submission-list";
import { NextPanel } from "@/components/plan/next-panel";
import { PlanChip } from "@/components/plan/plan-chip";
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
import { useFitScreen } from "@/hooks/use-media";
import { useShown } from "@/hooks/use-shown";
import { api, messageOf } from "@/lib/api";
import { companyName } from "@/lib/companies";
import { cpuTime } from "@/lib/format";
import type { Plan } from "@/lib/plan";
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

const route = getRouteApi("/code/$slug");

const CodeEditor = lazy(async () => ({
	default: (await import("@/components/code/code-editor")).CodeEditor,
}));

/**
 * CodeMirror is most of this page's code, so it loads once the statement is on screen, and
 * starts only once its pane shows (on a phone, when you open the Code tab); until then an
 * empty box of the same size holds its place.
 */
function DeferredCodeEditor(props: ComponentProps<typeof CodeEditor>) {
	const painted = useAfterPaint();
	const box = useRef<HTMLDivElement>(null);
	const shown = useShown(box);
	const placeholder = <div ref={box} className={props.className} />;
	if (!painted || !shown) return placeholder;
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
 * results and submissions on the right (one at a time below `lg`). The draft saves itself.
 * Remount it (key by slug) for another problem.
 */
export function CodePage({ card, code, submissions: initial }: CodePageData) {
	const { problem } = card;
	const { slug } = problem;
	const starter = code.starter ?? "";
	const supported = code.judge.supported;

	const companies = useCompanies();
	const company = useCompany();
	// The root route's company and the page's own plan params.
	const plan: Plan = route.useSearch();
	const navigate = route.useNavigate();
	// The plan is remembered once the learner settles on a change, not on every pick.
	const planSave = useAutosave(
		(next: Plan) => api.rememberPlan(next).then(() => undefined),
		1500,
	);
	const changePlan = (next: Plan) => {
		navigate({
			search: (prev) => ({ ...prev, ...next }),
			replace: true,
			resetScroll: false,
		});
		planSave.schedule(next);
	};
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

	/** Where the page scrolls, brings the result panel into view once it renders. */
	const panel = useRef<HTMLDivElement>(null);
	const fit = useFitScreen();
	const showPanel = () =>
		!fit &&
		requestAnimationFrame(() =>
			panel.current?.scrollIntoView({ block: "nearest", behavior: "smooth" }),
		);

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
		showPanel();
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
							"justify-self-start text-muted-foreground max-sm:col-span-2",
						)}
						title="Back to the study queue"
					>
						<ArrowLeftIcon data-icon="inline-start" />
						Study · {companyName(companies, company)}
					</Link>
					<span className="text-sm text-muted-foreground max-sm:col-span-2">
						Python 3{supported && ` · ${judgeSummary(code.judge)}`}
					</span>
				</>
			}
		>
			<ProblemCard
				problem={problem}
				actions={
					<>
						<PlanChip plan={plan} onChange={changePlan} />
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
							className="h-[50svh] min-h-64 fit:h-auto fit:min-h-0 fit:flex-[3]"
						/>
						<div
							ref={panel}
							className="flex scroll-mt-16 scroll-mb-16 flex-col gap-2 border-t border-dashed px-4 py-2 sm:px-6 fit:min-h-0 fit:flex-[2]"
						>
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
							<div className="fit:min-h-0 fit:flex-1 fit:overflow-y-auto">
								{tab === "testcase" && (
									<TestcasePanel
										value={testcase}
										onChange={setTestcase}
										custom={custom}
										onUseExamples={() => setTestcase(examples)}
									/>
								)}
								{tab === "result" && (
									<ResultPanel
										key={runs}
										busy={busy}
										outcome={outcome}
										plan={plan}
										slug={slug}
									/>
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
					<div className="flex items-center gap-1 sm:gap-2">
						<Button
							variant="ghost"
							size="sm"
							disabled={!code.starter || swapping}
							onClick={() => swapVersion("reset")}
							title="Replace your code with the starter code; Restore previous brings it back"
							className={ICON_ON_PHONE}
						>
							<RotateCcwIcon data-icon="inline-start" />
							<span className="max-sm:sr-only">Reset</span>
						</Button>
						<Button
							variant="ghost"
							size="sm"
							disabled={previous === null || swapping}
							onClick={() => swapVersion("restore")}
							title={restoreTitle(previous, starter)}
							className={ICON_ON_PHONE}
						>
							<HistoryIcon data-icon="inline-start" />
							<span className="max-sm:sr-only">Restore previous</span>
						</Button>
						<span
							className="min-w-0 flex-1 truncate text-xs text-muted-foreground"
							aria-live="polite"
						>
							{SAVE_TEXT[draft.status]}
						</span>
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
				name="testcase"
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
	plan,
	slug,
}: {
	busy: Job | null;
	outcome: Outcome | null;
	/** After an accepted submission, the plan whose next problem to offer. */
	plan: Plan;
	slug: string;
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
			return (
				<div className="space-y-3">
					<SubmitResultView result={outcome.result} />
					{outcome.result.verdict === "accepted" && (
						<NextPanel plan={plan} slug={slug} />
					)}
				</div>
			);
		case "error":
			return (
				<p role="alert" className="text-sm text-destructive">
					{outcome.message}
				</p>
			);
	}
}
