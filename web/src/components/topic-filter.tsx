import { type FilterOption, FilterPicker } from "@/components/filter-picker";
import { api, type TopicQuery } from "@/lib/api";
import { cn } from "@/lib/utils";

const ALL_TOPICS = "All topics";

/**
 * Chooses one topic of a list, with how many of the list's problems (of the chosen
 * difficulty) carry each; the counts load when the list first opens.
 */
export function TopicFilter({
	value,
	list: { company, period, difficulty },
	onChange,
	className,
}: {
	value: string | undefined;
	/** The list whose topics to count. */
	list: TopicQuery;
	onChange: (topic: string | undefined) => void;
	className?: string;
}) {
	return (
		<FilterPicker
			label="Topic"
			noun="topics"
			value={value ?? ""}
			valueLabel={value ?? ALL_TOPICS}
			options={async (): Promise<FilterOption[]> => [
				{ value: "", label: ALL_TOPICS, count: null },
				...(await api.topics({ company, period, difficulty })).map((t) => ({
					value: t.topic,
					label: t.topic,
					count: t.problems,
				})),
			]}
			optionsKey={`${company}|${period}|${difficulty ?? ""}`}
			onChange={(topic) => onChange(topic || undefined)}
			className={cn("w-44", className)}
		/>
	);
}
