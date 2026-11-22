import type { TestProject } from "vitest/node";

declare module "vitest" {
	export interface ProvidedContext {
		baseUrl: string;
		/** The suite's session cookie ("name=token"). */
		cookie: string;
	}
}

/**
 * Points the end-to-end suite at a running app: E2E_BASE_URL, or the local docker compose
 * stack at http://openleet.localhost. The suite runs as an account of its own, deleted at
 * the end, so other accounts' progress stays as it was. Sign-ups must be open; on a server with
 * no admin yet, set E2E_SETUP_CODE and the suite's account becomes the admin (and is kept).
 */
export default async function setup(project: TestProject) {
	const baseUrl = (
		process.env.E2E_BASE_URL ?? "http://openleet.localhost"
	).replace(/\/$/, "");
	const setupCode = process.env.E2E_SETUP_CODE;
	const email = `e2e-${crypto.randomUUID().slice(0, 12)}@openleet.invalid`;
	const password = crypto.randomUUID();
	let made: Response;
	try {
		made = await fetch(`${baseUrl}/api/users`, {
			method: "POST",
			headers: { "content-type": "application/json" },
			body: JSON.stringify({ email, password, setupCode }),
		});
	} catch (error) {
		throw new Error(`No app at ${baseUrl}; start it or set E2E_BASE_URL`, {
			cause: error,
		});
	}
	const cookie = made.headers.get("set-cookie")?.split(";")[0];
	if (made.status !== 201 || !cookie)
		throw new Error(
			`Could not make the suite's account: ${made.status} ${await made.text()}`,
		);
	project.provide("baseUrl", baseUrl);
	project.provide("cookie", cookie);
	return async () => {
		if (setupCode) return;
		await fetch(`${baseUrl}/api/account`, {
			method: "DELETE",
			headers: { "content-type": "application/json", cookie },
			body: JSON.stringify({ password }),
		});
	};
}
