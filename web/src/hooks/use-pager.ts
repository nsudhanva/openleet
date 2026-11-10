import { useState } from "react";
import { useHotkeys } from "@/hooks/use-hotkeys";

/**
 * The current page of `pages`, kept in range when the page count shrinks. With `arrowKeys`,
 * ← and → turn the pages while there is more than one.
 */
export function usePager(pages: number, arrowKeys = false) {
	const [wanted, setWanted] = useState(0);
	const last = Math.max(0, pages - 1);
	const page = Math.min(wanted, last);
	const turn = (by: number) =>
		setWanted(Math.min(last, Math.max(0, page + by)));
	useHotkeys(
		arrowKeys && pages > 1
			? { ArrowLeft: () => turn(-1), ArrowRight: () => turn(1) }
			: {},
	);
	return { page, pages, turn, reset: () => setWanted(0) };
}

export type Pager = ReturnType<typeof usePager>;
