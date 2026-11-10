import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { SearchHitLabel } from "@/components/search-hit";
import {
	Command,
	CommandDialog,
	CommandEmpty,
	CommandInput,
	CommandItem,
	CommandList,
} from "@/components/ui/command";
import { useSearch } from "@/hooks/use-search";

/**
 * The search dialog itself (cmdk in a dialog). It loads on first use, so it stays out of
 * the first page load; `SearchDialog` owns the button and the shortcuts.
 */
export function SearchPalette({
	open,
	onOpenChange,
}: {
	open: boolean;
	onOpenChange: (open: boolean) => void;
}) {
	const [query, setQuery] = useState("");
	const hits = useSearch(query);
	const navigate = useNavigate();

	function openProblem(slug: string) {
		onOpenChange(false);
		setQuery("");
		navigate({ to: "/", search: { set: "all", slug } });
	}

	return (
		<CommandDialog
			open={open}
			onOpenChange={onOpenChange}
			title="Search problems"
			description="Find a problem by LeetCode number, title, topic or statement text."
			className="sm:max-w-2xl"
		>
			{/* The server ranks the hits, so cmdk must not filter them again. */}
			<Command shouldFilter={false}>
				<CommandInput
					value={query}
					onValueChange={setQuery}
					placeholder="LeetCode number, title, topic, or words from the problem"
				/>
				<CommandList className="max-h-[60dvh]">
					{query.trim() && <CommandEmpty>No problem matches.</CommandEmpty>}
					{hits.map((hit) => (
						<CommandItem
							key={hit.slug}
							value={hit.slug}
							onSelect={() => openProblem(hit.slug)}
						>
							<SearchHitLabel hit={hit} />
						</CommandItem>
					))}
				</CommandList>
			</Command>
		</CommandDialog>
	);
}
