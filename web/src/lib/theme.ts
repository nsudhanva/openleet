/** Shared by the theme provider and the script that runs before first paint (vite.config.ts). */
export const THEME_STORAGE_KEY = "leetcode-cards:theme";

export type Theme = "light" | "dark" | "system";

export const themeScript = `(() => {
	try {
		const t = localStorage.getItem(${JSON.stringify(THEME_STORAGE_KEY)});
		const dark = t === "dark" || (t !== "light" && matchMedia("(prefers-color-scheme: dark)").matches);
		document.documentElement.classList.toggle("dark", dark);
	} catch {}
})()`;
