import type { TestProject } from "vitest/node";

declare module "vitest" {
	export interface ProvidedContext {
		baseUrl: string;
	}
}

/**
 * Points the end-to-end suite at a running app: E2E_BASE_URL, or the local docker compose
 * stack at http://openleet.localhost. The suite clears all progress, so use a throwaway database.
 */
export default async function setup(project: TestProject) {
	const baseUrl = (
		process.env.E2E_BASE_URL ?? "http://openleet.localhost"
	).replace(/\/$/, "");
	try {
		await fetch(`${baseUrl}/api/readiness`);
	} catch (error) {
		throw new Error(`No app at ${baseUrl}; start it or set E2E_BASE_URL`, {
			cause: error,
		});
	}
	project.provide("baseUrl", baseUrl);
}
