/** How a topic guess compares with the problem's tags; shown when the answer is revealed. */
export interface TopicResult {
	hits: string[];
	missed: string[];
	extra: string[];
	/** F1 of the guess against the listed topics. */
	score: number;
}

/** The same F1 the server stores with the attempt, computed here to show it at once. */
export function scoreTopics(guessed: string[], actual: string[]): TopicResult {
	const truth = new Set(actual);
	const guess = new Set(guessed);
	const hits = actual.filter((t) => guess.has(t));
	const missed = actual.filter((t) => !guess.has(t));
	const extra = guessed.filter((t) => !truth.has(t));
	const total = guess.size + truth.size;
	return { hits, missed, extra, score: total ? (2 * hits.length) / total : 0 };
}
