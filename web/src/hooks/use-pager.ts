import { useState } from "react";
import { useHotkeys } from "@/hooks/use-hotkeys";

/**
 * The current page of `pages`, kept in range when the page count shrinks, and back to the
 * first whenever `resetKey` changes (the filters of what is paged, however they changed:
 * a control, a link, the Back button). With `arrowKeys`, ← and → turn the pages while
 * there is more than one.
 */
export function usePager(pages: number, arrowKeys = false, resetKey = "") {
	const [state, setState] = useState({ key: resetKey, page: 0 });
	const setWanted = (page: number) => setState({ key: resetKey, page });
	const wanted = state.key === resetKey ? state.page : 0;
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
