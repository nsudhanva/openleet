import { useEffect, useRef, useState } from "react";
import type { ConfirmClearProps } from "@/components/confirm-clear";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
	AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

/**
 * The two-step dialog itself. Both steps open with "Keep progress" focused, and the second
 * step puts it where "Continue" was, so Enter, Space or a double click never clears anything.
 */
export function ConfirmClearDialog({
	trigger,
	children,
	title,
	description,
	onClear,
	defaultOpen = false,
}: ConfirmClearProps & { defaultOpen?: boolean }) {
	const [open, setOpen] = useState(defaultOpen);
	const [sure, setSure] = useState(false);
	const [busy, setBusy] = useState(false);
	const [failed, setFailed] = useState(false);
	const keep = useRef<HTMLButtonElement>(null);

	// The second question replaces the first in the same box; focus goes back to "Keep".
	useEffect(() => {
		if (sure) keep.current?.focus();
	}, [sure]);

	function onOpenChange(next: boolean) {
		setOpen(next);
		if (!next) {
			setSure(false);
			setFailed(false);
		}
	}

	async function clear() {
		setBusy(true);
		setFailed(false);
		try {
			await onClear();
			onOpenChange(false);
		} catch {
			setFailed(true);
		} finally {
			setBusy(false);
		}
	}

	return (
		<AlertDialog open={open} onOpenChange={onOpenChange}>
			<AlertDialogTrigger render={trigger}>{children}</AlertDialogTrigger>
			<AlertDialogContent initialFocus={keep}>
				<AlertDialogHeader>
					<AlertDialogTitle>{sure ? "Are you sure?" : title}</AlertDialogTitle>
					<AlertDialogDescription>
						{sure
							? "This is the last check. Cleared progress cannot be brought back."
							: description}
					</AlertDialogDescription>
					{failed && (
						<p role="alert" className="text-sm text-destructive">
							Not cleared. Try again.
						</p>
					)}
				</AlertDialogHeader>
				{/* "Keep progress" moves to where "Continue" was, so a double click keeps. */}
				<AlertDialogFooter>
					{sure ? (
						<>
							<AlertDialogAction
								variant="destructive"
								disabled={busy}
								onClick={clear}
							>
								Yes, clear it
							</AlertDialogAction>
							<AlertDialogCancel ref={keep}>Keep progress</AlertDialogCancel>
						</>
					) : (
						<>
							<AlertDialogCancel ref={keep}>Keep progress</AlertDialogCancel>
							<AlertDialogAction
								variant="outline"
								onClick={() => setSure(true)}
							>
								Continue
							</AlertDialogAction>
						</>
					)}
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
}
