import { MoonIcon, SunIcon } from "lucide-react";
import { type ComponentProps, lazy, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { useLoadOnUse } from "@/hooks/use-load-on-use";

const loadMenu = () => import("@/components/theme-menu");
const ThemeMenu = lazy(async () => ({ default: (await loadMenu()).ThemeMenu }));

/** The theme button: a sun in light mode, a moon in dark mode. */
export function ThemeButton(props: ComponentProps<typeof Button>) {
	return (
		<Button variant="ghost" size="icon" aria-label="Theme" {...props}>
			<SunIcon className="dark:hidden" />
			<MoonIcon className="hidden dark:block" />
		</Button>
	);
}

/** Light, dark or system theme; the menu loads on first use and opens at once. */
export function ModeToggle() {
	const { used, use, prefetchProps } = useLoadOnUse(loadMenu);
	if (!used) return <ThemeButton {...prefetchProps} onClick={use} />;
	return (
		<Suspense fallback={<ThemeButton disabled />}>
			<ThemeMenu defaultOpen />
		</Suspense>
	);
}
