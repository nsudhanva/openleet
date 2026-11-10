import {
	type KeyboardEvent,
	type PointerEvent,
	useId,
	useRef,
	useState,
} from "react";
import { VERDICT } from "@/components/code/verdict";
import { useWidth } from "@/hooks/use-width";
import { cpuTime, percent } from "@/lib/format";
import { TONE_FILL, type Tone } from "@/lib/tones";
import type { SubmissionSummary } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Status, not identity: each tone also has its own marker shape, so color never stands alone. */
const TONE_KEY: Record<Tone, { label: string; shape: Shape }> = {
	success: { label: "Accepted", shape: "circle" },
	warning: { label: "Limit exceeded", shape: "triangle" },
	destructive: { label: "Wrong answer or error", shape: "square" },
	muted: { label: "Other", shape: "diamond" },
};
const TONES = Object.keys(TONE_KEY) as Tone[];
type Shape = "circle" | "triangle" | "square" | "diamond";

// Geometry, px: two panels share the x scale (submission order, oldest first).
const LEFT = 44;
const RIGHT = 8;
const INSET = 8;
const PANEL = 44;
const PASSED_TOP = 16;
const CPU_TOP = PASSED_TOP + PANEL + 24;
const HEIGHT = CPU_TOP + PANEL + 18;
/** A limit this far above the slowest run would flatten every point, so it stays a note. */
const LIMIT_ON_SCALE = 1.5;

/** Date formats, made on first use: each Intl formatter costs milliseconds to build. */
const FORMATS = {
	day: { month: "short", day: "numeric" },
	time: { hour: "numeric", minute: "2-digit" },
	full: { dateStyle: "medium", timeStyle: "short" },
} satisfies Record<string, Intl.DateTimeFormatOptions>;
const formatters = new Map<keyof typeof FORMATS, Intl.DateTimeFormat>();

function formatDate(format: keyof typeof FORMATS, at: number): string {
	let formatter = formatters.get(format);
	if (!formatter) {
		formatter = new Intl.DateTimeFormat("en", FORMATS[format]);
		formatters.set(format, formatter);
	}
	return formatter.format(at);
}

/** "850 ms", "2.5 s": a CPU time short enough for an axis label. */
function compactTime(value: number): string {
	return value >= 1000
		? `${(value / 1000).toFixed(value >= 10_000 ? 0 : 1)} s`
		: `${Math.round(value)} ms`;
}

const NICE_STEPS = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];

/** The smallest round number (1, 1.2, 1.5, 2, … times a power of ten) at least `value`. */
function niceCeil(value: number): number {
	if (value <= 0) return 1;
	const power = 10 ** Math.floor(Math.log10(value));
	return (NICE_STEPS.find((step) => step * power >= value) ?? 10) * power;
}

const share = (s: SubmissionSummary) => (s.total ? s.passed / s.total : 0);

function Marker({
	shape,
	x,
	y,
	className,
}: {
	shape: Shape;
	x: number;
	y: number;
	className?: string;
}) {
	// About 9 px across, with a 2 px ring in the card color so crossing marks stay legible.
	const ring = cn("stroke-card stroke-2 [paint-order:stroke]", className);
	switch (shape) {
		case "circle":
			return <circle cx={x} cy={y} r={4.5} className={ring} />;
		case "triangle":
			return (
				<path
					d={`M${x},${y - 5.5}L${x + 5},${y + 3.5}L${x - 5},${y + 3.5}Z`}
					className={ring}
				/>
			);
		case "square":
			return <rect x={x - 4} y={y - 4} width={8} height={8} className={ring} />;
		case "diamond":
			return (
				<path
					d={`M${x},${y - 5.5}L${x + 5.5},${y}L${x},${y + 5.5}L${x - 5.5},${y}Z`}
					className={ring}
				/>
			);
	}
}

/** One submission in words, for screen readers. */
function describe(s: SubmissionSummary): string {
	return `${VERDICT[s.verdict].label}, ${s.passed} of ${s.total} tests, ${cpuTime(s.cpuMs)} CPU, ${formatDate("full", s.at)}`;
}

function summaryOf(
	points: SubmissionSummary[],
	timeLimitMs: number | null,
): string {
	const first = points[0];
	const last = points[points.length - 1];
	const accepted = points.filter((s) => s.verdict === "accepted").length;
	const limit = timeLimitMs
		? `, against a time limit of ${cpuTime(timeLimitMs)}`
		: "";
	return (
		`${points.length} submissions, oldest to newest, ${accepted} accepted. ` +
		`Tests passed went from ${percent(share(first))} to ${percent(share(last))}; ` +
		`CPU time from ${cpuTime(first.cpuMs)} to ${cpuTime(last.cpuMs)}${limit}. ` +
		"Arrow keys pick a submission and Enter loads its code; the list below has every submission."
	);
}

/**
 * Your submissions over time in two aligned panels: the share of tests passed, and CPU time
 * against the time limit. Markers show the verdict by color and shape. Hover, or focus and
 * use the arrow keys, to read a submission; click or Enter loads its code. Needs two or more.
 */
export function SubmissionChart(props: ChartProps) {
	return props.submissions.length < 2 ? null : <Chart {...props} />;
}

interface ChartProps {
	/** Newest first, as the API lists them. */
	submissions: SubmissionSummary[];
	timeLimitMs: number | null;
	onOpen: (id: number) => void;
}

function Chart({ submissions, timeLimitMs, onOpen }: ChartProps) {
	const box = useRef<HTMLDivElement>(null);
	const width = useWidth(box);
	const [active, setActive] = useState<number | null>(null);
	const summaryId = useId();

	const points = [...submissions].reverse();
	const n = points.length;

	const plotWidth = Math.max(0, width - LEFT - RIGHT - 2 * INSET);
	const x = (i: number) => LEFT + INSET + (i * plotWidth) / (n - 1);
	const slowest = Math.max(...points.map((s) => s.cpuMs));
	const limitShown =
		timeLimitMs !== null && timeLimitMs <= slowest * LIMIT_ON_SCALE;
	const cpuMax = niceCeil(
		Math.max(slowest, limitShown ? (timeLimitMs ?? 0) : 0) * 1.05,
	);
	const yPassed = (s: SubmissionSummary) => PASSED_TOP + PANEL * (1 - share(s));
	const yCpu = (value: number) =>
		CPU_TOP + PANEL * (1 - Math.min(value, cpuMax) / cpuMax);
	const series = [
		{ key: "passed", y: yPassed },
		{ key: "cpu", y: (s: SubmissionSummary) => yCpu(s.cpuMs) },
	];

	const sameDay =
		formatDate("day", points[0].at) === formatDate("day", points[n - 1].at);
	const dateLabel = (at: number) => formatDate(sameDay ? "time" : "day", at);
	const tones = TONES.filter((tone) =>
		points.some((s) => VERDICT[s.verdict].tone === tone),
	);

	function pick(event: PointerEvent<HTMLDivElement>) {
		const left = event.currentTarget.getBoundingClientRect().left;
		const at = event.clientX - left - LEFT - INSET;
		const i = Math.round((at / Math.max(1, plotWidth)) * (n - 1));
		setActive(Math.min(n - 1, Math.max(0, i)));
	}

	function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
		const current = active ?? n - 1;
		const next: Record<string, number> = {
			ArrowLeft: Math.max(0, current - 1),
			ArrowRight: Math.min(n - 1, current + 1),
			Home: 0,
			End: n - 1,
		};
		if (event.key in next) setActive(next[event.key]);
		else if (event.key === "Enter" || event.key === " ")
			onOpen(points[current].id);
		else if (event.key === "Escape") setActive(null);
		else return;
		// Handled here, so the page's arrow-key shortcuts (statement pages) stay out of it.
		event.preventDefault();
	}

	const shown = active === null ? null : points[active];
	const panelTitle = (y: number, text: string) => (
		<text
			x={LEFT}
			y={y - 6}
			className="fill-muted-foreground text-[11px] font-medium"
		>
			{text}
		</text>
	);
	const tick = (y: number, text: string) => (
		<g key={text}>
			<line
				x1={LEFT}
				x2={width - RIGHT}
				y1={y}
				y2={y}
				className="stroke-border"
			/>
			<text
				x={LEFT - 6}
				y={y}
				dy="0.32em"
				textAnchor="end"
				className="fill-muted-foreground text-[10px] tabular-nums"
			>
				{text}
			</text>
		</g>
	);

	return (
		<figure className="space-y-1">
			<div
				ref={box}
				// A slider over the submissions: arrow keys pick one, Enter loads its code.
				role="slider"
				aria-label="Submission"
				aria-describedby={summaryId}
				aria-valuemin={1}
				aria-valuemax={n}
				aria-valuenow={(active ?? n - 1) + 1}
				aria-valuetext={describe(points[active ?? n - 1])}
				tabIndex={0}
				className="relative cursor-pointer touch-none rounded-sm outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
				onPointerMove={pick}
				onPointerDown={pick}
				onPointerLeave={() => setActive(null)}
				onClick={() => shown && onOpen(shown.id)}
				onFocus={() => setActive((a) => a ?? n - 1)}
				onBlur={() => setActive(null)}
				onKeyDown={onKeyDown}
			>
				{width > 0 && (
					<svg width={width} height={HEIGHT} aria-hidden className="block">
						{panelTitle(PASSED_TOP, "Tests passed")}
						{tick(PASSED_TOP, "100%")}
						{tick(PASSED_TOP + PANEL, "0%")}
						{panelTitle(
							CPU_TOP,
							timeLimitMs && !limitShown
								? `CPU time (limit ${compactTime(timeLimitMs)}, above this range)`
								: "CPU time",
						)}
						{tick(CPU_TOP, compactTime(cpuMax))}
						{tick(CPU_TOP + PANEL, "0")}
						{limitShown && timeLimitMs && (
							<g>
								<line
									x1={LEFT}
									x2={width - RIGHT}
									y1={yCpu(timeLimitMs)}
									y2={yCpu(timeLimitMs)}
									strokeDasharray="4 3"
									className="stroke-muted-foreground"
								/>
								<text
									x={width - RIGHT}
									y={yCpu(timeLimitMs) - 3}
									textAnchor="end"
									className="fill-muted-foreground text-[10px]"
								>
									Limit {compactTime(timeLimitMs)}
								</text>
							</g>
						)}
						{shown && active !== null && (
							<line
								x1={x(active)}
								x2={x(active)}
								y1={PASSED_TOP}
								y2={CPU_TOP + PANEL}
								className="stroke-muted-foreground/60"
							/>
						)}
						{series.map(({ key, y }) => (
							<g key={key}>
								<polyline
									points={points.map((s, i) => `${x(i)},${y(s)}`).join(" ")}
									fill="none"
									strokeWidth={2}
									strokeLinejoin="round"
									strokeLinecap="round"
									className="stroke-muted-foreground/45"
								/>
								{points.map((s, i) => {
									const tone = VERDICT[s.verdict].tone;
									return (
										<Marker
											key={s.id}
											shape={TONE_KEY[tone].shape}
											x={x(i)}
											y={y(s)}
											className={TONE_FILL[tone]}
										/>
									);
								})}
							</g>
						))}
						<text
							x={x(0)}
							y={HEIGHT - 2}
							className="fill-muted-foreground text-[10px]"
						>
							{dateLabel(points[0].at)}
						</text>
						<text
							x={x(n - 1)}
							y={HEIGHT - 2}
							textAnchor="end"
							className="fill-muted-foreground text-[10px]"
						>
							{dateLabel(points[n - 1].at)}
						</text>
					</svg>
				)}
				{shown && active !== null && (
					<div
						className="pointer-events-none absolute top-0 z-10 w-max space-y-0.5 rounded-md border bg-popover px-2.5 py-1.5 text-xs text-popover-foreground shadow-md"
						style={
							x(active) > width / 2
								? { right: width - x(active) + 10 }
								: { left: x(active) + 10 }
						}
						aria-live="polite"
					>
						<p className="flex items-center gap-1.5 font-semibold">
							<ToneKey tone={VERDICT[shown.verdict].tone} />
							{VERDICT[shown.verdict].label}
						</p>
						<p>
							<strong className="tabular-nums">
								{shown.passed} / {shown.total}
							</strong>{" "}
							<span className="text-muted-foreground">tests passed</span>
						</p>
						<p>
							<strong className="tabular-nums">{cpuTime(shown.cpuMs)}</strong>{" "}
							<span className="text-muted-foreground">CPU</span>
						</p>
						<p className="text-muted-foreground">
							{formatDate("full", shown.at)}
						</p>
						<p className="text-muted-foreground">
							Click or Enter loads this code
						</p>
					</div>
				)}
			</div>
			<figcaption className="flex flex-wrap gap-x-3 gap-y-0.5 text-xs text-muted-foreground">
				<span id={summaryId} className="sr-only">
					{summaryOf(points, timeLimitMs)}
				</span>
				{tones.map((tone) => (
					<span key={tone} className="flex items-center gap-1">
						<ToneKey tone={tone} />
						{TONE_KEY[tone].label}
					</span>
				))}
			</figcaption>
		</figure>
	);
}

/** The tone's marker, for the legend and the tooltip. */
function ToneKey({ tone }: { tone: Tone }) {
	return (
		<svg width={12} height={12} aria-hidden className="shrink-0">
			<Marker
				shape={TONE_KEY[tone].shape}
				x={6}
				y={6.5}
				className={cn(TONE_FILL[tone], "stroke-0")}
			/>
		</svg>
	);
}
