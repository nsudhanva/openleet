import { type FormEvent, useState } from "react";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { messageOf } from "@/lib/api";

/** The longest name the server keeps. */
const MAX_NAME = 60;

interface DialogProps {
	open: boolean;
	onOpenChange: (open: boolean) => void;
}

/** Runs a change, keeping the dialog open with the error when it fails. */
function useChange(onOpenChange: (open: boolean) => void) {
	const [busy, setBusy] = useState(false);
	const [error, setError] = useState<string | null>(null);
	async function run(change: () => Promise<unknown>) {
		setBusy(true);
		setError(null);
		try {
			await change();
			onOpenChange(false);
		} catch (failure) {
			setError(messageOf(failure));
		} finally {
			setBusy(false);
		}
	}
	return { busy, error, run };
}

/** Asks for a list's name, to make a list or rename one. */
export function NameListDialog({
	open,
	onOpenChange,
	title,
	description,
	initial = "",
	action,
	onSave,
}: DialogProps & {
	title: string;
	description: string;
	initial?: string;
	/** The save button's text: "Create list", "Rename". */
	action: string;
	onSave: (name: string) => Promise<unknown>;
}) {
	const [name, setName] = useState(initial);
	const { busy, error, run } = useChange(onOpenChange);
	const submit = (event: FormEvent) => {
		event.preventDefault();
		const trimmed = name.trim();
		if (trimmed) void run(() => onSave(trimmed));
	};
	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent>
				<form onSubmit={submit} className="space-y-4">
					<DialogHeader>
						<DialogTitle>{title}</DialogTitle>
						<DialogDescription>{description}</DialogDescription>
					</DialogHeader>
					<Input
						// The dialog is there to take the name, so the cursor goes there.
						autoFocus
						aria-label="List name"
						name="list-name"
						value={name}
						maxLength={MAX_NAME}
						placeholder="For example: Stacks to redo"
						onChange={(event) => setName(event.target.value)}
					/>
					{error && (
						<p role="alert" className="text-sm text-destructive">
							{error}
						</p>
					)}
					<DialogFooter>
						<Button
							type="button"
							variant="outline"
							onClick={() => onOpenChange(false)}
						>
							Cancel
						</Button>
						<Button type="submit" disabled={busy || !name.trim()}>
							{action}
						</Button>
					</DialogFooter>
				</form>
			</DialogContent>
		</Dialog>
	);
}

/** Confirms that a list goes; its problems and your progress on them stay. */
export function DeleteListDialog({
	open,
	onOpenChange,
	name,
	onDelete,
}: DialogProps & { name: string; onDelete: () => Promise<unknown> }) {
	const { busy, error, run } = useChange(onOpenChange);
	return (
		<AlertDialog open={open} onOpenChange={onOpenChange}>
			<AlertDialogContent>
				<AlertDialogHeader>
					<AlertDialogTitle>Delete “{name}”?</AlertDialogTitle>
					<AlertDialogDescription>
						The list goes. Its problems, and your progress on them, stay.
					</AlertDialogDescription>
					{error && (
						<p role="alert" className="text-sm text-destructive">
							{error}
						</p>
					)}
				</AlertDialogHeader>
				<AlertDialogFooter>
					<AlertDialogCancel>Keep it</AlertDialogCancel>
					<AlertDialogAction
						variant="destructive"
						disabled={busy}
						onClick={() => void run(onDelete)}
					>
						Delete list
					</AlertDialogAction>
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
}
