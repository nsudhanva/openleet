import { useEffect, useRef } from "react";

type Handlers = Record<string, (event: KeyboardEvent) => void>;

function isTyping(target: EventTarget | null) {
	return (
		target instanceof HTMLElement &&
		(target.isContentEditable ||
			["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName))
	);
}

/** Listens on window with the newest handlers, without re-subscribing on every render. */
function useKeydown(
	handlers: Handlers,
	pick: (
		event: KeyboardEvent,
		handlers: Handlers,
	) => ((e: KeyboardEvent) => void) | undefined,
	capture = false,
) {
	const latest = useRef(handlers);
	latest.current = handlers;
	const picker = useRef(pick);
	picker.current = pick;

	useEffect(() => {
		function onKeyDown(event: KeyboardEvent) {
			const handler = picker.current(event, latest.current);
			if (!handler) return;
			event.preventDefault();
			event.stopPropagation();
			handler(event);
		}
		window.addEventListener("keydown", onKeyDown, capture);
		return () => window.removeEventListener("keydown", onKeyDown, capture);
	}, [capture]);
}

/**
 * Single-key shortcuts (`event.key`, such as "Enter" or "1"). Ignored while typing in a
 * field, with a modifier held, or when a dialog or menu has focus.
 */
export function useHotkeys(handlers: Handlers) {
	useKeydown(handlers, (event, latest) => {
		if (event.metaKey || event.ctrlKey || event.altKey) return;
		if (isTyping(event.target) || event.defaultPrevented) return;
		const target = event.target instanceof Element ? event.target : null;
		if (target?.closest("[role=dialog],[role=menu],[role=listbox]")) return;
		// Enter on a focused button or link activates that control, not the shortcut.
		// Toggle buttons (topic chips) toggle with Space and leave Enter to the shortcut.
		if (
			event.key === "Enter" &&
			target?.closest("button:not([aria-pressed]),a")
		)
			return;
		return latest[event.key];
	});
}

/**
 * ⌘ or Ctrl shortcuts such as "k", "Enter" or "Shift+Enter". They work while typing, even in
 * the code editor: the listener runs first (capture) and keeps the key from the field.
 */
export function useModKeys(handlers: Handlers) {
	useKeydown(
		handlers,
		(event, latest) => {
			if (!(event.metaKey || event.ctrlKey) || event.altKey) return;
			const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
			return latest[event.shiftKey ? `Shift+${key}` : key];
		},
		true,
	);
}
