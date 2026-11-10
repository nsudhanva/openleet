import { indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { indentUnit } from "@codemirror/language";
import { EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { basicSetup } from "codemirror";
import { type Ref, useEffect, useImperativeHandle, useRef } from "react";
import { editorTheme } from "@/components/code/editor-theme";
import { cn } from "@/lib/utils";

export interface CodeEditorHandle {
	/** Replaces the whole text as one undoable change. */
	setValue: (code: string) => void;
	focus: () => void;
}

/**
 * A Python editor (CodeMirror 6): line numbers, bracket matching, autoindent, Tab indents.
 * Uncontrolled: it starts from `initial` and reports every change through `onChange`.
 */
export function CodeEditor({
	initial,
	onChange,
	label,
	className,
	ref,
}: {
	initial: string;
	onChange: (code: string) => void;
	label: string;
	className?: string;
	ref?: Ref<CodeEditorHandle>;
}) {
	const host = useRef<HTMLDivElement>(null);
	const view = useRef<EditorView | null>(null);
	const latest = useRef({ initial, onChange, label });
	latest.current.onChange = onChange;

	useEffect(() => {
		const parent = host.current;
		if (!parent) return;
		const editor = new EditorView({
			parent,
			state: EditorState.create({
				doc: latest.current.initial,
				extensions: [
					basicSetup,
					keymap.of([indentWithTab]),
					indentUnit.of("    "),
					python(),
					editorTheme,
					EditorView.contentAttributes.of({
						"aria-label": latest.current.label,
					}),
					EditorView.updateListener.of((update) => {
						if (update.docChanged)
							latest.current.onChange(update.state.doc.toString());
					}),
				],
			}),
		});
		view.current = editor;
		return () => {
			editor.destroy();
			view.current = null;
		};
	}, []);

	useImperativeHandle(
		ref,
		() => ({
			setValue: (code) => {
				const editor = view.current;
				if (!editor) return;
				editor.dispatch({
					changes: { from: 0, to: editor.state.doc.length, insert: code },
				});
			},
			focus: () => view.current?.focus(),
		}),
		[],
	);

	return <div ref={host} className={cn("h-full font-mono", className)} />;
}
