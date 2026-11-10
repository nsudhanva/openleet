import { type RefObject, useLayoutEffect, useState } from "react";

/** The element's content width in px, updated when it resizes (0 before the first layout). */
export function useWidth(ref: RefObject<HTMLElement | null>): number {
	const [width, setWidth] = useState(0);
	useLayoutEffect(() => {
		const element = ref.current;
		if (!element) return;
		const observer = new ResizeObserver(([entry]) =>
			setWidth(Math.floor(entry.contentRect.width)),
		);
		observer.observe(element);
		return () => observer.disconnect();
	}, [ref]);
	return width;
}
