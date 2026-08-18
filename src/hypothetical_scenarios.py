from pathlib import Path

import yaml

def load_hypothetical_scenarios(
    config_path="config/hypothetical_scenarios.yaml",
):
    """
    Load stress scenarios from a YAML configuration file.
    """
    path = Path(config_path)

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config["scenarios"]

def validate_hypothetical_scenarios(scenarios):
    """
    Validate the basic structure of each stress scenario.
    """
    if not scenarios:
        raise ValueError("No stress scenarios found.")

    for scenario_id, scenario in scenarios.items():
        if "name" not in scenario:
            raise ValueError(
                f"Scenario '{scenario_id}' is missing a name."
            )

        if "shocks" not in scenario:
            raise ValueError(
                f"Scenario '{scenario_id}' is missing shocks."
            )

        if not scenario["shocks"]:
            raise ValueError(
                f"Scenario '{scenario_id}' contains no shocks."
            )

        for risk_factor, shock in scenario["shocks"].items():
            if not isinstance(shock, (int, float)):
                raise ValueError(
                    f"Shock for '{risk_factor}' in scenario "
                    f"'{scenario_id}' must be numeric."
                )

    return True