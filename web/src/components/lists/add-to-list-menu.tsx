import { PlusIcon } from "lucide-react";
import { useState } from "react";
import { AddToListTrigger } from "@/components/lists/add-to-list";
import { NameListDialog } from "@/components/lists/list-dialogs";
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuGroup,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { messageOf } from "@/lib/api";
import {
	addToList,
	createList,
	removeFromList,
	useUserLists,
} from "@/lib/user-lists";

/**
 * Your lists with a tick on those that hold every one of `slugs`: ticking adds them at the
 * end of a list, unticking takes them off. "New list" starts a list with them.
 */
export function AddToListMenu({
	slugs,
	onChange,
	className,
	defaultOpen,
}: {
	slugs: string[];
	onChange?: () => void;
	className?: string;
	defaultOpen: boolean;
}) {
	const lists = useUserLists();
	const [naming, setNaming] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const what = slugs.length === 1 ? "this problem" : `${slugs.length} problems`;

	async function run(change: Promise<unknown>) {
		setError(null);
		try {
			await change;
			onChange?.();
		} catch (failure) {
			setError(messageOf(failure));
		}
	}

	return (
		<>
			<DropdownMenu defaultOpen={defaultOpen}>
				<DropdownMenuTrigger
					render={<AddToListTrigger className={className} />}
				/>
				<DropdownMenuContent align="end" className="w-64">
					<DropdownMenuGroup>
						<DropdownMenuLabel>Add {what} to</DropdownMenuLabel>
						{lists === undefined && (
							<DropdownMenuItem disabled>Loading your lists…</DropdownMenuItem>
						)}
						{lists?.length === 0 && (
							<DropdownMenuItem disabled>
								You have no lists yet
							</DropdownMenuItem>
						)}
						{lists?.map((list) => {
							const holds = slugs.every((s) => list.slugs.includes(s));
							return (
								<DropdownMenuCheckboxItem
									key={list.id}
									checked={holds}
									closeOnClick={false}
									onCheckedChange={(checked) =>
										void run(
											checked
												? addToList(list, slugs)
												: removeFromList(list, slugs),
										)
									}
								>
									<span className="min-w-0 flex-1 truncate">{list.name}</span>
									<span className="text-xs text-muted-foreground tabular-nums">
										{list.slugs.length}
									</span>
								</DropdownMenuCheckboxItem>
							);
						})}
					</DropdownMenuGroup>
					{error && (
						<p role="alert" className="px-1.5 py-1 text-xs text-destructive">
							{error}
						</p>
					)}
					<DropdownMenuSeparator />
					<DropdownMenuItem onClick={() => setNaming(true)}>
						<PlusIcon />
						New list with {what}
					</DropdownMenuItem>
				</DropdownMenuContent>
			</DropdownMenu>
			{naming && (
				<NameListDialog
					open
					onOpenChange={setNaming}
					title="New list"
					description={`Name the list. It starts with ${what}.`}
					action="Create list"
					onSave={(name) => createList(name, slugs).then(() => onChange?.())}
				/>
			)}
		</>
	);
}
