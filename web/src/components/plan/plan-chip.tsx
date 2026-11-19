import { ChevronDownIcon, ListChecksIcon } from "lucide-react";
import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button";
import { useCompanies } from "@/hooks/use-companies";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { companyName } from "@/lib/companies";
import { type Plan, planChipLabel } from "@/lib/plan";
import { listNameOf, useUserLists } from "@/lib/user-lists";
import { cn } from "@/lib/utils";

const loadEditor = () => import("@/components/plan/plan-editor");

/** The chip's button: the plan in a few words. */
export function PlanButton({
	label,
	className,
	...props
}: ComponentProps<typeof Button> & { label: string }) {
	return (
		<Button
			variant="outline"
			size="xs"
			aria-label={`Practice plan: ${label}`}
			title="Practice plan: where Next goes"
			className={cn(
				"min-w-0 max-w-full shrink bg-card font-normal text-foreground",
				className,
			)}
			{...props}
		>
			<ListChecksIcon data-icon="inline-start" className="text-primary" />
			<span className="truncate">{label}</span>
			<ChevronDownIcon
				data-icon="inline-end"
				className="text-muted-foreground"
			/>
		</Button>
	);
}

/**
 * The code page's practice plan, as a chip in the problem header; it opens the plan's
 * controls (a popover, a sheet on a phone), whose code loads on first use.
 */
export function PlanChip({
	plan,
	onChange,
}: {
	plan: Plan;
	onChange: (plan: Plan) => void;
}) {
	const companies = useCompanies();
	const lists = useUserLists(plan.list !== undefined);
	const label = planChipLabel(
		plan,
		(slug) => companyName(companies, slug),
		listNameOf(lists),
	);
	const { loaded, use, prefetchProps } = useLoadOnUse(loadEditor);
	if (!loaded)
		return <PlanButton label={label} {...prefetchProps} onClick={use} />;
	return (
		<loaded.PlanEditor
			plan={plan}
			label={label}
			onChange={onChange}
			defaultOpen
		/>
	);
}
