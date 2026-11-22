import { useId } from "react";
import { Input } from "@/components/ui/input";

/** A labelled text input; the label stays visible, so it needs no placeholder. */
export function Field({
	label,
	...props
}: { label: string } & React.ComponentProps<typeof Input>) {
	const id = useId();
	return (
		<div className="space-y-1.5">
			<label htmlFor={id} className="text-sm font-medium">
				{label}
			</label>
			<Input id={id} {...props} />
		</div>
	);
}
