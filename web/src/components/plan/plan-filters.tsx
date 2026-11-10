import { Segmented } from "@/components/segmented";
import { SelectPicker } from "@/components/select-picker";
import { ORDER_LABEL, STATUS_LABEL } from "@/lib/plan";
import { PLAN_ORDERS, type PlanOrder, type PlanStatus } from "@/lib/types";
import { cn } from "@/lib/utils";

/** All first, as the problem table shows it by default; a plan defaults to Unsolved. */
const STATUS_ORDER: readonly PlanStatus[] = ["all", "unsolved", "untried"];
const STATUS_OPTIONS = STATUS_ORDER.map((value) => ({
	value,
	label: STATUS_LABEL[value],
}));
const ORDER_ITEMS = PLAN_ORDERS.map((value) => ({
	value,
	label: ORDER_LABEL[value],
}));

/**
 * All, Unsolved or Untried: which problems a plan (or the problem table) keeps. On a phone it
 * takes a whole row of the filter grid, its options sharing it, like the difficulty switch.
 */
export function StatusFilter({
	value,
	onChange,
	className,
}: {
	value: PlanStatus;
	onChange: (status: PlanStatus) => void;
	className?: string;
}) {
	return (
		<Segmented<PlanStatus>
			label="Problems to show"
			value={value}
			options={STATUS_OPTIONS}
			onChange={onChange}
			className={cn(
				"max-sm:col-span-2 max-sm:grid max-sm:w-full max-sm:grid-cols-3",
				className,
			)}
			itemClassName="bg-card"
		/>
	);
}

/** The order a plan (or the problem table) walks its problems in. */
export function OrderPicker({
	value,
	onChange,
	className,
}: {
	value: PlanOrder;
	onChange: (order: PlanOrder) => void;
	className?: string;
}) {
	return (
		<SelectPicker<PlanOrder>
			label="Order"
			value={value}
			items={ORDER_ITEMS}
			onChange={onChange}
			className={className}
		/>
	);
}
