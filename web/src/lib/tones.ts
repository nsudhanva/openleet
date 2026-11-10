/** Washed-background badge colors from the theme, shared by every status badge. */
export const TONE = {
	success: "bg-success-wash text-success",
	warning: "bg-warning-wash text-warning",
	destructive: "bg-destructive-wash text-destructive",
	muted: "bg-muted text-muted-foreground",
} as const;
export type Tone = keyof typeof TONE;

/** The same tones as plain text color, for headings. */
export const TONE_TEXT: Record<Tone, string> = {
	success: "text-success",
	warning: "text-warning",
	destructive: "text-destructive",
	muted: "text-muted-foreground",
};
