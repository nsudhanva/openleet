import { useMemo } from "react";
import { Panel } from "@/components/progress/panel";
import { count } from "@/lib/format";
import {
	ACTIVITY_LEVELS,
	activitySummary,
	calendarWeeks,
	dayLabel,
} from "@/lib/insights";
import type { Activity } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * The shades by level, one hue (the primary) over the card: every shade of a day with
 * practice keeps 3:1 against the card in both themes; a day without is the muted fill.
 */
const LEVEL_FILL = [
	"bg-muted",
	"bg-[color-mix(in_oklab,var(--primary)_62%,var(--card))]",
	"bg-[color-mix(in_oklab,var(--primary)_76%,var(--card))]",
	"bg-[color-mix(in_oklab,var(--primary)_88%,var(--card))]",
	"bg-primary",
];

/**
 * The last 26 weeks as a grid of days, a column per week (Monday on top), shaded by the
 * day's flashcard reviews and submissions together. Each day names its counts; the summary
 * and the day list say the same in words, for keyboards and screen readers.
 */
export function ActivityPanel({
	activity,
	streakDays,
}: {
	activity: Activity;
	/** Consecutive days with practice, the calendar's days, ending today or yesterday. */
	streakDays: number;
}) {
	const { weeks, months } = useMemo(() => calendarWeeks(activity), [activity]);
	const columns = {
		gridTemplateColumns: `repeat(${weeks.length}, minmax(0, 1fr))`,
	};
	return (
		<Panel
			id="activity"
			title="Activity"
			note="Graded cards and submissions per day on any list, in the server's time zone."
			action={
				<p className="shrink-0 text-right text-sm">
					<span className="text-muted-foreground">Streak</span>{" "}
					<span className="font-semibold tabular-nums">
						{count(streakDays, "day")}
					</span>
				</p>
			}
			className="md:max-lg:col-span-2"
		>
			{/* Cells grow with the panel, up to a size that still reads as one calendar. */}
			<div className="w-full max-w-xl space-y-1">
				<div
					aria-hidden
					className="grid gap-[3px] text-xs text-muted-foreground"
					style={columns}
				>
					{months.map((month, i) => (
						// biome-ignore lint/suspicious/noArrayIndexKey: one label per week, in order
						<span key={i} className="overflow-visible whitespace-nowrap">
							{month}
						</span>
					))}
				</div>
				<div className="grid gap-[3px]" style={columns}>
					{weeks.map((week) => (
						<div key={week[0].day} className="grid grid-rows-7 gap-[3px]">
							{week.map((d) => (
								<span
									key={d.day}
									role="img"
									aria-label={d.label}
									title={d.label}
									className={cn(
										"aspect-square rounded-[2px]",
										LEVEL_FILL[d.level],
									)}
								/>
							))}
						</div>
					))}
				</div>
			</div>
			<div className="mt-2 flex w-full max-w-xl items-center justify-end gap-1 text-xs text-muted-foreground">
				<span>Less</span>
				{LEVEL_FILL.map((fill, level) => (
					<span
						key={fill}
						aria-hidden
						className={cn("size-2.5 rounded-[2px]", fill)}
						title={level ? `${ACTIVITY_LEVELS[level - 1]} or more` : "None"}
					/>
				))}
				<span>More</span>
				<span className="sr-only">
					Shades from none to {ACTIVITY_LEVELS.join(", ")} or more reviews and
					submissions a day.
				</span>
			</div>
			<p className="mt-2 text-sm">{activitySummary(activity)}</p>
			{activity.days.length > 0 && (
				<details className="mt-1 text-sm">
					<summary className="cursor-pointer text-primary underline-offset-4 hover:underline">
						List the days
					</summary>
					<table className="mt-2 w-full text-left tabular-nums">
						<thead className="text-xs text-muted-foreground">
							<tr>
								<th className="py-1 font-medium">Day</th>
								<th className="py-1 text-right font-medium">Reviews</th>
								<th className="py-1 text-right font-medium">Submissions</th>
							</tr>
						</thead>
						<tbody>
							{[...activity.days].reverse().map((d) => (
								<tr key={d.day} className="border-t">
									<td className="py-1">{dayLabel(d.day)}</td>
									<td className="py-1 text-right">{d.reviews}</td>
									<td className="py-1 text-right">{d.submissions}</td>
								</tr>
							))}
						</tbody>
					</table>
					<p className="sr-only">
						{count(activity.days.length, "day")} with practice.
					</p>
				</details>
			)}
		</Panel>
	);
}
