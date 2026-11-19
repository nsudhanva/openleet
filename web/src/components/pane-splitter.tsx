import {
	type KeyboardEvent,
	type PointerEvent,
	useCallback,
	useRef,
	useState,
} from "react";
import { cn } from "@/lib/utils";

/** Two panes that share a box, side by side (`x`) or one above the other (`y`). */
export interface Split {
	axis: "x" | "y";
	/** The CSS variable that holds the first pane's share, on the panes' parent. */
	variable: `--${string}`;
	storageKey: string;
	fallback: number;
	min: number;
	max: number;
}

/**
 * The statement and the other pane, from `lg` up. The statement's share is about 1.2 to the
 * other pane's 1. It is the same on the study and code pages, so the statement keeps its width
 * between them.
 */
export const STATEMENT_SPLIT: Split = {
	axis: "x",
	variable: "--share",
	storageKey: "openleet:statement-share",
	fallback: 0.545,
	min: 0.25,
	max: 0.75,
};

/** The code editor above the test panel, on a `fit:` screen: 3 to 2. */
export const EDITOR_SPLIT: Split = {
	axis: "y",
	variable: "--editor-share",
	storageKey: "openleet:editor-share",
	fallback: 0.6,
	min: 0.2,
	max: 0.85,
};

/** How far an arrow key moves the handle. */
const STEP = 0.02;

function clampShare(split: Split, share: number): number {
	const clamped = Math.min(split.max, Math.max(split.min, share));
	return Math.round(clamped * 1000) / 1000;
}

/** The share the browser keeps, or the fallback. */
export function savedShare(split: Split): number {
	try {
		const share = Number(localStorage.getItem(split.storageKey));
		return share > 0 ? clampShare(split, share) : split.fallback;
	} catch {
		return split.fallback;
	}
}

function storeShare(split: Split, share: number) {
	try {
		if (share === split.fallback) localStorage.removeItem(split.storageKey);
		else localStorage.setItem(split.storageKey, String(share));
	} catch {}
}

const AXIS = {
	x: {
		back: "ArrowLeft",
		forward: "ArrowRight",
		// A separator between left and right panes is a vertical line.
		orientation: "vertical",
		// Over the panes' grid, at the share; shown from lg up.
		className:
			"absolute inset-y-0 left-[calc(var(--share)*100%)] h-full w-3 -translate-x-1/2 cursor-col-resize px-[5px] max-lg:hidden",
	},
	y: {
		back: "ArrowUp",
		forward: "ArrowDown",
		orientation: "horizontal",
		// In the flow between the panes, taking no room (its margins cancel its height); shown
		// on a `fit:` screen, where the panes share the height.
		className:
			"relative -my-1.5 hidden h-3 w-full cursor-row-resize py-[5px] fit:block",
	},
} as const;

/**
 * The handle between two panes: drag it, or focus it and press the arrow keys (Home, End), to
 * give either pane more room; a double click puts it back. It goes straight inside the panes'
 * parent, which renders with the split's variable set to `initial` (from `savedShare`), and
 * moves that variable on it. The browser keeps the share.
 */
export function PaneSplitter({
	split,
	label,
	initial,
}: {
	split: Split;
	label: string;
	initial: number;
}) {
	const axis = AXIS[split.axis];
	const [share, setShare] = useState(initial);
	const handle = useRef<HTMLHRElement>(null);
	// The share on screen, ahead of `share` while a drag or held key moves it.
	const current = useRef(share);

	// Draws a share without a render, so a drag stays smooth however heavy the panes are.
	const show = useCallback(
		(next: number) => {
			handle.current?.parentElement?.style.setProperty(
				split.variable,
				String(next),
			);
			handle.current?.setAttribute(
				"aria-valuenow",
				String(Math.round(next * 100)),
			);
		},
		[split],
	);

	const commit = (next: number) => {
		const clamped = clampShare(split, next);
		current.current = clamped;
		setShare(clamped);
		storeShare(split, clamped);
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
		const at =
			split.axis === "x"
				? (event.clientX - box.left) / box.width
				: (event.clientY - box.top) / box.height;
		current.current = clampShare(split, at);
		show(current.current);
	};
	const onPointerUp = (event: PointerEvent<HTMLHRElement>) => {
		if (!event.currentTarget.hasPointerCapture(event.pointerId)) return;
		event.currentTarget.releasePointerCapture(event.pointerId);
		commit(current.current);
	};
	const onKeyDown = (event: KeyboardEvent<HTMLHRElement>) => {
		const next = {
			[axis.back]: current.current - STEP,
			[axis.forward]: current.current + STEP,
			Home: split.min,
			End: split.max,
		}[event.key];
		if (next === undefined) return;
		// Handled here, so the page does not also scroll or turn a page.
		event.preventDefault();
		commit(next);
	};

	return (
		// An <hr> is a separator; focusable, with a value, it is one you can move. The line it
		// shows on hover and focus is its 2px content box.
		<hr
			ref={handle}
			aria-orientation={axis.orientation}
			aria-label={label}
			aria-valuemin={split.min * 100}
			aria-valuemax={split.max * 100}
			aria-valuenow={Math.round(share * 100)}
			tabIndex={0}
			title="Drag to resize; double-click to reset"
			onPointerDown={onPointerDown}
			onPointerMove={onPointerMove}
			onPointerUp={onPointerUp}
			onPointerCancel={onPointerUp}
			onKeyDown={onKeyDown}
			onDoubleClick={() => commit(split.fallback)}
			className={cn(
				"z-10 m-0 touch-none border-0 bg-clip-content outline-none transition-colors hover:bg-primary/50 focus-visible:bg-primary active:bg-primary",
				axis.className,
			)}
		/>
	);
}
