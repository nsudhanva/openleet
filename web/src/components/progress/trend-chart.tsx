import { count, percent } from "@/lib/format";
import { dayLabel, daysBetween, shortDay, trendScale } from "@/lib/insights";
import type { Trend } from "@/lib/types";

/** The trend waits for this many days with practice (the server sends no points before). */
const MIN_DAYS = 7;

/** The plot inside the SVG's coordinates; the left margin holds the value labels. */
const WIDTH = 320;
const HEIGHT = 96;
const LEFT = 34;
const BOTTOM = 16;
const TOP = 6;

/**
 * Readiness at the end of each day as a line over real dates, with a labelled value axis
 * scaled to the values. Days before readiness had any data leave the line's start later.
 */
export function TrendChart({ trend }: { trend: Trend }) {
	const { points, practiceDays } = trend;
	if (practiceDays < MIN_DAYS || points.length < 2) {
		return (
			<p className="text-sm text-muted-foreground">
				{`A trend line shows once you have practiced on ${MIN_DAYS} different days (${practiceDays} so far).`}
			</p>
		);
	}
	const first = points[0];
	const last = points[points.length - 1];
	const span = Math.max(daysBetween(first.day, last.day), 1);
	const { lo, hi, ticks } = trendScale(points.map((p) => p.readiness));
	const plot = WIDTH - LEFT;
	const tall = HEIGHT - TOP - BOTTOM;
	const x = (day: string) => LEFT + (daysBetween(first.day, day) / span) * plot;
	const y = (value: number) => TOP + (1 - (value - lo) / (hi - lo)) * tall;
	const line = points
		.map((p) => `${x(p.day).toFixed(1)},${y(p.readiness).toFixed(1)}`)
		.join(" ");
	return (
		<figure>
			<svg
				viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
				className="h-auto w-full overflow-visible text-muted-foreground"
				role="img"
				aria-label={`Readiness from ${percent(first.readiness)} on ${dayLabel(first.day)} to ${percent(last.readiness)} on ${dayLabel(last.day)}`}
			>
				{ticks.map((t) => (
					<g key={t}>
						<line
							x1={LEFT}
							x2={WIDTH}
							y1={y(t)}
							y2={y(t)}
							stroke="currentColor"
							strokeOpacity={0.25}
							vectorEffect="non-scaling-stroke"
						/>
						<text
							x={LEFT - 6}
							y={y(t)}
							dy="0.32em"
							textAnchor="end"
							fontSize={10}
							fill="currentColor"
						>
							{percent(t)}
						</text>
					</g>
				))}
				<polyline
					points={line}
					fill="none"
					className="text-primary"
					stroke="currentColor"
					strokeWidth={2}
					strokeLinejoin="round"
					vectorEffect="non-scaling-stroke"
				/>
				{[first, last].map((p, i) => (
					<text
						key={p.day}
						x={x(p.day)}
						y={HEIGHT - 2}
						textAnchor={i ? "end" : "start"}
						fontSize={10}
						fill="currentColor"
					>
						{shortDay(p.day)}
					</text>
				))}
			</svg>
			<figcaption className="sr-only">
				Readiness at the end of each day, over {count(points.length, "day")}.
			</figcaption>
		</figure>
	);
}
