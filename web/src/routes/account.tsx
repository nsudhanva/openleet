import {
	createFileRoute,
	Navigate,
	useLoaderData,
} from "@tanstack/react-router";
import {
	type FormEvent,
	type ReactNode,
	useEffect,
	useId,
	useState,
} from "react";
import { Field } from "@/components/field";
import { PageHeader } from "@/components/page-header";
import {
	AlertDialog,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
	AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { api, messageOf } from "@/lib/api";
import { pageTitle } from "@/lib/format";
import type { AdminSettings } from "@/lib/types";

export const Route = createFileRoute("/account")({
	head: () => ({ meta: [{ title: pageTitle("Account") }] }),
	component: Account,
});

/**
 * One settings row: its title and description, beside the card from `lg` and above it below
 * `lg`. The card holds the controls and an optional footer for the row's action.
 */
function Setting({
	title,
	description,
	footer,
	onSubmit,
	danger,
	children,
}: {
	title: string;
	description: ReactNode;
	footer?: ReactNode;
	onSubmit?: (event: FormEvent) => void;
	danger?: boolean;
	children?: ReactNode;
}) {
	const id = useId();
	const Body = onSubmit ? "form" : "div";
	return (
		<section
			aria-labelledby={id}
			className="grid gap-x-8 gap-y-3 py-6 first:pt-2 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]"
		>
			<div className="space-y-1">
				<h2
					id={id}
					className={`font-semibold tracking-tight ${danger ? "text-destructive" : ""}`}
				>
					{title}
				</h2>
				<p className="max-w-prose text-sm text-muted-foreground">
					{description}
				</p>
			</div>
			<Body
				onSubmit={onSubmit}
				className={`overflow-hidden rounded-sm bg-card shadow-[0_1px_0_var(--border)] ${danger ? "ring-1 ring-destructive/30" : ""}`}
			>
				{children && <div className="space-y-4 p-5">{children}</div>}
				{footer && (
					<div className="flex flex-wrap items-center justify-end gap-x-4 gap-y-2 border-t bg-muted/40 px-5 py-3">
						{footer}
					</div>
				)}
			</Body>
		</section>
	);
}

/** A line of text in a card footer, left of its button. Errors and results are announced. */
function Note({
	tone,
	children,
}: {
	tone?: "error" | "result";
	children: ReactNode;
}) {
	return (
		<p
			role={
				tone === "error" ? "alert" : tone === "result" ? "status" : undefined
			}
			className={`mr-auto text-sm ${tone === "error" ? "text-destructive" : "text-muted-foreground"}`}
		>
			{children}
		</p>
	);
}

function Account() {
	const { session } = useLoaderData({ from: "__root__" });
	const { user } = session;
	if (!user) return <Navigate to="/login" search={{ redirect: "/account" }} />;

	return (
		<div className="max-w-5xl">
			<PageHeader title="Account">
				Your sign-in details{user.admin && " and the server's settings"}.
			</PageHeader>
			<div className="divide-y">
				<Profile email={user.email} admin={user.admin} />
				<PasswordForm email={user.email} />
				{user.admin ? <ServerSettings /> : <DeleteAccount />}
			</div>
		</div>
	);
}

function Profile({ email, admin }: { email: string; admin: boolean }) {
	const [error, setError] = useState("");

	async function signOut() {
		try {
			await api.signOut();
			window.location.assign("/login");
		} catch (e) {
			setError(messageOf(e));
		}
	}

	return (
		<Setting
			title="Profile"
			description="The email you sign in with. Your progress belongs to this account only."
			footer={
				<>
					{error ? (
						<Note tone="error">{error}</Note>
					) : (
						<Note>Signing out ends the session in this browser.</Note>
					)}
					<Button variant="outline" onClick={signOut}>
						Sign out
					</Button>
				</>
			}
		>
			<dl className="grid gap-x-6 gap-y-3 text-sm grid-cols-[6rem_minmax(0,1fr)]">
				<dt className="text-muted-foreground">Email</dt>
				<dd className="font-medium break-all">{email}</dd>
				<dt className="text-muted-foreground">Role</dt>
				<dd>
					<Badge variant={admin ? "default" : "secondary"}>
						{admin ? "Admin" : "Member"}
					</Badge>
				</dd>
			</dl>
		</Setting>
	);
}

function PasswordForm({ email }: { email: string }) {
	const [current, setCurrent] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [done, setDone] = useState(false);
	const [busy, setBusy] = useState(false);

	async function submit(event: FormEvent) {
		event.preventDefault();
		setBusy(true);
		setError("");
		setDone(false);
		try {
			await api.changePassword(current, password);
			setCurrent("");
			setPassword("");
			setDone(true);
		} catch (e) {
			setError(messageOf(e));
		} finally {
			setBusy(false);
		}
	}

	return (
		<Setting
			title="Password"
			description="Use 8 to 128 characters. Changing it signs out your other sessions."
			onSubmit={submit}
			footer={
				<>
					{error && <Note tone="error">{error}</Note>}
					{done && <Note tone="result">Password changed.</Note>}
					<Button type="submit" disabled={busy}>
						Change password
					</Button>
				</>
			}
		>
			{/* Tells password managers which account the new password is for. */}
			<input
				type="email"
				name="username"
				autoComplete="username"
				value={email}
				readOnly
				hidden
			/>
			<div className="grid gap-4 sm:grid-cols-2">
				<Field
					label="Current password"
					type="password"
					name="current-password"
					autoComplete="current-password"
					required
					value={current}
					onChange={(e) => setCurrent(e.target.value)}
				/>
				<Field
					label="New password"
					type="password"
					name="new-password"
					autoComplete="new-password"
					minLength={8}
					maxLength={128}
					required
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
			</div>
		</Setting>
	);
}

function ServerSettings() {
	const [settings, setSettings] = useState<AdminSettings>();
	const [error, setError] = useState("");
	const label = useId();
	const hint = useId();

	useEffect(() => {
		api
			.adminSettings()
			.then(setSettings)
			.catch((e) => setError(messageOf(e)));
	}, []);

	async function toggle(signupsOpen: boolean) {
		setError("");
		try {
			setSettings(await api.editAdminSettings({ signupsOpen }));
		} catch (e) {
			setError(messageOf(e));
		}
	}

	return (
		<Setting
			title="Server"
			description="Settings for everyone on this server. Only admins see them."
		>
			<dl className="grid gap-x-6 gap-y-3 text-sm grid-cols-[6rem_minmax(0,1fr)]">
				<dt className="text-muted-foreground">Accounts</dt>
				<dd className="font-medium tabular-nums">{settings?.users ?? "…"}</dd>
			</dl>
			<div className="flex items-start justify-between gap-4 border-t pt-4">
				<div className="space-y-0.5">
					<p id={label} className="text-sm font-medium">
						Allow new sign-ups
					</p>
					<p id={hint} className="text-sm text-muted-foreground">
						When off, only existing accounts can sign in.
					</p>
				</div>
				<Switch
					aria-labelledby={label}
					aria-describedby={hint}
					checked={settings?.signupsOpen ?? false}
					disabled={!settings}
					onCheckedChange={toggle}
					className="mt-0.5"
				/>
			</div>
			{error && (
				<p role="alert" className="text-sm text-destructive">
					{error}
				</p>
			)}
		</Setting>
	);
}

function DeleteAccount() {
	const [open, setOpen] = useState(false);
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [busy, setBusy] = useState(false);

	function onOpenChange(next: boolean) {
		setOpen(next);
		if (!next) {
			setPassword("");
			setError("");
		}
	}

	async function remove(event: FormEvent) {
		event.preventDefault();
		setBusy(true);
		setError("");
		try {
			await api.deleteAccount(password);
			window.location.assign("/login");
		} catch (e) {
			setError(messageOf(e));
			setBusy(false);
		}
	}

	return (
		<Setting
			title="Delete account"
			description="Removes this account for good."
			danger
			footer={
				<AlertDialog open={open} onOpenChange={onOpenChange}>
					<AlertDialogTrigger render={<Button variant="destructive" />}>
						Delete account
					</AlertDialogTrigger>
					<AlertDialogContent>
						<form onSubmit={remove} className="contents">
							<AlertDialogHeader>
								<AlertDialogTitle>Delete your account?</AlertDialogTitle>
								<AlertDialogDescription>
									All your progress is deleted for good. Enter your password to
									confirm.
								</AlertDialogDescription>
							</AlertDialogHeader>
							<Field
								label="Password"
								type="password"
								name="password"
								autoComplete="current-password"
								required
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
							{error && (
								<p role="alert" className="text-sm text-destructive">
									{error}
								</p>
							)}
							<AlertDialogFooter>
								<AlertDialogCancel>Keep account</AlertDialogCancel>
								<Button type="submit" variant="destructive" disabled={busy}>
									Delete account
								</Button>
							</AlertDialogFooter>
						</form>
					</AlertDialogContent>
				</AlertDialog>
			}
		>
			<p className="text-sm">
				Your progress, notes, drafts, submissions, plans and lists are deleted
				with the account. This cannot be undone.
			</p>
		</Setting>
	);
}
