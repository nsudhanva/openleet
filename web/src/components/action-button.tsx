import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button";
import { Kbd } from "@/components/ui/kbd";

/** A button that shows its keyboard shortcut (hidden on a phone). */
export function ActionButton({
	label,
	shortcut,
	children,
	...props
}: ComponentProps<typeof Button> & { label: string; shortcut: string }) {
	return (
		<Button {...props}>
			{children}
			{label}
			<Kbd className="hidden sm:inline-flex">{shortcut}</Kbd>
		</Button>
	);
}
