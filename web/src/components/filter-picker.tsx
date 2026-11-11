import { ChevronDownIcon } from "lucide-react";
import { type ComponentProps, lazy, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { cn } from "@/lib/utils";

const loadCombobox = () => import("@/components/filter-combobox");
const FilterCombobox = lazy(async () => ({
	default: (await loadCombobox()).FilterCombobox,
}));

/** One choice of a filter: its URL value, its text, and its problem count (null: none shown). */
export interface FilterOption {
	value: string;
	label: string;
	count: number | null;
}

export interface FilterPickerProps {
	/** What it filters by, such as "Company"; with the chosen option, the accessible name. */
	label: string;
	/** What the list holds, plural, such as "companies": "Search companies". */
	noun: string;
	value: string;
	/** The chosen option's text, shown before the list loads. */
	valueLabel: string;
	/**
	 * The choices, or a loader that the list calls when it opens and again when `optionsKey`
	 * changes. Pointing at the button calls it early, so it should be cached.
	 */
	options: FilterOption[] | (() => Promise<FilterOption[]>);
	/** Names the loaded choices: a new key loads them again. */
	optionsKey?: string;
	/** What the counts count, shown above the choices, such as "Problems asked, all time". */
	countNote?: string;
	onChange: (value: string) => void;
	disabled?: boolean;
	/** Sets the width, which stays the same whatever is chosen, so nothing around it moves. */
	className?: string;
}

/** The picker's button; the combobox draws its own chevron, the placeholder needs one. */
export function FilterButton({
	className,
	withChevron = true,
	children,
	...props
}: ComponentProps<typeof Button> & { withChevron?: boolean }) {
	return (
		<Button
			variant="outline"
			size="sm"
			className={cn("justify-between bg-card font-normal", className)}
			{...props}
		>
			{children}
			{withChevron && (
				<ChevronDownIcon className="pointer-events-none size-4 text-muted-foreground" />
			)}
		</Button>
	);
}

/** The button's text, cut off with an ellipsis so the button keeps its width. */
export function FilterButtonText({ children }: { children: React.ReactNode }) {
	return <span className="min-w-0 truncate">{children}</span>;
}

/**
 * A searchable list of choices with counts, for one filter (companies, topics). Its code and
 * its choices load on first use, so until then it is a plain button with the chosen option.
 */
export function FilterPicker(props: FilterPickerProps) {
	const { options } = props;
	const { used, use, prefetchProps } = useLoadOnUse(() =>
		Promise.all([
			loadCombobox(),
			typeof options === "function" ? options().catch(() => null) : null,
		]),
	);
	const placeholder = (
		<FilterButton
			aria-label={`${props.label}: ${props.valueLabel}`}
			title={props.valueLabel}
			className={props.className}
			disabled={props.disabled}
			{...prefetchProps}
			onClick={use}
		>
			<FilterButtonText>{props.valueLabel}</FilterButtonText>
		</FilterButton>
	);
	if (!used) return placeholder;
	return (
		<Suspense fallback={placeholder}>
			<FilterCombobox {...props} defaultOpen />
		</Suspense>
	);
}
