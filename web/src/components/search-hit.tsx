import { DifficultyBadge } from "@/components/difficulty-badge";
import type { SearchField, SearchHit } from "@/lib/types";

const MATCHED_IN: Partial<Record<SearchField, string>> = {
	topic: "matched a topic",
	statement: "matched the statement",
};

/** Title line of a search result, with where it matched when that is not the title. */
export function SearchHitLabel({ hit }: { hit: SearchHit }) {
	const where = MATCHED_IN[hit.field];
	return (
		<div className="min-w-0 flex-1">
			<div className="flex items-center gap-2">
				<span className="w-12 shrink-0 text-xs text-muted-foreground tabular-nums">
					LC {hit.id}
				</span>
				<span className="truncate font-medium">{hit.title}</span>
				<DifficultyBadge difficulty={hit.difficulty} />
				{where && (
					<span className="shrink-0 text-xs text-muted-foreground">
						{where}
					</span>
				)}
			</div>
			{hit.snippet && (
				<p className="mt-0.5 truncate pl-14 text-xs text-muted-foreground">
					{hit.snippet}
				</p>
			)}
		</div>
	);
}
