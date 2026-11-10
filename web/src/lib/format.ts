/** Made on first use: building an Intl formatter costs milliseconds the page load can skip. */
let relative: Intl.RelativeTimeFormat | undefined;
const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
	["day", 86_400_000],
	["hour", 3_600_000],
	["minute", 60_000],
];

/** "2 days ago", "in 3 hours", "now". */
export function timeFrom(at: number, now = Date.now()): string {
	const diff = at - now;
	for (const [unit, ms] of UNITS) {
		if (Math.abs(diff) >= ms) {
			relative ??= new Intl.RelativeTimeFormat("en", { numeric: "auto" });
			return relative.format(Math.round(diff / ms), unit);
		}
	}
	return "now";
}

/** "17 ms": a CPU time as the judge reports it. */
export function cpuTime(ms: number): string {
	return `${ms} ms`;
}

/**
 * A share (0..1) as "42%", or "42.5%" with `digits` 1. A share above 0 that would round to 0
 * shows as "<1%" ("<0.1%"), and one below 1 that would round to 100 as ">99%" (">99.9%"), so a
 * little progress never reads as none and almost never as all. Text only: a CSS width needs
 * the raw number.
 */
export function percent(value: number, digits = 0): string {
	const text = (value * 100).toFixed(digits);
	const step = (10 ** -digits).toFixed(digits);
	if (value > 0 && Number(text) === 0) return `<${step}%`;
	if (value < 1 && Number(text) === 100)
		return `>${(100 - Number(step)).toFixed(digits)}%`;
	return `${text}%`;
}

const SITE = "OpenLeet";

/** "Problems | OpenLeet"; the site name alone without parts. */
export function pageTitle(...parts: string[]): string {
	return [...parts, SITE].join(" | ");
}
