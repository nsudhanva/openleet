import {
	type CSSProperties,
	type ReactNode,
	useLayoutEffect,
	useRef,
	useState,
} from "react";
import { PagerControls } from "@/components/pager";
import { usePager } from "@/hooks/use-pager";
import { cn } from "@/lib/utils";

/** Font sizes to try, largest first; below the last one the content pages instead. */
const FONT_SIZES = [15, 14, 13, 12];
const COLUMN_GAP = 32;
const PAGER_HEIGHT = 28;

interface Layout {
	fontSize: number;
	pages: number;
	/** Column width and height while paged; 0 when everything fits on one page. */
	width: number;
	height: number;
}

/**
 * Fits its content in the box it is given, with no scrolling: it first shrinks the text,
 * then splits the content into side-by-side pages with a pager. With `arrowKeys`, ← and →
 * turn the pages. The box may be a fixed height or a shrinkable flex item that is only as
 * tall as its content.
 */
export function FitPages({
	children,
	className,
	arrowKeys = false,
}: {
	children: ReactNode;
	className?: string;
	arrowKeys?: boolean;
}) {
	const viewport = useRef<HTMLDivElement>(null);
	const content = useRef<HTMLDivElement>(null);
	const [layout, setLayout] = useState<Layout>({
		fontSize: FONT_SIZES[0],
		pages: 1,
		width: 0,
		height: 0,
	});
	const pager = usePager(layout.pages, arrowKeys);
	const { page } = pager;

	useLayoutEffect(() => {
		const box = viewport.current;
		const inner = content.current;
		if (!box || !inner) return;

		// The box size the layout was last measured for.
		let measured = { width: -1, height: -1 };

		function measure() {
			if (!box || !inner) return;
			measured = { width: box.clientWidth, height: box.clientHeight };
			const fits = (fontSize: number) => {
				Object.assign(inner.style, {
					fontSize: `${fontSize}px`,
					height: "",
					columnWidth: "",
				});
				return inner.scrollHeight <= box.clientHeight;
			};
			// Each try is a layout, so after the largest size try the smallest: when even that
			// is too big, the sizes between need no try.
			const largest = FONT_SIZES[0];
			const smallest = FONT_SIZES[FONT_SIZES.length - 1];
			const fontSize = fits(largest)
				? largest
				: fits(smallest)
					? (FONT_SIZES.slice(1, -1).find(fits) ?? smallest)
					: undefined;
			if (fontSize) {
				inner.style.fontSize = `${fontSize}px`;
				setLayout({ fontSize, pages: 1, width: 0, height: 0 });
				return;
			}
			const width = box.clientWidth;
			const height = box.clientHeight - PAGER_HEIGHT;
			Object.assign(inner.style, {
				fontSize: `${smallest}px`,
				height: `${height}px`,
				columnWidth: `${width}px`,
				columnGap: `${COLUMN_GAP}px`,
			});
			const pages = Math.max(
				1,
				Math.round((inner.scrollWidth + COLUMN_GAP) / (width + COLUMN_GAP)),
			);
			setLayout({ fontSize: smallest, pages, width, height });
		}

		measure();
		// Its first callback, and any after a change that kept the size, would redo the same work.
		const observer = new ResizeObserver(() => {
			if (
				box.clientWidth !== measured.width ||
				box.clientHeight !== measured.height
			)
				measure();
		});
		observer.observe(box);
		// Images and fonts load late and change the content height.
		for (const img of inner.querySelectorAll("img")) {
			img.addEventListener("load", measure, { once: true });
		}
		return () => observer.disconnect();
	}, []);

	const paged = layout.pages > 1;

	const style: CSSProperties = paged
		? {
				fontSize: layout.fontSize,
				height: layout.height,
				columnWidth: layout.width,
				columnGap: COLUMN_GAP,
				columnFill: "auto",
				transform: `translateX(-${page * (layout.width + COLUMN_GAP)}px)`,
			}
		: { fontSize: layout.fontSize };

	return (
		<div
			ref={viewport}
			// The pager sits in the bottom padding, so a content-sized box keeps its height.
			style={paged ? { paddingBottom: PAGER_HEIGHT } : undefined}
			className={cn("relative min-h-0 overflow-hidden", className)}
		>
			<div
				ref={content}
				style={style}
				className="transition-transform duration-200 motion-reduce:transition-none"
			>
				{children}
			</div>
			{paged && (
				<PagerControls
					pager={pager}
					size="xs"
					className="absolute right-0 bottom-0 h-7 gap-1 bg-card text-xs"
				>
					Page {page + 1} of {layout.pages}
				</PagerControls>
			)}
		</div>
	);
}
