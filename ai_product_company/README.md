# ai_product_company

A classic Python/YAML CrewAI project for generating product requirements,
technical architecture, draft plans, quality reviews, and final product plans.

## Project Structure

```text
ai_product_company/
├── knowledge/
├── output/
├── scripts/
├── schemas/
├── skills/
├── src/
│   └── ai_product_company/
│       ├── crew.py
│       ├── main.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
└── legacy_jsonc/
```

## Environment Setup

Create or update `.env` with the required model provider credentials. This
project uses Groq through an OpenAI-compatible endpoint, so `GROQ_API_KEY` or
`OPENAI_API_KEY` must be available in the environment.

Install dependencies with the existing project manager:

```bash
uv sync
```

## Running

Run the crew from the project directory:

```bash
crewai run
```

The classic entry point is `ai_product_company.main:run`, exposed as the
`run_crew` project script. Default runtime inputs are defined in
`src/ai_product_company/main.py`. To override them without exposing secrets,
pass a JSON object through `CREW_INPUTS_JSON` when calling the script directly:

```bash
CREW_INPUTS_JSON='{"product_name":"TaskFlow"}' uv run run_crew
```

## Configuration

Agents are configured in:

```text
src/ai_product_company/config/agents.yaml
```

Tasks are configured in:

```text
src/ai_product_company/config/tasks.yaml
```

Custom tools belong in:

```text
src/ai_product_company/tools/
```

## Outputs

Generated files are written to:

```text
output/product_requirements.json
output/draft_product_plan.md
output/quality_review.md
output/product_plan.md
```

## Validation

Validate the generated product requirements JSON:

```bash
python scripts/validate_product_requirements.py
```

The validator uses `schemas/product_requirements.py` and catches invalid JSON
shape, missing confirmed requirements, invalid feature priority/source
combinations, invented missing success targets, and missing client-requested
features.

## Legacy JSONC

The pre-migration JSONC configuration is preserved under `legacy_jsonc/` after
the classic migration has passed local checks.
