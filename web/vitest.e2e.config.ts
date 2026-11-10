import { defineConfig } from "vitest/config";

/** End-to-end suite against a running app: `E2E_BASE_URL=http://localhost:8080 bun run test:e2e`. */
export default defineConfig({
	test: {
		include: ["e2e/**/*.test.ts"],
		globalSetup: ["e2e/setup.ts"],
		testTimeout: 15_000,
	},
});
