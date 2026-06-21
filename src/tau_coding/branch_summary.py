"""Model-assisted summaries for abandoned session-tree branches."""

import json
from collections.abc import Sequence

from tau_agent.messages import AgentMessage, AssistantMessage, ToolResultMessage, UserMessage
from tau_ai import ModelProvider, ProviderErrorEvent, ProviderResponseEndEvent

BRANCH_SUMMARY_SYSTEM_PROMPT = (
    "You summarize abandoned coding-agent conversation branches for context replay. "
    "Write a concise, factual summary that preserves user intent, decisions, file paths, "
    "commands, errors, and unfinished tasks. Return only the summary."
)

MAX_SUMMARY_SOURCE_MESSAGE_CHARS = 4_000
MAX_SUMMARY_SOURCE_TOTAL_CHARS = 60_000


async def summarize_branch_messages_with_model(
    *,
    provider: ModelProvider,
    model: str,
    messages: Sequence[AgentMessage],
) -> str | None:
    """Return a model-generated branch summary, or None when generation fails."""
    if not messages:
        return None

    response: AssistantMessage | None = None
    async for event in provider.stream_response(
        model=model,
        system=BRANCH_SUMMARY_SYSTEM_PROMPT,
        messages=[UserMessage(content=_branch_summary_prompt(messages))],
        tools=[],
    ):
        if isinstance(event, ProviderErrorEvent):
            return None
        if isinstance(event, ProviderResponseEndEvent):
            response = event.message

    if response is None:
        return None
    summary = response.content.strip()
    return summary or None


def _branch_summary_prompt(messages: Sequence[AgentMessage]) -> str:
    lines = [
        "Summarize the abandoned branch below for future context replay.",
        "Keep it concise but include details needed to continue from the selected branch point.",
        "Do not include a preamble.",
        "",
        "Abandoned branch transcript:",
    ]
    remaining_chars = MAX_SUMMARY_SOURCE_TOTAL_CHARS
    omitted_count = 0

    for index, message in enumerate(messages, start=1):
        rendered = f"{index}. {_format_summary_source_message(message)}"
        if len(rendered) > remaining_chars:
            omitted_count = len(messages) - index + 1
            break
        lines.append(rendered)
        remaining_chars -= len(rendered)

    if omitted_count:
        lines.append(f"... {omitted_count} message(s) omitted because the branch was too long.")

    return "\n".join(lines)


def _format_summary_source_message(message: AgentMessage) -> str:
    match message:
        case UserMessage():
            return f"user:\n{_trim_summary_source_text(message.content)}"
        case AssistantMessage():
            return _format_assistant_summary_source(message)
        case ToolResultMessage():
            status = "ok" if message.ok else "failed"
            return f"tool {message.name} ({status}):\n{_trim_summary_source_text(message.content)}"


def _format_assistant_summary_source(message: AssistantMessage) -> str:
    lines = [f"assistant:\n{_trim_summary_source_text(message.content)}"]
    if message.tool_calls:
        calls = [
            f"{call.name}({json.dumps(call.arguments, sort_keys=True)})"
            for call in message.tool_calls
        ]
        lines.append(f"tool calls: {', '.join(calls)}")
    return "\n".join(lines)


def _trim_summary_source_text(text: str) -> str:
    normalized = text.strip() or "(empty)"
    if len(normalized) <= MAX_SUMMARY_SOURCE_MESSAGE_CHARS:
        return normalized
    return normalized[: MAX_SUMMARY_SOURCE_MESSAGE_CHARS - 3].rstrip() + "..."
