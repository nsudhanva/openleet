import { useMemo } from "react";
import { type FilterOption, FilterPicker } from "@/components/filter-picker";
import { useCompanies } from "@/hooks/use-companies";
import { ANY_COMPANY, companyName } from "@/lib/companies";
import { cn } from "@/lib/utils";

/**
 * Chooses the company whose lists you study: "Any company", then every company by count.
 * On a phone it fills its cell of the filter grid.
 */
export function CompanyPicker({
	value,
	onChange,
	disabled,
	className,
}: {
	value: string;
	onChange: (company: string) => void;
	disabled?: boolean;
	className?: string;
}) {
	const companies = useCompanies();
	const options = useMemo<FilterOption[]>(
		() => [
			{
				value: ANY_COMPANY,
				label: companyName(companies, ANY_COMPANY),
				count: null,
			},
			...companies.map((c) => ({
				value: c.slug,
				label: c.name,
				count: c.problems,
			})),
		],
		[companies],
	);
	return (
		<FilterPicker
			label="Company"
			noun="companies"
			value={value}
			valueLabel={companyName(companies, value)}
			options={options}
			onChange={onChange}
			disabled={disabled}
			className={cn("w-36 max-sm:w-full", className)}
		/>
	);
}
