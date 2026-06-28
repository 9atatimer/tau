---
title: The interactive session
description: Get fluent in Tau's terminal UI — prompting, steering, the command palette, tool output, and pickers.
---

Running `tau` with no arguments opens the interactive terminal UI (TUI). This is
where most work happens. This guide covers the moving parts; for the exact keys
see [Keyboard shortcuts](../reference/keybindings.md).

## Sending a prompt

Type into the prompt box at the bottom and press **Enter** to submit.
**Shift+Enter** inserts a newline for multi-line prompts. Tau streams the
assistant's reply above the prompt, showing tool calls as they run.

Clicking anywhere in the window returns focus to the prompt, so you can scroll
the transcript and keep typing without tabbing back.

## Cancelling and steering a run

While the agent is working you don't have to wait:

- **Esc** cancels the active run. Cancellation is treated as an intentional stop,
  not an error.
- **Enter** (while running) queues your text as **steering** — extra guidance
  applied to the current run.
- **Alt+Enter** queues a **follow-up** — a prompt that waits until the current
  run would otherwise finish.
- Press **Up** on an empty prompt while running to pull the most recently queued
  follow-up back into the prompt for editing.

## The command palette and slash commands

In-session commands start with `/`. Open the **command palette** with **Ctrl+K**
to search and run them. Common ones:

- `/session` — show model, tools, skills, and context usage for the session
- `/model` — pick the active model
- `/compact` — summarize and shrink the context
- `/resume`, `/tree` — open previous sessions or branch from history
- `/hotkeys` — show the keyboard shortcuts

The full list is in the [Slash commands reference](../reference/slash-commands.md).

## Running shell commands directly

You can run a shell command yourself without asking the model:

- `!<command>` runs it in the session's working directory **and** records the
  command and output in the conversation context.
- `!!<command>` runs it and shows the output **without** adding it to context.

While typing a path after `!`/`!!`, press **Tab** to complete filenames from the
working directory.

## Referencing files with `@`

Type `@` in the prompt to open file suggestions from the project tree, and insert
a path like `@src/app.py`. Tau skips hidden and generated directories (`.git`,
`.venv`, `node_modules`, `__pycache__`, `build`, `dist`).

## Tool output

Tool results (like long `read` or `bash` output) render as compact previews so
the transcript stays readable. Toggle full tool output with **Ctrl+O**.

## Picking models and themes

- **`/model`** opens the model picker. Selecting a model from another provider
  switches the active provider too.
- **Ctrl+P** quickly cycles through your *scoped* (favorite) models without
  opening the picker. Manage that list with `/scoped-models` or by pressing
  `Space` on a model in the `/model` picker.
- **`/theme`** switches between `tau-dark`, `tau-light`, and `high-contrast`.

## The sidebar

On wide-enough terminals Tau shows a sidebar with the active provider/model,
thinking mode, loaded tools, skills, prompt templates, and context files such as
`AGENTS.md`. It hides automatically when the terminal is small.

## Next

- [Sessions](./sessions.md) — resume, branch, rename, export.
- [Providers & models](./providers-and-models.md) — switch and add models.
- [Managing context](./context.md) — compaction and thinking modes.
