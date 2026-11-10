import { Badge } from "@/components/ui/badge";

/** Marks a LeetCode Premium problem; information only, nothing is held back. */
export function PremiumBadge() {
	return (
		<Badge variant="outline" className="font-normal text-muted-foreground">
			Premium
		</Badge>
	);
}
