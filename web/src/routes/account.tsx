import {
	createFileRoute,
	Navigate,
	useLoaderData,
} from "@tanstack/react-router";
import { type FormEvent, useEffect, useState } from "react";
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
import { Button } from "@/components/ui/button";
import { api, messageOf } from "@/lib/api";
import { pageTitle } from "@/lib/format";
import type { AdminSettings } from "@/lib/types";

export const Route = createFileRoute("/account")({
	head: () => ({ meta: [{ title: pageTitle("Account") }] }),
	component: Account,
});

function Section({
	title,
	children,
}: {
	title: string;
	children: React.ReactNode;
}) {
	return (
		<section className="max-w-sm space-y-3 rounded-sm bg-card p-5 shadow-[0_1px_0_var(--border)]">
			<h2 className="font-semibold tracking-tight">{title}</h2>
			{children}
		</section>
	);
}

function Account() {
	const { session } = useLoaderData({ from: "__root__" });
	const { user } = session;
	const [error, setError] = useState("");
	if (!user) return <Navigate to="/login" search={{ redirect: "/account" }} />;

	async function signOut() {
		try {
			await api.signOut();
			window.location.assign("/login");
		} catch (e) {
			setError(messageOf(e));
		}
	}

	return (
		<div className="space-y-3">
			<PageHeader title="Account">
				Signed in as <strong className="text-foreground">{user.email}</strong>
				{user.admin && " (admin)"}.
			</PageHeader>
			<Section title="Session">
				<Button variant="outline" onClick={signOut}>
					Sign out
				</Button>
				{error && (
					<p role="alert" className="text-sm text-destructive">
						{error}
					</p>
				)}
			</Section>
			<PasswordForm email={user.email} />
			{user.admin ? <AdminSection /> : <DeleteSection />}
		</div>
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
		<Section title="Change password">
			<form onSubmit={submit} className="space-y-3">
				{/* Tells password managers which account the new password is for. */}
				<input
					type="email"
					name="username"
					autoComplete="username"
					value={email}
					readOnly
					hidden
				/>
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
				<p className="text-sm text-muted-foreground">
					Your other sessions end when the password changes.
				</p>
				{error && (
					<p role="alert" className="text-sm text-destructive">
						{error}
					</p>
				)}
				{done && (
					<p role="status" className="text-sm text-muted-foreground">
						Password changed.
					</p>
				)}
				<Button type="submit" disabled={busy}>
					Change password
				</Button>
			</form>
		</Section>
	);
}

function AdminSection() {
	const [settings, setSettings] = useState<AdminSettings>();
	const [error, setError] = useState("");

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
		<Section title="Server">
			{settings && (
				<>
					<p className="text-sm text-muted-foreground">
						{settings.users} {settings.users === 1 ? "account" : "accounts"} on
						this server.
					</p>
					<label className="flex items-center gap-2 text-sm">
						<input
							type="checkbox"
							className="size-4 accent-primary"
							checked={settings.signupsOpen}
							onChange={(e) => toggle(e.target.checked)}
						/>
						Allow new sign-ups
					</label>
				</>
			)}
			{error && (
				<p role="alert" className="text-sm text-destructive">
					{error}
				</p>
			)}
		</Section>
	);
}

function DeleteSection() {
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
		<Section title="Delete account">
			<p className="text-sm text-muted-foreground">
				Deleting the account removes all its progress, notes, drafts, plans and
				lists. This cannot be undone.
			</p>
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
		</Section>
	);
}
