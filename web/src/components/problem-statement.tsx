import { useEffect, useRef } from "react";
import { FitPages } from "@/components/fit-pages";
import type { Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Waits before each new try of an image that did not load. */
const RETRY_DELAYS_MS = [1_000, 4_000, 10_000];

/**
 * A problem's statement fitted to its box: it shrinks, then pages (← → with `arrowKeys`).
 */
export function ProblemStatement({
	problem,
	arrowKeys = false,
	className,
}: {
	problem: Pick<Problem, "description">;
	arrowKeys?: boolean;
	className?: string;
}) {
	const body = useRef<HTMLDivElement>(null);
	useEffect(() => {
		const root = body.current;
		if (root && problem.description) return retryBrokenImages(root);
	}, [problem.description]);

	return (
		<FitPages
			arrowKeys={arrowKeys}
			className={cn("statement fit:h-full", className)}
		>
			<div
				ref={body}
				// biome-ignore lint/security/noDangerouslySetInnerHtml: statements are allowlist-sanitized at ingest (src/openleet/sanitize.py)
				dangerouslySetInnerHTML={{ __html: problem.description ?? "" }}
			/>
		</FitPages>
	);
}

/**
 * Loads each image under `root` again when it fails. Statement images come from a CDN, and a
 * browser does not try a failed image again, so one dropped request shows a broken image until
 * the page reloads. Returns the cleanup.
 */
function retryBrokenImages(root: HTMLElement): () => void {
	const tries = new WeakMap<HTMLImageElement, number>();
	const timers = new Set<ReturnType<typeof setTimeout>>();
	const retry = (img: HTMLImageElement) => {
		const count = tries.get(img) ?? 0;
		const delay = RETRY_DELAYS_MS[count];
		const src = img.getAttribute("src");
		if (delay === undefined || !src) return;
		tries.set(img, count + 1);
		const timer = setTimeout(() => {
			timers.delete(timer);
			// Setting `src`, even to the same URL, makes the browser request the image again.
			img.setAttribute("src", src);
		}, delay);
		timers.add(timer);
	};
	// `error` does not bubble, so listen in the capture phase.
	const onError = (event: Event) => {
		if (event.target instanceof HTMLImageElement) retry(event.target);
	};
	root.addEventListener("error", onError, true);
	// An image can fail before this effect runs.
	for (const img of root.querySelectorAll("img")) {
		if (img.complete && img.naturalWidth === 0) retry(img);
	}
	return () => {
		root.removeEventListener("error", onError, true);
		for (const timer of timers) clearTimeout(timer);
	};
}
