from __future__ import annotations

from learning_system import init_learning_system, process_study_turn


def test_learning_flow_explain_quiz_grade_plan() -> None:
    state = init_learning_system()

    step1 = process_study_turn(state, "Explain recursion in linked lists")
    assert "Retrieval" in step1["actions"]
    assert "Explanation" in step1["actions"]
    assert "rag_search_tool" in step1["tools_called"]
    assert "explanation_tool" in step1["tools_called"]

    sid = step1["session_id"]

    step2 = process_study_turn(state, "Generate a quiz", session_id=sid)
    assert "Quiz tool" in step2["actions"]
    assert "quiz_tool" in step2["tools_called"]
    assert step2["session"]["awaiting_quiz_answer"] is True

    step3 = process_study_turn(state, "I think recursion just repeats forever", session_id=sid)
    assert "Grading" in step3["actions"]
    assert "Mistake tracking" in step3["actions"]
    assert "grading_tool" in step3["tools_called"]
    assert isinstance(step3["analytics"]["weak_topics"], list)

    step4 = process_study_turn(state, "Create revision plan for next 7 days", session_id=sid)
    assert "Planner tool" in step4["actions"]
    assert "planner_tool" in step4["tools_called"]
    assert int(step4["payloads"]["plan"]["days"]) == 7
    assert len(step4["payloads"]["plan"]["plan"]) == 7


def test_process_study_turn_emits_stream_events() -> None:
    state = init_learning_system()
    events: list[dict] = []

    result = process_study_turn(
        state,
        "Explain linked list with one example",
        on_event=events.append,
    )

    assert result["tools_called"] == ["rag_search_tool", "explanation_tool"]
    assert any(e.get("type") == "status" and e.get("action") == "Retrieval" for e in events)
    assert any(e.get("type") == "status" and e.get("action") == "Explanation" for e in events)
    assert any(e.get("type") == "output" and "Definition:" in e.get("chunk", "") for e in events)


def test_generate_quiz_reuses_previous_explanation_topic_when_prompt_is_generic() -> None:
    state = init_learning_system()

    explain = process_study_turn(state, "Explain recursion in linked lists")
    sid = explain["session_id"]

    quiz = process_study_turn(state, "Generate a quiz", session_id=sid)
    question = quiz["payloads"]["quiz"]["question"].lower()

    assert "recursion in linked lists" in question
    assert "generate a quiz" not in question
    assert quiz["session"]["current_topic"] == "recursion in linked lists"


def test_generate_quiz_extracts_explicit_topic_from_prompt() -> None:
    state = init_learning_system()

    quiz = process_study_turn(state, "Generate a quiz on binary search")
    question = quiz["payloads"]["quiz"]["question"].lower()

    assert "binary search" in question
    assert "generate a quiz" not in question
    assert quiz["session"]["current_topic"] == "binary search"


def test_quiz_after_explain_includes_multi_aspect_focus() -> None:
    state = init_learning_system()

    explain = process_study_turn(state, "Explain dynamic programming")
    quiz = process_study_turn(state, "Generate a quiz", session_id=explain["session_id"])
    hint = quiz["payloads"]["quiz"]["hint"].lower()

    assert "definition" in hint
    assert "intuition" in hint
    assert "example" in hint


def test_quiz_uses_previous_dialogue_context() -> None:
    state = init_learning_system()

    explain = process_study_turn(
        state,
        "Explain recursion and focus on base case plus stack overflow risk",
    )
    sid = explain["session_id"]

    process_study_turn(
        state,
        "Explain tail recursion versus normal recursion and discuss trade-offs",
        session_id=sid,
    )
    quiz = process_study_turn(state, "Generate a quiz", session_id=sid)
    hint = quiz["payloads"]["quiz"]["hint"].lower()

    assert "stack overflow" in hint
    assert "trade-offs" in hint or "trade offs" in hint


def test_quiz_context_excludes_control_prompts() -> None:
    state = init_learning_system()

    first = process_study_turn(state, "Explain recursion")
    sid = first["session_id"]
    process_study_turn(state, "Generate a quiz", session_id=sid)
    process_study_turn(state, "My answer is recursion repeats.", session_id=sid)
    second_quiz = process_study_turn(state, "Generate a quiz", session_id=sid)
    hint = second_quiz["payloads"]["quiz"]["hint"].lower()

    assert "generate a quiz" not in hint


def test_empty_message_returns_consistent_response_schema() -> None:
    state = init_learning_system()

    result = process_study_turn(state, "   ")

    assert result["session_id"]
    assert result["response"] == "Please enter a question."
    assert result["actions"] == []
    assert result["tools_called"] == []
    assert "payloads" in result
    assert "session" in result
