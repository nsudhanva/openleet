import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { SearchHit } from "@/lib/types";

const DEBOUNCE_MS = 120;
const MAX_QUERY = 200;

/** Server-ranked hits for a query, debounced; a newer query cancels the older request. */
export function useSearch(query: string, limit = 20): SearchHit[] {
	const [hits, setHits] = useState<SearchHit[]>([]);

	useEffect(() => {
		const q = query.trim().slice(0, MAX_QUERY);
		if (!q) {
			setHits([]);
			return;
		}
		const abort = new AbortController();
		const timer = setTimeout(async () => {
			try {
				setHits(await api.search(q, limit, abort.signal));
			} catch (error) {
				if (abort.signal.aborted) return;
				console.error("Search failed", error);
				setHits([]);
			}
		}, DEBOUNCE_MS);
		return () => {
			abort.abort();
			clearTimeout(timer);
		};
	}, [query, limit]);

	return hits;
}
