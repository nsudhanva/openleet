import {
	PICKER_CLASS,
	pickerName,
	type SelectPickerProps,
} from "@/components/select-picker";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

/** The select behind `SelectPicker`, loaded on first use. */
export function SelectPickerMenu<T extends string | null>({
	defaultOpen = false,
	...props
}: SelectPickerProps<T> & { defaultOpen?: boolean }) {
	const { value, items, onChange, className } = props;
	return (
		<Select
			value={value}
			items={items}
			onValueChange={(next) => onChange(next as T)}
			defaultOpen={defaultOpen}
		>
			<SelectTrigger
				aria-label={pickerName(props)}
				size="sm"
				className={cn(PICKER_CLASS, className)}
			>
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
