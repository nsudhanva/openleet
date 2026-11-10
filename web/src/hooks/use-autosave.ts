import { useCallback, useEffect, useRef, useState } from "react";

export type SaveStatus = "idle" | "pending" | "saving" | "saved" | "failed";

/**
 * Saves the latest value `delay` ms after the last change, one save at a time and in order.
 * A pending change is saved at once when the page hides or the component unmounts.
 */
export function useAutosave<T>(
	save: (value: T, keepalive: boolean) => Promise<void>,
	delay = 800,
) {
	const [status, setStatus] = useState<SaveStatus>("idle");
	const latestSave = useRef(save);
	latestSave.current = save;
	const pending = useRef<{ value: T } | null>(null);
	const timer = useRef<ReturnType<typeof setTimeout>>(undefined);
	const queue = useRef(Promise.resolve());

	const flush = useCallback((keepalive = false) => {
		clearTimeout(timer.current);
		const next = pending.current;
		if (!next) return queue.current;
		pending.current = null;
		queue.current = queue.current.then(async () => {
			setStatus("saving");
			try {
				await latestSave.current(next.value, keepalive);
				if (!pending.current) setStatus("saved");
			} catch (error) {
				console.error("Autosave failed", error);
				setStatus("failed");
			}
		});
		return queue.current;
	}, []);

	const schedule = useCallback(
		(value: T) => {
			pending.current = { value };
			setStatus("pending");
			clearTimeout(timer.current);
			timer.current = setTimeout(flush, delay);
		},
		[delay, flush],
	);

	useEffect(() => {
		const onHide = () => flush(true);
		window.addEventListener("pagehide", onHide);
		return () => {
			window.removeEventListener("pagehide", onHide);
			flush(true);
		};
	}, [flush]);

	return { status, schedule, flush };
}
