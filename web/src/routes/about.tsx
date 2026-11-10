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
				Flashcards for the LeetCode problems Google asked in the last six
				months. Read the problem, name its topics, then check the approach.
			</PageHeader>
			<div className="grid gap-x-10 gap-y-6 rounded-sm bg-card p-5 shadow-[0_1px_0_var(--border)] lg:grid-cols-2">
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
					<Section title="Scoring">
						<p>
							Each graded card scores half its topic guess (F1 against the tags,
							less a quarter per hint) and half your grade. Mastery fades with
							time since the last review. <strong>Readiness</strong> weights
							mastery by how often Google asks each problem.
						</p>
					</Section>
				</div>
				<div className="space-y-6">
					<Section title="Approaches and hints">
						<p>
							Claude wrote every approach and hint. Claude agents reviewed each
							approach against the problem and the doocs/leetcode reference
							solution. Codex CLI gave an independent second opinion on every
							approach and most hints; a separate Claude reviewer covered the
							hints Codex could not reach. Every disagreement was settled by
							hand. Hints never name the technique you are guessing. They can
							still be wrong; check the LeetCode editorial when something looks
							off.
						</p>
					</Section>
					<Section title="API">
						<p>
							The app serves JSON under <code>/api</code>:{" "}
							<code>GET /api/search?q=</code>, <code>GET /api/problems</code>,{" "}
							<code>GET /api/problems/:slug</code>, <code>GET /api/deck</code>,{" "}
							<code>POST /api/attempts</code>, <code>DELETE /api/progress</code>
							, <code>GET /api/report</code>, and for code{" "}
							<code>GET /api/code/:slug</code>, <code>POST /api/run</code>,{" "}
							<code>POST /api/submit</code> and{" "}
							<code>GET /api/submissions</code>.
						</p>
					</Section>
					<Section title="Sources">
						<p>
							Problem list, frequency and topics:{" "}
							<a href="https://github.com/liquidslr/leetcode-company-wise-problems">
								liquidslr/leetcode-company-wise-problems
							</a>{" "}
							(Google, six months). Statements:{" "}
							<a href="https://github.com/doocs/leetcode">doocs/leetcode</a>, CC
							BY-SA 4.0. Premium statements are not included.
						</p>
					</Section>
				</div>
			</div>
		</div>
	);
}
