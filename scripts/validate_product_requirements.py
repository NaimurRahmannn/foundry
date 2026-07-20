import json
import sys
from pathlib import Path

from pydantic import ValidationError

from schemas.product_requirements import ProductRequirements


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/product_requirements.json")

    if not path.exists():
        print(f"❌ File not found: {path}")
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print("❌ Invalid JSON")
        print(error)
        return 1

    try:
        requirements = ProductRequirements.model_validate(data)
    except ValidationError as error:
        print("❌ Product requirements validation failed")
        print(error)
        return 1

    print("✅ Product requirements JSON is valid")
    print(f"Product: {requirements.product_name}")
    print(f"Confirmed requirements: {len(requirements.confirmed_client_requirements)}")
    print(f"Features: {len(requirements.features)}")
    print(f"Open questions: {len(requirements.open_questions)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())