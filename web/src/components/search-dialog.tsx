import { useNavigate } from "@tanstack/react-router";
import { SearchIcon } from "lucide-react";
import { useState } from "react";
import { SearchHitLabel } from "@/components/search-hit";
import { Button } from "@/components/ui/button";
import {
	Command,
	CommandDialog,
	CommandEmpty,
	CommandInput,
	CommandItem,
	CommandList,
} from "@/components/ui/command";
import { Kbd } from "@/components/ui/kbd";
import { useHotkeys, useModKeys } from "@/hooks/use-hotkeys";
import { useSearch } from "@/hooks/use-search";

/** Jump to any problem by LeetCode number, title, topic or statement text (⌘K or /). */
export function SearchDialog() {
	const [open, setOpen] = useState(false);
	const [query, setQuery] = useState("");
	const hits = useSearch(query);
	const navigate = useNavigate();

	useHotkeys({ "/": () => setOpen(true) });
	useModKeys({ k: () => setOpen((o) => !o) });

	function openProblem(slug: string) {
		setOpen(false);
		setQuery("");
		navigate({ to: "/", search: { set: "all", slug } });
	}

	return (
		<>
			<Button
				variant="outline"
				size="sm"
				className="w-9 justify-start text-muted-foreground sm:w-56"
				onClick={() => setOpen(true)}
				aria-label="Search problems"
			>
				<SearchIcon />
				<span className="hidden sm:inline">Search problems</span>
				<Kbd className="ml-auto hidden sm:inline-flex">⌘K</Kbd>
			</Button>
			<CommandDialog
				open={open}
				onOpenChange={setOpen}
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
		</>
	);
}
