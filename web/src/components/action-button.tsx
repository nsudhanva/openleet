import type { ComponentProps, ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Kbd } from "@/components/ui/kbd";
import { cn } from "@/lib/utils";

/** A bar button that shows only its icon on a phone, as square as the bar's others. */
export const ICON_ON_PHONE = "max-sm:w-10 max-sm:px-0";

/** A keyboard shortcut's key, shown only where a keyboard is likely: a fine pointer, from sm. */
export function KeyHint({ className, ...props }: ComponentProps<typeof Kbd>) {
	return (
		<Kbd
			className={cn("hidden sm:pointer-fine:inline-flex", className)}
			{...props}
		/>
	);
}

/**
 * A button that shows its keyboard shortcut where there is a keyboard. With an `icon`, a
 * phone shows only the icon (the label stays as its accessible name), so a bar of them fits.
 */
export function ActionButton({
	label,
	shortcut,
	icon,
	className,
	...props
}: ComponentProps<typeof Button> & {
	label: string;
	shortcut: string;
	icon?: ReactNode;
}) {
	return (
		<Button className={cn(icon && ICON_ON_PHONE, className)} {...props}>
			{icon && (
				<span aria-hidden className="contents sm:hidden">
					{icon}
				</span>
			)}
			<span className={cn(icon && "max-sm:sr-only")}>{label}</span>
			<KeyHint>{shortcut}</KeyHint>
		</Button>
	);
}
