import { useNavigate } from "@tanstack/react-router";
import { CheckIcon } from "lucide-react";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";
import type { CompanyRanking } from "@/lib/companies";
import {
	ASKED_PERIODS,
	type Asked,
	type AskedPeriod,
	PERIOD_LABEL,
} from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * Every company that asked a problem, with its rank and frequency in each period, most
 * relevant first (as the card's tags). Choosing one makes it the selected company. A bottom
 * sheet on a phone, a dialog elsewhere; it traps focus and gives it back on close.
 */
export function CompaniesDialog({
	open,
	onOpenChange,
	ranked,
	period,
	selected,
}: {
	open: boolean;
	onOpenChange: (open: boolean) => void;
	ranked: CompanyRanking[];
	period: AskedPeriod;
	selected: string;
}) {
	const navigate = useNavigate();
	function choose(company: string) {
		onOpenChange(false);
		navigate({ to: ".", search: (prev) => ({ ...prev, company }) });
	}

	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent className="gap-3 sm:max-w-2xl max-sm:top-auto max-sm:bottom-0 max-sm:max-w-none max-sm:translate-y-0 max-sm:rounded-b-none">
				<DialogHeader>
					<DialogTitle>
						Asked by {ranked.length}{" "}
						{ranked.length === 1 ? "company" : "companies"}
					</DialogTitle>
					<DialogDescription>
						Rank and frequency (0 to 100) in each list, sorted by the{" "}
						{PERIOD_LABEL[period].toLowerCase()} list. Choose a company to study
						its lists.
					</DialogDescription>
				</DialogHeader>
				<div className="max-h-[60dvh] overflow-y-auto">
					<table className="w-full text-sm">
						<thead className="sticky top-0 bg-popover text-xs text-muted-foreground">
							<tr>
								<th scope="col" className="py-1.5 pr-2 text-left font-medium">
									Company
								</th>
								{ASKED_PERIODS.map((p) => (
									<th
										key={p}
										scope="col"
										aria-sort={p === period ? "descending" : undefined}
										className={cn(
											"w-20 px-2 py-1.5 text-left font-medium",
											p === period && "text-foreground",
										)}
									>
										{PERIOD_LABEL[p]}
									</th>
								))}
							</tr>
						</thead>
						<tbody>
							{ranked.map((row) => (
								<tr
									key={row.slug}
									className="cursor-pointer border-t hover:bg-muted/60"
									onClick={() => choose(row.slug)}
								>
									<th scope="row" className="py-1 pr-2 text-left font-normal">
										<button
											type="button"
											className="flex items-center gap-1.5 rounded-sm font-medium outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
											aria-current={row.slug === selected || undefined}
											onClick={(event) => {
												// The row handles the click; the button gives keyboard access.
												event.stopPropagation();
												choose(row.slug);
											}}
										>
											{row.name}
											{row.slug === selected && (
												<CheckIcon className="size-3.5" aria-label="selected" />
											)}
										</button>
									</th>
									{ASKED_PERIODS.map((p) => (
										<td key={p} className="px-2 py-1">
											<RankCell stat={row.asked[p]} />
										</td>
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</DialogContent>
		</Dialog>
	);
}

/** "#3" over a small bar as long as the frequency; a dash when it is not on that list. */
function RankCell({ stat }: { stat: Asked | undefined }) {
	if (!stat)
		return (
			<span className="text-muted-foreground">
				<span aria-hidden>—</span>
				<span className="sr-only">not listed</span>
			</span>
		);
	return (
		<div className="space-y-0.5">
			<div className="flex items-baseline justify-between gap-1 tabular-nums">
				<span>#{stat.rank}</span>
				<span className="text-xs text-muted-foreground">
					<span className="sr-only">frequency </span>
					{Math.round(stat.frequency)}
				</span>
			</div>
			<div aria-hidden className="h-1 rounded-full bg-primary/15">
				<div
					className="h-full rounded-full bg-primary"
					style={{ width: `${stat.frequency}%` }}
				/>
			</div>
		</div>
	);
}
