<div align="center">

```
██████╗ ██╗   ██╗████████╗███████╗ ██████╗██╗      █████╗ ██╗    ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔════╝██║     ██╔══██╗██║    ██║
██████╔╝ ╚████╔╝    ██║   █████╗  ██║     ██║     ███████║██║ █╗ ██║
██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██║     ██║     ██╔══██║██║███╗██║
██████╔╝   ██║      ██║   ███████╗╚██████╗███████╗██║  ██║╚███╔███╔╝
╚═════╝    ╚═╝      ╚═╝   ╚══════╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝
```

**A dual-mode AI-powered CLI & Telegram bot for intelligent web research and code assistance**

[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Bun](https://img.shields.io/badge/Bun-1.3.14-fbf0df?style=for-the-badge&logo=bun&logoColor=black)](https://bun.sh/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-AI-6c63ff?style=for-the-badge)](https://openrouter.ai/)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-Web%20Scraping-ff6b35?style=for-the-badge)](https://firecrawl.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🦅 What is ByteClaw?

**ByteClaw** is a powerful, dual-mode AI assistant that runs both as an interactive **terminal CLI** and a **Telegram bot**. It combines the power of large language models (via OpenRouter) with real-time web scraping (via Firecrawl) to deliver intelligent, context-aware responses right from your terminal or Telegram chat.

Whether you're a developer researching docs, debugging code, or someone who wants an AI assistant in Telegram — ByteClaw has you covered.

---

## ✨ Features

- 🖥️ **CLI Mode** — A rich, interactive terminal UI built with `@clack/prompts` and styled with `chalk` and `figlet` banners
- 🤖 **Telegram Bot Mode** — Deploy ByteClaw as a Telegram bot powered by `telegraf`, accessible from anywhere
- 🌐 **Web Research** — Scrapes and crawls web pages in real-time using Firecrawl, feeding live content to the AI
- 🧠 **AI Reasoning** — Routes queries through OpenRouter, giving access to the best LLMs (GPT-4o, Claude, Gemini, and more)
- 📝 **Markdown Rendering** — Renders beautifully formatted AI responses in the terminal using `marked` + `marked-terminal`
- 🎨 **Beautiful TUI** — Animated ASCII banners via `figlet`, colored output with `chalk`, and polished prompts via `@clack/core`
- 🔁 **Mode Switching** — On startup, pick between CLI mode or Telegram bot mode interactively
- ⚡ **Blazing Fast** — Runs on Bun for near-instant startup and execution

---

## 🗂️ Project Structure

```
ByteClaw-/
├── index.ts            # CLI entry point — registers commands via commander
├── tui/
│   └── wakeup.ts       # TUI startup: renders banner & prompts mode selection
├── ai/                 # AI integration logic (OpenRouter calls, streaming)
├── modes/              # CLI mode logic & Telegram bot mode logic
├── .env.example        # Environment variable template
├── package.json        # Dependencies and scripts
└── tsconfig.json       # TypeScript configuration
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **[Bun](https://bun.sh/)** | JavaScript runtime & package manager |
| **[TypeScript 5](https://www.typescriptlang.org/)** | Statically typed language |
| **[Commander.js](https://github.com/tj/commander.js/)** | CLI command parsing and routing |
| **[OpenRouter AI SDK](https://openrouter.ai/)** | Access to 100+ LLMs (GPT-4o, Claude, Gemini, etc.) |
| **[Vercel AI SDK](https://sdk.vercel.ai/)** | Streaming AI responses (`ai` package) |
| **[Firecrawl](https://firecrawl.dev/)** | Web scraping & crawling for real-time data |
| **[@clack/prompts](https://github.com/bombshell-dev/clack)** | Beautiful interactive terminal prompts |
| **[Chalk](https://github.com/chalk/chalk)** | Terminal string styling and colors |
| **[Figlet](https://github.com/patorjk/figlet.js)** | ASCII art text banners |
| **[Marked](https://marked.js.org/) + marked-terminal** | Markdown rendering in the terminal |
| **[Telegraf](https://telegraf.js.org/)** | Telegram Bot framework |
| **[Diff](https://github.com/kpdecker/jsdiff)** | Text diff utilities |

---

## 🚀 Getting Started

### Prerequisites

- **[Bun](https://bun.sh/)** v1.3.14 or higher
- An **[OpenRouter API Key](https://openrouter.ai/)** — for AI model access
- A **[Firecrawl API Key](https://firecrawl.dev/)** — for web scraping
- (Optional) A **Telegram Bot Token** — only needed for Telegram mode

---

### 1. Clone the Repository

```bash
git clone https://github.com/UjjwalKumarKannojiya/ByteClaw-.git
cd ByteClaw-
```

### 2. Install Dependencies

```bash
bun install
```

### 3. Configure Environment Variables

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Open `.env` and set the following:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_DEFAULT_MODEL=openai/gpt-4o        # or any model on OpenRouter
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Only required for Telegram mode:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

---

### 4. Run ByteClaw

```bash
bun run index.ts wakeup
```

On launch, ByteClaw displays its ASCII banner and prompts you to pick a mode:

- **CLI Mode** — Chat with the AI directly in your terminal
- **Telegram Mode** — Start the Telegram bot and control it from your phone

---

## 🧩 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                        ByteClaw Launch                      │
│              bun run index.ts wakeup                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
              ┌─────────────▼──────────────┐
              │  TUI Banner + Mode Select  │
              │  (tui/wakeup.ts)           │
              └──────┬──────────────┬──────┘
                     │              │
          ┌──────────▼──┐    ┌──────▼──────────┐
          │   CLI Mode  │    │  Telegram Mode  │
          │ (modes/cli) │    │ (modes/telegram)│
          └──────┬──────┘    └──────┬──────────┘
                 │                  │
         ┌───────▼──────────────────▼───────┐
         │          AI Layer (ai/)           │
         │   OpenRouter → LLM Model          │
         │   + Firecrawl (web research)      │
         └──────────────────────────────────┘
```

1. **Startup** — `index.ts` registers the `wakeup` command via Commander.js
2. **TUI** — `tui/wakeup.ts` renders the ASCII banner and shows the mode selector
3. **Mode Routing** — User picks CLI or Telegram; the corresponding mode module initializes
4. **AI Queries** — User input is sent to OpenRouter; if a URL/research query is detected, Firecrawl crawls the web first
5. **Response** — The AI response streams back and is rendered as formatted Markdown in the terminal (or sent as a Telegram message)

---

## 📦 Available Scripts

| Command | Description |
|---|---|
| `bun run index.ts wakeup` | Start ByteClaw and pick a mode |
| `bun install` | Install all dependencies |

---

## 🔑 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Yes | Your OpenRouter API key for LLM access |
| `OPENROUTER_DEFAULT_MODEL` | ✅ Yes | Model to use (e.g. `openai/gpt-4o`, `anthropic/claude-3-5-sonnet`) |
| `FIRECRAWL_API_KEY` | ✅ Yes | API key for Firecrawl web scraping |
| `TELEGRAM_BOT_TOKEN` | ⚡ Telegram only | Bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | ⚡ Telegram only | Chat ID to authorize for the bot |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 👤 Author

**Ujjwal Kumar Kannojiya**

- GitHub: [@UjjwalKumarKannojiya](https://github.com/UjjwalKumarKannojiya)

---

## ⭐ Show Your Support

If you found this project useful, please consider giving it a ⭐ on GitHub — it means a lot!

---

<div align="center">
  <sub>Built with ⚡ Bun + TypeScript + OpenRouter + Firecrawl</sub>
</div>
