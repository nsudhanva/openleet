import { PencilIcon, PinIcon, PinOffIcon, Trash2Icon } from "lucide-react";
import { PlanMenuButton } from "@/components/plan/saved-plans";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

/** A saved plan's menu, loaded on first use (see `SavedPlans`). */
export function PlanMenu({
	name,
	pinned,
	onPin,
	onRename,
	onRemove,
	defaultOpen,
}: {
	name: string;
	pinned: boolean;
	onPin: () => void;
	onRename: () => void;
	onRemove: () => void;
	defaultOpen: boolean;
}) {
	return (
		<DropdownMenu defaultOpen={defaultOpen}>
			<DropdownMenuTrigger render={<PlanMenuButton name={name} />} />
			<DropdownMenuContent align="end" className="w-40">
				<DropdownMenuItem onClick={onPin}>
					{pinned ? <PinOffIcon /> : <PinIcon />}
					{pinned ? "Unpin" : "Pin"}
				</DropdownMenuItem>
				<DropdownMenuItem onClick={onRename}>
					<PencilIcon />
					Rename
				</DropdownMenuItem>
				<DropdownMenuItem variant="destructive" onClick={onRemove}>
					<Trash2Icon />
					Remove
				</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
