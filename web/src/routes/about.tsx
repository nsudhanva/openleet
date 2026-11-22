import { createFileRoute } from "@tanstack/react-router";
import {
	ArrowBigUpIcon,
	ArrowLeftIcon,
	ArrowRightIcon,
	CommandIcon,
	CornerDownLeftIcon,
	type LucideIcon,
} from "lucide-react";
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
	["N", "Code page: the next problem of your plan, solved or not"],
];

/**
 * Key symbols the text fonts lack, drawn as icons: a glyph from a fallback font costs the
 * first layout about 10 ms (a phone's first screen shows them), an icon nothing.
 */
const KEY_ICONS: Record<string, [LucideIcon, string]> = {
	"⌘": [CommandIcon, "Command"],
	"⇧": [ArrowBigUpIcon, "Shift"],
	"↵": [CornerDownLeftIcon, "Enter"],
	"←": [ArrowLeftIcon, "Left"],
	"→": [ArrowRightIcon, "Right"],
};

function KeyLabel({ keys }: { keys: string }) {
	return [...keys].map((char, i) => {
		const icon = KEY_ICONS[char];
		if (!icon) return char;
		const [Icon, name] = icon;
		return (
			// biome-ignore lint/suspicious/noArrayIndexKey: the characters of a fixed string never reorder
			<span key={i}>
				<Icon aria-hidden />
				<span className="sr-only">{name}</span>
			</span>
		);
	});
}

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
				Self-hosted LeetCode practice with company problem lists, flashcards,
				and a Python judge.
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
										<Kbd>
											<KeyLabel keys={key} />
										</Kbd>
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
							<strong>Readiness</strong> covers the selected company's 100
							most-asked problems of the last 6 months (of all time when its
							6-month list has fewer than 25), each weighted by how often the
							company asks it. A problem earns 60% for a clean solve in the
							judge (half for a shaky one) and 40% for a card graded Got it or
							Visit less often that is not overdue (half while it is overdue by
							less than its interval).
						</p>
						<p>
							A topic guess scores F1 against the card's tags. The Progress page
							rates a topic once 5 graded cards carried it.
						</p>
					</Section>
					<Section title="The judge">
						<p>
							Every problem has a code editor, and most include automated tests.{" "}
							<strong>Run</strong> executes your Python 3 solution against the
							statement examples or custom input. <strong>Submit</strong> runs
							examples, hidden tests, and max-size stress tests under a CPU time
							limit calibrated from reference solutions. Drafts auto-save;{" "}
							<strong>Reset</strong> restores the starter code and{" "}
							<strong>Restore previous</strong> brings back the code it
							replaced.
						</p>
						<p>
							<strong>Next</strong> (next to the plan chip) opens the next
							problem in your active practice plan, solved or not. Use the plan
							chip to adjust filters or order, or switch to a related plan after
							an Accepted submission. Pin plans from the Problems page to keep
							them.
						</p>
						<p>
							<strong>Your lists</strong> store custom problem sets. Add
							problems via <strong>Add to list</strong> on a problem page or by
							selecting rows on the Problems page. Problems stay in insertion
							order, and Next follows that order. Use a list's menu to rename or
							delete it.
						</p>
					</Section>
				</div>
				<div className="space-y-6">
					<Section title="Approaches and hints">
						<p>
							Selected problems include a written approach and hints; other
							cards show the problem statement and topics. Hints avoid naming
							the technique you are recalling. Check the LeetCode editorial if
							anything looks off.
						</p>
					</Section>
					<Section title="Accounts">
						<p>
							Sign in with an email and password. Progress, notes, drafts,
							plans, and custom lists are scoped to your account. Delete your
							account from the Account page to permanently remove all data.
						</p>
					</Section>
					<Section title="API">
						<p>
							JSON endpoints live under <code>/api</code>, including{" "}
							<code>/api/companies</code>, <code>/api/search</code>,{" "}
							<code>/api/problems</code>, <code>/api/deck</code>,{" "}
							<code>/api/attempts</code>, <code>/api/report</code>,{" "}
							<code>/api/code/:slug</code>, <code>/api/run</code>,{" "}
							<code>/api/submit</code>, and <code>/api/submissions</code>.
						</p>
					</Section>
					<Section title="Sources">
						<p>
							Company lists, frequency, and topics:{" "}
							<a href="https://github.com/liquidslr/leetcode-company-wise-problems">
								liquidslr/leetcode-company-wise-problems
							</a>
							. Statements:{" "}
							<a href="https://github.com/doocs/leetcode">doocs/leetcode</a> (CC
							BY-SA 4.0, including premium problems). Test inputs:{" "}
							<a href="https://huggingface.co/datasets/newfacade/LeetCodeDataset">
								LeetCodeDataset
							</a>{" "}
							(Apache-2.0) and statement examples. Videos:{" "}
							<a href="https://neetcode.io">neetcode.io</a>, Greg Hogg, and
							top-viewed YouTube walkthroughs.
						</p>
					</Section>
				</div>
			</div>
		</div>
	);
}
