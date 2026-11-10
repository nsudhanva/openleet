import type { SearchSchemaInput } from "@tanstack/react-router";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import {
	DIFFICULTIES,
	type Difficulty,
	PERIODS,
	type Period,
} from "@/lib/types";

/** Search params of the study page, which are also the query of GET /api/deck. */
// A type, not an interface, so it fits the API client's query record.
export type StudySearch = {
	set: StudySet;
	period: Period;
	topic?: string;
	difficulty?: Difficulty;
	/** Show this problem instead of the next one in the queue. */
	slug?: string;
};

const SET_KEYS = Object.keys(STUDY_SETS) as StudySet[];

function oneOf<T extends string>(
	values: readonly T[],
	value: unknown,
): T | undefined {
	return values.find((v) => v === value);
}

const text = (value: unknown) =>
	typeof value === "string" ? value : undefined;

/**
 * Parses the study page's search params: an invalid set or period falls back to the
 * default, any other invalid param is dropped. Links may leave out any of them.
 */
export function parseStudySearch(
	search: Partial<StudySearch> & SearchSchemaInput,
): StudySearch {
	// Typed for links; from the URL any value can be anything.
	const raw: Partial<Record<keyof StudySearch, unknown>> = search;
	const parsed: StudySearch = {
		set: oneOf(SET_KEYS, raw.set) ?? "smart",
		period: oneOf(PERIODS, raw.period) ?? "6m",
		topic: text(raw.topic),
		difficulty: oneOf(DIFFICULTIES, raw.difficulty),
		slug: text(raw.slug),
	};
	for (const key of Object.keys(parsed) as (keyof StudySearch)[]) {
		if (parsed[key] === undefined) delete parsed[key];
	}
	return parsed;
}
