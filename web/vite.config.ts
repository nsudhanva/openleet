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
	],
});
