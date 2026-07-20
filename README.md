# 🖥️ Windows Agent

> **An autonomous AI agent that controls your entire Windows desktop through natural language — powered entirely by a local LLM.**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)
![Architecture](https://img.shields.io/badge/Architecture-Agentic-orange)
![LLM](https://img.shields.io/badge/LLM-Qwen3%2014B-purple)
![Runtime](https://img.shields.io/badge/Ollama-Local-green)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Overview

**Windows Agent** is an autonomous AI system that operates your Windows desktop the way a human assistant would.

Instead of manually opening applications, browsing websites, creating files, or repeating tedious workflows, you describe the goal in plain language — the agent reasons about it, builds a plan, executes real actions, observes what actually happened, reflects on its progress, recovers from failures, and keeps iterating until the objective is done.

This isn't a chatbot that talks about tasks — it's a closed-loop agent that **does** them.

> **You describe the goal. The agent figures out the steps.**

---

## ✨ What It Can Do

```
"Open Google and search for LangGraph."
"Create a file on my Desktop and write my notes into it."
"Check if I have internet connectivity."
"Rename this file and read it back to me."
"Organize my Downloads folder."
```

The agent decides which tools to use, in what order, and adapts on the fly when something doesn't go as expected.

---

## 🧠 Powered by Local AI

Windows Agent runs **100% locally** via **Ollama** — no cloud calls, no API keys, no data leaving your machine.

```python
provider = "ollama"
model_name = "qwen3:14b"
```

| Benefit | Description |
|---|---|
| 🔒 Privacy First | Nothing leaves your machine |
| 💸 No API Cost | Fully free to run |
| 📴 Offline Capable | Works without internet once models are pulled |
| 🔁 Model-Agnostic | Swap in any Ollama-compatible model |
| ⚙️ No Cloud Dependency | You own the whole stack |

---

## 🏗️ Architecture

The agent runs a continuous reasoning loop, not a single-shot prompt/response:

```
                     User Goal
                         │
                         ▼
             Conversation Manager
                         │
                         ▼
                     Reasoner  ──────► strategy, long-term context
                         │
                         ▼
                     Planner   ──────► next action, tool, arguments
                         │
                         ▼
                     Executor  ──────► runs the chosen tool
                         │
                         ▼
                      Tools    ──────► Browser / File / Network / ...
                         │
                         ▼
                     Observer  ──────► what actually happened
                         │
                         ▼
                   World State ──────► persistent facts learned
                         │
                         ▼
                    Reflection ──────► progress? stuck? done?
                         │
                         ▼
                     Recovery  ──────► retry / replan / fallback / abort
                         │
                         ▼
              Repeat until goal completed
```

---

## 🧩 Core Components

| Component | Responsibility |
|---|---|
| **Conversation Manager** | Maintains user conversation and context across iterations |
| **Reasoner** | Strategic brain — understands the objective, tracks assumptions, learns from failures, guides the Planner |
| **Planner** | Tactical brain — picks the next tool, action, and arguments; predicts expected outcomes |
| **Executor** | Runs the chosen tool and captures structured execution results |
| **Observer** | Determines what *actually* happened vs. what was expected, and extracts new facts |
| **World State** | Persistent knowledge — current directory, browser URL, created files, network status, etc. |
| **Reflection** | Judges progress, detects failure or stagnation, decides if replanning is needed |
| **Recovery** | Chooses a strategy: continue, retry, replan, fallback tool, or abort |

Each node has a single, clearly scoped responsibility — this is what keeps the architecture extensible as new tools and capabilities are added.

---

## 🛠 Current Tools

- **Browser Tool** — navigation, search, page interaction
- **File Tool** — create, read, write, rename, delete files
- **Network Tool** — connectivity checks, public IP lookup
- **Tool Registry** — schema-driven tool discovery for the Planner
- **Executor Framework** — uniform execution + result capture across all tools

More tools are added continuously as the framework matures.

---

## 📁 Project Structure

```
src/
├── conversation/     # conversation history & context
├── reasoner/         # strategic reasoning node
├── planner/          # tactical planning node
├── executor/         # action execution
├── observer/         # outcome analysis
├── reflection/       # progress evaluation
├── recovery/         # failure recovery strategies
├── runtime/          # the pipeline that wires it all together
├── state/            # AgentState and sub-state schemas
├── world/            # world-state model
├── tools/            # browser / file / network / ... tools
├── prompts/          # per-node prompt builders
├── utils/
└── config/
```

---

## 💻 Example Tasks

**Browser Automation** — open sites, search the web, navigate pages, fill forms, extract information

**File Management** — create, read, write, rename, delete files; organize folders

**Desktop Automation** — launch applications, run workflows, automate repetitive tasks

**Planned** — email automation, calendar management, office document editing, coding assistance, research automation, full personal desktop assistant

---

## 🎯 Design Principles

- Modular architecture with strict separation of responsibilities
- Goal-oriented reasoning, not single-shot prompting
- Structured, typed agent state throughout the pipeline
- Extensible tool system with schema-driven discovery
- Failure-aware execution with dedicated recovery logic
- Production-oriented design from the start

---

## 📊 Current Status

**✅ Core autonomous agent architecture is complete and operational.**

Implemented and working end-to-end:

- Conversation Manager · Reasoner · Planner · Executor · Observer · Reflection · Recovery
- Full Runtime Pipeline with structured Agent State and World State
- Tool Registry with multi-tool dispatch

The agent successfully runs multi-iteration workflows: reasoning about a goal, planning an action, executing it, observing the real outcome, reflecting on progress, and recovering intelligently when something fails.

---

## 🚧 Currently Working On

The reasoning/planning/reflection loop is solid — the current bottleneck is the **tool layer** itself. We're hardening it so tools can absorb and recover from common execution failures (bad locators, brittle paths, transient timeouts) internally, instead of pushing every failure back up to the agent for replanning.

Focus areas right now:

- Intelligent Browser Tool (locator fallback chains, session/state ownership, retry policies)
- Robust File Tool (path/env-var resolution, permission handling, verification)
- Error classification (recoverable vs. non-recoverable)
- Action verification after execution
- Cross-platform abstractions

**Next up after that:** persistent conversation memory and long-term memory, so the agent can remember previous sessions, learn from past executions, and get more capable over time.

---

## 🧠 Future Roadmap

- Persistent conversation memory · long-term / episodic / semantic memory
- Memory-based planning and learning from past executions
- Multi-agent collaboration
- Vision capabilities
- Voice interaction
- Plugin ecosystem
- Cross-platform support (Linux & macOS)

---

## 🤝 Contributing

Contributions, ideas, bug reports, and feature requests are welcome — feel free to open an issue or submit a pull request.

---

## 🌟 Long-Term Vision

Windows Agent aims to become a fully autonomous desktop AI assistant — one that understands complex goals, reasons through problems, interacts with the operating system, learns from experience, and keeps improving over time.

Rather than just responding to prompts, it's built to **think, plan, execute, observe, recover, and eventually remember** — closing the gap toward a true autonomous desktop agent.
