import { useNavigate } from "@tanstack/react-router";
import { ListIcon, PencilIcon, Trash2Icon } from "lucide-react";
import { useState } from "react";
import {
	DeleteListDialog,
	NameListDialog,
} from "@/components/lists/list-dialogs";
import { PlanMenuButton } from "@/components/plan/saved-plans";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { UserList } from "@/lib/types";
import { deleteList, renameList } from "@/lib/user-lists";

/** A list's menu, loaded on first use (see `YourLists`): show, rename or delete it. */
export function ListMenu({
	list,
	onChange,
	defaultOpen,
}: {
	list: UserList;
	onChange: () => Promise<void>;
	defaultOpen: boolean;
}) {
	const navigate = useNavigate();
	const [dialog, setDialog] = useState<"rename" | "delete" | null>(null);
	const close = (open: boolean) => {
		if (!open) setDialog(null);
	};
	return (
		<>
			<DropdownMenu defaultOpen={defaultOpen}>
				<DropdownMenuTrigger render={<PlanMenuButton name={list.name} />} />
				<DropdownMenuContent align="end" className="w-44">
					<DropdownMenuItem
						onClick={() =>
							navigate({ to: "/problems", search: { list: list.id } })
						}
					>
						<ListIcon />
						Show its problems
					</DropdownMenuItem>
					<DropdownMenuItem onClick={() => setDialog("rename")}>
						<PencilIcon />
						Rename
					</DropdownMenuItem>
					<DropdownMenuItem
						variant="destructive"
						onClick={() => setDialog("delete")}
					>
						<Trash2Icon />
						Delete
					</DropdownMenuItem>
				</DropdownMenuContent>
			</DropdownMenu>
			{dialog === "rename" && (
				<NameListDialog
					open
					onOpenChange={close}
					title="Rename list"
					description="The new name shows wherever the list does."
					initial={list.name}
					action="Rename"
					onSave={(name) => renameList(list.id, name).then(onChange)}
				/>
			)}
			{dialog === "delete" && (
				<DeleteListDialog
					open
					onOpenChange={close}
					name={list.name}
					onDelete={() => deleteList(list.id).then(onChange)}
				/>
			)}
		</>
	);
}
