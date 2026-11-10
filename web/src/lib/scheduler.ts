/**
 * Study sets the server's Leitner scheduler can deal from (server/ owns the scheduling).
 * Keys are the `set` values of GET /api/deck; values are their labels.
 */
export const STUDY_SETS = {
	smart: "Due and new",
	due: "Due for review",
	new: "Not seen yet",
	again: "Visit again",
	less: "Visit less often",
	missed: "Missed topics",
	skipped: "Skipped",
	all: "All problems",
} as const;
export type StudySet = keyof typeof STUDY_SETS;
