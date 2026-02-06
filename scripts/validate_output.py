"""
Validate spider output JSON files against ChampionRaw model.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.champion_raw import ChampionRaw
from pydantic import ValidationError


def validate_json_file(filepath: Path) -> tuple[bool, list[str]]:
    """
    Validate a JSON file against ChampionRaw model.

    Returns:
        (is_valid, list of error messages)
    """
    errors = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]

    # Handle both single item and list output
    items = data if isinstance(data, list) else [data]

    for i, item in enumerate(items):
        try:
            ChampionRaw.model_validate(item)
        except ValidationError as e:
            for err in e.errors():
                errors.append(f"Item {i}: {err['loc']} - {err['msg']}")

    return len(errors) == 0, errors


def check_content_quality(filepath: Path) -> list[str]:
    """
    Check content quality (non-validation checks).

    Returns:
        List of warning messages
    """
    warnings = []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]

    for item in items:
        name = item.get("structure", {}).get("name", "Unknown")

        # Check for empty required content
        structure = item.get("structure", {})
        if not structure.get("background"):
            warnings.append(f"{name}: Missing background content")
        if not structure.get("quote"):
            warnings.append(f"{name}: Missing quote")

        # Check for HTML artifacts
        for field in ["background", "appearance", "personality"]:
            content = structure.get(field, "")
            if "<script" in content or "<style" in content:
                warnings.append(f"{name}: {field} contains script/style tags")

        # Check relations
        relations = structure.get("relations", [])
        if len(relations) == 0:
            warnings.append(f"{name}: No relations extracted")

        # Check abilities
        abilities = structure.get("abilities", "")
        if not abilities:
            warnings.append(f"{name}: No abilities extracted")

    return warnings


def print_champion_summary(item: dict) -> None:
    """Print a summary of champion data."""
    structure = item.get("structure", {})
    key_facts = item.get("key_facts", {})

    print(f"  Name: {structure.get('name', 'N/A')}")
    print(f"  Species: {key_facts.get('characteristics', {}).get('species', 'N/A')}")
    print(f"  Status: {key_facts.get('personal_status', {}).get('status', 'N/A')}")
    print(f"  Abilities: {len(structure.get('abilities', []))} extracted")
    print(f"  Relations: {len(structure.get('relations', []))} extracted")
    print(f"  Background: {len(structure.get('background', ''))} chars")


def main():
    output_dir = Path("output")

    if not output_dir.exists():
        print("ERROR: output/ directory not found")
        return 1

    json_files = list(output_dir.glob("*.json"))

    if not json_files:
        print("ERROR: No JSON files in output/")
        return 1

    all_valid = True
    total_champions = 0

    for filepath in json_files:
        print(f"\n{'=' * 50}")
        print(f"Validating: {filepath.name}")
        print("=" * 50)

        # Validate structure
        is_valid, errors = validate_json_file(filepath)

        if is_valid:
            print("  [PASS] Pydantic validation passed")
        else:
            print("  [FAIL] Pydantic validation failed:")
            for err in errors:
                print(f"    - {err}")
            all_valid = False

        # Check content quality
        warnings = check_content_quality(filepath)
        if warnings:
            print("  [WARN] Content quality issues:")
            for warn in warnings:
                print(f"    - {warn}")

        # Print summary
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else [data]
        total_champions += len(items)

        print(f"\n  Champions in file: {len(items)}")
        for item in items:
            print(f"\n  --- {item.get('structure', {}).get('name', 'Unknown')} ---")
            print_champion_summary(item)

    print(f"\n{'=' * 50}")
    print(f"Total champions validated: {total_champions}")
    if all_valid:
        print("All files validated successfully!")
        return 0
    else:
        print("Validation failed for some files")
        return 1


if __name__ == "__main__":
    sys.exit(main())
