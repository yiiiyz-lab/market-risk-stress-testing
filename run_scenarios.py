from src.hypothetical_scenarios import (
    load_hypothetical_scenarios,
    validate_hypothetical_scenarios,
)


scenarios = load_hypothetical_scenarios()

validate_hypothetical_scenarios(scenarios)

print("\nAvailable Stress Scenarios:")

for scenario_id, scenario in scenarios.items():
    print(f"\n{scenario_id}: {scenario['name']}")
    print(f"Description: {scenario['description']}")
    print("Shocks:")

    for risk_factor, shock in scenario["shocks"].items():
        print(f"  {risk_factor}: {shock}")