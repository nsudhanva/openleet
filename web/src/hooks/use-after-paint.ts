import { useEffect, useState } from "react";

/** False for the first paint, true right after it: for work that must not delay that paint. */
export function useAfterPaint(): boolean {
	const [painted, setPainted] = useState(false);
	useEffect(() => {
		// A frame callback runs just before the paint; a task queued from it runs after.
		let timer: ReturnType<typeof setTimeout> | undefined;
		const frame = requestAnimationFrame(() => {
			timer = setTimeout(() => setPainted(true));
		});
		return () => {
			cancelAnimationFrame(frame);
			clearTimeout(timer);
		};
	}, []);
	return painted;
}
