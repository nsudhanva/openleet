import { ChevronDownIcon, CirclePlayIcon } from "lucide-react";
import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import type { Video } from "@/lib/types";
import { cn } from "@/lib/utils";

const loadMenu = () => import("@/components/videos-menu");

/** The button that opens the video list. */
export function VideosTrigger({
	className,
	...props
}: ComponentProps<typeof Button>) {
	return (
		<Button
			variant="ghost"
			size="xs"
			className={cn("shrink-0 text-muted-foreground", className)}
			{...props}
		>
			<CirclePlayIcon data-icon="inline-start" />
			<span className="max-sm:sr-only">Videos</span>
			<ChevronDownIcon data-icon="inline-end" />
		</Button>
	);
}

/** YouTube explanations of a problem in a menu, loaded on first use; nothing when it has none. */
export function VideosButton({ videos }: { videos: Video[] }) {
	const { loaded, use, prefetchProps } = useLoadOnUse(loadMenu);
	if (videos.length === 0) return null;
	if (!loaded) return <VideosTrigger {...prefetchProps} onClick={use} />;
	return <loaded.VideosMenu videos={videos} defaultOpen />;
}
