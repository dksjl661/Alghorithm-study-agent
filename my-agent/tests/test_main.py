from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import sys
import json

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import (
    explanation_tool,
    rag_search_tool,
    route_tool_for_input,
    setup_agent,
    summarize_tool,
    quiz_tool,
    run_prompt,
)


def test_explanation_tool_returns_valid_schema() -> None:
    result = explanation_tool("recursion")

    assert isinstance(result, dict)
    assert set(result.keys()) == {"definition", "intuition", "example"}
    assert all(isinstance(result[k], str) and result[k].strip() for k in result)


def test_summary_tool_returns_valid_schema() -> None:
    result = summarize_tool("Merge sort uses divide and conquer to sort lists efficiently.")
    assert set(result.keys()) == {"summary", "key_points"}
    assert isinstance(result["summary"], str) and result["summary"].strip()
    assert isinstance(result["key_points"], list)


def test_quiz_tool_returns_valid_schema() -> None:
    result = quiz_tool("binary search")
    assert set(result.keys()) == {"question", "hint", "answer"}
    assert all(isinstance(result[k], str) and result[k].strip() for k in result)


def test_quiz_tool_random_mode_selects_style() -> None:
    result = quiz_tool("binary search", difficulty="medium")

    lowered_question = result["question"].lower()
    assert "[medium/" in lowered_question
    assert any(
        style in lowered_question for style in ("coding", "explaining", "scenario", "comparison", "debugging")
    )
    assert "binary search" in lowered_question


def test_quiz_tool_uses_multi_aspects_for_question_content() -> None:
    result = quiz_tool(
        "graph traversal",
        difficulty="hard",
        quiz_style="coding",
        aspects_csv="implementation, complexity, edge cases",
    )

    lowered_question = result["question"].lower()
    lowered_hint = result["hint"].lower()
    lowered_answer = result["answer"].lower()

    assert "[hard/coding]" in lowered_question
    assert "graph traversal" in lowered_question
    assert "implementation" in lowered_hint
    assert "complexity" in lowered_hint
    assert "edge cases" in lowered_answer


def test_explanation_tool_example_should_follow_topic_not_hardcoded() -> None:
    result = explanation_tool("linked list")
    assert "linked list" in result["example"].lower()
    assert "merge sort" not in result["example"].lower()


def test_route_tool_for_input_selects_different_tools() -> None:
    assert route_tool_for_input("Explain recursion")[0] == "explanation_tool"
    assert route_tool_for_input("Summarize: quicksort notes")[0] == "summarize_tool"
    assert route_tool_for_input("Quiz me on trees")[0] == "quiz_tool"
    assert route_tool_for_input("Based on my notes, what is radix sort?")[0] == "rag_search_tool"


def test_rag_search_tool_retrieves_from_knowledge_base(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    kb = tmp_path / "knowledge"
    kb.mkdir()
    (kb / "algorithms.md").write_text(
        "Merge sort splits a list into halves, recursively sorts halves, and merges results in order.",
        encoding="utf-8",
    )
    monkeypatch.setattr("main.KNOWLEDGE_DIR", kb)

    result = rag_search_tool("How does merge sort work?")
    assert set(result.keys()) == {"query", "context", "sources"}
    assert "merge sort" in result["context"].lower()
    assert len(result["sources"]) >= 1


def test_rag_search_tool_rejects_low_relevance_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    kb = tmp_path / "knowledge"
    kb.mkdir()
    (kb / "algorithms.md").write_text(
        "Merge sort splits a list into halves, recursively sorts halves, and merges results in order.",
        encoding="utf-8",
    )
    monkeypatch.setattr("main.KNOWLEDGE_DIR", kb)

    result = rag_search_tool("Explain linked list with one example")

    assert result["context"] == "No relevant knowledge found in local knowledge base."
    assert result["sources"] == []


def test_agent_has_max_iterations_set_to_3() -> None:
    agent_state = setup_agent()
    assert agent_state.agent.max_iterations == 3


def test_before_after_hooks_trigger_for_tool_call() -> None:
    agent_state = setup_agent()

    result = agent_state.agent.execute_tool(
        "explanation_tool",
        {"topic": "merge sort", "level": "beginner"},
    )

    assert result["status"] == "success"
    assert agent_state.before_tool_count == 1
    assert agent_state.after_tool_count == 1


def test_before_hook_rejects_empty_topic_and_error_hook_returns_fallback() -> None:
    agent_state = setup_agent()

    result = agent_state.agent.execute_tool(
        "explanation_tool",
        {"topic": "   ", "level": "beginner"},
    )

    assert result["status"] == "error"
    assert isinstance(agent_state.last_fallback, dict)
    assert agent_state.last_fallback["definition"] == "Error occurred"


def test_run_prompt_returns_structured_output() -> None:
    fake_agent = SimpleNamespace(
        current_session={
            "trace": [
                {
                    "type": "tool_result",
                    "name": "explanation_tool",
                    "args": {"topic": "recursion", "level": "beginner"},
                    "timing_ms": 12.0,
                    "status": "success",
                    "result": '{"definition": "x", "intuition": "y", "example": "z"}',
                }
            ]
        }
    )

    class FakeState:
        def __init__(self) -> None:
            self.agent = fake_agent

        def run(self, user_input: str) -> str:
            return "done"

    output = run_prompt(FakeState(), "Explain recursion")

    assert set(output.keys()) == {"final_answer", "loop_count", "tool_history"}
    assert output["loop_count"] == 1
    assert isinstance(output["tool_history"], list)


def test_run_prompt_forces_quiz_tool_when_llm_skips_tools() -> None:
    class FakeAgent:
        def __init__(self) -> None:
            self.current_session = {"trace": []}
            self.called_tool_name = None

        def execute_tool(self, tool_name: str, args: dict) -> dict:
            self.called_tool_name = tool_name
            payload = {"question": "Q", "hint": "H", "answer": "A"}
            self.current_session["trace"].append(
                {
                    "type": "tool_result",
                    "name": tool_name,
                    "args": args,
                    "timing_ms": 1,
                    "status": "success",
                    "result": json.dumps(payload),
                }
            )
            return {"status": "success", "timing_ms": 1}

    class FakeState:
        def __init__(self) -> None:
            self.agent = FakeAgent()
            self.last_fallback = None
            self.tool_history = []

        def run(self, user_input: str) -> str:
            return "direct completion"

    state = FakeState()
    output = run_prompt(state, "Quiz me on graph traversal")

    assert state.agent.called_tool_name == "quiz_tool"
    assert output["loop_count"] == 1


def test_on_complete_hook_forces_tool_before_eval_when_trace_empty() -> None:
    agent_state = setup_agent()
    agent_state.agent.current_session = {
        "messages": [],
        "trace": [],
        "turn": 1,
        "iteration": 1,
        "user_prompt": "Quiz me on graph traversal",
    }

    agent_state._ensure_tools_for_eval(agent_state.agent)  # type: ignore[attr-defined]

    trace = agent_state.agent.current_session["trace"]
    tool_results = [t for t in trace if t.get("type") == "tool_result"]
    assert len(tool_results) >= 1
    assert tool_results[-1]["name"] == "quiz_tool"
    assert "forced_tool_execution:quiz_tool" == agent_state.agent.current_session.get("reason")
