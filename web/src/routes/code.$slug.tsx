import { createFileRoute, stripSearchParams } from "@tanstack/react-router";
import { CodePage } from "@/components/code/code-page";
import { api, orNotFound } from "@/lib/api";
import { pageTitle } from "@/lib/format";
import { PLAN_DEFAULTS, parsePlanSearch } from "@/lib/schemas";

/**
 * /code/two-sum: solve the problem in Python. Its search params are the practice plan whose
 * next problem the page offers after a solve. Its component (and CodeMirror) load lazily.
 */
export const Route = createFileRoute("/code/$slug")({
	validateSearch: parsePlanSearch,
	search: { middlewares: [stripSearchParams(PLAN_DEFAULTS)] },
	loader: async ({ params: { slug } }) => {
		const [card, code, submissions] = await orNotFound(
			Promise.all([api.problem(slug), api.code(slug), api.submissions(slug)]),
		);
		return { card, code, submissions };
	},
	// Changing the plan changes only the search params: the problem's data stays.
	shouldReload: ({ cause }) => cause !== "stay",
	head: ({ loaderData }) => ({
		meta: [
			{
				title: loaderData
					? pageTitle(loaderData.card.problem.title, "Code")
					: pageTitle("Code"),
			},
		],
	}),
	component: Code,
});

function Code() {
	const data = Route.useLoaderData();
	return <CodePage key={data.card.problem.slug} {...data} />;
}
