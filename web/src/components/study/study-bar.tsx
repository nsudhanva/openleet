import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
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
const PERIOD_ITEMS = PERIODS.map((value) => ({
	value,
	label: isAskedPeriod(value)
		? `Asked in ${PERIOD_LABEL[value]}`
		: PERIOD_LABEL[value],
}));

function Picker<T extends string | null>({
	label,
	value,
	items,
	onChange,
}: {
	label: string;
	value: T;
	items: { value: T; label: string }[];
	onChange: (value: T) => void;
}) {
	return (
		<Select
			value={value}
			items={items}
			onValueChange={(next) => onChange(next as T)}
		>
			<SelectTrigger aria-label={label} size="sm" className="bg-card">
				<SelectValue />
			</SelectTrigger>
			<SelectContent>
				{items.map((item) => (
					<SelectItem key={item.value ?? ""} value={item.value}>
						{item.label}
					</SelectItem>
				))}
			</SelectContent>
		</Select>
	);
}

/** Chooses which cards the session draws from. Changing a filter drops any pinned card. */
export function StudyBar({
	search,
	topics,
	remaining,
	onChange,
}: {
	search: StudySearch;
	topics: string[];
	remaining: number;
	onChange: (next: Partial<StudySearch>) => void;
}) {
	const topicItems = [
		{ value: null, label: "All topics" },
		...[...topics].sort().map((t) => ({ value: t, label: t })),
	];
	return (
		<div className="flex flex-wrap items-center gap-2">
			<Picker<Period>
				label="Problem list"
				value={search.period}
				items={PERIOD_ITEMS}
				onChange={(period) => onChange({ period, slug: undefined })}
			/>
			<Picker
				label="Study set"
				value={search.set}
				items={SET_ITEMS}
				onChange={(set) => onChange({ set, slug: undefined })}
			/>
			<Picker<string | null>
				label="Topic"
				value={search.topic ?? null}
				items={topicItems}
				onChange={(topic) =>
					onChange({ topic: topic ?? undefined, slug: undefined })
				}
			/>
			<ToggleGroup
				variant="outline"
				size="sm"
				aria-label="Difficulty"
				value={search.difficulty ? [search.difficulty] : []}
				onValueChange={(value) =>
					onChange({
						difficulty: value.at(-1) as Difficulty | undefined,
						slug: undefined,
					})
				}
			>
				{DIFFICULTIES.map((d) => (
					<ToggleGroupItem key={d} value={d} className="bg-card">
						{d}
					</ToggleGroupItem>
				))}
			</ToggleGroup>
			<p className="ml-auto text-sm text-muted-foreground tabular-nums">
				{remaining} {remaining === 1 ? "card" : "cards"} in this set
			</p>
		</div>
	);
}
