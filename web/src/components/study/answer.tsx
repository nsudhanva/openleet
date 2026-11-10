import { CheckIcon, MinusIcon, PlusIcon } from "lucide-react";
import type { ReactNode } from "react";
import { InlineCode } from "@/components/inline-code";
import type { TopicResult } from "@/lib/scorer";
import type { Approach } from "@/lib/types";
import { cn } from "@/lib/utils";

const CHIP_TONE = {
	hit: "border-success/40 bg-success-wash text-success",
	missed: "border-dashed border-warning/60 bg-warning-wash text-warning",
	extra: "border-destructive/30 text-destructive line-through decoration-1",
};
const CHIP_ICON = {
	hit: <CheckIcon className="size-[1em]" />,
	missed: <PlusIcon className="size-[1em]" />,
	extra: <MinusIcon className="size-[1em]" />,
};

function TopicVerdict({ result }: { result: TopicResult }) {
	const named = result.hits.length;
	const chips = [
		...result.hits.map((t) => ["hit", t] as const),
		...result.missed.map((t) => ["missed", t] as const),
		...result.extra.map((t) => ["extra", t] as const),
	];
	return (
		<section aria-labelledby="topics-heading">
			<h3 id="topics-heading" className="mb-1.5 font-semibold">
				You named {named} of {named + result.missed.length} topics
				{result.extra.length > 0 && (
					<span className="font-normal text-muted-foreground">
						{" "}
						and {result.extra.length} that do not apply
					</span>
				)}
			</h3>
			<ul>
				{chips.map(([tone, topic]) => (
					<li
						key={topic}
						className={cn(
							"mr-1.5 mb-1.5 inline-flex items-center gap-1 rounded-full border px-2 py-px fit-text-90",
							CHIP_TONE[tone],
						)}
					>
						{CHIP_ICON[tone]}
						{topic}
					</li>
				))}
			</ul>
		</section>
	);
}

function Labeled({ label, children }: { label: string; children: ReactNode }) {
	return (
		<p>
			<span className="font-semibold">{label}</span> {children}
		</p>
	);
}

export function Answer({
	result,
	approach,
}: {
	result: TopicResult;
	approach: Approach | null;
}) {
	return (
		<div className="space-y-3">
			<TopicVerdict result={result} />
			<section aria-labelledby="approach-heading" className="card-ruled">
				<h3 id="approach-heading" className="font-semibold">
					Approach
				</h3>
				{approach ? (
					<>
						<p className="font-medium">
							<InlineCode text={approach.insight} />
						</p>
						<ol className="list-decimal pl-[1.4em] marker:text-muted-foreground">
							{approach.steps.map((step) => (
								<li key={step}>
									<InlineCode text={step} />
								</li>
							))}
						</ol>
						<Labeled label="Complexity">
							time <span className="font-mono">{approach.time}</span>, space{" "}
							<span className="font-mono">{approach.space}</span>.
						</Labeled>
						{approach.hints.map((hint, i) => (
							<Labeled key={hint} label={`Hint ${i + 1}`}>
								<span className="text-muted-foreground">
									<InlineCode text={hint} />
								</span>
							</Labeled>
						))}
					</>
				) : (
					<p className="text-muted-foreground">
						No approach written for this problem yet.
					</p>
				)}
			</section>
		</div>
	);
}
