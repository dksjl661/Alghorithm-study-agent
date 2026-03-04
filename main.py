#!/usr/bin/env python3
"""Study Copilot Agent with multi-tool routing and local RAG."""

from __future__ import annotations

import ast
import json
import os
import random
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

try:
    from openonion import Agent  # type: ignore
except ImportError:
    from connectonion import Agent  # type: ignore

from connectonion import after_each_tool, before_each_tool, on_complete, on_error
from connectonion.useful_plugins import re_act
import yaml

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "logs/agent_iter1.log"
TRACE_LOG_PATH = BASE_DIR / "logs/agent_iter1_trace.log"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
RETRIEVAL_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "define",
    "does",
    "example",
    "explain",
    "for",
    "from",
    "give",
    "how",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "one",
    "please",
    "tell",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}
QUIZ_STYLES = ("coding", "explaining", "scenario", "comparison", "debugging")
DEFAULT_QUIZ_ASPECTS = ("definition", "intuition", "example", "implementation", "edge cases")


def tool(func: Callable[..., Any]) -> Callable[..., Any]:
    """Compatibility tool decorator for Iteration 1 style registration."""
    return func


@tool
def explanation_tool(topic: str, level: str = "beginner") -> dict:
    """Explain a topic with definition, intuition, and example."""
    print("🔥 explanation_tool CALLED")
    topic = topic.strip()
    level = (level or "beginner").strip().lower()

    if level == "advanced":
        definition = f"{topic} is a concept analyzed at formal depth, with focus on underlying mechanisms."
        intuition = "Think in terms of structure, invariants, and trade-offs rather than surface behavior."
        example = f"In algorithms, analyzing {topic} means proving correctness and complexity bounds."
    elif level == "intermediate":
        definition = f"{topic} is a concept used to solve practical problems with clear rules and patterns."
        intuition = "Treat it like a reusable pattern: recognize when it applies and when it does not."
        example = f"When studying {topic}, map each step to a concrete input/output transformation."
    else:
        lower_topic = topic.lower()
        definition = f"{topic} is the basic idea behind how something works."
        intuition = f"Imagine explaining {topic} to a friend using plain language and one simple mental model."
        if "linked list" in lower_topic:
            example = (
                "Example linked list: 1 -> 2 -> 3. "
                "Each node stores a value and a pointer to the next node. "
                "To insert 0 at the head, create node 0 and point it to node 1."
            )
        elif "merge sort" in lower_topic:
            example = "Split the list into halves, sort each half recursively, then merge the sorted halves."
        else:
            example = f"For {topic}, start with a tiny input, apply one rule at a time, then verify the output."

    return {
        "definition": definition,
        "intuition": intuition,
        "example": example,
    }


@tool
def summarize_tool(text: str) -> dict:
    """Summarize input text with key points."""
    print("🔥 summarize_tool CALLED")
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("text must be a non-empty string")

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
    if not sentences:
        sentences = [cleaned]

    summary = " ".join(sentences[:2])[:320]
    key_points = []
    for sentence in sentences[:3]:
        bullet = sentence[:120]
        if bullet and bullet not in key_points:
            key_points.append(bullet)

    return {
        "summary": summary,
        "key_points": key_points,
    }


@tool
def quiz_tool(
    topic: str,
    difficulty: str = "easy",
    quiz_style: str = "random",
    aspects_csv: str = "",
    reference_context: str = "",
) -> dict:
    """Generate one quiz question with random style and multi-aspect coverage."""
    print("🔥 quiz_tool CALLED")
    topic = topic.strip()
    difficulty = (difficulty or "easy").strip().lower()
    quiz_style = (quiz_style or "random").strip().lower()

    if not topic:
        raise ValueError("topic must be a non-empty string")

    if quiz_style == "random" or quiz_style not in QUIZ_STYLES:
        style = random.choice(QUIZ_STYLES)
    else:
        style = quiz_style

    raw_aspects = [a.strip().lower() for a in (aspects_csv or "").split(",") if a.strip()]
    seen: set[str] = set()
    aspects: list[str] = []
    for aspect in raw_aspects:
        if aspect not in seen:
            seen.add(aspect)
            aspects.append(aspect)
    if not aspects:
        aspects = list(DEFAULT_QUIZ_ASPECTS)

    if style == "coding":
        question = (
            f"[{difficulty}/{style}] Write short pseudocode for {topic}. "
            f"Explain why it works and where it can fail."
        )
    elif style == "explaining":
        question = (
            f"[{difficulty}/{style}] Explain {topic} to a beginner using plain language, "
            f"then give one concrete example."
        )
    elif style == "scenario":
        question = (
            f"[{difficulty}/{style}] You are solving a real problem. Decide whether to use {topic}, "
            f"and justify your choice."
        )
    elif style == "comparison":
        question = (
            f"[{difficulty}/{style}] Compare {topic} with a related approach and describe when each one is better."
        )
    else:
        question = (
            f"[{difficulty}/{style}] A student solution for {topic} gives wrong output on some inputs. "
            f"Find a likely bug and describe a fix."
        )

    aspects_text = ", ".join(aspects)
    hint = f"Focus aspects: {aspects_text}."
    compact_context = " ".join(reference_context.split())
    if compact_context:
        hint += f" Reuse prior dialogue context: {compact_context[:420]}"

    answer = (
        f"A strong answer should be specific to {topic} and cover these aspects: {aspects_text}. "
        f"It should include a clear method, a concrete example, and how to avoid common mistakes or edge cases."
    )

    return {
        "question": question,
        "hint": hint,
        "answer": answer,
    }


@tool
def grading_tool(topic: str, student_answer: str, expected_answer: str) -> dict:
    """Grade a student answer and highlight likely mistakes."""
    print("🔥 grading_tool CALLED")
    topic = topic.strip()
    student_answer = student_answer.strip()
    expected_answer = expected_answer.strip()
    if not topic or not student_answer:
        raise ValueError("topic and student_answer must be non-empty")

    expected_tokens = _tokenize(expected_answer) if expected_answer else set()
    answer_tokens = _tokenize(student_answer)
    overlap = len(expected_tokens.intersection(answer_tokens)) if expected_tokens else 0
    baseline = max(1, len(expected_tokens) // 3) if expected_tokens else 1
    score = min(100, int((overlap / baseline) * 100))
    verdict = "correct" if score >= 60 else "needs_improvement"

    missing = sorted(list(expected_tokens.difference(answer_tokens)))[:8] if expected_tokens else []
    feedback = (
        f"Good progress on {topic}. Strengthen core terminology and concrete usage examples."
        if verdict == "needs_improvement"
        else f"Solid understanding of {topic}. Keep practicing concise explanations."
    )

    return {
        "topic": topic,
        "score": score,
        "verdict": verdict,
        "feedback": feedback,
        "missing_keywords": missing,
    }


@tool
def planner_tool(weak_topics_csv: str, days: int = 7) -> dict:
    """Create a revision plan that prioritizes weak topics."""
    print("🔥 planner_tool CALLED")
    topics = [t.strip() for t in weak_topics_csv.split(",") if t.strip()]
    if not topics:
        topics = ["recursion", "dynamic programming"]

    days = max(1, min(days, 14))
    plan = []
    for day in range(1, days + 1):
        focus = topics[(day - 1) % len(topics)]
        plan.append(
            {
                "day": day,
                "focus": focus,
                "tasks": [
                    f"Review notes for {focus} (20 min)",
                    f"Solve 3 practice questions on {focus}",
                    f"Write a 5-line self-explanation of {focus}",
                ],
            }
        )

    return {
        "days": days,
        "recommended_focus": topics[:3],
        "plan": plan,
    }


def _tokenize(text: str, *, drop_stopwords: bool = False) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    if not drop_stopwords:
        return tokens
    return {token for token in tokens if len(token) > 2 and token not in RETRIEVAL_STOPWORDS}


def _chunk_text(text: str) -> list[str]:
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not normalized:
        return []

    paragraphs = [p.strip() for p in normalized.split("\n\n") if p.strip()]
    raw_chunks: list[str] = []

    for paragraph in paragraphs:
        if len(paragraph) <= CHUNK_SIZE:
            raw_chunks.append(paragraph)
            continue

        start = 0
        while start < len(paragraph):
            end = start + CHUNK_SIZE
            chunk = paragraph[start:end].strip()
            if chunk:
                raw_chunks.append(chunk)
            if end >= len(paragraph):
                break
            start = max(end - CHUNK_OVERLAP, start + 1)

    return raw_chunks


def _knowledge_chunks() -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    if not KNOWLEDGE_DIR.exists():
        return chunks

    for path in sorted(KNOWLEDGE_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for chunk in _chunk_text(text):
            chunks.append({
                "source": str(path),
                "text": chunk,
                "tokens": _tokenize(chunk, drop_stopwords=True),
            })

    return chunks


def _score_chunk(query_tokens: set[str], chunk_tokens: set[str]) -> float:
    if not query_tokens or not chunk_tokens:
        return 0.0
    overlap = len(query_tokens.intersection(chunk_tokens))
    if overlap == 0:
        return 0.0
    return overlap / (len(query_tokens) ** 0.5 * len(chunk_tokens) ** 0.5)


def _retrieve_context(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    query_tokens = _tokenize(query, drop_stopwords=True)
    if not query_tokens:
        return []

    min_overlap = 1 if len(query_tokens) <= 1 else 2
    ranked: list[dict[str, Any]] = []

    for chunk in _knowledge_chunks():
        overlap = len(query_tokens.intersection(chunk["tokens"]))
        if overlap < min_overlap:
            continue

        score = _score_chunk(query_tokens, chunk["tokens"])
        if score > 0:
            ranked.append({
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            })

    ranked.sort(key=lambda c: c["score"], reverse=True)
    return ranked[: max(1, top_k)]


@tool
def rag_search_tool(query: str, top_k: int = 3) -> dict:
    """Retrieve relevant local context from the knowledge base."""
    print("🔥 rag_search_tool CALLED")
    query = query.strip()
    if not query:
        raise ValueError("query must be a non-empty string")

    retrieved = _retrieve_context(query=query, top_k=top_k)
    if not retrieved:
        return {
            "query": query,
            "context": "No relevant knowledge found in local knowledge base.",
            "sources": [],
        }

    snippets = [
        f"[{idx + 1}] {item['text'][:260]} (source: {Path(item['source']).name})"
        for idx, item in enumerate(retrieved)
    ]

    return {
        "query": query,
        "context": "\n".join(snippets),
        "sources": [item["source"] for item in retrieved],
    }


def _extract_topic_from_prompt(user_input: str) -> str:
    topic = user_input.strip()
    patterns = [
        r"^explain\s+",
        r"^what\s+is\s+",
        r"^define\s+",
        r"^quiz\s+me\s+on\s+",
        r"^test\s+me\s+on\s+",
    ]
    for pattern in patterns:
        topic = re.sub(pattern, "", topic, flags=re.IGNORECASE).strip()
    topic = re.sub(r"\bwith\s+(one|an|a)\s+example\b.*$", "", topic, flags=re.IGNORECASE).strip(" :?.,")
    return topic or user_input.strip()


def route_tool_for_input(user_input: str) -> tuple[str, dict[str, Any]]:
    """Select a fallback tool route when LLM does not call tools."""
    text = user_input.strip()
    lowered = text.lower()

    if any(k in lowered for k in ["quiz", "test me", "practice question"]):
        return "quiz_tool", {"topic": _extract_topic_from_prompt(text), "difficulty": "easy"}

    if any(k in lowered for k in ["summarize", "summary", "tldr", "tl;dr"]):
        summary_text = text.split(":", 1)[1].strip() if ":" in text else text
        return "summarize_tool", {"text": summary_text}

    if any(k in lowered for k in ["notes", "docs", "document", "knowledge", "according to", "from my file"]):
        return "rag_search_tool", {"query": text, "top_k": 3}

    return "explanation_tool", {"topic": _extract_topic_from_prompt(text), "level": "beginner"}


@dataclass
class AgentState:
    agent: Any
    before_tool_count: int = 0
    after_tool_count: int = 0
    tool_history: list[dict[str, Any]] = field(default_factory=list)
    last_fallback: dict[str, str] | None = None

    def run(self, user_input: str) -> str:
        return self.agent.input(user_input)


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def _write_structured_log(tool_name: str, execution_time_ms: int, status: str) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_name": tool_name,
        "execution_time_ms": int(execution_time_ms),
        "status": status,
    }
    _append_jsonl(LOG_PATH, event)


def _write_trace_event(
    event_type: str,
    tool_name: str,
    execution_time_ms: int,
    status: str,
    **extra: Any,
) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "tool_name": tool_name,
        "execution_time_ms": int(execution_time_ms),
        "status": status,
    }
    event.update(extra)
    _append_jsonl(TRACE_LOG_PATH, event)


def setup_agent() -> AgentState:
    """Instantiate the study copilot agent with hooks and tool orchestration."""
    load_dotenv()

    state = AgentState(agent=None)

    required_arg_by_tool = {
        "explanation_tool": "topic",
        "summarize_tool": "text",
        "quiz_tool": "topic",
        "rag_search_tool": "query",
        "grading_tool": "topic",
        "planner_tool": "weak_topics_csv",
    }

    def validate_input(runtime_agent: Any) -> None:
        state.before_tool_count += 1
        pending = runtime_agent.current_session.get("pending_tool", {})
        tool_name = pending.get("name", "unknown_tool")
        arguments = pending.get("arguments", {}) or {}
        print(f"[before_tool] {tool_name} iteration={runtime_agent.current_session.get('iteration', 0)}")
        _write_trace_event(
            event_type="before_tool",
            tool_name=tool_name,
            execution_time_ms=0,
            status="success",
            arguments=arguments,
            iteration=runtime_agent.current_session.get("iteration", 0),
        )

        required_arg = required_arg_by_tool.get(tool_name)
        if required_arg:
            value = str(arguments.get(required_arg, "")).strip()
            if not value:
                raise ValueError(f"{required_arg} must be a non-empty string")

    def log_tool_result(runtime_agent: Any) -> None:
        state.after_tool_count += 1
        trace = runtime_agent.current_session.get("trace", [])
        if not trace:
            return

        tool_results = [t for t in trace if t.get("type") == "tool_result"]
        if not tool_results:
            return

        last = tool_results[-1]
        state.tool_history.append(
            {
                "tool_name": last.get("name", "unknown_tool"),
                "arguments": last.get("args", {}),
                "result": last.get("result"),
                "status": last.get("status", "error"),
                "execution_time_ms": int(last.get("timing_ms") or 0),
            }
        )

        _write_structured_log(
            tool_name=last.get("name", "unknown_tool"),
            execution_time_ms=int(last.get("timing_ms") or 0),
            status=last.get("status", "error"),
        )
        _write_trace_event(
            event_type="tool_execution",
            tool_name=last.get("name", "unknown_tool"),
            execution_time_ms=int(last.get("timing_ms") or 0),
            status=last.get("status", "error"),
            arguments=last.get("args", {}),
            iteration=runtime_agent.current_session.get("iteration", 0),
        )
        _write_trace_event(
            event_type="after_tool",
            tool_name=last.get("name", "unknown_tool"),
            execution_time_ms=int(last.get("timing_ms") or 0),
            status=last.get("status", "error"),
            iteration=runtime_agent.current_session.get("iteration", 0),
        )
        print(
            f"[tool_execution] {last.get('name', 'unknown_tool')} "
            f"({int(last.get('timing_ms') or 0)}ms) status={last.get('status', 'error')}"
        )
        print(f"[after_tool] {last.get('name', 'unknown_tool')}")

    def handle_error(runtime_agent: Any) -> dict:
        fallback = {
            "definition": "Error occurred",
            "intuition": "The request could not be processed safely. Try a clearer topic.",
            "example": "Example fallback: Explain recursion to a beginner.",
        }
        state.last_fallback = fallback

        trace = runtime_agent.current_session.get("trace", [])
        if trace:
            last_tool = next((t for t in reversed(trace) if t.get("type") == "tool_result"), None)
            if last_tool is not None:
                _write_structured_log(
                    tool_name=last_tool.get("name", "unknown_tool"),
                    execution_time_ms=int(last_tool.get("timing_ms") or 0),
                    status="error",
                )
                _write_trace_event(
                    event_type="on_error",
                    tool_name=last_tool.get("name", "unknown_tool"),
                    execution_time_ms=int(last_tool.get("timing_ms") or 0),
                    status="error",
                    iteration=runtime_agent.current_session.get("iteration", 0),
                    error=last_tool.get("error"),
                )
                print(f"[on_error] {last_tool.get('name', 'unknown_tool')} error={last_tool.get('error')}")

        return fallback

    def ensure_tools_for_eval(runtime_agent: Any) -> None:
        """Guarantee at least one tool_result exists before logger writes YAML."""
        session = runtime_agent.current_session or {}
        trace = session.get("trace", [])
        tool_results = [t for t in trace if t.get("type") == "tool_result"]
        if tool_results:
            session["reason"] = session.get("reason", "tool_called_by_llm")
            session["evaluation"] = session.get("evaluation", session["reason"])
            return

        prompt = str(session.get("user_prompt", "")).strip()
        if not prompt:
            session["reason"] = "empty_prompt"
            session["evaluation"] = "empty_prompt"
            return

        fallback_tool_name, fallback_args = route_tool_for_input(prompt)
        forced = runtime_agent.execute_tool(fallback_tool_name, fallback_args)
        session["reason"] = f"forced_tool_execution:{fallback_tool_name}"
        session["evaluation"] = session["reason"]
        _write_trace_event(
            event_type="forced_tool_execution",
            tool_name=fallback_tool_name,
            execution_time_ms=int(forced.get("timing_ms") or 0),
            status=forced.get("status", "error"),
            reason="llm_direct_completion_detected",
        )
        print(f"[forced_tool_execution] {fallback_tool_name}")

    events = [
        before_each_tool(validate_input),
        after_each_tool(log_tool_result),
        on_error(handle_error),
        on_complete(ensure_tools_for_eval),
    ]

    agent = Agent(
        name="study-copilot-iter1",
        tools=[explanation_tool, summarize_tool, quiz_tool, rag_search_tool, grading_tool, planner_tool],
        system_prompt=BASE_DIR / "prompts/system_iter1.md",
        model=os.getenv("MODEL", "co/o4-mini"),
        max_iterations=3,
        log=True,
        plugins=[re_act],
        on_events=events,
    )
    state.agent = agent

    # Patch eval YAML writer to persist a top-level `reason` per turn.
    original_log_turn = agent.logger.log_turn

    def log_turn_with_reason(user_input: str, result: str, duration_ms: float, session: dict, model: str) -> None:
        original_log_turn(user_input, result, duration_ms, session, model)
        eval_file = getattr(agent.logger, "eval_file", None)
        if not eval_file or not Path(eval_file).exists():
            return
        reason = session.get("reason")
        if not reason:
            return

        data = yaml.safe_load(Path(eval_file).read_text(encoding="utf-8")) or {}
        turns = data.get("turns", [])
        turn_index = max(0, int(session.get("turn", 1)) - 1)
        if turn_index < len(turns):
            turns[turn_index]["reason"] = reason
            Path(eval_file).write_text(
                yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )

    agent.logger.log_turn = log_turn_with_reason

    state._validate_input = validate_input  # type: ignore[attr-defined]
    state._log_tool_result = log_tool_result  # type: ignore[attr-defined]
    state._handle_error = handle_error  # type: ignore[attr-defined]
    state._ensure_tools_for_eval = ensure_tools_for_eval  # type: ignore[attr-defined]

    return state


def _parse_tool_payload(raw: Any) -> dict[str, Any] | None:
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return None

    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(raw)
            return parsed if isinstance(parsed, dict) else None
        except (ValueError, SyntaxError):
            return None


def _format_structured_answer(structured: dict[str, Any]) -> str:
    if all(k in structured for k in ("definition", "intuition", "example")):
        return (
            f"Definition: {structured['definition']}\n"
            f"Intuition: {structured['intuition']}\n"
            f"Example: {structured['example']}"
        )

    if all(k in structured for k in ("summary", "key_points")):
        key_points = structured.get("key_points", [])
        bullet_text = "\n".join(f"- {point}" for point in key_points)
        return f"Summary: {structured['summary']}\nKey points:\n{bullet_text}".strip()

    if all(k in structured for k in ("question", "hint", "answer")):
        return (
            f"Question: {structured['question']}\n"
            f"Hint: {structured['hint']}\n"
            f"Answer: {structured['answer']}"
        )

    if all(k in structured for k in ("query", "context", "sources")):
        sources = structured.get("sources", [])
        source_text = "\n".join(f"- {src}" for src in sources) if sources else "- none"
        return (
            f"RAG Context for: {structured['query']}\n"
            f"{structured['context']}\n"
            f"Sources:\n{source_text}"
        )

    if all(k in structured for k in ("topic", "score", "verdict", "feedback")):
        missing = structured.get("missing_keywords", [])
        missing_text = ", ".join(missing) if missing else "none"
        return (
            f"Topic: {structured['topic']}\n"
            f"Score: {structured['score']}\n"
            f"Verdict: {structured['verdict']}\n"
            f"Feedback: {structured['feedback']}\n"
            f"Missing Keywords: {missing_text}"
        )

    if all(k in structured for k in ("days", "recommended_focus", "plan")):
        focus = ", ".join(structured.get("recommended_focus", []))
        day_one = structured["plan"][0] if structured.get("plan") else {"focus": "-", "tasks": []}
        tasks = "; ".join(day_one.get("tasks", []))
        return (
            f"Revision Days: {structured['days']}\n"
            f"Recommended Focus: {focus}\n"
            f"Day 1 Focus: {day_one.get('focus')}\n"
            f"Day 1 Tasks: {tasks}"
        )

    return json.dumps(structured)


def run_prompt(agent_state: AgentState, user_input: str) -> dict[str, Any]:
    """Execute one user prompt and return structured payload."""
    _write_trace_event(
        event_type="agent_start",
        tool_name="agent",
        execution_time_ms=0,
        status="success",
        prompt=user_input,
    )
    if not user_input or not user_input.strip():
        fallback = {
            "definition": "Error occurred",
            "intuition": "Please provide a non-empty request.",
            "example": "Try: Explain merge sort to a beginner.",
        }
        result = {
            "final_answer": _format_structured_answer(fallback),
            "loop_count": 0,
            "tool_history": [],
        }
        _write_trace_event(
            event_type="agent_end",
            tool_name="agent",
            execution_time_ms=0,
            status="error",
            loop_count=0,
            reason="empty_input",
        )
        print("[agent_end] loop_count=0 reason=empty_input")
        return result

    final_answer = agent_state.run(user_input)
    trace = agent_state.agent.current_session.get("trace", []) if agent_state.agent.current_session else []

    tool_results = [t for t in trace if t.get("type") == "tool_result"]
    loop_count = len(tool_results)

    if loop_count == 0:
        fallback_tool_name, fallback_args = route_tool_for_input(user_input)
        forced = agent_state.agent.execute_tool(fallback_tool_name, fallback_args)
        if agent_state.agent.current_session is not None:
            agent_state.agent.current_session["reason"] = f"forced_tool_execution:{fallback_tool_name}"
            agent_state.agent.current_session["evaluation"] = agent_state.agent.current_session["reason"]
        _write_trace_event(
            event_type="forced_tool_execution",
            tool_name=fallback_tool_name,
            execution_time_ms=int(forced.get("timing_ms") or 0),
            status=forced.get("status", "error"),
            reason="llm_direct_completion_detected",
        )
        print(f"[forced_tool_execution] {fallback_tool_name}")
        trace = agent_state.agent.current_session.get("trace", []) if agent_state.agent.current_session else []
        tool_results = [t for t in trace if t.get("type") == "tool_result"]
        loop_count = len(tool_results)

    structured = None
    if tool_results:
        structured = _parse_tool_payload(tool_results[-1].get("result"))

    if structured:
        final_answer = _format_structured_answer(structured)
    elif agent_state.last_fallback:
        final_answer = _format_structured_answer(agent_state.last_fallback)

    result = {
        "final_answer": str(final_answer),
        "loop_count": loop_count,
        "tool_history": getattr(agent_state, "tool_history", []),
    }
    _write_trace_event(
        event_type="agent_end",
        tool_name="agent",
        execution_time_ms=0,
        status="success",
        loop_count=loop_count,
    )
    print(f"[agent_end] loop_count={loop_count}")
    return result


def _print_cli_response(result: dict[str, Any]) -> None:
    answer = result.get("final_answer", "")
    loop_count = result.get("loop_count", 0)

    print(answer)
    print(f"Loop count: {loop_count}")


def main() -> None:
    agent_state = setup_agent()

    print("Study Copilot Agent (Multi-Tool + RAG)")
    print("Type 'quit' to exit.")

    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_input.strip().lower() in {"quit", "exit", "q"}:
            print("Exiting.")
            break

        result = run_prompt(agent_state, user_input)
        _print_cli_response(result)


if __name__ == "__main__":
    main()
