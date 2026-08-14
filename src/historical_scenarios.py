from pathlib import Path

import yaml


def load_historical_scenarios(
    config_path="config/historical_scenarios.yaml",
):
    """
    Load historical stress scenario definitions.
    """
    path = Path(config_path)

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config["historical_scenarios"]


def validate_historical_scenarios(scenarios):
    """
    Validate historical stress scenario configuration.
    """
    if not scenarios:
        raise ValueError("No historical scenarios found.")

    required_fields = {
        "name",
        "start_date",
        "end_date",
    }

    for scenario_id, scenario in scenarios.items():
        missing = required_fields - scenario.keys()

        if missing:
            raise ValueError(
                f"Historical scenario '{scenario_id}' "
                f"is missing fields: {sorted(missing)}"
            )

        if scenario["start_date"] >= scenario["end_date"]:
            raise ValueError(
                f"Historical scenario '{scenario_id}' "
                f"has an invalid date range."
            )

    return True
