import { useLoaderData, useSearch } from "@tanstack/react-router";
import type { Company } from "@/lib/types";

/** Every company with problem lists, in picker order (the root route loads them). */
export function useCompanies(): Company[] {
	return useLoaderData({ from: "__root__" }).companies;
}

/** The selected company's slug (or "any"), from the URL; every page shares it. */
export function useCompany(): string {
	return useSearch({ from: "__root__" }).company;
}
