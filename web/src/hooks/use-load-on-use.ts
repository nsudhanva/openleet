import { useEffect, useEffectEvent, useState } from "react";

/** Modules already loaded, by the function that loads them. */
const modules = new WeakMap<() => Promise<unknown>, unknown>();

function logFailure(error: unknown) {
	console.error("Could not load a control's code", error);
}

/** Loads a module and keeps it, so a later first use finds it at once. */
function preload<M>(load: () => Promise<M>): Promise<M> {
	return load().then((module) => {
		modules.set(load, module);
		return module;
	});
}

/** What a person does before they open a menu; a page load alone does none of these. */
const FIRST_SIGNS = [
	"pointermove",
	"pointerdown",
	"touchstart",
	"keydown",
	"scroll",
];

/**
 * Runs `run` when the browser is next idle after the first sign of a person on the page, so
 * the page load itself never pays for it. Returns a cancel.
 */
function onFirstSign(run: () => void): () => void {
	// Safari has no requestIdleCallback; a short timeout stands in.
	const idle = typeof requestIdleCallback === "function";
	let pending: number | undefined;
	const stop = () => {
		for (const sign of FIRST_SIGNS) window.removeEventListener(sign, start);
	};
	function start() {
		stop();
		pending = idle
			? requestIdleCallback(run, { timeout: 500 })
			: window.setTimeout(run, 50);
	}
	for (const sign of FIRST_SIGNS)
		window.addEventListener(sign, start, { once: true, passive: true });
	return () => {
		stop();
		if (pending === undefined) return;
		if (idle) cancelIdleCallback(pending);
		else window.clearTimeout(pending);
	};
}

/**
 * For a control whose code (and data) load on demand, to keep them off the first page load.
 * `load` runs at the first sign of a person on the page (a pointer move, a touch, a key, a
 * scroll), and again (from its cache) when pointing at or focusing the placeholder (spread
 * `prefetchProps` on it). Call `use` when the control is activated:
 * `loaded` is then what `load` gave, at once when it is already in, else as soon as it
 * arrives. The control renders it directly, never through Suspense, whose reveal React holds
 * back for up to 300 ms.
 */
export function useLoadOnUse<M>(load: () => Promise<M>) {
	const [used, setUsed] = useState(false);
	const [module, setModule] = useState<M>();
	const whenIdle = useEffectEvent(() => {
		preload(load).catch(logFailure);
	});
	useEffect(() => onFirstSign(whenIdle), []);
	const fetch = useEffectEvent((live: () => boolean) =>
		preload(load).then((m) => live() && setModule(() => m), logFailure),
	);
	useEffect(() => {
		if (!used || module !== undefined) return;
		let live = true;
		void fetch(() => live);
		return () => {
			live = false;
		};
	}, [used, module]);
	const prefetch = () => {
		preload(load).catch(logFailure);
	};
	return {
		used,
		/** The module once the control was used; undefined until then and while it loads. */
		loaded: used ? (module ?? (modules.get(load) as M | undefined)) : undefined,
		use: () => setUsed(true),
		prefetchProps: { onPointerEnter: prefetch, onFocus: prefetch },
	};
}
