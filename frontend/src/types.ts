import { Project } from "./schemas/ProjectInput";
import { z } from "zod";

export type ProjectType = z.infer<typeof Project>;
