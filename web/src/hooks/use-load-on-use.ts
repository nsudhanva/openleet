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

/** Runs `run` once the browser is idle after the page has loaded; returns a cancel. */
function afterLoadWhenIdle(run: () => void): () => void {
	let cancel = () => {};
	const schedule = () => {
		if ("requestIdleCallback" in window) {
			const id = requestIdleCallback(run, { timeout: 4000 });
			cancel = () => cancelIdleCallback(id);
		} else {
			const timer = setTimeout(run, 2000);
			cancel = () => clearTimeout(timer);
		}
	};
	if (document.readyState === "complete") schedule();
	else window.addEventListener("load", schedule, { once: true });
	return () => {
		window.removeEventListener("load", schedule);
		cancel();
	};
}

/**
 * For a control whose code (and data) load on demand, to keep them off the first page load.
 * `load` runs once the page is idle, and again (from its cache) when pointing at or focusing
 * the placeholder (spread `prefetchProps` on it). Call `use` when the control is activated:
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
	useEffect(() => afterLoadWhenIdle(whenIdle), []);
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
