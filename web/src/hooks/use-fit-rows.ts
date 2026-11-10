import { type RefObject, useLayoutEffect, useState } from "react";

/** How many rows of `rowHeight` px fit in the element, updated when it resizes. */
export function useFitCount(
	ref: RefObject<HTMLElement | null>,
	rowHeight: number,
	minimum = 5,
): number {
	const [count, setCount] = useState(minimum);
	useLayoutEffect(() => {
		const element = ref.current;
		if (!element) return;
		const observer = new ResizeObserver(() =>
			setCount(Math.max(minimum, Math.floor(element.clientHeight / rowHeight))),
		);
		observer.observe(element);
		return () => observer.disconnect();
	}, [ref, rowHeight, minimum]);
	return count;
}
