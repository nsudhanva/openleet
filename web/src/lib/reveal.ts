/**
 * The topic guess (and the hints opened) locked when a card's answer was shown, kept for the
 * browser session: a reload, or Back and forward again, shows that answer with the same
 * guess instead of a fresh guess for a card whose answer you have seen. A card is its slug
 * and its last grade's time, so grading it starts the next review clean.
 */

const PREFIX = "openleet:revealed:";

/** What was locked as the answer showed. */
export interface Locked {
	guessed: string[];
	hints: number;
}

/** What was locked for this card, or null while its answer was not shown. */
export function lockedGuess(card: string): Locked | null {
	try {
		const raw = sessionStorage.getItem(PREFIX + card);
		const value: Partial<Locked> | null = raw === null ? null : JSON.parse(raw);
		if (!Array.isArray(value?.guessed)) return null;
		return {
			guessed: value.guessed.filter((t): t is string => typeof t === "string"),
			hints: Number.isInteger(value.hints) ? Number(value.hints) : 0,
		};
	} catch {
		return null;
	}
}

/** Locks the guess and hints for this card as its answer is shown. */
export function lockGuess(card: string, locked: Locked): void {
	try {
		sessionStorage.setItem(PREFIX + card, JSON.stringify(locked));
	} catch {
		// Private windows and blocked storage: the lock lasts until the card unmounts.
	}
}
