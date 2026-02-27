from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from main import setup_agent

DATA_DIR = Path(__file__).resolve().parent / "data"
TRACKING_FILE = DATA_DIR / "mistake_tracking.json"


@dataclass
class SessionState:
    session_id: str
    current_topic: str = ""
    awaiting_quiz_answer: bool = False
    last_quiz: dict[str, Any] | None = None
    last_explanation: dict[str, Any] | None = None
    last_retrieval_context: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class LearningSystemState:
    agent_state: Any
    sessions: dict[str, SessionState] = field(default_factory=dict)
    tracking: dict[str, Any] = field(default_factory=dict)


def _safe_parse_payload(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (SyntaxError, ValueError):
            return {}


def _load_tracking() -> dict[str, Any]:
    if TRACKING_FILE.exists():
        try:
            data = json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return {"topics": {}, "recent": []}


def _save_tracking(tracking: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRACKING_FILE.write_text(json.dumps(tracking, indent=2), encoding="utf-8")


def init_learning_system() -> LearningSystemState:
    return LearningSystemState(agent_state=setup_agent(), tracking=_load_tracking())


def _get_session(state: LearningSystemState, session_id: str | None) -> SessionState:
    sid = session_id or str(uuid4())
    if sid not in state.sessions:
        state.sessions[sid] = SessionState(session_id=sid)
    return state.sessions[sid]


def _call_tool(state: LearningSystemState, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    result = state.agent_state.agent.execute_tool(tool_name, args)
    payload = _safe_parse_payload(result.get("result"))
    return {
        "tool_name": tool_name,
        "status": result.get("status", "error"),
        "payload": payload,
    }


def _normalize_topic(topic: str) -> str:
    cleaned = " ".join(topic.strip().lower().split())
    return cleaned or "general"


def _update_mistakes(state: LearningSystemState, topic: str, verdict: str, score: int, misses: list[str]) -> None:
    key = _normalize_topic(topic)
    topics = state.tracking.setdefault("topics", {})
    stat = topics.setdefault(key, {"attempts": 0, "incorrect": 0, "scores": [], "misses": {}})
    stat["attempts"] += 1
    stat["scores"].append(score)
    if verdict != "correct":
        stat["incorrect"] += 1
    for miss in misses:
        stat["misses"][miss] = stat["misses"].get(miss, 0) + 1

    recent = state.tracking.setdefault("recent", [])
    recent.append({"topic": key, "score": score, "verdict": verdict})
    state.tracking["recent"] = recent[-40:]
    _save_tracking(state.tracking)


def _analytics_snapshot(state: LearningSystemState) -> dict[str, Any]:
    topics = state.tracking.get("topics", {})
    rows = []
    for topic, stat in topics.items():
        attempts = max(1, int(stat.get("attempts", 0)))
        incorrect = int(stat.get("incorrect", 0))
        weak_ratio = incorrect / attempts
        rows.append(
            {
                "topic": topic,
                "attempts": attempts,
                "incorrect": incorrect,
                "error_frequency": round(weak_ratio, 2),
                "avg_score": round(sum(stat.get("scores", [])) / max(1, len(stat.get("scores", []))), 1),
            }
        )

    rows.sort(key=lambda r: (r["error_frequency"], r["incorrect"], -r["avg_score"]), reverse=True)
    weak_topics = [r["topic"] for r in rows[:3]]

    recommended_focus = weak_topics if weak_topics else ["recursion", "dynamic programming"]

    return {
        "weak_topics": rows[:8],
        "recommended_focus": recommended_focus,
    }


def _is_explain(message: str) -> bool:
    m = message.lower()
    return any(k in m for k in ["explain", "what is", "how does", "define"])


def _is_quiz_request(message: str) -> bool:
    m = message.lower()
    return any(k in m for k in ["quiz", "test me", "generate a quiz", "practice question"])


def _is_revision_request(message: str) -> bool:
    m = message.lower()
    return "revision plan" in m or ("plan" in m and "7" in m)


def _extract_topic(message: str, fallback: str = "") -> str:
    text = message.strip()
    if not text:
        return fallback or "general"

    generic_quiz_commands = {
        "quiz",
        "a quiz",
        "generate quiz",
        "generate a quiz",
        "create a quiz",
        "make a quiz",
        "give me a quiz",
        "test me",
        "practice question",
        "practice questions",
    }
    if " ".join(text.lower().split()) in generic_quiz_commands:
        return fallback or "general"

    prefixes = [
        "explain",
        "what is",
        "how does",
        "define",
        "quiz me on",
        "test me on",
        "quiz on",
        "generate a quiz on",
        "generate quiz on",
        "create a quiz on",
        "make a quiz on",
        "give me a quiz on",
        "quiz about",
        "generate a quiz about",
        "generate quiz about",
        "create a quiz about",
        "make a quiz about",
    ]
    for prefix in prefixes:
        if text.lower().startswith(prefix):
            text = text[len(prefix):].strip(" :?.,")
            break

    text = re.sub(r"^(on|about)\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwith\s+(one|an|a)\s+example\b.*$", "", text, flags=re.IGNORECASE).strip(" :?.,")

    normalized = " ".join(text.lower().split())
    if not normalized or normalized in generic_quiz_commands:
        return fallback or "general"
    return text


def _quiz_aspects_for_session(session: SessionState) -> list[str]:
    aspects: list[str] = []
    explanation = session.last_explanation or {}
    for key in ("definition", "intuition", "example"):
        if str(explanation.get(key, "")).strip():
            aspects.append(key)

    retrieval_context = (session.last_retrieval_context or "").strip().lower()
    if retrieval_context and "no relevant knowledge found" not in retrieval_context:
        aspects.append("application")

    # Always include implementation-oriented thinking to support coding-style quizzes.
    aspects.extend(["implementation", "edge cases"])

    deduped: list[str] = []
    seen: set[str] = set()
    for aspect in aspects:
        if aspect not in seen:
            seen.add(aspect)
            deduped.append(aspect)
    return deduped or ["definition", "implementation", "edge cases"]


def _dialogue_context(session: SessionState, max_turns: int = 4) -> str:
    recent = session.history[-max_turns:]
    if not recent:
        return ""

    snippets: list[str] = []
    seen: set[str] = set()
    for turn in recent:
        message = str(turn.get("message", "")).strip()
        if message and not (_is_quiz_request(message) or _is_revision_request(message)):
            normalized = " ".join(message.split())
            if normalized and normalized.lower() not in seen:
                seen.add(normalized.lower())
                snippets.append(normalized)

        response_excerpt = str(turn.get("response_excerpt", "")).strip()
        if response_excerpt:
            normalized_response = " ".join(response_excerpt.split())
            if normalized_response and normalized_response.lower() not in seen:
                seen.add(normalized_response.lower())
                snippets.append(normalized_response)

    return " | ".join(snippets)


def _dialogue_aspects(dialogue_text: str) -> list[str]:
    lowered = dialogue_text.lower()
    mapped: list[str] = []
    if any(k in lowered for k in ("compare", "versus", "vs", "trade-off", "tradeoff")):
        mapped.append("comparison")
    if any(k in lowered for k in ("complexity", "big-o", "time complexity", "space complexity")):
        mapped.append("complexity")
    if any(k in lowered for k in ("debug", "bug", "fix", "error")):
        mapped.append("debugging")
    if any(k in lowered for k in ("edge case", "corner case")):
        mapped.append("edge cases")
    if any(k in lowered for k in ("implement", "code", "pseudocode")):
        mapped.append("implementation")
    return mapped


def process_study_turn(
    state: LearningSystemState,
    message: str,
    session_id: str | None = None,
    on_event: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    session = _get_session(state, session_id)
    user_message = message.strip()

    def emit(event: dict[str, Any]) -> None:
        if on_event is not None:
            on_event(event)

    emit({"type": "meta", "session_id": session.session_id})
    if not user_message:
        emit({"type": "output", "chunk": "Please enter a question."})
        return {
            "session_id": session.session_id,
            "response": "Please enter a question.",
            "actions": [],
            "tools_called": [],
            "payloads": {},
            "analytics": _analytics_snapshot(state),
            "session": {
                "current_topic": session.current_topic,
                "awaiting_quiz_answer": session.awaiting_quiz_answer,
            },
        }

    actions: list[str] = []
    tools_called: list[str] = []
    payloads: dict[str, Any] = {}

    if session.awaiting_quiz_answer and not _is_quiz_request(user_message) and not _is_revision_request(user_message):
        quiz = session.last_quiz or {}
        topic = quiz.get("topic") or session.current_topic or "general"
        emit({"type": "status", "action": "Grading", "tool": "grading_tool", "phase": "start"})
        grade = _call_tool(
            state,
            "grading_tool",
            {
                "topic": topic,
                "student_answer": user_message,
                "expected_answer": quiz.get("answer", ""),
            },
        )
        tools_called.append("grading_tool")
        actions.append("Grading")
        emit({"type": "status", "action": "Grading", "tool": "grading_tool", "phase": "done"})
        payloads["grading"] = grade["payload"]

        emit({"type": "status", "action": "Mistake tracking", "phase": "start"})
        _update_mistakes(
            state,
            topic=payloads["grading"].get("topic", topic),
            verdict=payloads["grading"].get("verdict", "needs_improvement"),
            score=int(payloads["grading"].get("score", 0)),
            misses=list(payloads["grading"].get("missing_keywords", [])),
        )
        actions.append("Mistake tracking")
        emit({"type": "status", "action": "Mistake tracking", "phase": "done"})
        session.awaiting_quiz_answer = False

        response = (
            f"Score: {payloads['grading'].get('score', 0)}\n"
            f"Verdict: {payloads['grading'].get('verdict', 'needs_improvement')}\n"
            f"Feedback: {payloads['grading'].get('feedback', '')}"
        )
        for line in response.splitlines():
            emit({"type": "output", "chunk": f"{line}\n"})
    elif _is_revision_request(user_message):
        analytics = _analytics_snapshot(state)
        focus = analytics.get("recommended_focus", [session.current_topic or "recursion"])
        emit({"type": "status", "action": "Planner tool", "tool": "planner_tool", "phase": "start"})
        plan = _call_tool(state, "planner_tool", {"weak_topics_csv": ", ".join(focus), "days": 7})
        tools_called.append("planner_tool")
        actions.append("Planner tool")
        emit({"type": "status", "action": "Planner tool", "tool": "planner_tool", "phase": "done"})
        payloads["plan"] = plan["payload"]

        plan_list = payloads["plan"].get("plan")
        if not isinstance(plan_list, list) or not plan_list:
            plan_list = [{}]
        day1 = plan_list[0] if isinstance(plan_list[0], dict) else {}
        
        tasks_list = day1.get("tasks", [])
        if not isinstance(tasks_list, list):
            tasks_list = [str(tasks_list)]
        tasks = " | ".join(str(t) for t in tasks_list)
        response = (
            f"7-day revision plan ready.\n"
            f"Recommended focus: {', '.join(payloads['plan'].get('recommended_focus', []))}\n"
            f"Day 1: {day1.get('focus', '-')}: {tasks}"
        )
        for line in response.splitlines():
            emit({"type": "output", "chunk": f"{line}\n"})
    elif _is_quiz_request(user_message):
        topic = _extract_topic(user_message, fallback=session.current_topic)
        aspects = _quiz_aspects_for_session(session)
        dialogue_context = _dialogue_context(session)
        aspects.extend(_dialogue_aspects(dialogue_context))
        deduped_aspects: list[str] = []
        seen_aspects: set[str] = set()
        for aspect in aspects:
            if aspect not in seen_aspects:
                seen_aspects.add(aspect)
                deduped_aspects.append(aspect)
        explanation = session.last_explanation or {}
        reference_context = "\n".join(
            part
            for part in [
                dialogue_context,
                str(explanation.get("definition", "")).strip(),
                str(explanation.get("intuition", "")).strip(),
                str(explanation.get("example", "")).strip(),
                session.last_retrieval_context.strip(),
            ]
            if part
        )
        emit({"type": "status", "action": "Quiz tool", "tool": "quiz_tool", "phase": "start"})
        quiz = _call_tool(
            state,
            "quiz_tool",
            {
                "topic": topic,
                "difficulty": "easy",
                "quiz_style": "random",
                "aspects_csv": ", ".join(deduped_aspects),
                "reference_context": reference_context,
            },
        )
        tools_called.append("quiz_tool")
        actions.append("Quiz tool")
        emit({"type": "status", "action": "Quiz tool", "tool": "quiz_tool", "phase": "done"})
        payloads["quiz"] = quiz["payload"]

        session.current_topic = topic
        session.awaiting_quiz_answer = True
        session.last_quiz = {"topic": topic, **payloads["quiz"]}

        response = (
            f"Question: {payloads['quiz'].get('question', '')}\n"
            f"Hint: {payloads['quiz'].get('hint', '')}\n"
            f"Reply with your answer and I will grade it."
        )
        for line in response.splitlines():
            emit({"type": "output", "chunk": f"{line}\n"})
    else:
        topic = _extract_topic(user_message)
        emit({"type": "status", "action": "Retrieval", "tool": "rag_search_tool", "phase": "start"})
        retrieval = _call_tool(state, "rag_search_tool", {"query": user_message, "top_k": 3})
        emit({"type": "status", "action": "Retrieval", "tool": "rag_search_tool", "phase": "done"})
        emit({"type": "status", "action": "Explanation", "tool": "explanation_tool", "phase": "start"})
        explanation = _call_tool(state, "explanation_tool", {"topic": topic, "level": "beginner"})
        emit({"type": "status", "action": "Explanation", "tool": "explanation_tool", "phase": "done"})
        tools_called.extend(["rag_search_tool", "explanation_tool"])
        actions.extend(["Retrieval", "Explanation"])
        payloads["retrieval"] = retrieval["payload"]
        payloads["explanation"] = explanation["payload"]

        session.current_topic = topic
        session.last_explanation = payloads["explanation"]
        session.last_retrieval_context = str(payloads["retrieval"].get("context", ""))
        response = (
            f"Definition: {payloads['explanation'].get('definition', '')}\n"
            f"Intuition: {payloads['explanation'].get('intuition', '')}\n"
            f"Example: {payloads['explanation'].get('example', '')}\n\n"
            f"Retrieved context: {payloads['retrieval'].get('context', '')}"
        )
        emit({"type": "output", "chunk": f"Definition: {payloads['explanation'].get('definition', '')}\n"})
        emit({"type": "output", "chunk": f"Intuition: {payloads['explanation'].get('intuition', '')}\n"})
        emit({"type": "output", "chunk": f"Example: {payloads['explanation'].get('example', '')}\n\n"})
        emit({"type": "output", "chunk": f"Retrieved context: {payloads['retrieval'].get('context', '')}"})

    analytics = _analytics_snapshot(state)

    record = {
        "message": user_message,
        "actions": actions,
        "tools_called": tools_called,
        "response_excerpt": " ".join(response.split())[:280],
    }
    session.history.append(record)

    final_result = {
        "session_id": session.session_id,
        "response": response,
        "actions": actions,
        "tools_called": tools_called,
        "payloads": payloads,
        "analytics": analytics,
        "session": {
            "current_topic": session.current_topic,
            "awaiting_quiz_answer": session.awaiting_quiz_answer,
        },
    }
    emit({"type": "final", "result": final_result})
    return final_result


def get_analytics(state: LearningSystemState) -> dict[str, Any]:
    return _analytics_snapshot(state)
