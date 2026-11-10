import { cn } from "@/lib/utils";

/** A share from 0 to 1 as a bar; decorative, so the share must also be said in text. */
export function ProgressBar({
	value,
	className,
}: {
	value: number;
	className?: string;
}) {
	return (
		<div
			aria-hidden
			className={cn("h-2 overflow-hidden rounded-full bg-muted", className)}
		>
			<div
				className="h-full rounded-full bg-primary"
				style={{ width: `${Math.min(1, Math.max(0, value)) * 100}%` }}
			/>
		</div>
	);
}
