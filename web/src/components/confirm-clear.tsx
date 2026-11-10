import {
	cloneElement,
	lazy,
	type ReactElement,
	type ReactNode,
	Suspense,
} from "react";
import { useLoadOnUse } from "@/hooks/use-load-on-use";

const loadDialog = () => import("@/components/confirm-clear-dialog");
const ConfirmClearDialog = lazy(async () => ({
	default: (await loadDialog()).ConfirmClearDialog,
}));

export interface ConfirmClearProps {
	/** The trigger element, for example `<Button variant="destructive" />`. */
	trigger: ReactElement<{ onClick?: () => void; children?: ReactNode }>;
	/** What the trigger shows. */
	children: ReactNode;
	title: string;
	description: string;
	onClear: () => Promise<void>;
}

/**
 * Clears progress only after you confirm twice. The dialog loads on first use, so until
 * then the trigger is all there is.
 */
export function ConfirmClear(props: ConfirmClearProps) {
	const { used, use, prefetchProps } = useLoadOnUse(loadDialog);
	const placeholder = cloneElement(props.trigger, {
		...prefetchProps,
		onClick: use,
		children: props.children,
	});
	if (!used) return placeholder;
	return (
		<Suspense fallback={placeholder}>
			<ConfirmClearDialog {...props} defaultOpen />
		</Suspense>
	);
}
