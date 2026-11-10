import { useEffect, useEffectEvent, useState } from "react";
import {
	FilterButton,
	FilterButtonText,
	type FilterOption,
	type FilterPickerProps,
} from "@/components/filter-picker";
import {
	Combobox,
	ComboboxContent,
	ComboboxEmpty,
	ComboboxInput,
	ComboboxItem,
	ComboboxList,
	ComboboxTrigger,
	ComboboxValue,
} from "@/components/ui/combobox";

type Loaded = FilterOption[] | "error" | null;

/**
 * The choices: given, or loaded for the current `key`. While a new key loads, the last
 * choices stay, so the open list does not flash empty; an answer for an old key is dropped.
 */
function useOptions(
	options: FilterPickerProps["options"],
	key: string | undefined,
): Loaded {
	const [loaded, setLoaded] = useState<Loaded>(null);
	const load = useEffectEvent(() =>
		typeof options === "function" ? options() : null,
	);
	useEffect(() => {
		const request = load();
		if (!request) return;
		let current = true;
		request.then(
			(items) => current && setLoaded(items),
			(error: unknown) => {
				if (!current) return;
				console.error(`Could not load the options for ${key}`, error);
				setLoaded("error");
			},
		);
		return () => {
			current = false;
		};
	}, [key]);
	return Array.isArray(options) ? options : loaded;
}

/** The picker behind `FilterPicker`, loaded on first use. */
export function FilterCombobox({
	label,
	noun,
	value,
	valueLabel,
	options,
	optionsKey,
	onChange,
	disabled = false,
	className,
	defaultOpen = false,
}: FilterPickerProps & { defaultOpen?: boolean }) {
	const loaded = useOptions(options, optionsKey);
	const items = Array.isArray(loaded) ? loaded : [];
	const selected = items.find((o) => o.value === value) ?? {
		value,
		label: valueLabel,
		count: null,
	};
	const one = label.toLowerCase();

	return (
		<Combobox
			items={items}
			value={selected}
			onValueChange={(next: FilterOption | null) =>
				next && onChange(next.value)
			}
			itemToStringLabel={(o: FilterOption) => o.label}
			isItemEqualToValue={(a: FilterOption, b: FilterOption) =>
				a.value === b.value
			}
			disabled={disabled}
			// Typing highlights the first match, so Enter picks it.
			autoHighlight
			defaultOpen={defaultOpen}
		>
			<ComboboxTrigger
				render={
					<FilterButton
						aria-label={`${label}: ${selected.label}`}
						title={selected.label}
						className={className}
						withChevron={false}
					/>
				}
			>
				<FilterButtonText>
					<ComboboxValue />
				</FilterButtonText>
			</ComboboxTrigger>
			<ComboboxContent className="min-w-60">
				<ComboboxInput
					showTrigger={false}
					placeholder={`Search ${noun}`}
					aria-label={`Search ${noun}`}
				/>
				<ComboboxEmpty>
					{loaded === null
						? `Loading ${noun}…`
						: loaded === "error"
							? `Could not load the ${noun}.`
							: `No ${one} matches.`}
				</ComboboxEmpty>
				<ComboboxList>
					{(option: FilterOption) => (
						<ComboboxItem key={option.value} value={option}>
							{option.label}
							{option.count !== null && (
								<span className="ml-auto pl-3 text-xs text-muted-foreground tabular-nums">
									{option.count}
									<span className="sr-only">
										{option.count === 1 ? " problem" : " problems"}
									</span>
								</span>
							)}
						</ComboboxItem>
					)}
				</ComboboxList>
			</ComboboxContent>
		</Combobox>
	);
}
