import {
	createFileRoute,
	Link,
	stripSearchParams,
	useRouter,
	useRouterState,
} from "@tanstack/react-router";
import { CodeXmlIcon, RotateCcwIcon, SearchIcon } from "lucide-react";
import { useEffect, useEffectEvent, useRef, useState } from "react";
import { CompanyPicker } from "@/components/company-picker";
import { CompanyChip } from "@/components/company-tags";
import { ConfirmClear } from "@/components/confirm-clear";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { DifficultyFilter } from "@/components/difficulty-filter";
import { ListBadge } from "@/components/list-badge";
import { PageHeader } from "@/components/page-header";
import { PagerControls } from "@/components/pager";
import { OrderPicker, StatusFilter } from "@/components/plan/plan-filters";
import { PlanLink } from "@/components/plan/plan-link";
import { PracticeButton } from "@/components/plan/practice-button";
import { SavedPlans } from "@/components/plan/saved-plans";
import { PremiumBadge } from "@/components/premium-badge";
import { Segmented } from "@/components/segmented";
import { SelectPicker } from "@/components/select-picker";
import { TopicFilter } from "@/components/topic-filter";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import { useCompanies } from "@/hooks/use-companies";
import { useFitRows } from "@/hooks/use-fit-rows";
import { useFitScreen } from "@/hooks/use-media";
import { usePager } from "@/hooks/use-pager";
import { api } from "@/lib/api";
import { ANY_COMPANY, type CompanySearch, companyName } from "@/lib/companies";
import { pageTitle, percent, timeFrom } from "@/lib/format";
import { tablePlan } from "@/lib/plan";
import {
	cleanQuery,
	PROBLEMS_DEFAULTS,
	type ProblemsSearch,
	parseProblemsSearch,
	problemsQuery,
} from "@/lib/schemas";
import {
	isAskedPeriod,
	PERIOD_OPTIONS,
	PERIOD_PHRASE,
	type Period,
	type PlanOrder,
	type ProblemRow,
} from "@/lib/types";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/problems")({
	validateSearch: parseProblemsSearch,
	search: { middlewares: [stripSearchParams(PROBLEMS_DEFAULTS)] },
	// The server filters, searches and orders; a newer navigation aborts the older request.
	loaderDeps: ({ search }) => problemsQuery(search),
	head: () => ({ meta: [{ title: pageTitle("Problems") }] }),
	loader: async ({ deps, abortController }) => {
		const { signal } = abortController;
		const [rows, plans] = await Promise.all([
			api.problems(deps, signal),
			api.plans(signal),
		]);
		return { rows, plans };
	},
	component: Problems,
});

/** Company tags a row shows before folding the rest into "+n". */
const ROW_TAGS = 3;

/** Rows a page shows where the page scrolls; on a `fit:` screen, as many as fit. */
const SCROLL_PAGE_ROWS = 25;

/** Typing waits this long for a pause before it searches. */
const SEARCH_DEBOUNCE_MS = 150;

function formatFrequency(row: ProblemRow): string {
	return row.frequency ? String(Math.round(row.frequency)) : "";
}

/** How the table is ordered when it is not in list order. */
const ORDER_PHRASE: Record<Exclude<PlanOrder, "rank">, string> = {
	number: "by number",
	"easy-first": "easy first",
	random: "shuffled",
};

/** "Problems Meta asked in the last 30 days, most frequent first": what the list holds. */
function describeList(
	company: string,
	period: Period,
	order: ProblemsSearch["order"],
): string {
	if (!isAskedPeriod(period))
		return `LeetCode problems numbered 1 to 1000, ${order ? ORDER_PHRASE[order] : "in order"}; frequency is the highest any company gives.`;
	const who = company === ANY_COMPANY ? "any listed company" : company;
	return `Problems ${who} asked ${PERIOD_PHRASE[period]}, ${order ? ORDER_PHRASE[order] : "most frequent first"}.`;
}

function statusText(row: ProblemRow): string {
	if (row.status === "new") return "";
	if (row.status === "due" || row.due === null) return "Due now";
	return `Due ${timeFrom(row.due)}`;
}

function Problems() {
	const { rows, plans } = Route.useLoaderData();
	const search = Route.useSearch();
	const { company, period, topic, difficulty, status, order, q } = search;
	const plan = tablePlan(search);
	const navigate = Route.useNavigate();
	const companies = useCompanies();
	const router = useRouter();
	const loading = useRouterState({ select: (s) => s.isLoading });
	const tableArea = useRef<HTMLDivElement>(null);
	const fit = useFitScreen();
	const fitRows = useFitRows(tableArea, fit);
	const pageSize = fit ? fitRows : SCROLL_PAGE_ROWS;

	// Every filter lives in the URL; typing replaces the entry instead of adding one per key.
	const choose = (
		next: Partial<ProblemsSearch & CompanySearch>,
		replace = false,
	) =>
		navigate({
			search: (prev) => ({ ...prev, ...next }),
			replace,
			resetScroll: false,
		});

	// Any change of filter, however it came (a control, Back), starts again at page 1.
	const pager = usePager(
		Math.ceil(rows.length / pageSize),
		true,
		JSON.stringify([company, period, topic, difficulty, status, order, q]),
	);
	const first = pager.page * pageSize;
	const visible = rows.slice(first, first + pageSize);

	// A new page of a long scrolled table starts at its top.
	const shownPage = useRef(pager.page);
	useEffect(() => {
		if (shownPage.current === pager.page) return;
		shownPage.current = pager.page;
		const table = tableArea.current;
		if (table && table.getBoundingClientRect().top < 0)
			table.scrollIntoView({ block: "start" });
	}, [pager.page]);

	async function reset(slug: string) {
		await api.clearProgress({ slug });
		await router.invalidate();
	}

	return (
		<div className="flex flex-col fit:h-full fit:min-h-0">
			<PageHeader title="Problems">
				{describeList(companyName(companies, company), period, order)} Topics
				stay hidden unless you filter or search by one.
			</PageHeader>
			<SavedPlans plans={plans} onChange={() => router.invalidate()} />
			{/* Two to a row on a phone, the search first; one wrapping row from sm. */}
			<div className="mb-3 grid grid-cols-2 gap-2 sm:flex sm:flex-wrap sm:items-center">
				<CompanyPicker
					value={company}
					disabled={!isAskedPeriod(period)}
					onChange={(next) => choose({ company: next })}
				/>
				<SelectPicker<Period>
					label="Problem list"
					value={period}
					items={PERIOD_OPTIONS}
					onChange={(next) => choose({ period: next })}
					className="sm:hidden"
				/>
				<Segmented
					label="Problem list"
					value={period}
					options={PERIOD_OPTIONS}
					onChange={(next) => choose({ period: next })}
					className="flex-wrap max-sm:hidden"
				/>
				<TopicFilter
					value={topic}
					list={{ company, period, difficulty }}
					onChange={(next) => choose({ topic: next })}
					className="max-sm:col-span-2"
				/>
				<DifficultyFilter
					value={difficulty}
					onChange={(next) => choose({ difficulty: next })}
				/>
				<StatusFilter
					value={status ?? "all"}
					onChange={(next) =>
						choose({ status: next === "all" ? undefined : next })
					}
				/>
				<OrderPicker
					value={order ?? "rank"}
					onChange={(next) =>
						choose({ order: next === "rank" ? undefined : next })
					}
				/>
				<div className="flex flex-wrap items-center gap-2 sm:ml-auto">
					<PracticeButton
						plan={plan}
						className="max-sm:w-full"
						title="Solve this list's problems in order, with Next after each one"
					/>
				</div>
				<SearchBox value={q} onChange={(next) => choose({ q: next }, true)} />
			</div>

			<div
				ref={tableArea}
				aria-busy={loading}
				className={cn(
					"scroll-mt-16 rounded-sm bg-card shadow-[0_1px_0_var(--border)] transition-opacity fit:min-h-0 fit:flex-1 fit:overflow-hidden",
					loading && "opacity-60",
				)}
			>
				<Table>
					<TableHeader>
						<TableRow>
							<TableHead className="w-12 text-right">Rank</TableHead>
							<TableHead className="hidden w-14 text-right sm:table-cell">
								Freq.
							</TableHead>
							<TableHead className="w-16">LC</TableHead>
							<TableHead>Problem</TableHead>
							<TableHead className="hidden sm:table-cell">Difficulty</TableHead>
							<TableHead className="hidden xl:table-cell">Asked by</TableHead>
							<TableHead className="hidden md:table-cell">Status</TableHead>
							<TableHead className="hidden text-right md:table-cell">
								Last topics
							</TableHead>
							<TableHead className="w-10">
								<span className="sr-only">Code</span>
							</TableHead>
							<TableHead className="w-10">
								<span className="sr-only">Clear progress</span>
							</TableHead>
						</TableRow>
					</TableHeader>
					<TableBody>
						{visible.map((row) => (
							<TableRow
								key={row.slug}
								// As tall as the icon buttons, so every row is the same height.
								className="h-10"
							>
								<TableCell className="text-right text-muted-foreground tabular-nums">
									{row.rank}
								</TableCell>
								<TableCell className="hidden text-right text-muted-foreground tabular-nums sm:table-cell">
									{formatFrequency(row)}
								</TableCell>
								<TableCell className="text-muted-foreground tabular-nums">
									{row.id}
								</TableCell>
								<TableCell className="w-full max-w-0">
									<Link
										to="/"
										// Studying from here keeps the table's list and filters.
										search={{
											set: "all",
											period,
											topic,
											difficulty,
											slug: row.slug,
										}}
										className="flex items-baseline gap-2 font-medium hover:text-primary hover:underline max-sm:flex-wrap"
									>
										<span className="max-w-full shrink-0 truncate max-sm:shrink max-sm:whitespace-normal">
											{row.title}
										</span>
										{row.premium && <PremiumBadge />}
										{row.snippet && (
											<span className="hidden min-w-0 truncate text-xs font-normal text-muted-foreground md:inline">
												{row.snippet}
											</span>
										)}
									</Link>
									{/* A phone has no room for these columns: they go under the title. */}
									<div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground sm:hidden">
										<DifficultyBadge difficulty={row.difficulty} />
										<ListBadge list={row.list} />
										{statusText(row)}
									</div>
								</TableCell>
								<TableCell className="hidden sm:table-cell">
									<DifficultyBadge difficulty={row.difficulty} />
								</TableCell>
								<TableCell className="hidden xl:table-cell">
									<RowCompanies slugs={row.companies} selected={company} />
								</TableCell>
								<TableCell className="hidden md:table-cell">
									<div className="flex items-center gap-2 text-muted-foreground">
										<ListBadge list={row.list} />
										{statusText(row)}
									</div>
								</TableCell>
								<TableCell className="hidden text-right tabular-nums md:table-cell">
									{row.lastScore === null ? "—" : percent(row.lastScore)}
								</TableCell>
								<TableCell>
									{/* The plan of the table: Next goes on from this row. */}
									<PlanLink
										plan={plan}
										slug={row.slug}
										className={cn(
											buttonVariants({ variant: "ghost", size: "icon-xs" }),
											"text-muted-foreground",
										)}
										aria-label={`Code ${row.title}`}
										title="Solve it in Python"
									>
										<CodeXmlIcon />
									</PlanLink>
								</TableCell>
								<TableCell>
									{row.lastAt && (
										<ConfirmClear
											trigger={
												<Button
													variant="ghost"
													size="icon-xs"
													aria-label={`Clear progress for ${row.title}`}
													title="Clear progress"
												/>
											}
											title={`Clear progress for ${row.title}?`}
											description="This deletes its grades and takes it off your lists. Your own answer stays."
											onClear={() => reset(row.slug)}
										>
											<RotateCcwIcon />
										</ConfirmClear>
									)}
								</TableCell>
							</TableRow>
						))}
					</TableBody>
				</Table>
				{visible.length === 0 && (
					<p className="px-4 py-8 text-center text-muted-foreground">
						{q
							? `No problem in this list matches “${q}”.`
							: "No problem in this list has this topic and difficulty."}
					</p>
				)}
			</div>

			<nav
				aria-label="Pages"
				className="flex items-center justify-end gap-2 pt-2 text-sm text-muted-foreground tabular-nums"
			>
				{rows.length > 0 &&
					`${first + 1}–${first + visible.length} of ${rows.length}`}
				<PagerControls pager={pager} className="gap-2" />
			</nav>
		</div>
	);
}

/**
 * The table's search box. What you type shows at once and goes to the URL (`q`) after a
 * pause; when the URL changes by itself (Back, a link), the box shows its query.
 */
function SearchBox({
	value = "",
	onChange,
}: {
	value: string | undefined;
	onChange: (q: string | undefined) => void;
}) {
	const [draft, setDraft] = useState(value);
	const [shown, setShown] = useState(value);
	if (value !== shown) {
		setShown(value);
		if (value !== draft.trim()) setDraft(value);
	}
	const commit = useEffectEvent((next: string) => {
		if (next !== value) onChange(next || undefined);
	});
	useEffect(() => {
		const timer = setTimeout(
			() => commit(cleanQuery(draft)),
			SEARCH_DEBOUNCE_MS,
		);
		return () => clearTimeout(timer);
	}, [draft]);

	return (
		<div className="relative col-span-2 w-full max-sm:order-first sm:w-64">
			<SearchIcon
				className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground"
				aria-hidden
			/>
			<Input
				type="search"
				value={draft}
				onChange={(e) => setDraft(e.target.value)}
				onKeyDown={(e) => {
					if (e.key === "Enter") commit(cleanQuery(draft));
				}}
				placeholder="Number, title, topic, or problem text"
				aria-label="Search problems"
				className="bg-card pl-8"
			/>
		</div>
	);
}

/** A row's companies, compact: the first few (the selected one first) and "+n". */
function RowCompanies({
	slugs,
	selected,
}: {
	slugs: string[];
	selected: string;
}) {
	const companies = useCompanies();
	const ordered = slugs.includes(selected)
		? [selected, ...slugs.filter((s) => s !== selected)]
		: slugs;
	const rest = ordered.slice(ROW_TAGS);
	return (
		<div className="flex items-center gap-1">
			{ordered.slice(0, ROW_TAGS).map((slug) => (
				<CompanyChip
					key={slug}
					name={companyName(companies, slug)}
					selected={slug === selected}
				/>
			))}
			{rest.length > 0 && (
				<span
					className="text-xs text-muted-foreground tabular-nums"
					title={rest.map((slug) => companyName(companies, slug)).join(", ")}
				>
					+{rest.length}
				</span>
			)}
		</div>
	);
}
