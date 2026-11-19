import { useEffect, useSyncExternalStore } from "react";
import { api } from "@/lib/api";
import type { UserList } from "@/lib/types";

/**
 * Your lists, shared by every component that shows or edits them: fetched on first use (the
 * problem table's loader hands over what it fetched), and fetched again after each edit made
 * here.
 */
let lists: UserList[] | undefined;
let loading: Promise<UserList[]> | undefined;
const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
	listeners.add(listener);
	return () => listeners.delete(listener);
}

/** Replaces the known lists, for example with what a route loader fetched. */
export function setUserLists(next: UserList[]) {
	lists = next;
	for (const listener of listeners) listener();
}

function load(): Promise<UserList[]> {
	loading ??= api.lists().then(
		(fetched) => {
			setUserLists(fetched);
			return fetched;
		},
		(error: unknown) => {
			loading = undefined;
			throw error;
		},
	);
	return loading;
}

/** Your lists, newest first; undefined until they arrive. Fetches them only when `wanted`. */
export function useUserLists(wanted = true): UserList[] | undefined {
	const current = useSyncExternalStore(
		subscribe,
		() => lists,
		() => lists,
	);
	useEffect(() => {
		if (wanted && !lists)
			load().catch((error: unknown) =>
				console.error("Could not load your lists", error),
			);
	}, [wanted]);
	return current;
}

/** The name of one of your lists, while the lists are known. */
export function listNameOf(
	known: UserList[] | undefined,
): (id: number) => string | undefined {
	return (id) => known?.find((list) => list.id === id)?.name;
}

/** Runs an edit, then fetches the lists again so every view shows the change. */
async function edited<T>(change: Promise<T>): Promise<T> {
	const result = await change;
	loading = undefined;
	await load();
	return result;
}

export const createList = (name: string, slugs: string[] = []) =>
	edited(api.createList(name, slugs));

export const renameList = (id: number, name: string) =>
	edited(api.editList(id, { name }));

export const deleteList = (id: number) => edited(api.deleteList(id));

/** Adds problems at the end of a list, each once. */
export const addToList = (list: UserList, slugs: string[]) =>
	edited(
		api.editList(list.id, {
			slugs: [...list.slugs, ...slugs.filter((s) => !list.slugs.includes(s))],
		}),
	);

/** Takes problems off a list, keeping the order of the rest. */
export const removeFromList = (list: UserList, slugs: string[]) =>
	edited(
		api.editList(list.id, {
			slugs: list.slugs.filter((s) => !slugs.includes(s)),
		}),
	);
