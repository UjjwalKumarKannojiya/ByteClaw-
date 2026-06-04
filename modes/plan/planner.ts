import {
  Output,
  extractJsonMiddleware,
  generateText,
  stepCountIs,
  tool,
  wrapLanguageModel,
} from "ai";
import { z } from "zod";
import chalk from "chalk";
import { getAgentModel } from "../../ai/ai.config.ts";
import { ActionTracker } from "../agent/action-tracker.ts";
import { ToolExecutor } from "../agent/tool-executor.ts";
import { defaultAgentConfig } from "../agent/types.ts";
import type { Plan, PlanStep } from "./types.ts";
import { createWebTools } from "./web-tools.ts";

const planSchema = z.object({
  researchSummary: z.string().optional(),
  steps: z
    .array(
      z.object({
        title: z.string(),
        description: z.string(),
        hints: z.array(z.string()).optional(),
        complexity: z.enum(["low", "medium", "high"]).optional(),
      }),
    )
    .min(1)
    .max(15),
});

type PlannerOutput = z.infer<typeof planSchema>;

function readOnlyTools(executor: ToolExecutor) {
  return {
    read_file: tool({
      description:
        "Read a text file from the workspace. Use a path relative to the project root.",
      inputSchema: z.object({
        path: z.string().describe("Relative file path"),
      }),
      execute: async ({ path }) => executor.readFile(path),
    }),

    list_files: tool({
      description: "List files and directories under a path.",
      inputSchema: z.object({
        path: z.string(),
        recursive: z.boolean().optional().default(false),
      }),
      execute: async ({ path, recursive }) =>
        executor.listFiles(path, recursive),
    }),

    search_files: tool({
      description:
        'Find files matching a glob pattern, for example "*.ts" or "**/*.md". Optional content substring filter.',
      inputSchema: z.object({
        root: z.string().describe("Directory to search, relative to root"),
        pattern: z
          .string()
          .describe("Glob-like pattern using * and ** with forward slashes"),
        content_contains: z.string().optional(),
      }),
      execute: async ({ root, pattern, content_contains }) =>
        executor.searchFiles(root, pattern, content_contains),
    }),

    analyze_codebase: tool({
      description:
        "Summarize codebase structure: file counts, size, and extensions. Read-only.",
      inputSchema: z.object({
        path: z.string().default("."),
      }),
      execute: async ({ path }) => executor.analyzeCodebase(path),
    }),

    list_skills: tool({
      description:
        "List absolute paths to SKILL.md files under configured skill directories.",
      inputSchema: z.object({}),
      execute: async () => executor.listSkills(),
    }),

    read_skill: tool({
      description:
        "Read a SKILL.md file. Path must be absolute and under skill roots, or use a path returned by list_skills.",
      inputSchema: z.object({
        path: z.string(),
      }),
      execute: async ({ path }) => executor.readSkill(path),
    }),
  };
}

function getPlanInstructions(codebasePath: string, hasWeb: boolean): string {
  return [
    "You are ByteClaw Plan Mode planner.",
    "You only create a plan. You do not modify files.",
    `Workspace: ${codebasePath}`,
    "Use read-only tools for codebase and skill research.",
    hasWeb
      ? "Web tools are available: web_search, web_crawl, fetch_url. Use them only when external research is necessary."
      : "Web tools are unavailable because FIRECRAWL_API_KEY is missing.",
    "Return only valid JSON matching the provided schema.",
    "Keep the plan practical and short.",
    "Create between 1 and 15 steps.",
    "Each step must be executable and clear.",
  ].join("\n");
}

function normalizeSteps(steps: PlannerOutput["steps"]): PlanStep[] {
  return steps.map((step, index) => ({
    id: `step-${index + 1}`,
    title: step.title,
    description: step.description,
    hints: step.hints ?? [],
    complexity: step.complexity ?? "medium",
  }));
}

export async function generatePlan(goal: string): Promise<Plan> {
  const config = defaultAgentConfig();
  const tracker = new ActionTracker();
  const executor = new ToolExecutor(tracker, config);

  const hasWeb = Boolean(process.env.FIRECRAWL_API_KEY);

  const model = wrapLanguageModel({
    model: getAgentModel(),
    middleware: extractJsonMiddleware(),
  });

  const tools = {
    ...readOnlyTools(executor),
    ...(hasWeb ? createWebTools(tracker) : {}),
  };

  console.log(chalk.cyan("\n🔍 Researching & drafting a plan...\n"));

  try {
    const result = await generateText({
      model,
      tools,

      // Keep this higher because structured output with tools needs extra steps.
      stopWhen: stepCountIs(25),

      system: getPlanInstructions(config.codebasePath, hasWeb),

      prompt: [
        "User goal:",
        goal,
        "",
        "Create a useful execution plan.",
        "Research the workspace first if needed.",
      ].join("\n"),

      output: Output.object({
        schema: planSchema,
      }),
    });

    const validated = planSchema.parse(result.output);

    return {
      goal,
      researchSummary: validated.researchSummary,
      steps: normalizeSteps(validated.steps),
    };
  } catch (error) {
    console.log(chalk.red("\nFailed to generate plan.\n"));

    if (error instanceof Error) {
      console.log(chalk.dim(error.message));
    } else {
      console.log(chalk.dim(String(error)));
    }

    throw error;
  }
}