import { NotebookPenIcon } from "lucide-react";
import {
	type KeyboardEvent,
	type ReactNode,
	useEffect,
	useRef,
	useState,
} from "react";
import { KeyHint } from "@/components/action-button";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

/**
 * Your answer to the problem, in your own words, written on the card's ruled lines.
 * Hidden when you have not written one; edited in place in the same box.
 * Cmd/Ctrl+Enter saves, Escape cancels.
 */
export function MyAnswer({
	note,
	editing,
	onEdit,
	onSave,
	onCancel,
}: {
	note: string | null;
	editing: boolean;
	onEdit: () => void;
	onSave: (text: string) => Promise<void>;
	onCancel: () => void;
}) {
	if (editing)
		return (
			<NoteEditor initial={note ?? ""} onSave={onSave} onCancel={onCancel} />
		);
	if (!note) return null;
	return (
		<NoteBox
			action={
				<Button variant="ghost" size="xs" onClick={onEdit}>
					Edit
					<KeyHint>M</KeyHint>
				</Button>
			}
		>
			<p className="card-ruled max-h-[11.9em] overflow-y-auto whitespace-pre-wrap">
				{note}
			</p>
		</NoteBox>
	);
}

function NoteBox({
	action,
	children,
	className,
}: {
	action?: ReactNode;
	children: ReactNode;
	className?: string;
}) {
	return (
		<section
			aria-label="My answer"
			className={cn(
				"shrink-0 rounded-md border border-dashed border-primary/40 px-3 pt-1.5 pb-2 text-sm",
				className,
			)}
		>
			<header className="flex h-6 items-center gap-1.5 text-xs font-medium text-muted-foreground">
				<NotebookPenIcon className="size-3.5 text-primary" aria-hidden />
				My answer
				<span className="ml-auto">{action}</span>
			</header>
			{children}
		</section>
	);
}

function NoteEditor({
	initial,
	onSave,
	onCancel,
}: {
	initial: string;
	onSave: (text: string) => Promise<void>;
	onCancel: () => void;
}) {
	const [draft, setDraft] = useState(initial);
	const [saving, setSaving] = useState(false);
	const [failed, setFailed] = useState(false);
	const field = useRef<HTMLTextAreaElement>(null);

	// Opening the editor is the user's own action, so the cursor goes there, after the text.
	useEffect(() => {
		const textarea = field.current;
		textarea?.focus();
		textarea?.setSelectionRange(textarea.value.length, textarea.value.length);
	}, []);

	async function save() {
		setSaving(true);
		setFailed(false);
		try {
			await onSave(draft);
		} catch {
			setFailed(true);
			setSaving(false);
		}
	}

	function onKeyDown(event: KeyboardEvent) {
		if (event.key === "Escape") onCancel();
		if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) save();
	}

	return (
		<NoteBox
			className="border-solid border-primary/70"
			action={
				!draft.trim() && initial && <span>Saving it empty deletes it</span>
			}
		>
			<form
				onSubmit={(event) => {
					event.preventDefault();
					save();
				}}
			>
				<textarea
					ref={field}
					aria-label="My answer"
					value={draft}
					maxLength={4000}
					placeholder="What you understood: the idea, the steps, the catch."
					onChange={(event) => setDraft(event.target.value)}
					onKeyDown={onKeyDown}
					className="card-ruled block field-sizing-content max-h-[11.9em] min-h-[3.4em] w-full resize-none bg-transparent [background-attachment:local] outline-none placeholder:text-muted-foreground"
				/>
				<div className="mt-2 flex items-center gap-2">
					<Button type="submit" size="xs" disabled={saving}>
						Save
						<KeyHint>⌘↵</KeyHint>
					</Button>
					<Button type="button" size="xs" variant="ghost" onClick={onCancel}>
						Cancel
						<KeyHint>Esc</KeyHint>
					</Button>
					{failed && (
						<p role="alert" className="text-xs text-destructive">
							Not saved. Try again.
						</p>
					)}
				</div>
			</form>
		</NoteBox>
	);
}
