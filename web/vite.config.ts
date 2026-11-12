import tailwindcss from "@tailwindcss/vite";
import { devtools } from "@tanstack/devtools-vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import viteReact from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vite";
import { widePageScript } from "./src/lib/layout.ts";
import { themeScript } from "./src/lib/theme.ts";

/**
 * Puts the theme script in <head> so a stored dark theme never flashes light, and the page
 * width script so the shell paints at the page's width (lib/layout.ts).
 */
function themeBeforePaint(): Plugin {
	return {
		name: "theme-before-paint",
		transformIndexHtml: () => [
			{ tag: "script", children: themeScript, injectTo: "head" },
			{ tag: "script", children: widePageScript, injectTo: "head" },
		],
	};
}

/**
 * Routes (files in src/routes) that show code text, in the mono font: problem statements and
 * the About page's API table. Elsewhere it is not needed for the first screen.
 */
const MONO_ROUTES = ["index", "code.$slug", "about"];

/**
 * Preloads the Latin subsets of the fonts, so they arrive with the scripts and the app's
 * first render already uses them: no reflow when they swap in. The mono font only on
 * MONO_ROUTES: `data-routes` tells the server which pages keep the link (server/build.rs).
 * They go at the end of the body: Chrome holds the first paint for font preloads in the head
 * (about 100 ms), and the static shell paints fine with a fallback font.
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
							...(file.includes("-mono-") && {
								"data-routes": MONO_ROUTES.join(" "),
							}),
						},
						injectTo: "body" as const,
					})),
		},
	};
}

/**
 * Inlines the stylesheet into index.html, so the page (and its static shell) paints from the
 * HTML alone, with no request in between. It is one file for the whole app; the HTML that
 * carries it is cached and revalidated like any page.
 */
function inlineCss(): Plugin {
	return {
		name: "inline-css",
		apply: "build",
		transformIndexHtml: {
			order: "post",
			handler: (html, { bundle = {} }) =>
				html.replace(
					/<link rel="stylesheet"[^>]*href="\/([^"]+\.css)"[^>]*>/g,
					(link, file: string) => {
						const asset = bundle[file];
						if (asset?.type !== "asset") return link;
						delete bundle[file];
						return `<style>${String(asset.source)}</style>`;
					},
				),
		},
	};
}

/**
 * Where `vite` and `vite preview` send /api: the Rust server (server/) by default. The request
 * carries the target's host name, so a name-based proxy such as the compose stack's Caddy
 * (`API_URL=http://openleet.localhost`) answers it.
 */
const proxy = {
	"/api": {
		target: process.env.API_URL ?? "http://127.0.0.1:8080",
		changeOrigin: true,
	},
};

/** A static SPA in dist/: the Rust server (server/) serves it and the JSON API under /api. */
export default defineConfig({
	resolve: { tsconfigPaths: true },
	build: {
		// One stylesheet for the whole app (inlined by inlineCss), so no chunk loads CSS of its own.
		cssCodeSplit: false,
		// The server reads it to preload each page's route code (server/build.rs).
		manifest: true,
	},
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
		inlineCss(),
	],
});
