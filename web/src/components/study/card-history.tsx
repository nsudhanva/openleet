import { ListBadge } from "@/components/list-badge";
import { count, percent, timeFrom } from "@/lib/format";
import type { CardState } from "@/lib/types";

export function CardHistory({ state }: { state: CardState | null }) {
	if (!state) return null;
	if (!state.reviews) return <span>Skipped earlier</span>;
	return (
		<>
			<span>
				Seen {count(state.reviews, "time")}, last {timeFrom(state.lastAt)}
				{state.lastScore !== null && `, topics ${percent(state.lastScore)}`}
			</span>
			<ListBadge list={state.list} />
		</>
	);
}
