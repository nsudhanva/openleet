import { toggleVariants } from "@/components/ui/toggle";
import { cn } from "@/lib/utils";

/**
 * A small one-of-N switch of plain toggle buttons (each `aria-pressed`), light enough to
 * render several per page. Clicking the active option keeps it, unless `deselectable`, when
 * it clears the choice to null.
 */
type SegmentedProps<T extends string> = {
	label: string;
	options: { value: T; label: string }[];
	className?: string;
	itemClassName?: string;
} & (
	| { deselectable?: false; value: T; onChange: (value: T) => void }
	| { deselectable: true; value: T | null; onChange: (value: T | null) => void }
);

export function Segmented<T extends string>(props: SegmentedProps<T>) {
	const { label, value, options, className, itemClassName } = props;
	function choose(option: T) {
		if (!props.deselectable) props.onChange(option);
		else props.onChange(option === props.value ? null : option);
	}
	return (
		// biome-ignore lint/a11y/useSemanticElements: a group of toggle buttons, not a form fieldset
		<div
			role="group"
			aria-label={label}
			className={cn("flex w-fit items-center gap-2", className)}
		>
			{options.map((option) => (
				<button
					key={option.value}
					type="button"
					aria-pressed={option.value === value}
					onClick={() => choose(option.value)}
					className={cn(
						"shrink-0",
						toggleVariants({ variant: "outline", size: "sm" }),
						itemClassName,
					)}
				>
					{option.label}
				</button>
			))}
		</div>
	);
}
