import {
	CompanyButton,
	type CompanyPickerProps,
} from "@/components/company-picker";
import {
	Combobox,
	ComboboxContent,
	ComboboxEmpty,
	ComboboxInput,
	ComboboxItem,
	ComboboxList,
	ComboboxTrigger,
	ComboboxValue,
} from "@/components/ui/combobox";
import { useCompanies } from "@/hooks/use-companies";
import { ANY_COMPANY, companyName } from "@/lib/companies";

interface Option {
	value: string;
	label: string;
	/** Problems the company asked, all time; null for "Any company". */
	count: number | null;
}

/** The picker itself: a searchable list of every company, "Any company" first. */
export function CompanyCombobox({
	value,
	onChange,
	disabled = false,
	className,
	defaultOpen = false,
}: CompanyPickerProps & { defaultOpen?: boolean }) {
	const companies = useCompanies();
	const options: Option[] = [
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
	];
	const selected = options.find((o) => o.value === value) ?? {
		value,
		label: companyName(companies, value),
		count: null,
	};

	return (
		<Combobox
			items={options}
			value={selected}
			onValueChange={(next: Option | null) => next && onChange(next.value)}
			itemToStringLabel={(o: Option) => o.label}
			isItemEqualToValue={(a: Option, b: Option) => a.value === b.value}
			disabled={disabled}
			// Typing highlights the first match, so Enter picks it.
			autoHighlight
			defaultOpen={defaultOpen}
		>
			<ComboboxTrigger
				render={<CompanyButton className={className} withChevron={false} />}
			>
				<ComboboxValue />
			</ComboboxTrigger>
			<ComboboxContent className="min-w-56">
				<ComboboxInput
					showTrigger={false}
					placeholder="Search companies"
					aria-label="Search companies"
				/>
				<ComboboxEmpty>No company matches.</ComboboxEmpty>
				<ComboboxList>
					{(option: Option) => (
						<ComboboxItem key={option.value} value={option}>
							{option.label}
							{option.count !== null && (
								<span className="ml-auto text-xs text-muted-foreground tabular-nums">
									{option.count}
									<span className="sr-only"> problems</span>
								</span>
							)}
						</ComboboxItem>
					)}
				</ComboboxList>
			</ComboboxContent>
		</Combobox>
	);
}
