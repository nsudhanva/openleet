import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { FIT_SCREEN } from "./screen";

describe("FIT_SCREEN", () => {
	it("is the media query of the fit: variant in styles.css", () => {
		const css = readFileSync(new URL("../styles.css", import.meta.url), "utf8");
		const variant = css.match(/@custom-variant fit \(@media (.+)\);/);
		expect(variant?.[1]).toBe(FIT_SCREEN);
	});
});
