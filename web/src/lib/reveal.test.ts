import { afterEach, describe, expect, it, vi } from "vitest";
import { lockedGuess, lockGuess } from "@/lib/reveal";

/** A session store in memory, as a browser tab has. */
function memoryStorage(): Storage {
	const items = new Map<string, string>();
	return {
		get length() {
			return items.size;
		},
		clear: () => items.clear(),
		getItem: (key) => items.get(key) ?? null,
		key: (i) => [...items.keys()][i] ?? null,
		removeItem: (key) => void items.delete(key),
		setItem: (key, value) => void items.set(key, value),
	};
}

describe("a revealed card's guess", () => {
	afterEach(() => vi.unstubAllGlobals());

	it("stays locked for the card until it is graded", () => {
		vi.stubGlobal("sessionStorage", memoryStorage());
		expect(lockedGuess("two-sum:0")).toBeNull();
		lockGuess("two-sum:0", { guessed: ["Array"], hints: 1 });
		expect(lockedGuess("two-sum:0")).toEqual({ guessed: ["Array"], hints: 1 });
		// Grading gives the card a new last-graded time: a fresh guess.
		expect(lockedGuess("two-sum:1793316907566")).toBeNull();
	});

	it("ignores what it cannot read, and storage that is not there", () => {
		const storage = memoryStorage();
		vi.stubGlobal("sessionStorage", storage);
		storage.setItem("openleet:revealed:a:0", "{not json");
		storage.setItem("openleet:revealed:b:0", '{"guessed": "Array"}');
		expect(lockedGuess("a:0")).toBeNull();
		expect(lockedGuess("b:0")).toBeNull();
		vi.stubGlobal("sessionStorage", undefined);
		expect(() => lockGuess("a:0", { guessed: [], hints: 0 })).not.toThrow();
		expect(lockedGuess("a:0")).toBeNull();
	});
});
