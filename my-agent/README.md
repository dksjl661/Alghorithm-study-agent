# Study Copilot (Learning Analytics System)

Study copilot backend with multi-tool orchestration.

## Core Capabilities

- Retrieval + explanation flow for concept questions
- Quiz generation
- Answer grading
- Mistake tracking (weak topics + error frequency)
- 7-day revision planner prioritized by weak areas
- Local RAG over `knowledge/` files

## Agent Tools

- `explanation_tool`
- `summarize_tool`
- `quiz_tool`
- `rag_search_tool`
- `grading_tool`
- `planner_tool`

## Setup

```bash
cd /Users/zifeizhou/code/connection/my-agent
python3 -m venv .venv
source .venv/bin/activate
pip install connectonion python-dotenv pytest pyyaml
```

## Run Backend API

```bash
source .venv/bin/activate
python study_api.py
```

API endpoints:
- `POST /study-turn`
- `GET /analytics`
- `GET /health`

## Backend API Usage

Example request:

```bash
curl -X POST http://127.0.0.1:8001/study-turn \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain recursion in linked lists"}'
```

## Scenario Flow (Implemented)

1. Student: `Explain recursion in linked lists`
   - Agent actions: `Retrieval`, `Explanation`
2. Student: `Generate a quiz`
   - Agent actions: `Quiz tool`
3. Student submits answer
   - Agent actions: `Grading`, `Mistake tracking`
4. Student: `Create revision plan for next 7 days`
   - Agent actions: `Planner tool` with weak-topic priority

## Tests

```bash
source .venv/bin/activate
pytest -q tests/test_main.py tests/test_learning_system.py
```
# Alghorithm-study-agent
# Alghorithm-study-agent
