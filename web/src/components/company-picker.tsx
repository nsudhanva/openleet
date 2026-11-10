import { ChevronDownIcon } from "lucide-react";
import { type ComponentProps, lazy, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { useCompanies } from "@/hooks/use-companies";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { companyName } from "@/lib/companies";
import { cn } from "@/lib/utils";

const loadCombobox = () => import("@/components/company-combobox");
const CompanyCombobox = lazy(async () => ({
	default: (await loadCombobox()).CompanyCombobox,
}));

export interface CompanyPickerProps {
	value: string;
	onChange: (company: string) => void;
	disabled?: boolean;
	className?: string;
}

/** The picker's button; the combobox draws its own chevron, the placeholder needs one. */
export function CompanyButton({
	className,
	withChevron = true,
	children,
	...props
}: ComponentProps<typeof Button> & { withChevron?: boolean }) {
	return (
		<Button
			variant="outline"
			size="sm"
			aria-label="Company"
			className={cn("justify-between bg-card font-normal", className)}
			{...props}
		>
			{children}
			{withChevron && (
				<ChevronDownIcon className="pointer-events-none size-4 text-muted-foreground" />
			)}
		</Button>
	);
}

/**
 * Chooses the company whose lists you study. The searchable list loads on first use, so
 * until then this is a plain button with the company's name.
 */
export function CompanyPicker(props: CompanyPickerProps) {
	const name = companyName(useCompanies(), props.value);
	const { used, use, prefetchProps } = useLoadOnUse(loadCombobox);
	const placeholder = (
		<CompanyButton
			className={props.className}
			disabled={props.disabled}
			{...prefetchProps}
			onClick={use}
		>
			{name}
		</CompanyButton>
	);
	if (!used) return placeholder;
	return (
		<Suspense fallback={placeholder}>
			<CompanyCombobox {...props} defaultOpen />
		</Suspense>
	);
}
