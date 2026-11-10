import { Link, type LinkProps } from "@tanstack/react-router";
import { GalleryVerticalEndIcon } from "lucide-react";
import { ModeToggle } from "@/components/mode-toggle";
import { SearchDialog } from "@/components/search-dialog";
import { buttonVariants } from "@/components/ui/button";
import { percent } from "@/lib/format";
import { cn } from "@/lib/utils";

const NAV: { to: LinkProps["to"]; label: string; exact?: boolean }[] = [
	{ to: "/", label: "Study", exact: true },
	{ to: "/problems", label: "Problems" },
	{ to: "/progress", label: "Progress" },
	{ to: "/about", label: "About" },
];

/** `readiness` is null while the server cannot say; the header then leaves it out. */
export function SiteHeader({ readiness }: { readiness: number | null }) {
	return (
		<header className="sticky top-0 z-40 h-12 border-b bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/70">
			<div className="mx-auto flex h-full max-w-7xl items-center gap-1 px-2 sm:gap-2 sm:px-5">
				<Link
					to="/"
					search={{}}
					className="mr-1 flex items-center gap-2 font-bold tracking-tight sm:mr-2"
					aria-label="Google LeetCode cards home"
				>
					<GalleryVerticalEndIcon
						className="size-5 text-card-margin"
						aria-hidden
					/>
					<span className="hidden xl:inline">Google LeetCode cards</span>
				</Link>
				<nav aria-label="Main" className="flex items-center gap-0.5">
					{NAV.map(({ to, label, exact }) => (
						<Link
							key={label}
							to={to}
							activeOptions={{ exact, includeSearch: false }}
							className={cn(
								buttonVariants({ variant: "ghost", size: "sm" }),
								"px-2 text-muted-foreground data-[status=active]:bg-muted data-[status=active]:text-foreground sm:px-2.5",
							)}
						>
							{label}
						</Link>
					))}
				</nav>
				<div className="ml-auto flex items-center gap-0.5 sm:gap-1">
					<SearchDialog />
					{readiness !== null && (
						<Link
							to="/progress"
							className="hidden items-center gap-2 rounded-md px-2 py-1 text-sm text-muted-foreground hover:text-foreground lg:flex"
							title="Readiness, updated by the background scorer"
						>
							Readiness
							<span className="font-semibold text-foreground tabular-nums">
								{percent(readiness, 1)}
							</span>
						</Link>
					)}
					<ModeToggle />
				</div>
			</div>
		</header>
	);
}
