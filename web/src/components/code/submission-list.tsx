import { VerdictBadge } from "@/components/code/verdict";
import { cpuTime, timeFrom } from "@/lib/format";
import type { SubmissionSummary } from "@/lib/types";

/** Your submissions, newest first; choosing one loads its code into the editor. */
export function SubmissionList({
	submissions,
	loading,
	onOpen,
}: {
	submissions: SubmissionSummary[];
	/** The submission whose code is loading. */
	loading: number | null;
	onOpen: (id: number) => void;
}) {
	if (!submissions.length)
		return (
			<p className="text-sm text-muted-foreground">
				No submissions yet. Submit to run every test.
			</p>
		);
	return (
		<ul className="divide-y">
			{submissions.map((s) => (
				<li key={s.id}>
					<button
						type="button"
						disabled={loading !== null}
						onClick={() => onOpen(s.id)}
						title="Load this code into the editor"
						className="flex w-full items-center gap-3 px-1 py-1.5 text-left text-sm hover:bg-muted/60 disabled:opacity-60"
					>
						<VerdictBadge verdict={s.verdict} />
						<span className="text-muted-foreground tabular-nums">
							{s.passed} / {s.total}
						</span>
						<span className="text-muted-foreground tabular-nums">
							{cpuTime(s.cpuMs)}
						</span>
						<span className="ml-auto text-xs text-muted-foreground">
							{loading === s.id ? "Loading…" : timeFrom(s.at)}
						</span>
					</button>
				</li>
			))}
		</ul>
	);
}
