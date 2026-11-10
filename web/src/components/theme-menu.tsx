import { MonitorIcon, MoonIcon, SunIcon } from "lucide-react";
import { ThemeButton } from "@/components/mode-toggle";
import { type Theme, useTheme } from "@/components/theme-provider";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuRadioGroup,
	DropdownMenuRadioItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const OPTIONS: { value: Theme; label: string; Icon: typeof SunIcon }[] = [
	{ value: "light", label: "Light", Icon: SunIcon },
	{ value: "dark", label: "Dark", Icon: MoonIcon },
	{ value: "system", label: "System", Icon: MonitorIcon },
];

/** The theme menu itself; `ModeToggle` loads it on first use. */
export function ThemeMenu({ defaultOpen }: { defaultOpen: boolean }) {
	const { theme, setTheme } = useTheme();

	return (
		<DropdownMenu defaultOpen={defaultOpen}>
			<DropdownMenuTrigger render={<ThemeButton />} />
			<DropdownMenuContent align="end" className="w-36">
				<DropdownMenuRadioGroup
					value={theme}
					onValueChange={(value) => setTheme(value as Theme)}
				>
					{OPTIONS.map(({ value, label, Icon }) => (
						<DropdownMenuRadioItem key={value} value={value}>
							<Icon />
							{label}
						</DropdownMenuRadioItem>
					))}
				</DropdownMenuRadioGroup>
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
