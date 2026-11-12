/**
 * The page column is 64rem wide; the code page, with its editor beside the statement, gets
 * 80rem. `data-wide` on <html> picks the width (the `wide:` variant in styles.css), so the
 * header and the page share it: the script below sets it before the first paint, and
 * routes/__root.tsx on every navigation.
 */
const WIDE_PREFIX = "/code/";

export function isWidePage(pathname: string): boolean {
	return pathname.startsWith(WIDE_PREFIX);
}

/** Runs in <head> (vite.config.ts), so the static shell paints at the page's width. */
export const widePageScript = `document.documentElement.toggleAttribute("data-wide", location.pathname.startsWith(${JSON.stringify(WIDE_PREFIX)}))`;
