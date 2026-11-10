const relative = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
	["day", 86_400_000],
	["hour", 3_600_000],
	["minute", 60_000],
];

/** "2 days ago", "in 3 hours", "now". */
export function timeFrom(at: number, now = Date.now()): string {
	const diff = at - now;
	for (const [unit, ms] of UNITS) {
		if (Math.abs(diff) >= ms)
			return relative.format(Math.round(diff / ms), unit);
	}
	return "now";
}

/** "17 ms": a CPU time as the judge reports it. */
export function cpuTime(ms: number): string {
	return `${ms} ms`;
}

export function percent(value: number, digits = 0): string {
	return `${(value * 100).toFixed(digits)}%`;
}

const SITE = "OpenLeet";

/** "Problems | OpenLeet"; the site name alone without parts. */
export function pageTitle(...parts: string[]): string {
	return [...parts, SITE].join(" | ");
}
