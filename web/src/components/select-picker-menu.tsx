import type { SelectPickerProps } from "@/components/select-picker";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";

/** The select behind `SelectPicker`, loaded on first use. */
export function SelectPickerMenu<T extends string | null>({
	label,
	value,
	items,
	onChange,
	defaultOpen = false,
}: SelectPickerProps<T> & { defaultOpen?: boolean }) {
	return (
		<Select
			value={value}
			items={items}
			onValueChange={(next) => onChange(next as T)}
			defaultOpen={defaultOpen}
		>
			<SelectTrigger aria-label={label} size="sm" className="bg-card">
				<SelectValue />
			</SelectTrigger>
			<SelectContent>
				{items.map((item) => (
					<SelectItem key={item.value ?? ""} value={item.value}>
						{item.label}
					</SelectItem>
				))}
			</SelectContent>
		</Select>
	);
}
