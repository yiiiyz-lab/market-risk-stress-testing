# Market Risk Stress Testing

A Python-based framework for evaluating a multi-asset portfolio under both historical and hypothetical market stress scenarios. The project demonstrates scenario design, risk-factor mapping, stressed P&amp;L calculation, risk decomposition, and portfolio vulnerability analysis.

## Full Report

For the complete methodology, scenario analysis, attribution results, cross-framework comparison, limitations, and conclusions, see:

[Read the full Market Risk Stress Testing Report](report/market_risk_stress_testing_report.md)

## Project Overview

This project develops an end-to-end market risk stress-testing framework for a hypothetical **$100 million multi-asset portfolio** spanning Equity, Rates, Credit, Commodity, and FX exposures.

The framework combines two complementary approaches:

- **Hypothetical stress testing**, where predefined shocks are applied to modeled market risk factors and translated into position-level P&L using factor sensitivities, modified duration, and spread duration.
- **Historical stress testing**, where realized instrument returns from selected historical stress periods are replayed against the portfolio's current exposures.

The resulting analysis supports multiple levels of risk attribution:

- portfolio-level stress P&L;
- position-level attribution;
- asset-class attribution;
- risk-factor attribution for hypothetical scenarios;
- cross-scenario comparison and risk profiling.

The project is designed to emphasize both **stress severity** and **why the portfolio behaves differently across market regimes**, particularly when diversification relationships between Equity, Rates, and Credit change.

## Key Findings

Across the seven historical and hypothetical stress scenarios evaluated, the analysis identifies several recurring characteristics of the portfolio's risk profile:

- **Equity concentration is the primary structural source of downside.** Equity represents 50% of portfolio NAV and generates the largest negative asset-class contribution across the major loss scenarios.

- **The 2022 Inflation / Rates Sell-Off is the most severe overall scenario**, producing a portfolio loss of **$23.09 million, or 23.09% of NAV**.

- **Stagflation Shock is the most severe hypothetical scenario**, producing a portfolio loss of **$15.00 million, or 15.00% of NAV**.

- **Fixed-income diversification is regime-dependent.** Rates provide meaningful loss mitigation during conventional flight-to-quality stress, but can amplify portfolio losses when rising yields coincide with Equity weakness.

- **Cross-asset loss alignment is a key driver of stress severity.** The largest portfolio losses occur when Equity, Rates, and Credit exposures become adversely aligned rather than when a single asset class experiences the largest standalone decline.

- **Gold provides a partial defensive offset**, but its smaller portfolio weight limits its ability to counterbalance losses across the portfolio's larger exposures.

The central risk-management takeaway is that **portfolio diversification depends not only on the number of instruments or asset classes held, but also on the underlying economic risk drivers shared across those exposures**.

## Stress Testing Framework

The project evaluates portfolio risk through two complementary stress-testing approaches.

### Hypothetical Stress Testing

Hypothetical scenarios apply predefined shocks to the risk factors mapped to each position. The framework translates these shocks into stressed P&L using:

- direct factor sensitivities for Equity, Commodity, and FX exposures;
- modified duration for interest-rate exposures;
- spread duration for credit-spread exposures;
- multi-factor aggregation for positions exposed to more than one source of risk.

The resulting P&L can be decomposed from the underlying risk factor through the portfolio:

**Risk-Factor Shocks → Position P&L → Asset-Class P&L → Portfolio P&L**

### Historical Stress Testing

Historical scenarios replay realized instrument returns from selected periods of market stress against the portfolio's current exposures. This approach preserves the cross-asset relationships observed during each historical episode without requiring those relationships to be specified through modeled factor shocks.

The historical framework follows:

**Historical Market Window → Observed Instrument Returns → Position P&L → Asset-Class P&L → Portfolio P&L**

Together, the two approaches provide complementary perspectives: hypothetical stress allows specific economic shocks and risk-factor relationships to be examined explicitly, while historical replay anchors the analysis in realized market behavior.

## Scenario Set

The framework evaluates four hypothetical scenarios and three historical stress episodes designed to capture different market regimes and cross-asset relationships.

| Framework | Scenario | Primary Stress Theme |
|---|---|---|
| Hypothetical | Global Risk-Off | Equity weakness, credit deterioration, and flight-to-quality rate moves |
| Hypothetical | Stagflation Shock | Equity weakness, rising rates, wider credit spreads, and higher gold |
| Hypothetical | Rates Higher for Longer | Persistent upward pressure on Treasury yields and fixed-income valuations |
| Hypothetical | Growth / Risk-On Rally | Stronger risk assets, higher yields, and tighter credit spreads |
| Historical | COVID-19 Market Crash | Pandemic-driven risk-asset sell-off and flight to quality |
| Historical | 2022 Inflation / Rates Sell-Off | Inflation shock, aggressive monetary tightening, and simultaneous Equity and Rates weakness |
| Historical | 2023 Regional Banking Stress | Banking-sector stress accompanied by declining yields and defensive-asset strength |

The scenario set is intentionally diverse rather than exhaustive. Its purpose is to test how the same portfolio behaves when relationships among Equity, Rates, Credit, Commodity, and FX exposures change across market regimes.

## Selected Results

### Portfolio Stress Across Scenarios

Portfolio outcomes vary substantially across the seven scenarios, reflecting both the severity of the underlying market shocks and differences in cross-asset behavior.

![Historical vs. Hypothetical Portfolio Stress Results](outputs/figures/historical_vs_hypothetical.png)

The **2022 Inflation / Rates Sell-Off** produces the largest portfolio loss at **23.09% of NAV**, followed by the **COVID-19 Market Crash** at **16.39%**. Among the hypothetical scenarios, **Stagflation Shock** is the most severe at **15.00% of NAV**.

### Cross-Scenario Asset-Class Attribution

The asset-class heatmap illustrates how the composition of portfolio P&L changes across both historical and hypothetical stress environments.

![Cross-Scenario Asset-Class P&L Heatmap](outputs/figures/asset_class_scenario_heatmap.png)

The comparison highlights a key feature of the portfolio's risk profile: **Rates can either diversify or reinforce Equity losses depending on the stress regime**. Treasury exposure provides a positive offset during conventional flight-to-quality environments, but becomes a source of loss during inflationary and rising-rate stress. The most severe portfolio outcomes occur when negative contributions become aligned across multiple major asset classes.

For detailed position-level, asset-class, and risk-factor attribution, see the [full stress-testing report](report/market_risk_stress_testing_report.md).

## Repository Structure

The project separates portfolio and scenario configuration, reusable stress-testing logic, execution scripts, generated outputs, and analytical reporting.

```text
market-risk-stress-testing/
├── config/                  # Portfolio definitions and scenario assumptions
├── src/                     # Core stress-testing and attribution logic
├── scripts/                 # Executable analysis workflows
├── outputs/
│   ├── figures/             # Generated charts and heatmaps
│   └── tables/              # Generated stress-testing results
├── report/
│   └── market_risk_stress_testing_report.md
├── README.md
└── requirements.txt
```

## How to Run

### 1. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yiiiyz-lab/market-risk-stress-testing.git
cd market-risk-stress-testing
```

### 2. Create and Activate a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Stress Analysis

Run the hypothetical stress scenarios:

```bash
python -m scripts.run_hypothetical_scenarios
```

Run the historical stress scenarios:

```bash
python -m scripts.run_historical_scenarios
```

### 5. Generate P&L Attribution

Generate hypothetical stress attribution:

```bash
python -m scripts.analyze_hypothetical_decomposition
```

Generate historical stress attribution:

```bash
python -m scripts.analyze_historical_decomposition
```

### 6. Build the Cross-Scenario Risk Profile

```bash
python -m scripts.build_risk_profile
```

### 7. Compare Stress Scenarios

```bash
python -m scripts.compare_stress_scenarios
```

The analysis generates portfolio-, position-, asset-class-, and risk-factor-level results where applicable. Generated tables and figures are written to the `outputs/` directory and are used throughout the analytical report.

## Outputs

The stress-testing pipeline generates analytical tables and visualizations in the `outputs/` directory.

Key outputs include:

- portfolio-level P&L across historical and hypothetical scenarios;
- position-level stress P&L and return attribution;
- asset-class P&L attribution;
- risk-factor attribution for hypothetical scenarios;
- cross-scenario asset-class comparisons;
- portfolio stress comparison charts and attribution visualizations.

Selected outputs are incorporated into the [full stress-testing report](report/market_risk_stress_testing_report.md).

## Technologies

The project is implemented in Python and uses:

- **pandas** for data manipulation, aggregation, and tabular analysis;
- **PyYAML** for portfolio and scenario configuration;
- **yfinance** for historical market data retrieval;
- **Plotly** for analytical visualizations;
- **Kaleido** for static figure export.

Portfolio definitions and scenario assumptions are maintained separately from the analytical code, allowing the stress-testing logic to remain reusable across different configurations.

## Model Limitations

The framework is intentionally simplified and designed for transparent stress analysis rather than full portfolio valuation. Key limitations include the use of deterministic hypothetical shocks, manually specified factor sensitivities, first-order duration approximations, static portfolio exposures, and sensitivity of historical results to the selected stress windows. The scenario set is selective rather than exhaustive, and the framework does not explicitly model convexity, liquidity effects, transaction costs, nonlinear optionality, or dynamic portfolio rebalancing.

Stress results should therefore be interpreted as **conditional estimates under defined assumptions rather than forecasts, probabilities, or estimates of maximum possible loss**.

For a more detailed discussion, see [Model Limitations and Considerations](report/market_risk_stress_testing_report.md#6-model-limitations-and-considerations) in the full report.

## License

This project is licensed under the [MIT License](LICENSE).