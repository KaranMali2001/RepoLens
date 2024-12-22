import { Commit } from "./schemas/commit";
import { Project } from "./schemas/ProjectInput";
import { z } from "zod";

export type ProjectType = z.infer<typeof Project>;
export type CommitType = z.infer<typeof Commit>;
