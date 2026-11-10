import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import type { Pager } from "@/hooks/use-pager";
import { cn } from "@/lib/utils";

/** Previous and next page buttons, around `children` when given (the position, "Page 2 of 5"). */
export function PagerControls({
	pager: { page, pages, turn },
	size = "sm",
	className,
	children,
}: {
	pager: Pager;
	size?: "xs" | "sm";
	className?: string;
	children?: ReactNode;
}) {
	const icon = size === "xs" ? "icon-xs" : "icon-sm";
	return (
		<div
			className={cn(
				"flex items-center text-muted-foreground tabular-nums",
				className,
			)}
		>
			<Button
				variant="ghost"
				size={icon}
				aria-label="Previous page"
				disabled={page === 0}
				onClick={() => turn(-1)}
			>
				<ChevronLeftIcon />
			</Button>
			{children}
			<Button
				variant="ghost"
				size={icon}
				aria-label="Next page"
				disabled={page >= pages - 1}
				onClick={() => turn(1)}
			>
				<ChevronRightIcon />
			</Button>
		</div>
	);
}
