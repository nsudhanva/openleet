import {
	type KeyboardEvent,
	type PointerEvent,
	useCallback,
	useLayoutEffect,
	useRef,
	useState,
} from "react";

const STORAGE_KEY = "openleet:statement-share";
/** The statement's share of the card's width: about 1.2 to the other pane's 1. */
const DEFAULT_SHARE = 0.545;
const MIN_SHARE = 0.25;
const MAX_SHARE = 0.75;
/** How far ← and → move the handle. */
const STEP = 0.02;

function clampShare(share: number): number {
	const clamped = Math.min(MAX_SHARE, Math.max(MIN_SHARE, share));
	return Math.round(clamped * 1000) / 1000;
}

function storedShare(): number {
	try {
		const share = Number(localStorage.getItem(STORAGE_KEY));
		return share > 0 ? clampShare(share) : DEFAULT_SHARE;
	} catch {
		return DEFAULT_SHARE;
	}
}

function storeShare(share: number) {
	try {
		if (share === DEFAULT_SHARE) localStorage.removeItem(STORAGE_KEY);
		else localStorage.setItem(STORAGE_KEY, String(share));
	} catch {}
}

/**
 * The handle between the statement and the other pane, from `lg` up: drag it, or focus it and
 * press ← → (Home, End), to give either pane more room; a double click puts it back. It goes
 * straight inside the panes' grid and sets `--share`, the statement's share of the width, on
 * it for the columns to read. The share
 * is the same on the study and code pages, so the statement keeps its width between them, and
 * the browser keeps it.
 */
export function PaneSplitter({ label }: { label: string }) {
	const [share, setShare] = useState(storedShare);
	const handle = useRef<HTMLHRElement>(null);
	// The share on screen, ahead of `share` while a drag or held key moves it.
	const current = useRef(share);

	// Draws a share without a render, so a drag stays smooth however heavy the panes are.
	const show = useCallback((next: number) => {
		handle.current?.parentElement?.style.setProperty("--share", String(next));
		handle.current?.setAttribute(
			"aria-valuenow",
			String(Math.round(next * 100)),
		);
	}, []);
	useLayoutEffect(() => show(share), [show, share]);

	const commit = (next: number) => {
		const clamped = clampShare(next);
		current.current = clamped;
		setShare(clamped);
		storeShare(clamped);
		show(clamped);
	};

	const onPointerDown = (event: PointerEvent<HTMLHRElement>) => {
		if (event.button !== 0) return;
		// No text selection while dragging.
		event.preventDefault();
		event.currentTarget.setPointerCapture(event.pointerId);
	};
	const onPointerMove = (event: PointerEvent<HTMLHRElement>) => {
		const box = handle.current?.parentElement?.getBoundingClientRect();
		if (!box || !event.currentTarget.hasPointerCapture(event.pointerId)) return;
		current.current = clampShare((event.clientX - box.left) / box.width);
		show(current.current);
	};
	const onPointerUp = (event: PointerEvent<HTMLHRElement>) => {
		if (!event.currentTarget.hasPointerCapture(event.pointerId)) return;
		event.currentTarget.releasePointerCapture(event.pointerId);
		commit(current.current);
	};
	const onKeyDown = (event: KeyboardEvent<HTMLHRElement>) => {
		const next = {
			ArrowLeft: current.current - STEP,
			ArrowRight: current.current + STEP,
			Home: MIN_SHARE,
			End: MAX_SHARE,
		}[event.key];
		if (next === undefined) return;
		// Handled here, so the statement does not also turn a page.
		event.preventDefault();
		commit(next);
	};

	return (
		// An <hr> is a separator; focusable, with a value, it is one you can move. The line it
		// shows on hover and focus is its 2px content box.
		<hr
			ref={handle}
			aria-orientation="vertical"
			aria-label={label}
			aria-valuemin={MIN_SHARE * 100}
			aria-valuemax={MAX_SHARE * 100}
			aria-valuenow={Math.round(share * 100)}
			tabIndex={0}
			title="Drag to resize; double-click to reset"
			onPointerDown={onPointerDown}
			onPointerMove={onPointerMove}
			onPointerUp={onPointerUp}
			onPointerCancel={onPointerUp}
			onKeyDown={onKeyDown}
			onDoubleClick={() => commit(DEFAULT_SHARE)}
			className="absolute inset-y-0 left-[calc(var(--share)*100%)] z-10 m-0 h-full w-3 -translate-x-1/2 cursor-col-resize touch-none border-0 bg-clip-content px-[5px] outline-none transition-colors hover:bg-primary/50 focus-visible:bg-primary active:bg-primary max-lg:hidden"
		/>
	);
}
