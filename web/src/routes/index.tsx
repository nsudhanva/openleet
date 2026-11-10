import {
	createFileRoute,
	Link,
	stripSearchParams,
	useRouter,
} from "@tanstack/react-router";
import { useState } from "react";
import { ProblemPage } from "@/components/problem-frame";
import { type Answered, Flashcard } from "@/components/study/flashcard";
import { StudyBar } from "@/components/study/study-bar";
import { buttonVariants } from "@/components/ui/button";
import { api } from "@/lib/api";
import type { CompanySearch } from "@/lib/companies";
import { STUDY_SETS } from "@/lib/scheduler";
import {
	parseStudySearch,
	STUDY_DEFAULTS,
	type StudySearch,
} from "@/lib/schemas";
import { isAskedPeriod } from "@/lib/types";

export const Route = createFileRoute("/")({
	validateSearch: parseStudySearch,
	search: { middlewares: [stripSearchParams(STUDY_DEFAULTS)] },
	// Every param picks the card; a newer navigation aborts the older request.
	loaderDeps: ({ search }) => search,
	loader: ({ deps, abortController }) => api.deck(deps, abortController.signal),
	component: Study,
});

function Study() {
	const { card, remaining, topics } = Route.useLoaderData();
	const search = Route.useSearch();
	const navigate = Route.useNavigate();
	const router = useRouter();
	const [history, setHistory] = useState<string[]>([]);
	const [busy, setBusy] = useState(false);

	const go = (next: Partial<StudySearch & CompanySearch>) =>
		navigate({ search: (prev) => ({ ...prev, ...next }) });

	async function answer(answered: Answered) {
		if (!card) return;
		setBusy(true);
		try {
			await api.recordAttempt({ slug: card.problem.slug, ...answered });
			setHistory((h) => [...h, card.problem.slug]);
			// A pinned card (opened from the list, or reached with Back) returns to the queue.
			if (search.slug) await go({ slug: undefined });
			else await router.invalidate();
		} finally {
			setBusy(false);
		}
	}

	// Clearing keeps you on the same card, now unseen, instead of moving to the next one.
	async function clear() {
		if (!card) return;
		await api.clearProgress({ slug: card.problem.slug });
		if (search.slug) await router.invalidate();
		else await go({ slug: card.problem.slug });
	}

	function back() {
		const previous = history.at(-1);
		if (!previous) return;
		setHistory((h) => h.slice(0, -1));
		go({ slug: previous });
	}

	return (
		<ProblemPage
			toolbar={<StudyBar search={search} remaining={remaining} onChange={go} />}
		>
			{card ? (
				<Flashcard
					key={`${card.problem.slug}:${card.state?.lastAt ?? 0}`}
					card={card}
					period={isAskedPeriod(search.period) ? search.period : "6m"}
					topics={topics}
					busy={busy}
					canGoBack={history.length > 0}
					onBack={back}
					onAnswer={answer}
					onSaveNote={async (text) =>
						(await api.saveNote(card.problem.slug, text)).note
					}
					onClear={clear}
				/>
			) : (
				<EmptySet setLabel={STUDY_SETS[search.set]} />
			)}
		</ProblemPage>
	);
}

function EmptySet({ setLabel }: { setLabel: string }) {
	return (
		<div className="rounded-sm border border-dashed bg-card/60 px-6 py-14 text-center">
			<h1 className="text-2xl font-semibold tracking-tight">
				Nothing left in “{setLabel}”
			</h1>
			<p className="mx-auto mt-2 max-w-md text-muted-foreground">
				Every card in this set is scheduled for later. Pick another set, or
				study all problems to work ahead.
			</p>
			<div className="mt-6 flex justify-center gap-2">
				<Link to="/" search={{ set: "all" }} className={buttonVariants()}>
					Study all problems
				</Link>
				<Link to="/progress" className={buttonVariants({ variant: "outline" })}>
					See progress
				</Link>
			</div>
		</div>
	);
}
