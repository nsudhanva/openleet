import { Badge } from "@/components/ui/badge";
import type { CardList } from "@/lib/types";

export const LIST_LABEL: Record<CardList, string> = {
	again: "Visit again",
	less: "Visit less often",
};

export function ListBadge({ list }: { list: CardList | null }) {
	if (!list) return null;
	return (
		<Badge variant={list === "again" ? "default" : "secondary"}>
			{LIST_LABEL[list]}
		</Badge>
	);
}
