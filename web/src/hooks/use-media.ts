import { useSyncExternalStore } from "react";
import { FIT_SCREEN } from "@/lib/screen";

/** Whether the screen matches `query`, updated as it changes (a resized window, a rotation). */
export function useMedia(query: string): boolean {
	return useSyncExternalStore(
		(onChange) => {
			const list = window.matchMedia(query);
			list.addEventListener("change", onChange);
			return () => list.removeEventListener("change", onChange);
		},
		() => window.matchMedia(query).matches,
	);
}

/** Whether pages fit the screen (FIT_SCREEN, the `fit:` variant) rather than scroll. */
export const useFitScreen = () => useMedia(FIT_SCREEN);
