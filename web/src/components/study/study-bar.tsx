import { CompanyPicker } from "@/components/company-picker";
import { DifficultyFilter } from "@/components/difficulty-filter";
import { SelectPicker } from "@/components/select-picker";
import { TopicFilter } from "@/components/topic-filter";
import type { CompanySearch } from "@/lib/companies";
import { count } from "@/lib/format";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import type { StudySearch } from "@/lib/schemas";
import { isAskedPeriod, PERIOD_LABEL, PERIODS, type Period } from "@/lib/types";

const SET_ITEMS = Object.entries(STUDY_SETS).map(([value, label]) => ({
	value: value as StudySet,
	label,
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
	remaining,
	onChange,
}: {
	search: StudySearch & CompanySearch;
	remaining: number;
	onChange: (next: Partial<StudySearch & CompanySearch>) => void;
}) {
	const change = (next: Partial<StudySearch & CompanySearch>) =>
		onChange({ ...next, slug: undefined });
	return (
		<>
			<CompanyPicker
				value={search.company}
				// LC 1–1000 is the same list for every company.
				disabled={!isAskedPeriod(search.period)}
				onChange={(company) => change({ company })}
			/>
			<SelectPicker<Period>
				label="Problem list"
				value={search.period}
				items={PERIOD_ITEMS}
				onChange={(period) => change({ period })}
			/>
			<SelectPicker
				label="Study set"
				value={search.set}
				items={SET_ITEMS}
				onChange={(set) => change({ set })}
			/>
			<TopicFilter
				value={search.topic}
				list={search}
				onChange={(topic) => change({ topic })}
			/>
			<DifficultyFilter
				value={search.difficulty}
				onChange={(difficulty) => change({ difficulty })}
			/>
			{/*
			 * Wide enough for "3092 cards in this set", so a new count never moves the row; on a
			 * fit: screen too narrow for the row, just "3092 cards".
			 */}
			<p className="text-sm text-muted-foreground tabular-nums max-sm:col-span-2 sm:ml-auto sm:min-w-[22ch] sm:text-right fit:max-xl:min-w-[10ch]">
				{count(remaining, "card")}
				<span className="fit:max-xl:hidden"> in this set</span>
			</p>
		</>
	);
}
