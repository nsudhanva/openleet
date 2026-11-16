import { ExternalLinkIcon } from "lucide-react";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { VideosTrigger } from "@/components/videos-button";
import type { Video } from "@/lib/types";

/** The video list itself; `VideosButton` loads it on first use. Each video opens on YouTube. */
export function VideosMenu({
	videos,
	defaultOpen,
}: {
	videos: Video[];
	defaultOpen: boolean;
}) {
	return (
		<DropdownMenu defaultOpen={defaultOpen}>
			<DropdownMenuTrigger render={<VideosTrigger />} />
			<DropdownMenuContent
				align="end"
				className="w-80 max-w-[calc(100vw-2rem)]"
			>
				{videos.map((video) => (
					<DropdownMenuItem
						key={video.id}
						render={
							<a
								href={`https://www.youtube.com/watch?v=${video.id}`}
								target="_blank"
								rel="noreferrer"
							/>
						}
						className="items-start py-1.5"
					>
						<span className="flex min-w-0 flex-1 flex-col">
							<span className="font-medium">{video.creator}</span>
							<span className="line-clamp-2 text-xs text-muted-foreground">
								{video.title}
							</span>
						</span>
						<ExternalLinkIcon className="mt-0.5 text-muted-foreground" />
					</DropdownMenuItem>
				))}
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
