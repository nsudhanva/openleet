import { Badge } from "@/components/ui/badge";
import { TONE, type Tone } from "@/lib/tones";
import type { Difficulty } from "@/lib/types";
import { cn } from "@/lib/utils";

const DIFFICULTY_TONE: Record<Difficulty, Tone> = {
	Easy: "success",
	Medium: "warning",
	Hard: "destructive",
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
	return (
		<Badge className={cn("font-semibold", TONE[DIFFICULTY_TONE[difficulty]])}>
			{difficulty}
		</Badge>
	);
}
