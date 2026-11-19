import { PlusIcon } from "lucide-react";
import { useState } from "react";
import { PlanCard } from "@/components/plan/plan-card";
import { PlanMenuButton } from "@/components/plan/saved-plans";
import { Button } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import type { UserList } from "@/lib/types";
import { createList } from "@/lib/user-lists";

const loadMenu = () => import("@/components/lists/list-menu");
const loadDialogs = () => import("@/components/lists/list-dialogs");

/**
 * Your own lists, newest first: each with its progress, its problems, Continue (its next
 * problem) and a menu to rename or delete it, and a button to make a new one. `onChange` reloads
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
			{naming && dialogs.loaded && (
				<dialogs.loaded.NameListDialog
					open
					onOpenChange={setNaming}
					title="New list"
					description="Name the list, then add problems with Add to list."
					action="Create list"
					onSave={(name) => createList(name).then(onChange)}
				/>
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
	const { loaded, use, prefetchProps } = useLoadOnUse(loadMenu);
	const menuButton = (
		<PlanMenuButton name={list.name} {...prefetchProps} onClick={use} />
	);
	return (
		<PlanCard
			title={<p className="truncate text-sm font-medium">{list.name}</p>}
			plan={list.plan}
			progress={list.progress}
			next={list.next}
			menu={
				loaded ? (
					<loaded.ListMenu list={list} onChange={onChange} defaultOpen />
				) : (
					menuButton
				)
			}
		/>
	);
}
