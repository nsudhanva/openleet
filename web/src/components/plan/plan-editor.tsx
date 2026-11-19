import { CompanyPicker } from "@/components/company-picker";
import { DifficultyFilter } from "@/components/difficulty-filter";
import { PlanButton } from "@/components/plan/plan-chip";
import { OrderPicker, StatusFilter } from "@/components/plan/plan-filters";
import { SelectPicker } from "@/components/select-picker";
import { TopicFilter } from "@/components/topic-filter";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import {
	Popover,
	PopoverContent,
	PopoverTitle,
	PopoverTrigger,
} from "@/components/ui/popover";
import { useMedia } from "@/hooks/use-media";
import type { Plan } from "@/lib/plan";
import { SM_SCREEN } from "@/lib/screen";
import { isAskedPeriod, PERIOD_OPTIONS, type Period } from "@/lib/types";
import { useUserLists } from "@/lib/user-lists";

const TITLE = "Practice plan";
const DESCRIPTION =
	"Which problems Next offers after an accepted submission, and in what order.";

/** The choice of a company list rather than one of your lists. */
const COMPANY_LISTS = "company";

/**
 * The plan's controls: the list (a company's, or one of yours), its filters, which problems
 * still count and the order.
 */
function PlanControls({
	plan,
	onChange,
}: {
	plan: Plan;
	onChange: (plan: Plan) => void;
}) {
	const change = (next: Partial<Plan>) => onChange({ ...plan, ...next });
	const lists = useUserLists();
	const source = plan.list === undefined ? COMPANY_LISTS : String(plan.list);
	return (
		<div className="grid grid-cols-2 gap-2">
			{lists && lists.length > 0 && (
				<SelectPicker<string>
					label="Walk"
					value={source}
					items={[
						{ value: COMPANY_LISTS, label: "A company list" },
						...lists.map((list) => ({
							value: String(list.id),
							label: `Your list: ${list.name}`,
						})),
					]}
					onChange={(next) =>
						change({ list: next === COMPANY_LISTS ? undefined : Number(next) })
					}
					className="col-span-2 w-full"
				/>
			)}
			{plan.list === undefined && (
				<>
					<CompanyPicker
						value={plan.company}
						disabled={!isAskedPeriod(plan.period)}
						onChange={(company) => change({ company })}
						className="w-full"
					/>
					<SelectPicker<Period>
						label="Problem list"
						value={plan.period}
						items={PERIOD_OPTIONS}
						onChange={(period) => change({ period })}
						className="w-full"
					/>
				</>
			)}
			<TopicFilter
				value={plan.topic}
				list={plan}
				onChange={(topic) => change({ topic })}
				className="col-span-2 w-full"
			/>
			<DifficultyFilter
				value={plan.difficulty}
				onChange={(difficulty) => change({ difficulty })}
				className="col-span-2 grid w-full grid-cols-4"
			/>
			<StatusFilter
				value={plan.status}
				onChange={(status) => change({ status })}
				className="w-full"
			/>
			<OrderPicker
				value={plan.order}
				onChange={(order) => change({ order })}
				className="w-full"
			/>
		</div>
	);
}

/**
 * The plan chip's controls, loaded on first use: a popover under the chip, or a sheet from
 * the bottom of a phone's screen.
 */
export function PlanEditor({
	plan,
	label,
	onChange,
	defaultOpen,
}: {
	plan: Plan;
	label: string;
	onChange: (plan: Plan) => void;
	defaultOpen: boolean;
}) {
	const wide = useMedia(SM_SCREEN);
	const controls = <PlanControls plan={plan} onChange={onChange} />;
	if (wide)
		return (
			<Popover defaultOpen={defaultOpen}>
				<PopoverTrigger render={<PlanButton label={label} />} />
				<PopoverContent className="w-[22rem] space-y-3">
					<div className="space-y-1">
						<PopoverTitle>{TITLE}</PopoverTitle>
						<p className="text-xs text-muted-foreground">{DESCRIPTION}</p>
					</div>
					{controls}
				</PopoverContent>
			</Popover>
		);
	return (
		<Dialog defaultOpen={defaultOpen}>
			<DialogTrigger render={<PlanButton label={label} />} />
			<DialogContent className="max-sm:top-auto max-sm:bottom-0 max-sm:max-w-none max-sm:translate-y-0 max-sm:rounded-b-none">
				<DialogHeader>
					<DialogTitle>{TITLE}</DialogTitle>
					<DialogDescription>{DESCRIPTION}</DialogDescription>
				</DialogHeader>
				{controls}
			</DialogContent>
		</Dialog>
	);
}
