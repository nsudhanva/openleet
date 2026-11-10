import { ListIcon } from "lucide-react";
import {
	lazy,
	Suspense,
	useLayoutEffect,
	useMemo,
	useRef,
	useState,
} from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useCompanies, useCompany } from "@/hooks/use-companies";
import { useHotkeys } from "@/hooks/use-hotkeys";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import {
	askedSummary,
	type CompanyRanking,
	rankCompanies,
} from "@/lib/companies";
import type { AskedPeriod, Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

const loadDialog = () => import("@/components/companies-dialog");
const CompaniesDialog = lazy(async () => ({
	default: (await loadDialog()).CompaniesDialog,
}));

/** Space between chips, px (Tailwind gap-1). */
const GAP = 4;

/**
 * Frequency as a sequential tint of one hue (the primary), lightest for the rarest. Text
 * stays in the foreground color, which keeps 4.5:1 on every step in both themes.
 */
const FREQUENCY_TINT = [
	"bg-[color-mix(in_oklab,var(--primary)_8%,var(--card))]",
	"bg-[color-mix(in_oklab,var(--primary)_16%,var(--card))]",
	"bg-[color-mix(in_oklab,var(--primary)_24%,var(--card))]",
	"bg-[color-mix(in_oklab,var(--primary)_34%,var(--card))]",
];

function tintOf(frequency: number): string {
	const step = Math.min(3, Math.floor(frequency / 25));
	return FREQUENCY_TINT[step];
}

/**
 * Who asked a problem, in one line that never wraps: the selected company first with its
 * rank, then the others by how often they ask it (tinted by frequency), as many as fit.
 * The button at the end (or C) opens every company with its ranks per period.
 */
export function CompanyTags({
	asked,
	period,
	className,
}: {
	asked: Problem["companies"];
	period: AskedPeriod;
	className?: string;
}) {
	const companies = useCompanies();
	const selected = useCompany();
	const ranked = useMemo(
		() => rankCompanies(asked, companies, selected, period),
		[asked, companies, selected, period],
	);
	const { used, use, prefetchProps } = useLoadOnUse(loadDialog);
	const [open, setOpen] = useState(false);
	const show = () => {
		use();
		setOpen(true);
	};
	useHotkeys(ranked.length ? { c: show } : {});

	if (!ranked.length) return null;
	return (
		<div className={cn("flex min-w-0 items-center gap-1", className)}>
			{/* Remount on a new order, so the chips are measured again. */}
			<FittedChips
				key={ranked.map((r) => r.slug).join()}
				ranked={ranked}
				selected={selected}
				onOverflow={show}
				prefetchProps={prefetchProps}
			/>
			{used && (
				<Suspense fallback={null}>
					<CompaniesDialog
						open={open}
						onOpenChange={setOpen}
						ranked={ranked}
						period={period}
						selected={selected}
					/>
				</Suspense>
			)}
		</div>
	);
}

function FittedChips({
	ranked,
	selected,
	onOverflow,
	prefetchProps,
}: {
	ranked: CompanyRanking[];
	selected: string;
	onOverflow: () => void;
	prefetchProps: ReturnType<typeof useLoadOnUse>["prefetchProps"];
}) {
	const list = useRef<HTMLUListElement>(null);
	const more = useRef<HTMLButtonElement>(null);
	// Every chip renders for the first measurement; the layout effect trims before paint.
	const [shown, setShown] = useState(ranked.length);

	useLayoutEffect(() => {
		const element = list.current;
		const box = element?.parentElement;
		if (!element || !box) return;
		const widths = [...element.children].map(
			(chip) => chip.getBoundingClientRect().width,
		);
		// The box's width comes from the header, not from the chips, so it is safe to watch.
		const trim = () => {
			const room = box.clientWidth - (more.current?.offsetWidth ?? 0) - GAP;
			let used = 0;
			let count = 0;
			for (const width of widths) {
				used += width + (count ? GAP : 0);
				if (used > room) break;
				count++;
			}
			setShown(count);
		};
		trim();
		const observer = new ResizeObserver(trim);
		observer.observe(box);
		return () => observer.disconnect();
	}, []);

	const hidden = ranked.length - shown;
	const label = `All ${ranked.length} ${ranked.length === 1 ? "company" : "companies"}`;
	return (
		<>
			<ul
				ref={list}
				aria-label="Asked by"
				className="flex h-5 min-w-0 items-center gap-1 overflow-hidden"
			>
				{ranked.map((row, i) => (
					<li
						key={row.slug}
						className={cn("flex shrink-0", i >= shown && "hidden")}
					>
						<CompanyChip
							name={row.name}
							selected={row.slug === selected}
							rank={
								row.slug === selected && row.stat
									? `#${row.stat.rank} · ${row.statPeriod}`
									: undefined
							}
							frequency={row.stat?.frequency}
							title={askedSummary(row.name, row.asked)}
						/>
					</li>
				))}
			</ul>
			<Button
				ref={more}
				variant="ghost"
				size="xs"
				className="shrink-0 px-1.5 text-muted-foreground tabular-nums"
				aria-label={hidden ? `+${hidden}, ${label}` : label}
				aria-haspopup="dialog"
				aria-keyshortcuts="C"
				title={`${label} (C)`}
				onClick={onOverflow}
				{...prefetchProps}
			>
				{hidden ? `+${hidden}` : <ListIcon />}
			</Button>
		</>
	);
}

/**
 * A company's tag. The selected company's is filled and can carry its rank ("#3 · 6m");
 * the others are tinted by `frequency`, how often they ask the problem.
 */
export function CompanyChip({
	name,
	selected,
	rank,
	frequency = 0,
	title,
}: {
	name: string;
	selected: boolean;
	rank?: string;
	frequency?: number;
	title?: string;
}) {
	return (
		<Badge
			variant={selected ? "default" : "outline"}
			className={cn(
				"font-normal tabular-nums",
				!selected && ["border-transparent text-foreground", tintOf(frequency)],
			)}
			title={title}
		>
			{name}
			{rank && ` ${rank}`}
		</Badge>
	);
}
