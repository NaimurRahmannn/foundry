import json
import os
import sys
from typing import Any

from ai_product_company.crew import AiProductCompany


DEFAULT_INPUTS: dict[str, str] = {
    "product_description": (
        "A task management application that helps small software teams organize "
        "projects, assign tasks, track deadlines, and monitor project progress."
    ),
    "product_name": "TaskFlow",
    "requested_features": (
        "User registration, project creation, task creation, task assignment, "
        "deadlines, task statuses, comments, and a project progress dashboard."
    ),
    "target_users": "Team members, project managers, and administrators.",
    "budget": "Small-team MVP budget",
    "deadline": "8 weeks",
    "constraints": "Keep the MVP simple and avoid unnecessary infrastructure complexity.",
}


def _load_inputs() -> dict[str, Any]:
    raw_inputs = os.getenv("CREW_INPUTS_JSON")
    if len(sys.argv) > 1:
        raw_inputs = sys.argv[1]

    if not raw_inputs:
        return DEFAULT_INPUTS.copy()

    try:
        loaded = json.loads(raw_inputs)
    except json.JSONDecodeError as exc:
        raise ValueError("Runtime inputs must be valid JSON.") from exc

    if not isinstance(loaded, dict):
        raise ValueError("Runtime inputs JSON must be an object.")

    inputs = DEFAULT_INPUTS.copy()
    inputs.update(loaded)
    return inputs


def run() -> None:
    inputs = _load_inputs()
    AiProductCompany().crew().kickoff(inputs=inputs)


def train() -> None:
    inputs = _load_inputs()
    n_iterations = int(os.getenv("CREWAI_TRAIN_ITERATIONS", "1"))
    filename = os.getenv("CREWAI_TRAIN_FILENAME", "training.pkl")
    AiProductCompany().crew().train(
        n_iterations=n_iterations,
        filename=filename,
        inputs=inputs,
    )


def replay() -> None:
    if len(sys.argv) < 2:
        raise ValueError("Replay requires a task ID argument.")

    AiProductCompany().crew().replay(task_id=sys.argv[1], inputs=_load_inputs())


def test() -> None:
    inputs = _load_inputs()
    n_iterations = int(os.getenv("CREWAI_TEST_ITERATIONS", "1"))
    eval_llm = os.getenv("CREWAI_TEST_EVAL_LLM", "gpt-4o-mini")
    AiProductCompany().crew().test(
        n_iterations=n_iterations,
        eval_llm=eval_llm,
        inputs=inputs,
    )


if __name__ == "__main__":
    run()
