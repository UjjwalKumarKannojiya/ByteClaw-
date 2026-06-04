import { createOpenRouter } from "@openrouter/ai-sdk-provider";

function getRequiredEnv(name: string): string {
  const value = process.env[name];

  if (!value || value.trim() === "") {
    throw new Error(`${name} is missing in .env`);
  }

  return value;
}

export function getAgentModel() {
  const apiKey = getRequiredEnv("OPENROUTER_API_KEY");
  const modelId = getRequiredEnv("OPENROUTER_DEFAULT_MODEL");

  const provider = createOpenRouter({
    apiKey,
  });

  return provider(modelId);
}