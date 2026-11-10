import type { ReactNode } from "react";

/**
 * Compact page title with an optional description, and actions: under the text below `lg`,
 * on its right from `lg`.
 */
export function PageHeader({
	title,
	children,
	actions,
}: {
	title: string;
	children?: ReactNode;
	actions?: ReactNode;
}) {
	return (
		<header className="mb-3 flex flex-col gap-x-6 gap-y-3 lg:flex-row lg:items-end">
			<div className="min-w-0 lg:flex-1">
				<h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
				{children && (
					<p className="max-w-prose text-sm text-muted-foreground">
						{children}
					</p>
				)}
			</div>
			{actions}
		</header>
	);
}
