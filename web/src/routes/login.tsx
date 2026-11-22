import {
	createFileRoute,
	Navigate,
	useLoaderData,
} from "@tanstack/react-router";
import { type FormEvent, useState } from "react";
import { Field } from "@/components/field";
import { Button } from "@/components/ui/button";
import { api, messageOf } from "@/lib/api";
import { pageTitle } from "@/lib/format";
import { safeRedirect } from "@/lib/redirect";

export const Route = createFileRoute("/login")({
	validateSearch: (search): { redirect: string } => ({
		redirect: safeRedirect(search.redirect, window.location.origin),
	}),
	head: () => ({ meta: [{ title: pageTitle("Sign in") }] }),
	component: Login,
});

function Login() {
	const { redirect } = Route.useSearch();
	const { session } = useLoaderData({ from: "__root__" });
	const [creating, setCreating] = useState(session.needsSetup);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [setupCode, setSetupCode] = useState("");
	const [error, setError] = useState("");
	const [busy, setBusy] = useState(false);

	if (session.user) return <Navigate to="/" />;

	const canCreate = session.signupsOpen || session.needsSetup;

	async function submit(event: FormEvent) {
		event.preventDefault();
		setBusy(true);
		setError("");
		try {
			if (creating) {
				await api.signUp(
					email,
					password,
					session.needsSetup ? setupCode.trim() : undefined,
				);
			} else {
				await api.signIn(email, password);
			}
			// A full load, so every loader asks again as the new user.
			window.location.assign(redirect);
		} catch (e) {
			setError(messageOf(e));
			setBusy(false);
		}
	}

	return (
		<div className="mx-auto w-full max-w-sm space-y-4 pt-8 sm:pt-16">
			<h1 className="text-2xl font-semibold tracking-tight">
				{creating ? "Create account" : "Sign in"}
			</h1>
			{session.needsSetup && (
				<p className="text-sm text-muted-foreground">
					This server has no accounts yet. The setup code is in the{" "}
					<code className="font-mono">setup-code</code> file in the server's
					state directory. The first account made with it is the admin.
				</p>
			)}
			<form onSubmit={submit} className="space-y-3">
				<Field
					label="Email"
					type="email"
					name="email"
					autoComplete={creating ? "email" : "username"}
					required
					value={email}
					onChange={(e) => setEmail(e.target.value)}
				/>
				<Field
					label="Password"
					type="password"
					name="password"
					autoComplete={creating ? "new-password" : "current-password"}
					minLength={creating ? 8 : undefined}
					maxLength={128}
					required
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				{creating && session.needsSetup && (
					<Field
						label="Setup code"
						type="text"
						name="setup-code"
						autoComplete="off"
						required
						value={setupCode}
						onChange={(e) => setSetupCode(e.target.value)}
					/>
				)}
				{creating && !session.needsSetup && (
					<p className="text-sm text-muted-foreground">
						Use at least 8 characters.
					</p>
				)}
				{error && (
					<p role="alert" className="text-sm text-destructive">
						{error}
					</p>
				)}
				<Button type="submit" size="lg" className="w-full" disabled={busy}>
					{creating ? "Create account" : "Sign in"}
				</Button>
			</form>
			{!session.needsSetup &&
				(canCreate ? (
					<p className="text-sm text-muted-foreground">
						{creating ? "Have an account?" : "No account?"}{" "}
						<button
							type="button"
							className="text-primary underline underline-offset-4"
							onClick={() => {
								setCreating(!creating);
								setError("");
							}}
						>
							{creating ? "Sign in" : "Create account"}
						</button>
					</p>
				) : (
					<p className="text-sm text-muted-foreground">
						New accounts are closed on this server.
					</p>
				))}
		</div>
	);
}
