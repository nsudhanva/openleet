import tailwindcss from "@tailwindcss/vite";
import { devtools } from "@tanstack/devtools-vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import viteReact from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vite";
import { themeScript } from "./src/lib/theme.ts";

/** Puts the theme script in <head> so a stored dark theme never flashes light. */
function themeBeforePaint(): Plugin {
	return {
		name: "theme-before-paint",
		transformIndexHtml: () => [
			{ tag: "script", children: themeScript, injectTo: "head" },
		],
	};
}

/**
 * Preloads the Latin subsets of the two fonts (both are on every page), so they arrive with
 * the scripts and the first render already uses them: no reflow when they swap in.
 */
function preloadFonts(): Plugin {
	return {
		name: "preload-fonts",
		transformIndexHtml: {
			order: "post",
			handler: (_html, { bundle = {} }) =>
				Object.keys(bundle)
					.filter((file) => /-latin-wght-normal-[\w-]+\.woff2$/.test(file))
					.map((file) => ({
						tag: "link",
						attrs: {
							rel: "preload",
							href: `/${file}`,
							as: "font",
							type: "font/woff2",
							crossorigin: "",
						},
						injectTo: "head" as const,
					})),
		},
	};
}

/** Where `vite` and `vite preview` send /api: the Rust server (server/) by default. */
const proxy = { "/api": process.env.API_URL ?? "http://127.0.0.1:8080" };

/** A static SPA in dist/: the Rust server (server/) serves it and the JSON API under /api. */
export default defineConfig({
	resolve: { tsconfigPaths: true },
	server: { port: 3000, proxy },
	preview: { port: 3000, proxy },
	plugins: [
		devtools(),
		// Each route's component is its own chunk, so CodeMirror loads only on /code pages.
		tanstackRouter({ target: "react", autoCodeSplitting: true }),
		viteReact(),
		tailwindcss(),
		themeBeforePaint(),
		preloadFonts(),
	],
});
