import { Badge } from "@/components/ui/badge";
import { TONE, TONE_TEXT, type Tone } from "@/lib/tones";
import type { Verdict } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Every verdict's label and status tone (success, warning, destructive or muted). */
export const VERDICT: Record<Verdict, { label: string; tone: Tone }> = {
	accepted: { label: "Accepted", tone: "success" },
	wrong_answer: { label: "Wrong Answer", tone: "destructive" },
	time_limit_exceeded: { label: "Time Limit Exceeded", tone: "warning" },
	memory_limit_exceeded: { label: "Memory Limit Exceeded", tone: "warning" },
	output_limit_exceeded: { label: "Output Limit Exceeded", tone: "warning" },
	runtime_error: { label: "Runtime Error", tone: "destructive" },
	compile_error: { label: "Compile Error", tone: "destructive" },
	internal_error: { label: "Internal Error", tone: "muted" },
	finished: { label: "Finished", tone: "muted" },
};

/** A judge verdict as a small colored badge (lists) or a colored heading (results). */
export function VerdictBadge({
	verdict,
	heading = false,
	className,
}: {
	verdict: Verdict;
	heading?: boolean;
	className?: string;
}) {
	const { label, tone } = VERDICT[verdict];
	if (heading)
		return (
			<span className={cn("text-lg font-semibold", TONE_TEXT[tone], className)}>
				{label}
			</span>
		);
	return (
		<Badge className={cn("font-semibold", TONE[tone], className)}>
			{label}
		</Badge>
	);
}
