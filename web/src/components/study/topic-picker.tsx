import { SearchIcon } from "lucide-react";
import { useState } from "react";
import { FitPages } from "@/components/fit-pages";
import { Segmented } from "@/components/segmented";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

const COMMON_COUNT = 24;

export function TopicPicker({
	topics,
	selected,
	onToggle,
	className,
}: {
	/** Every topic, most common first. */
	topics: string[];
	selected: string[];
	onToggle: (topic: string) => void;
	className?: string;
}) {
	const [query, setQuery] = useState("");
	const [scope, setScope] = useState<"common" | "all">("common");

	const needle = query.trim().toLowerCase();
	const common = topics.slice(0, COMMON_COUNT);
	const visible = needle
		? topics.filter((t) => t.toLowerCase().includes(needle))
		: scope === "all"
			? topics
			: [...common, ...selected.filter((t) => !common.includes(t))];

	return (
		<div className={cn("flex min-h-0 flex-col gap-2", className)}>
			<div className="flex items-center gap-2">
				<div className="relative flex-1">
					<SearchIcon
						className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground"
						aria-hidden
					/>
					<Input
						value={query}
						onChange={(e) => setQuery(e.target.value)}
						onKeyDown={(e) => {
							if (e.key === "Enter" && visible[0]) {
								e.preventDefault();
								onToggle(visible[0]);
								setQuery("");
							}
							if (e.key === "Escape") e.currentTarget.blur();
						}}
						placeholder={`Find among ${topics.length} topics`}
						aria-label="Find a topic"
						className="h-7 pl-8 text-sm"
					/>
				</div>
				<Segmented
					label="Topics to show"
					value={scope}
					onChange={setScope}
					options={[
						{ value: "common", label: "Common" },
						{ value: "all", label: "All" },
					]}
				/>
			</div>
			{/* Remount when the list changes so FitPages measures the new chips. */}
			<FitPages key={`${needle}|${scope}|${visible.length}`}>
				{/* Inline chips, not flex, so they flow across FitPages columns. */}
				<ul aria-label="Topics">
					{visible.map((topic) => {
						const on = selected.includes(topic);
						return (
							<li key={topic} className="mr-1.5 mb-1.5 inline-block">
								<button
									type="button"
									aria-pressed={on}
									onClick={() => onToggle(topic)}
									className={cn(
										"rounded-full border px-2.5 py-0.5 fit-text-90 transition-colors focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:outline-none",
										on
											? "border-primary bg-primary text-primary-foreground"
											: "bg-card text-foreground hover:border-primary/60 hover:bg-muted",
									)}
								>
									{topic}
								</button>
							</li>
						);
					})}
					{needle && visible.length === 0 && (
						<li className="text-muted-foreground">
							No topic matches “{query}”.
						</li>
					)}
				</ul>
			</FitPages>
		</div>
	);
}
