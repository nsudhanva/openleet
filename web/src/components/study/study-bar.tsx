import { CompanyPicker } from "@/components/company-picker";
import { Segmented } from "@/components/segmented";
import { SelectPicker } from "@/components/select-picker";
import type { CompanySearch } from "@/lib/companies";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import type { StudySearch } from "@/lib/schemas";
import {
	DIFFICULTIES,
	type Difficulty,
	isAskedPeriod,
	PERIOD_LABEL,
	PERIODS,
	type Period,
} from "@/lib/types";

const SET_ITEMS = Object.entries(STUDY_SETS).map(([value, label]) => ({
	value: value as StudySet,
	label,
}));
const DIFFICULTY_OPTIONS = DIFFICULTIES.map((value) => ({
	value,
	label: value,
}));
const PERIOD_ITEMS = PERIODS.map((value) => ({
	value,
	label: !isAskedPeriod(value)
		? PERIOD_LABEL[value]
		: value === "all"
			? "Asked any time"
			: `Asked in ${PERIOD_LABEL[value]}`,
}));

/**
 * Chooses which cards the session draws from, as items of the page's toolbar row. Changing
 * a filter drops any pinned card.
 */
export function StudyBar({
	search,
	topics,
	remaining,
	onChange,
}: {
	search: StudySearch & CompanySearch;
	topics: string[];
	remaining: number;
	onChange: (next: Partial<StudySearch & CompanySearch>) => void;
}) {
	const topicItems = [
		{ value: null, label: "All topics" },
		...[...topics].sort().map((t) => ({ value: t, label: t })),
	];
	return (
		<>
			<CompanyPicker
				value={search.company}
				// LC 1–1000 is the same list for every company.
				disabled={!isAskedPeriod(search.period)}
				onChange={(company) => onChange({ company, slug: undefined })}
			/>
			<SelectPicker<Period>
				label="Problem list"
				value={search.period}
				items={PERIOD_ITEMS}
				onChange={(period) => onChange({ period, slug: undefined })}
			/>
			<SelectPicker
				label="Study set"
				value={search.set}
				items={SET_ITEMS}
				onChange={(set) => onChange({ set, slug: undefined })}
			/>
			<SelectPicker<string | null>
				label="Topic"
				value={search.topic ?? null}
				items={topicItems}
				onChange={(topic) =>
					onChange({ topic: topic ?? undefined, slug: undefined })
				}
			/>
			<Segmented<Difficulty>
				label="Difficulty"
				value={search.difficulty ?? null}
				options={DIFFICULTY_OPTIONS}
				deselectable
				itemClassName="bg-card"
				onChange={(difficulty) =>
					onChange({ difficulty: difficulty ?? undefined, slug: undefined })
				}
			/>
			<p className="ml-auto text-sm text-muted-foreground tabular-nums">
				{remaining} {remaining === 1 ? "card" : "cards"} in this set
			</p>
		</>
	);
}
