import { cloneElement, type ReactElement, type ReactNode } from "react";
import { useLoadOnUse } from "@/hooks/use-load-on-use";

const loadDialog = () => import("@/components/confirm-clear-dialog");

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
	const { loaded, use, prefetchProps } = useLoadOnUse(loadDialog);
	const placeholder = cloneElement(props.trigger, {
		...prefetchProps,
		onClick: use,
		children: props.children,
	});
	if (!loaded) return placeholder;
	return <loaded.ConfirmClearDialog {...props} defaultOpen />;
}
