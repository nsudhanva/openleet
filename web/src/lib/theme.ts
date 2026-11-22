/** Shared by the theme provider and the script that runs before first paint (vite.config.ts). */
export const THEME_STORAGE_KEY = "openleet:theme";
/** The key the app used before its rename. The script copies its value to the current key once. */
const LEGACY_THEME_KEY = "leetcode-cards:theme";

export type Theme = "light" | "dark" | "system";

export const themeScript = `(() => {
	try {
		const key = ${JSON.stringify(THEME_STORAGE_KEY)}, legacy = ${JSON.stringify(LEGACY_THEME_KEY)};
		const old = localStorage.getItem(legacy);
		if (old !== null) {
			if (localStorage.getItem(key) === null) localStorage.setItem(key, old);
			localStorage.removeItem(legacy);
		}
		const t = localStorage.getItem(key);
		const dark = t === "dark" || (t !== "light" && matchMedia("(prefers-color-scheme: dark)").matches);
		document.documentElement.classList.toggle("dark", dark);
	} catch {}
})()`;
