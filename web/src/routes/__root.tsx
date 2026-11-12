import { TanStackDevtools } from "@tanstack/react-devtools";
import {
	createRootRoute,
	HeadContent,
	Link,
	Outlet,
	retainSearchParams,
	stripSearchParams,
	useRouterState,
} from "@tanstack/react-router";
import { TanStackRouterDevtoolsPanel } from "@tanstack/react-router-devtools";
import { useLayoutEffect } from "react";
import { SiteHeader } from "@/components/site-header";
import { ThemeProvider } from "@/components/theme-provider";
import { buttonVariants } from "@/components/ui/button";
import { api } from "@/lib/api";
import { DEFAULT_COMPANY, parseCompanySearch } from "@/lib/companies";
import { pageTitle } from "@/lib/format";
import { isWidePage } from "@/lib/layout";

export const Route = createRootRoute({
	// The company is the one filter every page shares, so it follows you between pages.
	validateSearch: parseCompanySearch,
	search: {
		middlewares: [
			retainSearchParams(["company"]),
			stripSearchParams({ company: DEFAULT_COMPANY }),
		],
	},
	loaderDeps: ({ search: { company } }) => ({ company }),
	// Awaited, so the page paints in one go (a Suspense fallback would hold back the content
	// that follows it). Both are niceties: when they fail, the page's own loader reports it.
	loader: async ({ deps: { company } }) => {
		const [readiness, companies] = await Promise.all([
			api.readiness(company).catch(() => null),
			api.companies(),
		]);
		return { readiness, companies };
	},
	head: () => ({ meta: [{ title: pageTitle() }] }),
	component: Root,
	notFoundComponent: NotFound,
});

function Root() {
	const { readiness } = Route.useLoaderData();
	// The width follows the page on screen: the one being left stays as it was while the next loads.
	const pathname = useRouterState({
		select: (s) => (s.resolvedLocation ?? s.location).pathname,
	});
	useLayoutEffect(() => {
		document.documentElement.toggleAttribute("data-wide", isWidePage(pathname));
	}, [pathname]);
	return (
		<ThemeProvider>
			<HeadContent />
			<SiteHeader readiness={readiness} />
			{/* On a fit: screen every page fits it below the 3rem header; elsewhere the document scrolls. */}
			<main className="mx-auto flex w-full max-w-5xl wide:max-w-7xl flex-col px-3 py-3 sm:px-5 fit:h-[calc(100dvh-3rem)] fit:overflow-y-auto">
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
