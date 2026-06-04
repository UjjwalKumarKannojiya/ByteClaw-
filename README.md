<div align="center">

```txt
██████╗ ██╗   ██╗████████╗███████╗ ██████╗██╗      █████╗ ██╗    ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔════╝██║     ██╔══██╗██║    ██║
██████╔╝ ╚████╔╝    ██║   █████╗  ██║     ██║     ███████║██║ █╗ ██║
██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██║     ██║     ██╔══██║██║███╗██║
██████╔╝   ██║      ██║   ███████╗╚██████╗███████╗██║  ██║╚███╔███╔╝
╚═════╝    ╚═╝      ╚═╝   ╚══════╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝
```

<h3>AI-powered terminal and Telegram assistant for understanding, planning, and modifying codebases</h3>

<p>
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Bun-1.3+-000000?style=for-the-badge&logo=bun&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenRouter-AI-7C3AED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Firecrawl-Web%20Tools-FF6B35?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Telegram-Bot-229ED9?style=for-the-badge&logo=telegram&logoColor=white" />
</p>

<p>
  <b>Ask your codebase.</b> Generate plans. Let the agent stage changes. Approve before applying.
</p>

</div>

---

## ✦ What is ByteClaw?

**ByteClaw** is an AI-powered developer assistant that runs as an interactive **terminal CLI** and also supports **Telegram bot mode**.

It helps developers inspect a codebase, ask questions, generate implementation plans, and let an AI agent safely stage project changes before applying them.

ByteClaw is built for fast local developer workflows using **Bun**, **TypeScript**, **OpenRouter**, **Vercel AI SDK**, **Firecrawl**, and **Telegraf**.

---

## ✦ Features

<table>
<tr>
<td width="50%">

### 🖥️ CLI Mode

A polished terminal experience with a futuristic wakeup screen and interactive prompts.

**Includes:**

* Terminal mode selector
* Agent Mode
* Plan Mode
* Ask Mode
* Markdown output rendering
* Styled terminal interface

</td>
<td width="50%">

### 🤖 Telegram Bot

Run ByteClaw from Telegram and control your codebase assistant remotely.

**Commands:**

* `/ask`
* `/agent`
* `/plan`

Useful for quick planning, asking, and agent workflows from anywhere.

</td>
</tr>

<tr>
<td width="50%">

### 🔎 Ask Mode

Ask questions about your local codebase.

**Can help with:**

* Explaining files
* Understanding project structure
* Searching modules
* Finding logic
* Saving answers as Markdown

</td>
<td width="50%">

### 🧠 Agent Mode

Let the AI agent work on your project with approval-first changes.

**Can stage:**

* File creation
* File modification
* File deletion
* Folder creation
* Shell command execution

</td>
</tr>

<tr>
<td width="50%">

### 🧭 Plan Mode

Generate a step-by-step plan before coding.

**Includes:**

* Plan summary
* Step titles
* Step descriptions
* Hints
* Complexity level
* Selective execution

</td>
<td width="50%">

### 🌐 Web Tools

Use Firecrawl-powered tools for research and external context.

**Supports:**

* Web search
* URL fetching
* Web crawling
* Documentation lookup
* Research-assisted planning

</td>
</tr>
</table>

---

## ✦ Project Structure

```txt
ByteClaw-
├── ai/
│   ├── ai.config.ts
│   └── index.ts
│
├── modes/
│   ├── agent/
│   │   ├── action-tracker.ts
│   │   ├── agent-tools.ts
│   │   ├── approval.ts
│   │   ├── diff-view.ts
│   │   ├── orchestrator.ts
│   │   ├── tool-executor.ts
│   │   └── types.ts
│   │
│   ├── ask/
│   │   └── orchestrator.ts
│   │
│   ├── plan/
│   │   ├── orchestrator.ts
│   │   ├── planner.ts
│   │   ├── selection.ts
│   │   ├── types.ts
│   │   └── web-tools.ts
│   │
│   ├── telegram/
│   │   ├── agent-run.ts
│   │   ├── approval-session.ts
│   │   ├── auth.ts
│   │   ├── constants.ts
│   │   ├── handlers.ts
│   │   ├── index.ts
│   │   ├── plan-session.ts
│   │   └── text.ts
│   │
│   └── cli.ts
│
├── tui/
│   ├── terminal-md.ts
│   └── wakeup.ts
│
├── index.ts
├── package.json
├── tsconfig.json
├── bun.lock
└── README.md
```

---

## ✦ Tech Stack

| Technology                   | Purpose                                |
| ---------------------------- | -------------------------------------- |
| **Bun**                      | JavaScript runtime and package manager |
| **TypeScript**               | Type-safe project development          |
| **Commander.js**             | CLI command registration               |
| **Clack Prompts**            | Interactive terminal prompts           |
| **Chalk**                    | Terminal colors and styling            |
| **Figlet**                   | ASCII banner generation                |
| **Vercel AI SDK**            | Tool-loop agent and AI generation      |
| **OpenRouter**               | AI model provider                      |
| **Zod**                      | Schema validation                      |
| **Firecrawl**                | Web search, crawl, and fetch tools     |
| **Telegraf**                 | Telegram bot framework                 |
| **Marked + marked-terminal** | Terminal Markdown rendering            |
| **Diff**                     | Text diff utilities                    |

---

## ✦ Getting Started

<table>
<tr>
<td width="50%">

### 1. Clone Repository

```bash
git clone https://github.com/UjjwalKumarKannojiya/ByteClaw-.git
cd ByteClaw-
```

</td>
<td width="50%">

### 2. Install Dependencies

```bash
bun install
```

</td>
</tr>

<tr>
<td width="50%">

### 3. Create Environment File

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

</td>
<td width="50%">

### 4. Run ByteClaw

```bash
bun index.ts wakeup
```

Or:

```bash
bun run byteclaw-build wakeup
```

</td>
</tr>
</table>

---

## ✦ Environment Variables

<table>
<tr>
<td width="50%">

### Required

```env
OPENROUTER_API_KEY=
OPENROUTER_DEFAULT_MODEL=
```

Used for AI model access through OpenRouter.

</td>
<td width="50%">

### Optional Web Tools

```env
FIRECRAWL_API_KEY=
```

Used for web search, crawling, and URL fetching.

</td>
</tr>

<tr>
<td width="50%">

### Telegram Bot

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_OWNER_ID=
```

Used for running ByteClaw in Telegram mode.

</td>
<td width="50%">

### Example Model

```env
OPENROUTER_DEFAULT_MODEL=openai/gpt-4o-mini
```

You can use any supported OpenRouter model.

</td>
</tr>
</table>

---

## ✦ Available Commands

### Start Wakeup Screen

```bash
byteclaw-build wakeup
```

### Run Directly With Bun

```bash
bun index.ts wakeup
```

### Link Globally

```bash
bun link --global
```

Then run:

```bash
byteclaw-build wakeup
```

---

## ✦ CLI Flow

```txt
byteclaw-build wakeup
        │
        ▼
┌───────────────────────┐
│   Wakeup Interface    │
│  Banner + Mode Select │
└───────────┬───────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
  CLI Mode   Telegram Mode
      │           │
      ▼           ▼
Ask / Plan / Agent   Telegram Commands
```

---

## ✦ How It Works

```txt
User Input
   ↓
CLI / Telegram Interface
   ↓
AI Model through OpenRouter
   ↓
Tool Loop Agent
   ↓
Codebase Tools + Web Tools
   ↓
Staged Actions
   ↓
User Approval
   ↓
Applied Changes
```

---

## ✦ Mode Examples

<table>
<tr>
<td width="33%">

### 🔎 Ask

```txt
Explain the project structure
```

```txt
Where is Telegram mode handled?
```

```txt
Find all files related to plan mode
```

</td>
<td width="33%">

### 🧭 Plan

```txt
Add Telegram webhook support
```

```txt
Improve CLI responsiveness
```

```txt
Create better env validation
```

</td>
<td width="33%">

### 🧠 Agent

```txt
Fix Telegram chat id error
```

```txt
Refactor wakeup UI
```

```txt
Improve error handling
```

</td>
</tr>
</table>

---

## ✦ Safety Workflow

ByteClaw does not directly apply agent-generated mutations without review.

```txt
Agent suggests changes
        ↓
Actions are staged
        ↓
User reviews operations
        ↓
User approves/rejects
        ↓
Approved changes are applied
```

---

## ✦ Telegram Commands

```txt
/ask
/agent
/plan
```

Examples:

```txt
/ask explain this project
```

```txt
/plan add webhook deployment
```

```txt
/agent improve Telegram error handling
```

---

## ✦ Main Dependencies

```json
{
  "@clack/core": "^1.4.0",
  "@clack/prompts": "^1.5.0",
  "@mendable/firecrawl-js": "^4.25.2",
  "@openrouter/ai-sdk-provider": "^2.9.0",
  "ai": "^6.0.196",
  "chalk": "^5.6.2",
  "commander": "^15.0.0",
  "diff": "^9.0.0",
  "figlet": "^1.11.0",
  "marked": "^18.0.4",
  "marked-terminal": "^7.3.0",
  "telegraf": "^4.16.3"
}
```

---

## ✦ Roadmap

* Better responsive terminal banner
* Telegram webhook deployment support
* Model selector from CLI
* Persistent session history
* Advanced diff preview
* Plugin-based tool system
* Web dashboard for sessions
* Multi-agent workflow
* Safer project-wide refactoring
* Configurable workspace root

---

## ✦ Author

<div align="center">

### Ujjwal Kumar Kannojiya

[![GitHub](https://img.shields.io/badge/GitHub-UjjwalKumarKannojiya-181717?style=for-the-badge\&logo=github)](https://github.com/UjjwalKumarKannojiya)

</div>

---

## ✦ Support

<div align="center">

If you like this project, consider giving it a star.

<br />

⭐ Star the repo   |   🍴 Fork it   |   🛠 Improve it   |   🚀 Build with it

</div>

---

<div align="center">

## ⚡ ByteClaw

### Your AI-powered codebase companion.

Built with Bun, TypeScript, OpenRouter, Telegram, and terminal energy.

</div>

