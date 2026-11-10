import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

/** A titled block of the progress page. */
export function Panel({
	id,
	title,
	note,
	action,
	className,
	children,
}: {
	id: string;
	title: string;
	note?: string;
	/** A control at the end of the title row. */
	action?: ReactNode;
	className?: string;
	children: ReactNode;
}) {
	return (
		<section
			aria-labelledby={id}
			className={cn(
				"flex min-w-0 flex-col rounded-sm bg-card p-4 shadow-[0_1px_0_var(--border)]",
				className,
			)}
		>
			<div className="flex items-start gap-3">
				<div className="min-w-0 flex-1">
					<h2 id={id} className="font-semibold tracking-tight">
						{title}
					</h2>
					{note && <p className="text-xs text-muted-foreground">{note}</p>}
				</div>
				{action}
			</div>
			<div className="mt-3 flex min-h-0 flex-1 flex-col">{children}</div>
		</section>
	);
}

/** A figure with its label, for a `<dl>`. */
export function Stat({
	label,
	value,
	detail,
}: {
	label: string;
	value: string;
	detail?: string;
}) {
	return (
		<div>
			<dt className="text-sm text-muted-foreground">{label}</dt>
			<dd className="text-xl font-semibold tabular-nums">
				{value}
				{detail && (
					<span className="ml-1.5 text-xs font-normal text-muted-foreground">
						{detail}
					</span>
				)}
			</dd>
		</div>
	);
}

/** What a panel shows before there is anything to show. */
export function EmptyNote({ children }: { children: ReactNode }) {
	return <p className="text-sm text-muted-foreground">{children}</p>;
}
