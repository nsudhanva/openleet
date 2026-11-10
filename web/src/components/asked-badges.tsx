import { Badge } from "@/components/ui/badge";
import { ASKED_PERIODS, PERIOD_LABEL, type Problem } from "@/lib/types";

/**
 * Google's rank for the problem in each period it was asked; frequency on hover. A classic
 * problem Google did not ask has none.
 */
export function AskedBadges({ asked }: { asked: Problem["asked"] }) {
	return ASKED_PERIODS.map((period) => {
		const stat = asked[period];
		if (!stat) return null;
		return (
			<Badge
				key={period}
				variant="outline"
				className="font-normal tabular-nums"
				title={`Frequency ${stat.frequency} in the last ${PERIOD_LABEL[period]}`}
			>
				#{stat.rank} in {PERIOD_LABEL[period]}
			</Badge>
		);
	});
}
