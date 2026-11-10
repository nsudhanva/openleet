import { createFileRoute } from "@tanstack/react-router";
import { CodePage } from "@/components/code/code-page";
import { api, orNotFound } from "@/lib/api";
import { pageTitle } from "@/lib/format";

/** /code/two-sum: solve the problem in Python. Its component (and CodeMirror) load lazily. */
export const Route = createFileRoute("/code/$slug")({
	loader: async ({ params: { slug } }) => {
		const [card, code, submissions] = await orNotFound(
			Promise.all([api.problem(slug), api.code(slug), api.submissions(slug)]),
		);
		return { card, code, submissions };
	},
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
