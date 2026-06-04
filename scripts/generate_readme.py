#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "readme_config.json"
ASSETS_DIR = ROOT / "assets"
SVG_PATH = ASSETS_DIR / "byteclaw-readme.svg"
README_PATH = ROOT / "README.md"

DEFAULT_CONFIG: Dict[str, Any] = {
    "project": {
        "name": "ByteClaw",
        "tagline": "AI-powered terminal and Telegram assistant",
        "headline": "for understanding, planning, and modifying codebases.",
        "description": "Run CLI workflows, ask questions about your project, generate implementation plans, and control coding tasks through Telegram.",
        "status": "built for dev productivity",
        "repo_url": "https://github.com/UjjwalKumarKannojiya/ByteClaw-",
        "author": "Ujjwal Kumar Kannojiya",
    },
    "badges": ["TypeScript", "Node.js", "Bun", "CLI", "Telegram Bot", "OpenRouter AI"],
    "features": [],
    "commands": [],
    "env": ["OPENROUTER_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "FIRECRAWL_API_KEY", "TAVILY_API_KEY"],
    "fallback_tech": ["TypeScript", "JavaScript", "Node.js", "Bun", "CLI", "Telegram Bot", "OpenRouter AI", "Markdown", "GitHub Actions"],
}

TECH_NORMALIZE = {
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "bun": "Bun",
    "tsx": "TSX",
    "react": "React",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "vite": "Vite",
    "tailwind": "TailwindCSS",
    "tailwindcss": "TailwindCSS",
    "telegram": "Telegram Bot",
    "telegraf": "Telegram Bot",
    "grammy": "Telegram Bot",
    "openai": "OpenAI SDK",
    "@openai/agents": "OpenAI Agents",
    "openrouter": "OpenRouter AI",
    "ai": "AI SDK",
    "zod": "Zod",
    "chalk": "Chalk",
    "figlet": "Figlet",
    "clack": "Clack Prompts",
    "@clack/prompts": "Clack Prompts",
    "commander": "Commander",
    "inquirer": "Inquirer",
    "dotenv": "Dotenv",
    "axios": "Axios",
    "firecrawl": "Firecrawl",
    "tavily": "Tavily",
    "markdown": "Markdown",
    "github actions": "GitHub Actions",
}

EXT_TECH = {
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".json": "JSON",
    ".md": "Markdown",
    ".yml": "GitHub Actions",
    ".yaml": "YAML",
}

PACKAGE_HINTS = {
    "@clack/prompts": "Clack Prompts",
    "chalk": "Chalk",
    "figlet": "Figlet",
    "telegraf": "Telegram Bot",
    "grammy": "Telegram Bot",
    "openai": "OpenAI SDK",
    "ai": "AI SDK",
    "zod": "Zod",
    "commander": "Commander",
    "inquirer": "Inquirer",
    "dotenv": "Dotenv",
    "axios": "Axios",
    "tsx": "TSX",
    "typescript": "TypeScript",
    "firecrawl": "Firecrawl",
    "@mendable/firecrawl-js": "Firecrawl",
}

EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", ".turbo", ".vercel"}


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def short(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def wrap_text(value: Any, limit: int, max_lines: int = 2) -> List[str]:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        return []
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        next_line = word if not current else f"{current} {word}"
        if len(next_line) <= limit:
            current = next_line
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) == max_lines - 1:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = short(lines[-1], max(8, limit - 1))
    return lines[:max_lines]


def slug_to_title(value: str) -> str:
    text = re.sub(r"[@_/.-]+", " ", value).strip()
    return " ".join(part.capitalize() for part in text.split())


def normalize_tech(name: str) -> str:
    raw = str(name or "").strip()
    if not raw:
        return ""
    key = raw.lower().strip()
    if key in TECH_NORMALIZE:
        return TECH_NORMALIZE[key]
    if key.startswith("@types/"):
        return "TypeScript"
    if key.startswith("@clack/"):
        return "Clack Prompts"
    if key.startswith("@telegram"):
        return "Telegram Bot"
    return PACKAGE_HINTS.get(raw, slug_to_title(raw))


def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        merged = dict(DEFAULT_CONFIG)
        merged.update(loaded)
        merged["project"] = {**DEFAULT_CONFIG["project"], **loaded.get("project", {})}
        return merged
    return DEFAULT_CONFIG


def read_package_tech() -> List[str]:
    package_path = ROOT / "package.json"
    if not package_path.exists():
        return []
    try:
        pkg = json.loads(package_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    found: List[str] = []
    if pkg.get("type") == "module":
        found.append("ES Modules")

    if pkg.get("bin"):
        found.append("CLI")

    scripts = " ".join(str(v).lower() for v in (pkg.get("scripts") or {}).values())
    if "bun" in scripts:
        found.append("Bun")
    if "tsx" in scripts:
        found.append("TSX")

    for field in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        for dep in (pkg.get(field) or {}).keys():
            found.append(normalize_tech(dep))

    return found


def scan_file_tech() -> List[str]:
    found: List[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        tech = EXT_TECH.get(path.suffix.lower())
        if tech:
            found.append(tech)
        name = path.name.lower()
        if name in {"bun.lock", "bun.lockb"}:
            found.append("Bun")
        if name.startswith("dockerfile"):
            found.append("Docker")
        if path.match(".github/workflows/*"):
            found.append("GitHub Actions")
    return found


def unique_ordered(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        clean = normalize_tech(item) if item else ""
        if not clean or clean.lower() in seen:
            continue
        seen.add(clean.lower())
        out.append(clean)
    return out


def detected_tech(config: Dict[str, Any]) -> List[str]:
    configured = config.get("badges", []) + config.get("fallback_tech", [])
    dynamic = read_package_tech() + scan_file_tech()
    result = unique_ordered(dynamic + configured)
    preferred = [
        "TypeScript", "JavaScript", "Node.js", "Bun", "CLI", "Telegram Bot", "OpenRouter AI",
        "OpenAI SDK", "Clack Prompts", "Chalk", "Figlet", "Zod", "Axios", "Firecrawl", "Markdown", "GitHub Actions",
    ]
    rank = {name: index for index, name in enumerate(preferred)}
    return sorted(result, key=lambda x: (rank.get(x, 999), x.lower()))[:18]


def pill(label: str, x: int, y: int, color: str, height: int = 26) -> Tuple[str, int]:
    width = max(66, len(label) * 7 + 26)
    return f'''
      <g transform="translate({x} {y})">
        <rect width="{width}" height="{height}" rx="{height // 2}" fill="{color}" fill-opacity="0.11" stroke="{color}" stroke-opacity="0.42"/>
        <text x="{width/2:.1f}" y="17" text-anchor="middle" class="pill" fill="{color}">{esc(label)}</text>
        <animateTransform attributeName="transform" type="translate" values="{x} {y};{x} {y-2};{x} {y}" dur="5s" repeatCount="indefinite" additive="replace"/>
      </g>''', width


def centered_pills(labels: List[str], start_y: int, max_width: int = 780, start_x: int = 60, gap: int = 8, row_gap: int = 34) -> str:
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#D29922", "#F85149", "#39C5CF"]
    rows: List[List[Tuple[str, int, str]]] = []
    row: List[Tuple[str, int, str]] = []
    row_w = 0
    for i, label in enumerate(labels):
        width = max(66, len(label) * 7 + 26)
        extra = width if not row else width + gap
        if row and row_w + extra > max_width:
            rows.append(row)
            row = []
            row_w = 0
            extra = width
        row.append((label, width, colors[i % len(colors)]))
        row_w += extra
    if row:
        rows.append(row)

    parts = []
    for r, items in enumerate(rows):
        total = sum(w for _, w, _ in items) + gap * (len(items) - 1)
        x = start_x + (max_width - total) // 2
        y = start_y + r * row_gap
        for label, width, color in items:
            item, _ = pill(label, x, y, color)
            parts.append(item)
            x += width + gap
    return "\n".join(parts)


def badges_svg(labels: List[str]) -> str:
    return centered_pills(labels[:6], start_y=182, max_width=720, start_x=90, gap=8, row_gap=32)


def section_title(title: str, y: int) -> str:
    return f'<text x="52" y="{y}" class="section">// {esc(title)}</text><line x1="52" y1="{y+16}" x2="848" y2="{y+16}" stroke="#30363D"/>'


def feature_cards_svg(features: List[Dict[str, Any]]) -> str:
    if not features:
        features = DEFAULT_CONFIG.get("features", [])
    cards = []
    card_w, card_h = 386, 128
    start_x, start_y = 52, 482
    gap_x, gap_y = 24, 20
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#F85149", "#D29922", "#39C5CF"]
    for i, feature in enumerate(features[:6]):
        col = i % 2
        row = i // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        color = colors[i % len(colors)]
        items = feature.get("items", [])[:4]
        lis = []
        for j, item in enumerate(items):
            yy = 60 + j * 18
            lis.append(f'<circle cx="22" cy="{yy-4}" r="2.8" fill="{color}"/><text x="34" y="{yy}" class="cardItem">{esc(short(item, 43))}</text>')
        cards.append(f'''
    <g transform="translate({x} {y})">
      <rect width="{card_w}" height="{card_h}" rx="12" fill="#161B22" stroke="#30363D"/>
      <rect x="0" y="0" width="{card_w}" height="3" rx="12" fill="{color}">
        <animate attributeName="opacity" values="0.45;1;0.45" dur="4.5s" begin="{i*0.2:.2f}s" repeatCount="indefinite"/>
      </rect>
      <circle cx="28" cy="26" r="7" fill="{color}" fill-opacity="0.18" stroke="{color}"/>
      <circle cx="28" cy="26" r="3" fill="{color}"/>
      <text x="48" y="32" class="cardTitle">{esc(feature.get('title', 'Feature'))}</text>
      {''.join(lis)}
      <animateTransform attributeName="transform" type="translate" values="{x} {y};{x} {y-2};{x} {y}" dur="6s" begin="{i*0.18:.2f}s" repeatCount="indefinite" additive="replace"/>
    </g>''')
    return "\n".join(cards)


def command_cards_svg(commands: List[Dict[str, str]]) -> str:
    parts = []
    x, y = 52, 1476
    card_w, card_h = 386, 84
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#D29922"]
    for i, c in enumerate(commands[:4]):
        col = i % 2
        row = i // 2
        xx = x + col * 410
        yy = y + row * 102
        cmd_lines = str(c.get("cmd", "")).splitlines()[:3]
        cmd_text = "".join(
            f'<text x="24" y="{50 + n*17}" class="cmdText">{esc(short(line, 42))}</text>' for n, line in enumerate(cmd_lines)
        )
        color = colors[i % len(colors)]
        parts.append(f'''
    <g transform="translate({xx} {yy})">
      <rect width="{card_w}" height="{card_h}" rx="11" fill="#161B22" stroke="#30363D"/>
      <circle cx="22" cy="23" r="6" fill="{color}"/>
      <text x="40" y="28" class="cardTitle">{esc(c.get('title', 'Step'))}</text>
      {cmd_text}
    </g>''')
    return "\n".join(parts)


def env_cards_svg(envs: List[str]) -> str:
    parts = []
    x, y = 52, 1748
    for i, name in enumerate(envs[:6]):
        col = i % 3
        row = i // 3
        xx = x + col * 274
        yy = y + row * 62
        parts.append(f'''
    <g transform="translate({xx} {yy})">
      <rect width="246" height="48" rx="9" fill="#161B22" stroke="#30363D"/>
      <text x="16" y="21" class="envKey">{esc(name)}</text>
      <text x="16" y="37" class="envHint">paste your key here</text>
    </g>''')
    return "\n".join(parts)


def project_structure_svg() -> str:
    lines = [
        "ByteClaw-/",
        "|- ai/",
        "|- modes/",
        "|  |- agent/",
        "|  |- ask/",
        "|  |- plan/",
        "|  `- telegram/",
        "|- tui/",
        "|- scripts/",
        "`- index.ts",
    ]
    return "".join(
        f'<text x="76" y="{1006 + i*18}" class="treeText">{esc(line)}</text>' for i, line in enumerate(lines)
    )


def workflow_svg() -> str:
    steps = ["Understand", "Ask / Plan", "Run Actions", "Review", "Telegram"]
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#D29922", "#F85149"]
    x, y = 76, 1250
    parts = []
    for i, step in enumerate(steps):
        width = max(88, len(step) * 8 + 28)
        parts.append(f'''
      <g transform="translate({x} {y})">
        <rect width="{width}" height="30" rx="7" fill="#0D1117" stroke="{colors[i]}" stroke-opacity="0.5"/>
        <text x="{width/2:.1f}" y="20" text-anchor="middle" class="monoSmall" fill="{colors[i]}">{esc(step)}</text>
      </g>''')
        if i < len(steps) - 1:
            parts.append(f'<path d="M{x+width+10} {y+15} H{x+width+34}" stroke="#30363D" stroke-width="2" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" values="0;-40" dur="2s" repeatCount="indefinite"/></path>')
        x += width + 42
    return "\n".join(parts)


def svg_document(config: Dict[str, Any]) -> str:
    project = config.get("project", {})
    techs = detected_tech(config)
    project_name = project.get("name", "ByteClaw")
    tagline = project.get("tagline", DEFAULT_CONFIG["project"]["tagline"])
    headline = project.get("headline", DEFAULT_CONFIG["project"]["headline"])
    description = project.get("description", DEFAULT_CONFIG["project"]["description"])
    status = project.get("status", "built for dev productivity")
    commands = config.get("commands") or DEFAULT_CONFIG.get("commands", [])
    envs = config.get("env") or DEFAULT_CONFIG.get("env", [])
    features = config.get("features") or []
    badges = config.get("badges") or techs[:6]
    desc_lines = wrap_text(description, 78, 2)
    desc_svg = "".join(f'<text x="450" y="{242 + i*20}" text-anchor="middle" class="desc">{esc(line)}</text>' for i, line in enumerate(desc_lines))

    return f'''<svg width="900" height="1940" viewBox="0 0 900 1940" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(project_name)} animated README interface">
  <defs>
    <linearGradient id="titleGrad" x1="230" y1="40" x2="670" y2="120" gradientUnits="userSpaceOnUse">
      <stop stop-color="#58A6FF"/>
      <stop offset="0.55" stop-color="#A371F7"/>
      <stop offset="1" stop-color="#39D353"/>
    </linearGradient>
    <radialGradient id="glowBlue" cx="50%" cy="50%" r="50%"><stop stop-color="#58A6FF" stop-opacity="0.18"/><stop offset="1" stop-color="#58A6FF" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowPurple" cx="50%" cy="50%" r="50%"><stop stop-color="#A371F7" stop-opacity="0.16"/><stop offset="1" stop-color="#A371F7" stop-opacity="0"/></radialGradient>
    <clipPath id="clip"><rect width="900" height="1940" rx="18"/></clipPath>
    <style>
      .title {{ font: 900 58px Inter, Segoe UI, Arial, sans-serif; letter-spacing: 5px; fill: url(#titleGrad); }}
      .subtitle {{ font: 700 17px Inter, Segoe UI, Arial, sans-serif; fill: #E6EDF3; }}
      .desc {{ font: 500 14px Inter, Segoe UI, Arial, sans-serif; fill: #8B949E; }}
      .section {{ font: 800 14px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #58A6FF; letter-spacing: 2px; }}
      .muted {{ font: 500 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8B949E; }}
      .pill {{ font: 800 11px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; letter-spacing: .25px; }}
      .cardTitle {{ font: 800 15px Inter, Segoe UI, Arial, sans-serif; fill: #E6EDF3; }}
      .cardItem {{ font: 500 12px Inter, Segoe UI, Arial, sans-serif; fill: #8B949E; }}
      .featureIcon {{ font: 900 17px Inter, Segoe UI, Arial, sans-serif; }}
      .treeText {{ font: 600 13px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #C9D1D9; }}
      .monoSmall {{ font: 800 11px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
      .cmdText {{ font: 700 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #C9D1D9; }}
      .envKey {{ font: 800 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #3FB950; }}
      .envHint {{ font: 500 10.5px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8B949E; }}
    </style>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="900" height="1940" rx="18" fill="#0D1117"/>
    <rect x="1" y="1" width="898" height="1938" rx="17" stroke="#30363D"/>

    <circle cx="96" cy="92" r="150" fill="url(#glowBlue)">
      <animate attributeName="cx" values="96;140;96" dur="9s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="92;126;92" dur="9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="806" cy="140" r="185" fill="url(#glowPurple)">
      <animate attributeName="cx" values="806;748;806" dur="11s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="140;98;140" dur="11s" repeatCount="indefinite"/>
    </circle>
    <path d="M190 100 C320 32 560 34 718 104" stroke="#58A6FF" stroke-width="1.4" stroke-dasharray="10 18" opacity="0.35">
      <animate attributeName="stroke-dashoffset" values="0;-320" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.18;0.48;0.18" dur="8s" repeatCount="indefinite"/>
    </path>

    <g>
      <rect x="32" y="32" width="836" height="286" rx="18" fill="#0F1623" stroke="#30363D"/>
      <g>
        <text x="450" y="112" text-anchor="middle" class="title">BYTECLAW</text>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="6s" repeatCount="indefinite"/>
      </g>
      <text x="450" y="148" text-anchor="middle" class="subtitle">{esc(tagline)}</text>
      <text x="450" y="172" text-anchor="middle" class="subtitle" fill="#58A6FF">{esc(headline)}</text>
      {badges_svg(badges)}
      {desc_svg}
      <rect x="338" y="278" width="224" height="28" rx="14" fill="#161B22" stroke="#3FB950" stroke-opacity="0.5"/>
      <circle cx="358" cy="292" r="4.5" fill="#3FB950"><animate attributeName="opacity" values="0.35;1;0.35" dur="1.4s" repeatCount="indefinite"/></circle>
      <text x="376" y="296" class="muted">{esc(status)}</text>
    </g>

    {section_title('WHAT IS ' + project_name.upper() + '?', 360)}
    <text x="60" y="404" class="desc"><tspan fill="#58A6FF" font-weight="800">{esc(project_name)}</tspan> combines terminal workflows, AI planning, project understanding, and Telegram control.</text>

    {section_title('FEATURES', 448)}
    {feature_cards_svg(features)}

    {section_title('PROJECT STRUCTURE', 950)}
    <rect x="52" y="978" width="386" height="194" rx="12" fill="#161B22" stroke="#30363D"/>
    {project_structure_svg()}
    <rect x="462" y="978" width="386" height="194" rx="12" fill="#161B22" stroke="#30363D"/>
    <text x="490" y="1016" class="cardTitle">Terminal-first experience</text>
    <text x="490" y="1046" class="cardItem">Designed for fast local workflows with clean prompts,</text>
    <text x="490" y="1066" class="cardItem">AI-powered planning, and remote Telegram control.</text>
    <rect x="490" y="1102" width="314" height="28" rx="6" fill="#0D1117" stroke="#30363D"/>
    <text x="508" y="1121" class="cmdText">$ byteclaw-build wakeup</text>

    {section_title('HOW IT WORKS', 1220)}
    {workflow_svg()}

    {section_title('TECH STACK', 1322)}
    {centered_pills(techs, start_y=1354, max_width=796, start_x=52, gap=8, row_gap=34)}

    {section_title('GETTING STARTED', 1446)}
    {command_cards_svg(commands)}

    {section_title('ENVIRONMENT VARIABLES', 1718)}
    {env_cards_svg(envs)}

    <line x1="52" y1="1888" x2="848" y2="1888" stroke="#30363D"/>
    <text x="450" y="1914" text-anchor="middle" class="muted">Built by {esc(project.get('author', 'Ujjwal'))}</text>
  </g>
</svg>'''


def readme_document(config: Dict[str, Any]) -> str:
    project = config.get("project", {})
    name = project.get("name", "ByteClaw")
    repo_url = project.get("repo_url", "https://github.com/UjjwalKumarKannojiya/ByteClaw-")
    return f'''<div align="center">

<img src="./assets/byteclaw-readme.svg" width="100%" alt="{esc(name)} animated README interface" />

</div>

## Quick Start

```bash
git clone {repo_url}.git
cd ByteClaw-
bun install
bun run dev
```

## CLI

```bash
byteclaw-build wakeup
```

## Environment Variables

Create a `.env` file and add the keys used by your setup:

```env
OPENROUTER_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
FIRECRAWL_API_KEY=
TAVILY_API_KEY=
```

---

<div align="center">
  <strong>Built for developers who want a clean AI workflow inside terminal + Telegram.</strong>
</div>
'''


def main() -> int:
    config = load_config()
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(svg_document(config), encoding="utf-8")
    README_PATH.write_text(readme_document(config), encoding="utf-8")
    print(f"Generated {SVG_PATH.relative_to(ROOT)} and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
