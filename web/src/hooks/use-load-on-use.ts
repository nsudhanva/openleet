import { useState } from "react";

/**
 * For a control whose code loads on first use, to keep it off the first page load: spread
 * `prefetchProps` on its placeholder so pointing at or focusing it starts loading, and call
 * `use` when it is activated; `used` then stays true.
 */
export function useLoadOnUse(load: () => Promise<unknown>) {
	const [used, setUsed] = useState(false);
	const prefetch = () => {
		void load();
	};
	return {
		used,
		use: () => setUsed(true),
		prefetchProps: { onPointerEnter: prefetch, onFocus: prefetch },
	};
}
