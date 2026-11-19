import { EllipsisIcon, PinIcon } from "lucide-react";
import { type ComponentProps, type KeyboardEvent, useState } from "react";
import { PlanCard } from "@/components/plan/plan-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useLoadOnUse } from "@/hooks/use-load-on-use";
import { useMedia } from "@/hooks/use-media";
import { api, messageOf } from "@/lib/api";
import { SM_SCREEN } from "@/lib/screen";
import type { SavedPlan } from "@/lib/types";

const loadMenu = () => import("@/components/plan/plan-menu");

/** Plans shown before "Show all" (pinned ones come first): two rows of the grid. */
const SHOWN = { wide: 6, phone: 3 };
/** The longest name the server keeps. */
const MAX_NAME = 60;

/** The menu's button, the same before and after the menu loads. */
export function PlanMenuButton({
	name,
	...props
}: ComponentProps<typeof Button> & { name: string }) {
	return (
		<Button
			variant="ghost"
			size="icon-sm"
			aria-label={`More for ${name}`}
			className="text-muted-foreground"
			{...props}
		>
			<EllipsisIcon />
		</Button>
	);
}

/**
 * The plans the learner used, pinned first: each with its progress, Continue (its next
 * problem) and a menu to pin, rename or remove it. Nothing shows until a plan is used.
 * `onChange` reloads them after an edit.
 */
export function SavedPlans({
	plans,
	onChange,
}: {
	plans: SavedPlan[];
	onChange: () => Promise<void>;
}) {
	const [all, setAll] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const limit = useMedia(SM_SCREEN) ? SHOWN.wide : SHOWN.phone;
	if (!plans.length) return null;
	const shown = all ? plans : plans.slice(0, limit);

	const run = async (change: Promise<unknown>) => {
		setError(null);
		try {
			await change;
			await onChange();
		} catch (failure) {
			setError(messageOf(failure));
		}
	};

	return (
		<section aria-labelledby="plans-heading" className="mb-3">
			<div className="mb-1.5 flex items-baseline gap-3">
				<h2 id="plans-heading" className="text-sm font-semibold">
					Your plans
				</h2>
				<p className="text-xs text-muted-foreground max-sm:hidden">
					Remembered as you practice; pin the ones to keep.
				</p>
				{plans.length > limit && (
					<Button
						variant="link"
						size="xs"
						className="ml-auto px-0"
						onClick={() => setAll((a) => !a)}
					>
						{all ? "Show fewer" : `Show all ${plans.length}`}
					</Button>
				)}
			</div>
			<ul className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
				{shown.map((plan) => (
					<PlanRow key={plan.id} plan={plan} run={run} />
				))}
			</ul>
			{error && (
				<p role="alert" className="mt-1.5 text-xs text-destructive">
					{error}
				</p>
			)}
		</section>
	);
}

function PlanRow({
	plan,
	run,
}: {
	plan: SavedPlan;
	run: (change: Promise<unknown>) => Promise<void>;
}) {
	const [renaming, setRenaming] = useState(false);
	const { loaded, use, prefetchProps } = useLoadOnUse(loadMenu);
	const title = plan.name ?? plan.plan.label;

	const rename = (text: string) => {
		setRenaming(false);
		const name = text.trim() || null;
		if (name !== plan.name) void run(api.editPlan(plan.id, { name }));
	};
	const menuButton = (
		<PlanMenuButton name={title} {...prefetchProps} onClick={use} />
	);

	return (
		<PlanCard
			title={
				renaming ? (
					<NameInput
						initial={plan.name ?? ""}
						placeholder={plan.plan.label}
						onDone={rename}
						onCancel={() => setRenaming(false)}
					/>
				) : (
					<p className="flex min-w-0 items-center gap-1.5 text-sm font-medium">
						{plan.pinned && (
							<PinIcon
								className="size-3.5 shrink-0 text-primary"
								aria-label="Pinned"
							/>
						)}
						<span className="truncate" title={plan.plan.label}>
							{title}
						</span>
					</p>
				)
			}
			plan={plan.plan}
			progress={plan.progress}
			next={plan.next}
			menu={
				loaded ? (
					<loaded.PlanMenu
						name={title}
						pinned={plan.pinned}
						onPin={() =>
							void run(api.editPlan(plan.id, { pinned: !plan.pinned }))
						}
						onRename={() => setRenaming(true)}
						onRemove={() => void run(api.deletePlan(plan.id))}
						defaultOpen
					/>
				) : (
					menuButton
				)
			}
		/>
	);
}

/** Renaming in place: Enter or leaving the field saves, Escape cancels; empty drops the name. */
function NameInput({
	initial,
	placeholder,
	onDone,
	onCancel,
}: {
	initial: string;
	placeholder: string;
	onDone: (text: string) => void;
	onCancel: () => void;
}) {
	const [draft, setDraft] = useState(initial);
	const onKeyDown = (event: KeyboardEvent) => {
		if (event.key === "Enter") onDone(draft);
		if (event.key === "Escape") onCancel();
	};
	return (
		<Input
			// The learner asked to rename, so the cursor goes there.
			autoFocus
			aria-label="Plan name"
			value={draft}
			maxLength={MAX_NAME}
			placeholder={placeholder}
			onChange={(event) => setDraft(event.target.value)}
			onKeyDown={onKeyDown}
			onBlur={() => onDone(draft)}
			className="h-7 text-sm"
		/>
	);
}
