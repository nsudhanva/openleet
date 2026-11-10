import { ChevronDownIcon, ListChecksIcon } from "lucide-react";
import { type ComponentProps, lazy, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { useCompanies } from "@/hooks/use-companies";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { companyName } from "@/lib/companies";
import { type Plan, planChipLabel } from "@/lib/plan";
import { cn } from "@/lib/utils";

const loadEditor = () => import("@/components/plan/plan-editor");
const PlanEditor = lazy(async () => ({
	default: (await loadEditor()).PlanEditor,
}));

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
			title="Practice plan: what Next offers after a solve"
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
	const label = planChipLabel(plan, (slug) => companyName(companies, slug));
	const { used, use, prefetchProps } = useLoadOnUse(loadEditor);
	const button = <PlanButton label={label} {...prefetchProps} onClick={use} />;
	if (!used) return button;
	return (
		<Suspense fallback={button}>
			<PlanEditor plan={plan} label={label} onChange={onChange} defaultOpen />
		</Suspense>
	);
}
