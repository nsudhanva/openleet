import { ChevronDownIcon } from "lucide-react";
import { lazy, Suspense } from "react";
import { selectTriggerClassName } from "@/components/ui/select-trigger";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { cn } from "@/lib/utils";

/** The trigger's look, the same before and after the list loads. */
export const PICKER_CLASS = "bg-card max-sm:w-full";

/** The trigger's accessible name, which includes its text: "Problem list: Asked in 6 months". */
export function pickerName<T extends string | null>({
	label,
	value,
	items,
}: SelectPickerProps<T>): string {
	const chosen = items.find((item) => item.value === value)?.label;
	return chosen ? `${label}: ${chosen}` : label;
}

const loadMenu = () => import("@/components/select-picker-menu");
const SelectPickerMenu = lazy(async () => ({
	default: (await loadMenu()).SelectPickerMenu,
})) as typeof import("@/components/select-picker-menu").SelectPickerMenu;

export interface SelectPickerProps<T extends string | null> {
	label: string;
	value: T;
	items: { value: T; label: string }[];
	onChange: (value: T) => void;
	className?: string;
}

/**
 * A small select, as wide as a phone's filter grid cell (filters go two to a row there). The
 * list loads on first use, so until then this is a button that looks like the select's
 * trigger and shows the chosen item.
 */
export function SelectPicker<T extends string | null>(
	props: SelectPickerProps<T>,
) {
	const { used, use, prefetchProps } = useLoadOnUse(loadMenu);
	const placeholder = (
		<button
			type="button"
			aria-label={pickerName(props)}
			data-size="sm"
			className={cn(selectTriggerClassName, PICKER_CLASS, props.className)}
			{...prefetchProps}
			onClick={use}
		>
			<span data-slot="select-value" className="flex flex-1 text-left">
				{props.items.find((item) => item.value === props.value)?.label}
			</span>
			<ChevronDownIcon className="pointer-events-none size-4 text-muted-foreground" />
		</button>
	);
	if (!used) return placeholder;
	return (
		<Suspense fallback={placeholder}>
			<SelectPickerMenu {...props} defaultOpen />
		</Suspense>
	);
}
