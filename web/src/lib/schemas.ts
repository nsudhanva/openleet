import { z } from "zod";
import { STUDY_SETS, type StudySet } from "@/lib/scheduler";
import { DIFFICULTIES, PERIODS } from "@/lib/types";

const SET_KEYS = Object.keys(STUDY_SETS) as [StudySet, ...StudySet[]];

/** Search params of the study page, which are also the query of GET /api/deck. */
export const studySearchSchema = z.object({
	set: z.enum(SET_KEYS).catch("smart").default("smart"),
	period: z.enum(PERIODS).catch("6m").default("6m"),
	topic: z.string().optional().catch(undefined),
	difficulty: z.enum(DIFFICULTIES).optional().catch(undefined),
	/** Show this problem instead of the next one in the queue. */
	slug: z.string().optional().catch(undefined),
});
export type StudySearch = z.infer<typeof studySearchSchema>;
