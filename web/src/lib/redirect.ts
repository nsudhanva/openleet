/**
 * Only a page of this site. The browser resolves the value as a URL, the way it will on the way
 * back, so a full URL, `//host`, or a tab or backslash that makes one of them goes to "/".
 */
export function safeRedirect(value: unknown, origin: string): string {
	if (typeof value !== "string" || !value.startsWith("/")) return "/";
	try {
		const url = new URL(value, origin);
		return url.origin === origin ? url.pathname + url.search + url.hash : "/";
	} catch {
		return "/";
	}
}
