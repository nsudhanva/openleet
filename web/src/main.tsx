import { RouterProvider } from "@tanstack/react-router";
import { StrictMode, startTransition } from "react";
import { createRoot } from "react-dom/client";
import { router } from "./router";
import "./styles.css";

const root = document.getElementById("app");
if (!root) throw new Error("index.html has no #app element");

// index.html's static shell (the header and an empty page) stays on screen until the first
// page's code and data are in, so the app replaces it in one paint. The server preloads that
// data with the page (server/src/preload.rs). A failed load still renders: the route shows
// its error.
router
	.load()
	.catch(console.error)
	.finally(() =>
		// A transition renders in slices, between which the browser stays responsive.
		startTransition(() =>
			createRoot(root).render(
				<StrictMode>
					<RouterProvider router={router} />
				</StrictMode>,
			),
		),
	);
