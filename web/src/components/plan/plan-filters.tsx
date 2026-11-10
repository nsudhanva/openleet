import { SelectPicker } from "@/components/select-picker";
import { ORDER_LABEL, STATUS_LABEL } from "@/lib/plan";
import { PLAN_ORDERS, type PlanOrder, type PlanStatus } from "@/lib/types";

/** All first, as the problem table shows it by default; a plan defaults to Unsolved. */
const STATUS_ORDER: readonly PlanStatus[] = [
	"all",
	"unsolved",
	"untried",
	"shaky",
];
const STATUS_ITEMS = STATUS_ORDER.map((value) => ({
	value,
	label: STATUS_LABEL[value],
}));
const ORDER_ITEMS = PLAN_ORDERS.map((value) => ({
	value,
	label: ORDER_LABEL[value],
}));

/**
 * Which problems a plan (or the problem table) keeps: all, the unsolved, the untried, or the
 * shaky solves (solved only after failing). A select, so the four fit any screen.
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
		<SelectPicker<PlanStatus>
			label="Problems to show"
			value={value}
			items={STATUS_ITEMS}
			onChange={onChange}
			className={className}
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
