import { ChevronDownIcon, ListPlusIcon } from "lucide-react";
import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { cn } from "@/lib/utils";

const loadMenu = () => import("@/components/lists/add-to-list-menu");

/** The button that opens the menu of your lists. */
export function AddToListTrigger({
	className,
	...props
}: ComponentProps<typeof Button>) {
	return (
		<Button
			variant="ghost"
			size="xs"
			className={cn("shrink-0 text-muted-foreground", className)}
			{...props}
		>
			<ListPlusIcon data-icon="inline-start" />
			<span className="max-sm:sr-only">Add to list</span>
			<ChevronDownIcon data-icon="inline-end" />
		</Button>
	);
}

/**
 * Puts `slugs` on your lists or takes them off, or starts a new list with them. The menu
 * loads on first use. `onChange` runs after each change.
 */
export function AddToListButton({
	slugs,
	onChange,
	className,
}: {
	slugs: string[];
	onChange?: () => void;
	className?: string;
}) {
	const { loaded, use, prefetchProps } = useLoadOnUse(loadMenu);
	if (!loaded)
		return (
			<AddToListTrigger
				className={className}
				{...prefetchProps}
				onClick={use}
			/>
		);
	return (
		<loaded.AddToListMenu
			slugs={slugs}
			onChange={onChange}
			className={className}
			defaultOpen
		/>
	);
}
