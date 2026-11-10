import { Segmented } from "@/components/segmented";
import { DIFFICULTIES, type Difficulty } from "@/lib/types";
import { cn } from "@/lib/utils";

type Choice = Difficulty | "all";

const OPTIONS: { value: Choice; label: string }[] = [
	{ value: "all", label: "All" },
	...DIFFICULTIES.map((value) => ({ value, label: value })),
];

/**
 * All, Easy, Medium or Hard: one switch, the same on every page that filters problems. On a
 * phone it takes a whole row of the filter grid, its options sharing it.
 */
export function DifficultyFilter({
	value,
	onChange,
	className,
}: {
	value: Difficulty | undefined;
	onChange: (difficulty: Difficulty | undefined) => void;
	className?: string;
}) {
	return (
		<Segmented<Choice>
			label="Difficulty"
			value={value ?? "all"}
			options={OPTIONS}
			onChange={(next) => onChange(next === "all" ? undefined : next)}
			className={cn(
				"max-sm:col-span-2 max-sm:grid max-sm:w-full max-sm:grid-cols-4",
				className,
			)}
			itemClassName="bg-card"
		/>
	);
}
