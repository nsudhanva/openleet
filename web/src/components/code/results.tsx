import { CheckIcon, MinusIcon, XIcon } from "lucide-react";
import { type ReactNode, useState } from "react";
import { VerdictBadge } from "@/components/code/verdict";
import { Button } from "@/components/ui/button";
import { cpuTime } from "@/lib/format";
import type {
	FailingCase,
	RunCase,
	RunResult,
	SubmitResult,
	TestKind,
} from "@/lib/types";
import { cn } from "@/lib/utils";

/** A labeled monospace block: input, output, stdout or a traceback. */
function CodeBlock({
	label,
	text,
	danger = false,
}: {
	label: string;
	text: string;
	danger?: boolean;
}) {
	return (
		<div className="space-y-1">
			<h4 className="text-xs font-medium text-muted-foreground">{label}</h4>
			<pre
				className={cn(
					"overflow-x-auto rounded-md bg-muted px-3 py-2 font-mono text-xs leading-relaxed whitespace-pre-wrap",
					danger && "bg-destructive-wash text-destructive",
				)}
			>
				{text || " "}
			</pre>
		</div>
	);
}

function CaseDetails({
	test,
	ok,
}: {
	test: Omit<RunCase, "ok">;
	ok: boolean | null;
}) {
	return (
		<div className="space-y-2">
			<CodeBlock label="Input" text={test.input} />
			<CodeBlock
				label="Output"
				text={test.output ?? "(no output)"}
				danger={ok === false}
			/>
			{test.expected !== null && (
				<CodeBlock label="Expected" text={test.expected} />
			)}
			{test.stdout && <CodeBlock label="Stdout" text={test.stdout} />}
		</div>
	);
}

function Mark({ ok }: { ok: boolean | null }) {
	if (ok === null)
		return (
			<MinusIcon className="text-muted-foreground" aria-label="Not checked" />
		);
	return ok ? (
		<CheckIcon className="text-success" aria-label="Passed" />
	) : (
		<XIcon className="text-destructive" aria-label="Failed" />
	);
}

function Summary({
	verdict,
	children,
}: {
	verdict: RunResult["verdict"];
	children: ReactNode;
}) {
	return (
		<div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
			<VerdictBadge verdict={verdict} heading />
			<span className="text-sm text-muted-foreground tabular-nums">
				{children}
			</span>
		</div>
	);
}

/** Run: the verdict over the examples (or your test case), then each case in turn. */
export function RunResultView({ result }: { result: RunResult }) {
	const [index, setIndex] = useState(0);
	const current = result.cases[Math.min(index, result.cases.length - 1)];
	return (
		<div className="space-y-3">
			<Summary verdict={result.verdict}>
				Runtime {cpuTime(result.cpuMs)}
			</Summary>
			{result.error && <CodeBlock label="Error" text={result.error} danger />}
			{result.cases.length > 0 && (
				<div
					className="flex flex-wrap gap-1.5"
					role="tablist"
					aria-label="Cases"
				>
					{result.cases.map((test, i) => (
						<Button
							// biome-ignore lint/suspicious/noArrayIndexKey: cases are a fixed list, numbered by position
							key={i}
							role="tab"
							aria-selected={i === index}
							variant={i === index ? "secondary" : "ghost"}
							size="xs"
							onClick={() => setIndex(i)}
						>
							<Mark ok={test.ok} />
							Case {i + 1}
						</Button>
					))}
				</div>
			)}
			{current && <CaseDetails test={current} ok={current.ok} />}
		</div>
	);
}

const KIND_LABEL: Record<TestKind, string> = {
	example: "an example",
	hidden: "a hidden test",
	stress: "a large stress test",
};

function FailingTest({ test }: { test: FailingCase }) {
	return (
		<section className="space-y-2">
			<h3 className="text-sm font-semibold">
				Failed on {KIND_LABEL[test.kind]}
			</h3>
			<CaseDetails test={test} ok={false} />
		</section>
	);
}

/** Submit: verdict, tests passed, CPU time against the limit, and the first failing test. */
export function SubmitResultView({ result }: { result: SubmitResult }) {
	return (
		<div className="space-y-3">
			<Summary verdict={result.verdict}>
				{result.passed} / {result.total} tests passed · CPU {result.cpuMs} ms of{" "}
				{cpuTime(result.limitMs)} limit
			</Summary>
			{result.error && <CodeBlock label="Error" text={result.error} danger />}
			{result.failing && <FailingTest test={result.failing} />}
		</div>
	);
}
