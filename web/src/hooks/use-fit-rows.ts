import { type RefObject, useLayoutEffect, useState } from "react";

/**
 * How many body rows of the table inside `ref` fit in it, measured from the rows it renders
 * (header and borders included), so any row content or font gives the right count. It updates
 * when the box or the table resizes; with no rows to measure it keeps the last count. While
 * not `active` (the box is not sized to the screen) it measures nothing.
 */
export function useFitRows(
	ref: RefObject<HTMLElement | null>,
	active: boolean,
	minimum = 5,
): number {
	const [count, setCount] = useState(minimum);
	useLayoutEffect(() => {
		const box = ref.current;
		const table = box?.querySelector("table");
		if (!active || !box || !table) return;
		const measure = () => {
			const rows = table.tBodies[0]?.rows;
			if (!rows?.length) return;
			const first = rows[0].getBoundingClientRect();
			const last = rows[rows.length - 1].getBoundingClientRect();
			// Row to row, so collapsed borders count once; the last row has no bottom border.
			const pitch =
				rows.length > 1
					? (last.top - first.top) / (rows.length - 1)
					: first.height;
			const bottom =
				box.getBoundingClientRect().top + box.clientTop + box.clientHeight;
			// Rows from the first one down to the bottom of the box (1e-3 absorbs rounding).
			const fit =
				Math.floor((bottom - first.top - last.height) / pitch + 1e-3) + 1;
			setCount(Math.max(minimum, fit));
		};
		const observer = new ResizeObserver(measure);
		observer.observe(box);
		observer.observe(table);
		return () => observer.disconnect();
	}, [ref, active, minimum]);
	return count;
}
