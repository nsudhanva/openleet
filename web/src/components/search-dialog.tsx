import { SearchIcon } from "lucide-react";
import { lazy, Suspense, useState } from "react";
import { KeyHint } from "@/components/action-button";
import { Button } from "@/components/ui/button";
import { useHotkeys, useModKeys } from "@/hooks/use-hotkeys";
import { useLoadOnUse } from "@/hooks/use-load-on-use";

const loadPalette = () => import("@/components/search-palette");
const SearchPalette = lazy(async () => ({
	default: (await loadPalette()).SearchPalette,
}));

/**
 * Jump to any problem by LeetCode number, title, topic or statement text (⌘K or /). The
 * dialog loads when first wanted: on pointing at or focusing the button, or on opening.
 */
export function SearchDialog() {
	const [open, setOpen] = useState(false);
	// Once loaded it stays mounted, so closing can animate.
	const { used, use, prefetchProps } = useLoadOnUse(loadPalette);
	const toggle = (next: (open: boolean) => boolean) => {
		use();
		setOpen(next);
	};

	useHotkeys({ "/": () => toggle(() => true) });
	useModKeys({ k: () => toggle((o) => !o) });

	return (
		<>
			<Button
				variant="outline"
				size="sm"
				className="w-9 justify-start text-muted-foreground sm:w-56"
				onClick={() => toggle(() => true)}
				{...prefetchProps}
				// The name is the visible text, the shortcut included, so they never disagree.
				aria-keyshortcuts="Meta+K Control+K /"
			>
				<SearchIcon aria-hidden />
				<span className="max-sm:sr-only">Search problems</span>
				<KeyHint className="ml-auto">⌘K</KeyHint>
			</Button>
			{used && (
				<Suspense fallback={null}>
					<SearchPalette open={open} onOpenChange={setOpen} />
				</Suspense>
			)}
		</>
	);
}
