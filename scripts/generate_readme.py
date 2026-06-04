#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
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
        "repo_url": "https://github.com/UjjwalKumarKannojiya/ByteClaw",
        "author": "Ujjwal Kumar Kannojiya",
    },
    "badges": ["TypeScript", "Node.js", "CLI", "Telegram Bot", "OpenRouter AI", "Web Tools"],
    "features": [],
    "commands": [],
    "env": ["OPENROUTER_API_KEY", "TELEGRAM_BOT_TOKEN", "FIRECRAWL_API_KEY", "TAVILY_API_KEY"],
    "fallback_tech": ["TypeScript", "JavaScript", "Node.js", "Bun", "Telegram Bot", "OpenRouter AI", "CLI", "Markdown", "GitHub Actions"],
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
    # Keep clean framework/library names instead of huge scoped package names.
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

    bin_value = pkg.get("bin")
    if bin_value:
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
        "OpenAI SDK", "Clack Prompts", "Chalk", "Figlet", "Zod", "Axios", "Markdown", "GitHub Actions",
    ]
    rank = {name: index for index, name in enumerate(preferred)}
    return sorted(result, key=lambda x: (rank.get(x, 999), x.lower()))[:18]


def pill(label: str, x: int, y: int, color: str) -> Tuple[str, int]:
    width = max(70, len(label) * 8 + 28)
    return f'''
      <g transform="translate({x} {y})">
        <rect width="{width}" height="28" rx="14" fill="{color}" fill-opacity="0.11" stroke="{color}" stroke-opacity="0.42"/>
        <text x="{width/2:.1f}" y="18" text-anchor="middle" class="pill" fill="{color}">{esc(label)}</text>
        <animateTransform attributeName="transform" type="translate" values="{x} {y};{x} {y-2};{x} {y}" dur="5s" repeatCount="indefinite" additive="replace"/>
      </g>''', width


def flow_badge(text: str, x: int, y: int, color: str) -> Tuple[str, int]:
    width = max(92, len(text) * 8 + 30)
    return f'''
      <g transform="translate({x} {y})">
        <rect width="{width}" height="30" rx="7" fill="#0D1117" stroke="{color}" stroke-opacity="0.5"/>
        <text x="{width/2:.1f}" y="20" text-anchor="middle" class="monoSmall" fill="{color}">{esc(text)}</text>
      </g>''', width


def tech_pills_svg(techs: List[str]) -> str:
    palette = ["#58A6FF", "#A371F7", "#3FB950", "#D29922", "#F85149", "#39C5CF"]
    x, y = 56, 1238
    parts = []
    for i, label in enumerate(techs):
        item, width = pill(label, x, y, palette[i % len(palette)])
        if x + width > 944:
            x = 56
            y += 40
            item, width = pill(label, x, y, palette[i % len(palette)])
        parts.append(item)
        x += width + 10
    return "\n".join(parts)


def badges_svg(labels: List[str]) -> str:
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#F85149", "#D29922", "#39C5CF"]
    x, y = 245, 178
    parts = []
    for i, label in enumerate(labels[:7]):
        item, width = pill(label, x, y, colors[i % len(colors)])
        parts.append(item)
        x += width + 10
    return "\n".join(parts)


def feature_cards_svg(features: List[Dict[str, Any]]) -> str:
    if not features:
        features = DEFAULT_CONFIG.get("features", [])
    cards = []
    card_w, card_h = 286, 156
    start_x, start_y = 56, 472
    gap_x, gap_y = 22, 22
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#F85149", "#D29922", "#39C5CF"]
    for i, feature in enumerate(features[:6]):
        col = i % 3
        row = i // 3
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        color = colors[i % len(colors)]
        items = feature.get("items", [])[:4]
        lis = []
        for j, item in enumerate(items):
            yy = 72 + j * 20
            lis.append(f'<circle cx="22" cy="{yy-4}" r="2.8" fill="{color}"/><text x="34" y="{yy}" class="cardItem">{esc(short(item, 32))}</text>')
        cards.append(f'''
    <g transform="translate({x} {y})">
      <rect width="{card_w}" height="{card_h}" rx="12" fill="#161B22" stroke="#30363D"/>
      <rect x="0" y="0" width="{card_w}" height="3" rx="12" fill="{color}">
        <animate attributeName="opacity" values="0.45;1;0.45" dur="4.5s" begin="{i*0.25:.2f}s" repeatCount="indefinite"/>
      </rect>
      <text x="20" y="34" class="featureIcon" fill="{color}">{esc(feature.get('icon', '✦'))}</text>
      <text x="48" y="34" class="cardTitle">{esc(feature.get('title', 'Feature'))}</text>
      {''.join(lis)}
      <animateTransform attributeName="transform" type="translate" values="{x} {y};{x} {y-3};{x} {y}" dur="6s" begin="{i*0.18:.2f}s" repeatCount="indefinite" additive="replace"/>
    </g>''')
    return "\n".join(cards)


def command_cards_svg(commands: List[Dict[str, str]]) -> str:
    parts = []
    x, y = 56, 1442
    card_w, card_h = 434, 92
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#D29922"]
    for i, c in enumerate(commands[:4]):
        col = i % 2
        row = i // 2
        xx = x + col * 454
        yy = y + row * 112
        cmd_lines = str(c.get("cmd", "")).splitlines()[:3]
        cmd_text = "".join(
            f'<text x="24" y="{52 + n*18}" class="cmdText">{esc(line)}</text>' for n, line in enumerate(cmd_lines)
        )
        color = colors[i % len(colors)]
        parts.append(f'''
    <g transform="translate({xx} {yy})">
      <rect width="{card_w}" height="{card_h}" rx="11" fill="#161B22" stroke="#30363D"/>
      <circle cx="22" cy="24" r="6" fill="{color}"/>
      <text x="40" y="29" class="cardTitle">{esc(c.get('title', 'Step'))}</text>
      {cmd_text}
    </g>''')
    return "\n".join(parts)


def env_cards_svg(envs: List[str]) -> str:
    parts = []
    x, y = 56, 1712
    for i, name in enumerate(envs[:6]):
        col = i % 3
        row = i // 3
        xx = x + col * 308
        yy = y + row * 72
        parts.append(f'''
    <g transform="translate({xx} {yy})">
      <rect width="286" height="54" rx="9" fill="#161B22" stroke="#30363D"/>
      <text x="18" y="23" class="envKey">{esc(name)}</text>
      <text x="18" y="40" class="envHint">paste your key here</text>
    </g>''')
    return "\n".join(parts)


def project_structure_svg() -> str:
    lines = [
        "ByteClaw/",
        "├─ src/",
        "│  ├─ modes/",
        "│  │  ├─ cli.ts",
        "│  │  └─ telegram.ts",
        "│  ├─ agents/",
        "│  ├─ tools/",
        "│  └─ index.ts",
        "├─ scripts/",
        "├─ package.json",
        "└─ README.md",
    ]
    return "".join(
        f'<text x="82" y="{878 + i*20}" class="treeText">{esc(line)}</text>' for i, line in enumerate(lines)
    )


def workflow_svg() -> str:
    steps = ["Understand Repo", "Ask / Plan", "Run Actions", "CLI / Telegram", "Review"]
    colors = ["#58A6FF", "#A371F7", "#3FB950", "#D29922", "#F85149"]
    x, y = 56, 1132
    parts = []
    for i, step in enumerate(steps):
        item, width = flow_badge(step, x, y, colors[i])
        parts.append(item)
        if i < len(steps) - 1:
            parts.append(f'<path d="M{x+width+10} {y+15} H{x+width+40}" stroke="#30363D" stroke-width="2" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" values="0;-40" dur="2s" repeatCount="indefinite"/></path>')
        x += width + 46
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

    return f'''<svg width="1000" height="1860" viewBox="0 0 1000 1860" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(project_name)} animated README interface">
  <defs>
    <linearGradient id="titleGrad" x1="250" y1="40" x2="760" y2="120" gradientUnits="userSpaceOnUse">
      <stop stop-color="#58A6FF"/>
      <stop offset="0.55" stop-color="#A371F7"/>
      <stop offset="1" stop-color="#39D353"/>
    </linearGradient>
    <radialGradient id="glowBlue" cx="50%" cy="50%" r="50%"><stop stop-color="#58A6FF" stop-opacity="0.18"/><stop offset="1" stop-color="#58A6FF" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowPurple" cx="50%" cy="50%" r="50%"><stop stop-color="#A371F7" stop-opacity="0.16"/><stop offset="1" stop-color="#A371F7" stop-opacity="0"/></radialGradient>
    <filter id="softShadow"><feDropShadow dx="0" dy="12" stdDeviation="18" flood-color="#000000" flood-opacity="0.45"/></filter>
    <clipPath id="clip"><rect width="1000" height="1860" rx="18"/></clipPath>
    <style>
      .title {{ font: 900 72px Inter, Segoe UI, Arial, sans-serif; letter-spacing: 8px; fill: #E6EDF3; }}
      .subtitle {{ font: 600 18px Inter, Segoe UI, Arial, sans-serif; fill: #E6EDF3; }}
      .desc {{ font: 500 15px Inter, Segoe UI, Arial, sans-serif; fill: #8B949E; }}
      .section {{ font: 800 15px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #58A6FF; letter-spacing: 2.4px; }}
      .muted {{ font: 500 13px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8B949E; }}
      .pill {{ font: 800 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; letter-spacing: .3px; }}
      .cardTitle {{ font: 800 16px Inter, Segoe UI, Arial, sans-serif; fill: #E6EDF3; }}
      .cardItem {{ font: 500 13px Inter, Segoe UI, Arial, sans-serif; fill: #8B949E; }}
      .featureIcon {{ font: 900 18px Inter, Segoe UI, Arial, sans-serif; }}
      .treeText {{ font: 600 14px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #C9D1D9; }}
      .monoSmall {{ font: 800 12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
      .cmdText {{ font: 700 13px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #C9D1D9; }}
      .envKey {{ font: 800 13px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #3FB950; }}
      .envHint {{ font: 500 11px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8B949E; }}
    </style>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1000" height="1860" rx="18" fill="#0D1117"/>
    <rect x="1" y="1" width="998" height="1858" rx="17" stroke="#30363D"/>

    <circle cx="120" cy="100" r="180" fill="url(#glowBlue)">
      <animate attributeName="cx" values="120;170;120" dur="9s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="100;135;100" dur="9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="890" cy="170" r="220" fill="url(#glowPurple)">
      <animate attributeName="cx" values="890;820;890" dur="11s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="170;115;170" dur="11s" repeatCount="indefinite"/>
    </circle>
    <path d="M210 105 C360 28 625 30 800 110" stroke="#58A6FF" stroke-width="1.5" stroke-dasharray="10 18" opacity="0.35">
      <animate attributeName="stroke-dashoffset" values="0;-320" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.18;0.48;0.18" dur="8s" repeatCount="indefinite"/>
    </path>

    <g>
      <rect x="56" y="42" width="888" height="274" rx="18" fill="#0F1623" stroke="#30363D"/>
      <g transform="translate(0 0)">
        <text x="500" y="118" text-anchor="middle" class="title"><tspan fill="#58A6FF">BYTE</tspan><tspan fill="#E6EDF3">CLAW</tspan></text>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="6s" repeatCount="indefinite"/>
      </g>
      <text x="500" y="154" text-anchor="middle" class="subtitle">{esc(tagline)} <tspan fill="#58A6FF">{esc(headline)}</tspan></text>
      <text x="500" y="220" text-anchor="middle" class="desc">{esc(short(description, 105))}</text>
      {badges_svg(badges)}
      <rect x="410" y="258" width="180" height="34" rx="17" fill="#161B22" stroke="#3FB950" stroke-opacity="0.5"/>
      <circle cx="430" cy="275" r="5" fill="#3FB950"><animate attributeName="opacity" values="0.35;1;0.35" dur="1.4s" repeatCount="indefinite"/></circle>
      <text x="450" y="280" class="muted">{esc(status)}</text>
    </g>

    <text x="56" y="360" class="section">✦ WHAT IS {esc(project_name.upper())}?</text>
    <rect x="56" y="378" width="888" height="2" fill="#30363D"/>
    <text x="64" y="410" class="desc"><tspan fill="#58A6FF" font-weight="800">{esc(project_name)}</tspan> is a developer assistant that combines terminal workflows, AI planning, local project understanding, and Telegram control.</text>

    <text x="56" y="446" class="section">✦ FEATURES</text>

    {feature_cards_svg(features)}

    <text x="56" y="830" class="section">✦ PROJECT STRUCTURE</text>
    <rect x="56" y="850" width="432" height="164" rx="12" fill="#161B22" stroke="#30363D"/>
    {project_structure_svg()}
    <rect x="512" y="850" width="432" height="164" rx="12" fill="#161B22" stroke="#30363D"/>
    <text x="540" y="886" class="cardTitle">Terminal-first experience</text>
    <text x="540" y="916" class="cardItem">Designed for fast local workflows with clean prompts,</text>
    <text x="540" y="938" class="cardItem">AI-powered planning, and remote Telegram control.</text>
    <rect x="540" y="964" width="350" height="26" rx="6" fill="#0D1117" stroke="#30363D"/>
    <text x="558" y="982" class="cmdText">$ byteclaw-build wakeup</text>

    <text x="56" y="1108" class="section">✦ HOW IT WORKS</text>
    {workflow_svg()}

    <text x="56" y="1214" class="section">✦ TECH STACK</text>
    {tech_pills_svg(techs)}

    <text x="56" y="1418" class="section">✦ GETTING STARTED</text>
    {command_cards_svg(commands)}

    <text x="56" y="1688" class="section">✦ ENVIRONMENT VARIABLES</text>
    {env_cards_svg(envs)}

    <line x1="56" y1="1824" x2="944" y2="1824" stroke="#30363D"/>
    <text x="500" y="1844" text-anchor="middle" class="muted">Built with ✦ by {esc(project.get('author', 'Ujjwal'))}</text>
  </g>
</svg>'''


def readme_document(config: Dict[str, Any]) -> str:
    project = config.get("project", {})
    name = project.get("name", "ByteClaw")
    repo_url = project.get("repo_url", "#")
    return f'''<div align="center">

<img src="./assets/byteclaw-readme.svg" width="100%" alt="{esc(name)} animated README interface" />

</div>

## Quick Start

```bash
git clone {repo_url}.git
cd {name}
npm install
npm run dev
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
