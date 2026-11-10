import type { SearchSchemaInput } from "@tanstack/react-router";
import {
	createFileRoute,
	Link,
	stripSearchParams,
	useRouter,
} from "@tanstack/react-router";
import { CodeXmlIcon, RotateCcwIcon, SearchIcon } from "lucide-react";
import { useRef, useState } from "react";
import { CompanyPicker } from "@/components/company-picker";
import { CompanyChip } from "@/components/company-tags";
import { ConfirmClear } from "@/components/confirm-clear";
import { DifficultyBadge } from "@/components/difficulty-badge";
import { ListBadge } from "@/components/list-badge";
import { PageHeader } from "@/components/page-header";
import { PagerControls } from "@/components/pager";
import { PremiumBadge } from "@/components/premium-badge";
import { Segmented } from "@/components/segmented";
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
import { usePager } from "@/hooks/use-pager";
import { useSearch } from "@/hooks/use-search";
import { api } from "@/lib/api";
import { ANY_COMPANY, companyName } from "@/lib/companies";
import { pageTitle, percent, timeFrom } from "@/lib/format";
import {
	isAskedPeriod,
	PERIOD_LABEL,
	PERIOD_PHRASE,
	PERIODS,
	type Period,
	type ProblemRow,
} from "@/lib/types";
import { cn } from "@/lib/utils";

const DEFAULT_PERIOD: Period = "6m";

/** The list shown: `period` here, the company from the root route. */
function parsePeriod(search: { period?: Period } & SearchSchemaInput): {
	period: Period;
} {
	const period = PERIODS.find((p) => p === search.period) ?? DEFAULT_PERIOD;
	return { period };
}

export const Route = createFileRoute("/problems")({
	validateSearch: parsePeriod,
	search: { middlewares: [stripSearchParams({ period: DEFAULT_PERIOD })] },
	loaderDeps: ({ search: { company, period } }) => ({ company, period }),
	head: () => ({ meta: [{ title: pageTitle("Problems") }] }),
	// The server returns the list already in its order.
	loader: ({ deps }) => api.problems(deps),
	component: Problems,
});

/** Company tags a row shows before folding the rest into "+n". */
const ROW_TAGS = 3;

/** The API's largest page; a query rarely matches more, so the pager counts all matches. */
const SEARCH_LIMIT = 1000;

const PERIOD_OPTIONS = PERIODS.map((value) => ({
	value,
	label: PERIOD_LABEL[value],
}));

function formatFrequency(row: ProblemRow): string {
	return row.frequency ? String(Math.round(row.frequency)) : "";
}

/** "Meta asked in the last 30 days", "LC 1–1000": what the list holds, for its summary. */
function describeList(count: number, company: string, period: Period): string {
	if (!isAskedPeriod(period))
		return `${count} LeetCode problems numbered 1 to 1000, in order; frequency is the highest any company gives.`;
	const who = company === ANY_COMPANY ? "any listed company" : company;
	return `${count} problems ${who} asked ${PERIOD_PHRASE[period]}, most frequent first.`;
}

function statusText(row: ProblemRow): string {
	if (row.status === "new") return "";
	if (row.status === "due" || row.due === null) return "Due now";
	return `Due ${timeFrom(row.due)}`;
}

function Problems() {
	const rows = Route.useLoaderData();
	const { company, period } = Route.useSearch();
	const navigate = Route.useNavigate();
	const companies = useCompanies();
	const router = useRouter();
	const [query, setQuery] = useState("");
	const tableArea = useRef<HTMLDivElement>(null);
	const pageSize = useFitRows(tableArea);

	const hits = useSearch(query, SEARCH_LIMIT);
	// A search shows only problems in the chosen list.
	const bySlug = new Map(rows.map((r) => [r.slug, r]));
	const results = query.trim()
		? hits.flatMap((hit) => {
				const row = bySlug.get(hit.slug);
				return row ? [{ row, snippet: hit.snippet }] : [];
			})
		: rows.map((row) => ({ row, snippet: null }));
	const choose = (next: { company?: string; period?: Period }) => {
		pager.reset();
		navigate({ search: (prev) => ({ ...prev, ...next }) });
	};

	const pager = usePager(Math.ceil(results.length / pageSize), true);
	const first = pager.page * pageSize;
	const visible = results.slice(first, first + pageSize);

	async function reset(slug: string) {
		await api.clearProgress({ slug });
		await router.invalidate();
	}

	return (
		<div className="flex h-full min-h-0 flex-col">
			<PageHeader
				title="Problems"
				actions={
					<div className="flex w-full flex-wrap items-center gap-2 sm:w-auto">
						<CompanyPicker
							value={company}
							disabled={!isAskedPeriod(period)}
							onChange={(next) => choose({ company: next })}
						/>
						<Segmented
							label="Problem list"
							value={period}
							options={PERIOD_OPTIONS}
							onChange={(next) => choose({ period: next })}
							className="flex-wrap"
						/>
						<div className="relative w-full sm:w-72">
							<SearchIcon
								className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground"
								aria-hidden
							/>
							<Input
								value={query}
								onChange={(e) => {
									setQuery(e.target.value);
									pager.reset();
								}}
								placeholder="Number, title, topic, or problem text"
								aria-label="Search problems"
								className="bg-card pl-8"
							/>
						</div>
					</div>
				}
			>
				{describeList(rows.length, companyName(companies, company), period)}{" "}
				Topics stay hidden unless you search for one.
			</PageHeader>

			<div
				ref={tableArea}
				className="min-h-0 flex-1 overflow-hidden rounded-sm bg-card shadow-[0_1px_0_var(--border)]"
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
						{visible.map(({ row, snippet }) => (
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
										search={{ set: "all", period, slug: row.slug }}
										className="flex items-baseline gap-2 font-medium hover:text-primary hover:underline"
									>
										<span className="max-w-full shrink-0 truncate">
											{row.title}
										</span>
										{row.premium && <PremiumBadge />}
										{snippet && (
											<span className="hidden min-w-0 truncate text-xs font-normal text-muted-foreground md:inline">
												{snippet}
											</span>
										)}
									</Link>
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
									<Link
										to="/code/$slug"
										params={{ slug: row.slug }}
										className={cn(
											buttonVariants({ variant: "ghost", size: "icon-xs" }),
											"text-muted-foreground",
										)}
										aria-label={`Code ${row.title}`}
										title="Solve it in Python"
									>
										<CodeXmlIcon />
									</Link>
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
						No problem matches “{query}”.
					</p>
				)}
			</div>

			<nav
				aria-label="Pages"
				className="flex items-center justify-end gap-2 pt-2 text-sm text-muted-foreground tabular-nums"
			>
				{results.length > 0 &&
					`${first + 1}–${first + visible.length} of ${results.length}`}
				<PagerControls pager={pager} className="gap-2" />
			</nav>
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
