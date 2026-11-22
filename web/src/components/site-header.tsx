import { Link, type LinkProps } from "@tanstack/react-router";
import { GalleryVerticalEndIcon, UserRoundIcon } from "lucide-react";
import { ModeToggle } from "@/components/mode-toggle";
import { SearchDialog } from "@/components/search-dialog";
import { buttonVariants } from "@/components/ui/button";
import { useCompanies, useCompany } from "@/hooks/use-companies";
import { ANY_COMPANY, companyName } from "@/lib/companies";
import { readinessLabel, readinessText } from "@/lib/readiness";
import type { Session } from "@/lib/types";
import { cn } from "@/lib/utils";

const NAV: {
	to: LinkProps["to"];
	label: string;
	exact?: boolean;
	account?: boolean;
}[] = [
	{ to: "/", label: "Study", exact: true, account: true },
	{ to: "/problems", label: "Problems", account: true },
	{ to: "/progress", label: "Progress", account: true },
	{ to: "/about", label: "About" },
];

/**
 * The header shows readiness only once there is a score; before that it leaves it out. The
 * study pages need an account, so signed out it links only About and Sign in.
 */
export function SiteHeader({ session }: { session: Session }) {
	const { user, readiness } = session;
	const company = useCompany();
	const name = companyName(useCompanies(), company);
	return (
		<header className="sticky top-0 z-40 h-12 border-b bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/70">
			<div className="mx-auto flex h-full max-w-[96rem] items-center gap-1 px-1 xs:px-2 sm:gap-2 sm:px-5">
				<Link
					to="/"
					search={{}}
					className="mr-1 flex h-9 min-w-9 items-center justify-center gap-2 font-bold tracking-tight max-xs:hidden sm:mr-2 md:justify-start"
					aria-label="OpenLeet home"
				>
					<GalleryVerticalEndIcon
						className="size-5 text-card-margin"
						aria-hidden
					/>
					<span className="hidden md:inline">OpenLeet</span>
				</Link>
				<nav aria-label="Main" className="flex items-center xs:gap-0.5">
					{NAV.filter(({ account }) => user || !account).map(
						({ to, label, exact }) => (
							<Link
								key={label}
								to={to}
								activeOptions={{ exact, includeSearch: false }}
								className={cn(
									buttonVariants({ variant: "ghost", size: "sm" }),
									"px-1 text-muted-foreground data-[status=active]:bg-muted data-[status=active]:text-foreground sm:px-2 md:px-2.5",
								)}
							>
								{label}
							</Link>
						),
					)}
				</nav>
				<div className="ml-auto flex items-center gap-0.5 sm:gap-1">
					<SearchDialog />
					{readiness?.score != null && (
						<Link
							to="/progress"
							className="hidden items-center gap-2 rounded-md px-2 py-1 text-sm text-muted-foreground hover:text-foreground lg:flex"
							title={readinessLabel(
								company === ANY_COMPANY ? null : name,
								readiness,
							)}
						>
							Ready
							<span className="font-semibold text-foreground tabular-nums">
								{readinessText(readiness)}
							</span>
						</Link>
					)}
					{user ? (
						<Link
							to="/account"
							title={user.email}
							aria-label={`Account: ${user.email}`}
							className={cn(
								buttonVariants({ variant: "ghost", size: "sm" }),
								"max-w-48 px-1.5 text-muted-foreground sm:px-2 data-[status=active]:bg-muted data-[status=active]:text-foreground",
							)}
						>
							<UserRoundIcon aria-hidden />
							<span className="hidden truncate lg:inline">{user.email}</span>
						</Link>
					) : (
						<Link
							to="/login"
							search={{ redirect: "/" }}
							className={cn(
								buttonVariants({ variant: "ghost", size: "sm" }),
								"px-1.5 text-muted-foreground xs:px-2",
							)}
						>
							Sign in
						</Link>
					)}
					<ModeToggle />
				</div>
			</div>
		</header>
	);
}
