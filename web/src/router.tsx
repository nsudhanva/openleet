import { createRouter } from "@tanstack/react-router";
import { RouteError } from "@/components/route-error";
import { routeTree } from "./routeTree.gen";

export const router = createRouter({
	routeTree,
	scrollRestoration: true,
	defaultPreload: "intent",
	defaultPreloadStaleTime: 0,
	defaultErrorComponent: RouteError,
});

declare module "@tanstack/react-router" {
	interface Register {
		router: typeof router;
	}
}
