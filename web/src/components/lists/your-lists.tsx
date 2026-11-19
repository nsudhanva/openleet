import { PlusIcon } from "lucide-react";
import { lazy, Suspense, useState } from "react";
import { PlanLink } from "@/components/plan/plan-link";
import { PlanMenuButton } from "@/components/plan/saved-plans";
import { ProgressBar } from "@/components/progress-bar";
import { Button, buttonVariants } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { planOf, progressShare } from "@/lib/plan";
import type { UserList } from "@/lib/types";
import { createList } from "@/lib/user-lists";
import { cn } from "@/lib/utils";

const loadMenu = () => import("@/components/lists/list-menu");
const ListMenu = lazy(async () => ({ default: (await loadMenu()).ListMenu }));
const loadDialogs = () => import("@/components/lists/list-dialogs");
const NameListDialog = lazy(async () => ({
	default: (await loadDialogs()).NameListDialog,
}));

/**
 * Your own lists, newest first: each with its progress, Continue (its next problem) and a
 * menu to show, rename or delete it, and a button to make a new one. `onChange` reloads
 * them after an edit.
 */
export function YourLists({
	lists,
	onChange,
}: {
	lists: UserList[];
	onChange: () => Promise<void>;
}) {
	const [naming, setNaming] = useState(false);
	const dialogs = useLoadOnUse(loadDialogs);
	return (
		<section aria-labelledby="lists-heading" className="mb-3">
			<div className="mb-1.5 flex items-baseline gap-3">
				<h2 id="lists-heading" className="text-sm font-semibold">
					Your lists
				</h2>
				<p className="text-xs text-muted-foreground max-sm:hidden">
					{lists.length
						? "Problems you picked, in the order you added them."
						: "Tick problems below and add them to a list, or start an empty one."}
				</p>
				<Button
					variant="link"
					size="xs"
					className="ml-auto px-0"
					{...dialogs.prefetchProps}
					onClick={() => {
						dialogs.use();
						setNaming(true);
					}}
				>
					<PlusIcon data-icon="inline-start" />
					New list
				</Button>
			</div>
			{lists.length > 0 && (
				<ul className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
					{lists.map((list) => (
						<ListRow key={list.id} list={list} onChange={onChange} />
					))}
				</ul>
			)}
			{naming && (
				<Suspense fallback={null}>
					<NameListDialog
						open
						onOpenChange={setNaming}
						title="New list"
						description="Name the list, then add problems with Add to list."
						action="Create list"
						onSave={(name) => createList(name).then(onChange)}
					/>
				</Suspense>
			)}
		</section>
	);
}

function ListRow({
	list,
	onChange,
}: {
	list: UserList;
	onChange: () => Promise<void>;
}) {
	const { used, use, prefetchProps } = useLoadOnUse(loadMenu);
	const { solved, total } = list.progress;
	const menuButton = (
		<PlanMenuButton name={list.name} {...prefetchProps} onClick={use} />
	);
	return (
		<li className="flex min-w-0 items-center gap-2 rounded-sm bg-card py-2 pr-1.5 pl-3 shadow-[0_1px_0_var(--border)]">
			<div className="min-w-0 flex-1">
				<p className="truncate text-sm font-medium">{list.name}</p>
				<div className="mt-1 flex items-center gap-2">
					<ProgressBar
						value={progressShare(list.progress)}
						className="h-1.5 flex-1"
					/>
					<span className="shrink-0 text-xs text-muted-foreground tabular-nums">
						{solved} of {total}
					</span>
				</div>
			</div>
			{list.next ? (
				<PlanLink
					plan={planOf(list.plan)}
					slug={list.next.slug}
					title={`Next: ${list.next.title}`}
					className={cn(
						buttonVariants({ variant: "outline", size: "sm" }),
						"shrink-0 bg-card",
					)}
				>
					Continue
				</PlanLink>
			) : (
				<span
					className={cn(
						"shrink-0 px-2 text-xs",
						total ? "text-success" : "text-muted-foreground",
					)}
				>
					{total ? "All solved" : "Empty"}
				</span>
			)}
			{used ? (
				<Suspense fallback={menuButton}>
					<ListMenu list={list} onChange={onChange} defaultOpen />
				</Suspense>
			) : (
				menuButton
			)}
		</li>
	);
}
