
import { select, isCancel } from "@clack/prompts";
import chalk from "chalk";
import figlet from "figlet";
import { runCliMode } from "../modes/cli";
import { runTelegramMode } from "../modes/telegram";

const BANNER_FONT = "ANSI Shadow";

const neon = chalk.hex("#9D7CFF").bold;
const cyan = chalk.hex("#38BDF8");
const dim = chalk.hex("#6B7280");
const silver = chalk.hex("#E5E7EB");
const violet = chalk.hex("#A78BFA");
const shadow = chalk.hex("#241A45");

function line(width = 72) {
  console.log(dim("─".repeat(width)));
}

function center(text: string, width = 72) {
  const cleanLength = text.replace(/\x1b\[[0-9;]*m/g, "").length;
  const left = Math.max(0, Math.floor((width - cleanLength) / 2));
  return " ".repeat(left) + text;
}

function printBanner(ascii: string) {
  const bannerLines = ascii.replace(/\s+$/, "").split("\n");
  const maxLen = Math.max(...bannerLines.map((line) => line.length), 0);
  const rowWidth = maxLen + 4;

  console.log();

  for (const line of bannerLines) {
    console.log(shadow(("  " + line).padEnd(rowWidth)));
  }

  process.stdout.write(`\x1b[${bannerLines.length}A`);

  for (const line of bannerLines) {
    console.log(neon(line.padEnd(rowWidth)));
  }

  console.log();
}

function printHeader() {
  line();
  console.log(center(`${cyan("◆")} ${silver.bold("BYTECLAW BUILD SYSTEM")} ${cyan("◆")}`));
  console.log(center(dim("Next-gen automation CLI for developers")));
  line();
  console.log();
}

function printStatus() {
  console.log(`${violet("▸")} ${silver("Runtime")}     ${dim("Bun powered")}`);
  console.log(`${violet("▸")} ${silver("Interface")}   ${dim("Interactive terminal")}`);
  console.log(`${violet("▸")} ${silver("Status")}      ${chalk.greenBright("Online")}`);
  console.log();
  line();
  console.log();
}

export async function runwakeup() {
  console.clear();

  let ascii: string;

  try {
    ascii = figlet.textSync("ByteClaw", {
      font: BANNER_FONT,
      horizontalLayout: "default",
      verticalLayout: "default",
    });
  } catch {
    ascii = figlet.textSync("ByteClaw", {
      font: "Standard",
    });
  }

  printBanner(ascii);
  printHeader();
  printStatus();

  const mode = await select({
    message: chalk.hex("#E5E7EB").bold("Choose your launch mode"),
    options: [
      {
        value: "cli",
        label: "CLI Mode",
        hint: "Run ByteClaw directly in terminal",
      },
      {
        value: "telegram",
        label: "Telegram Mode",
        hint: "Connect ByteClaw with Telegram bot",
      },
      {
        value: "exit",
        label: "Exit",
        hint: "Close ByteClaw safely",
      },
    ],
  });

  if (isCancel(mode) || mode === "exit") {
    console.log();
    console.log(dim("Session terminated."));
    console.log(chalk.hex("#9D7CFF")("Goodbye, operator."));
    console.log();
    return;
  }

  if (mode === "cli") {
    console.log();
    console.log(`${cyan("▶")} ${silver("Launching CLI Mode...")}`);
    console.log();
    await runCliMode();
  }

  if (mode === "telegram") {
    console.log();
    console.log(`${cyan("▶")} ${silver("Launching Telegram Mode...")}`);
    console.log();
    await runTelegramMode();
  }
}