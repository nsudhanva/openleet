import { type RefObject, useLayoutEffect, useState } from "react";

/**
 * Whether the element has been laid out with a size: false while it (or an ancestor) is
 * display: none, true from the first time it shows, and true after that.
 */
export function useShown(ref: RefObject<HTMLElement | null>): boolean {
	const [shown, setShown] = useState(false);
	useLayoutEffect(() => {
		const element = ref.current;
		if (!element || shown) return;
		const observer = new ResizeObserver(([entry]) => {
			if (entry.contentRect.width > 0 || entry.contentRect.height > 0)
				setShown(true);
		});
		observer.observe(element);
		return () => observer.disconnect();
	}, [ref, shown]);
	return shown;
}
