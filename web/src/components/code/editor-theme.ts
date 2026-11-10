import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { EditorView } from "@codemirror/view";
import { tags as t } from "@lezer/highlight";

/**
 * Colors come from CSS variables (styles.css), so the editor follows the light and dark
 * themes without reconfiguring.
 */
const chrome = EditorView.theme({
	"&": {
		height: "100%",
		backgroundColor: "var(--card)",
		color: "var(--card-foreground)",
		fontSize: "13px",
	},
	"&.cm-focused": { outline: "none" },
	".cm-scroller": { fontFamily: "inherit", lineHeight: "1.6" },
	".cm-content": { caretColor: "var(--primary)" },
	".cm-cursor, .cm-dropCursor": { borderLeftColor: "var(--primary)" },
	"&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
		{ backgroundColor: "var(--code-selection)" },
	".cm-gutters": {
		backgroundColor: "var(--card)",
		color: "var(--muted-foreground)",
		borderRight: "1px dashed var(--border)",
	},
	".cm-activeLine": { backgroundColor: "var(--code-active-line)" },
	".cm-activeLineGutter": {
		backgroundColor: "var(--code-active-line)",
		color: "var(--foreground)",
	},
	"&.cm-focused .cm-matchingBracket": {
		backgroundColor: "var(--code-selection)",
		outline: "1px solid var(--primary)",
	},
	"&.cm-focused .cm-nonmatchingBracket": {
		backgroundColor: "var(--destructive-wash)",
	},
	".cm-searchMatch": { backgroundColor: "var(--warning-wash)" },
	".cm-foldPlaceholder": {
		backgroundColor: "var(--muted)",
		color: "var(--muted-foreground)",
		border: "none",
	},
	".cm-tooltip": {
		backgroundColor: "var(--popover)",
		color: "var(--popover-foreground)",
		border: "1px solid var(--border)",
		borderRadius: "6px",
	},
	".cm-tooltip-autocomplete > ul > li[aria-selected]": {
		backgroundColor: "var(--accent)",
		color: "var(--accent-foreground)",
	},
	".cm-panels": {
		backgroundColor: "var(--muted)",
		color: "var(--foreground)",
	},
});

const highlight = HighlightStyle.define([
	{
		tag: [
			t.keyword,
			t.controlKeyword,
			t.definitionKeyword,
			t.operatorKeyword,
			t.moduleKeyword,
		],
		color: "var(--syntax-keyword)",
	},
	{ tag: [t.string, t.special(t.string)], color: "var(--syntax-string)" },
	{ tag: [t.number, t.bool, t.null, t.atom], color: "var(--syntax-number)" },
	{ tag: t.comment, color: "var(--syntax-comment)", fontStyle: "italic" },
	{
		tag: [
			t.function(t.variableName),
			t.function(t.definition(t.variableName)),
			t.function(t.propertyName),
		],
		color: "var(--syntax-function)",
	},
	{
		tag: [t.className, t.definition(t.className), t.typeName, t.self],
		color: "var(--syntax-type)",
	},
	{
		tag: [t.operator, t.punctuation, t.bracket],
		color: "var(--muted-foreground)",
	},
	{ tag: t.invalid, color: "var(--destructive)" },
]);

export const editorTheme = [chrome, syntaxHighlighting(highlight)];
