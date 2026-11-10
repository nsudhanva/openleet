import { TanStackDevtools } from "@tanstack/react-devtools";
import {
	createRootRoute,
	HeadContent,
	Link,
	Outlet,
} from "@tanstack/react-router";
import { TanStackRouterDevtoolsPanel } from "@tanstack/react-router-devtools";
import { SiteHeader } from "@/components/site-header";
import { ThemeProvider } from "@/components/theme-provider";
import { buttonVariants } from "@/components/ui/button";
import { api } from "@/lib/api";
import { pageTitle } from "@/lib/format";

export const Route = createRootRoute({
	// The header's readiness is a nicety: when it fails, the page's own loader reports the error.
	loader: () => api.readiness().catch(() => null),
	head: () => ({ meta: [{ title: pageTitle() }] }),
	component: Root,
	notFoundComponent: NotFound,
});

function Root() {
	const readiness = Route.useLoaderData();
	return (
		<ThemeProvider>
			<HeadContent />
			<SiteHeader readiness={readiness} />
			{/* Every page fits the screen below the 3rem header; overflow scrolls only on very small screens. */}
			<main className="mx-auto flex h-[calc(100dvh-3rem)] w-full max-w-7xl flex-col overflow-y-auto px-3 py-3 sm:px-5">
				<Outlet />
			</main>
			<TanStackDevtools
				config={{ position: "bottom-right" }}
				plugins={[
					{
						name: "TanStack Router",
						render: <TanStackRouterDevtoolsPanel />,
					},
				]}
			/>
		</ThemeProvider>
	);
}

function NotFound() {
	return (
		<div className="space-y-4">
			<h1 className="text-3xl font-semibold tracking-tight">Page not found</h1>
			<p className="text-muted-foreground">That page doesn't exist.</p>
			<Link to="/" className={buttonVariants()}>
				Go to study
			</Link>
		</div>
	);
}
