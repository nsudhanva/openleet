import { createFileRoute } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { PageHeader } from "@/components/page-header";
import { Kbd } from "@/components/ui/kbd";
import { pageTitle } from "@/lib/format";

export const Route = createFileRoute("/about")({
	head: () => ({ meta: [{ title: pageTitle("About") }] }),
	component: About,
});

const SHORTCUTS: [string, string][] = [
	["Enter", "Show the answer"],
	["H", "Show the hint (costs a quarter of the topic score)"],
	["S", "Skip the card for an hour"],
	["1", "Visit again: back in 10 minutes"],
	["2", "Got it: next box (1, 3, 7, 16, 35, 90 days)"],
	["3", "Visit less often: two boxes up, double wait"],
	["B", "Back: hide the answer, or go to the previous card"],
	["M", "Write your own answer; it shows on the card from then on"],
	["C", "Every company that asked the problem, with its ranks; choose one"],
	["← →", "Turn the pages of a long statement"],
	["/ or ⌘K", "Search by number, title, topic or text"],
	["⌘↵", "Code page: run the examples or your test case"],
	["⌘⇧↵", "Code page: submit against every test"],
];

function Section({ title, children }: { title: string; children: ReactNode }) {
	return (
		<section className="space-y-2">
			<h2 className="font-semibold tracking-tight">{title}</h2>
			<div className="space-y-2 text-sm text-muted-foreground [&_a]:text-primary [&_a]:underline [&_code]:font-mono [&_strong]:text-foreground">
				{children}
			</div>
		</section>
	);
}

function About() {
	return (
		<div className="flex h-full min-h-0 flex-col">
			<PageHeader title="About">
				OpenLeet is LeetCode practice: flashcards and a Python judge for the
				problems top tech companies ask, and for every problem numbered 1 to
				1000.
			</PageHeader>
			<div className="grid gap-x-10 gap-y-6 rounded-sm bg-card p-5 shadow-[0_1px_0_var(--border)] lg:grid-cols-3">
				<div className="space-y-6">
					<Section title="How a card works">
						<p>
							Pick the topics you think the problem uses, open the hint if you
							are stuck, then show the answer. The card scores your guess
							against LeetCode's tags and shows a short approach. Grade yourself{" "}
							<strong>Visit again</strong>, <strong>Got it</strong> or{" "}
							<strong>Visit less often</strong>; the grade decides when the card
							returns and which list it joins.
						</p>
						<dl className="grid grid-cols-[auto_1fr] items-center gap-x-3 gap-y-1.5">
							{SHORTCUTS.map(([key, action]) => (
								<div key={key} className="contents">
									<dt>
										<Kbd>{key}</Kbd>
									</dt>
									<dd>{action}</dd>
								</div>
							))}
						</dl>
					</Section>
				</div>
				<div className="space-y-6">
					<Section title="Companies and lists">
						<p>
							Choose a company, or <strong>Any company</strong>, and a period:
							the problems it asked in the last 30 days, 3 months, 6 months, or
							at any time. Each list is a subset of the next and starts with the
							problem the company asks most. <strong>LC 1–1000</strong> holds
							every problem numbered 1 to 1000, in order, for any company. The
							company follows you between pages.
						</p>
					</Section>
					<Section title="Scoring">
						<p>
							Each graded card scores half its topic guess (F1 against the tags,
							less a quarter per hint) and half your grade. Mastery fades with
							time since the last review. <strong>Readiness</strong> weights
							mastery by how often the selected company asked each problem in
							the last 6 months.
						</p>
					</Section>
					<Section title="The judge">
						<p>
							Every problem has a code page, and most have tests.{" "}
							<strong>Run</strong> runs your Python 3 solution on the
							statement's examples or on your own input. <strong>Submit</strong>{" "}
							runs the examples, hidden tests and generated stress tests of
							maximum size against a CPU time limit set from reference
							solutions. A reference counts only if it reproduces every example;
							a test is kept only if all references agree on it. Your draft
							saves itself; <strong>Reset</strong> goes back to the starter code
							and <strong>Restore previous</strong> brings back the code it
							replaced.
						</p>
					</Section>
				</div>
				<div className="space-y-6">
					<Section title="Approaches and hints">
						<p>
							Approaches and hints cover the problems Google asked in the six
							months before they were written; other cards show the statement
							and topics only. Claude wrote every approach and hint. Claude
							agents and Codex CLI reviewed them, and every disagreement was
							settled by hand. Hints never name the technique you are guessing.
							They can still be wrong; check the LeetCode editorial when
							something looks off.
						</p>
					</Section>
					<Section title="API">
						<p>
							The app serves JSON under <code>/api</code>:{" "}
							<code>GET /api/companies</code>, <code>GET /api/search?q=</code>,{" "}
							<code>GET /api/problems?company=&amp;period=</code>,{" "}
							<code>GET /api/problems/:slug</code>, <code>GET /api/deck</code>,{" "}
							<code>POST /api/attempts</code>, <code>DELETE /api/progress</code>
							, <code>GET /api/report?company=</code>, and for code{" "}
							<code>GET /api/code/:slug</code>, <code>POST /api/run</code>,{" "}
							<code>POST /api/submit</code> and{" "}
							<code>GET /api/submissions</code>.
						</p>
					</Section>
					<Section title="Sources">
						<p>
							Company lists, frequency and topics:{" "}
							<a href="https://github.com/liquidslr/leetcode-company-wise-problems">
								liquidslr/leetcode-company-wise-problems
							</a>
							. Statements:{" "}
							<a href="https://github.com/doocs/leetcode">doocs/leetcode</a>, CC
							BY-SA 4.0, premium problems included. Test inputs:{" "}
							<a href="https://huggingface.co/datasets/newfacade/LeetCodeDataset">
								LeetCodeDataset
							</a>
							, Apache-2.0, and the statements' examples.
						</p>
					</Section>
				</div>
			</div>
		</div>
	);
}
