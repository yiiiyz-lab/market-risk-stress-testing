import plotly.express as px


def plot_scenario_comparison(scenario_summary):
    """
    Plot portfolio P&L across stress scenarios.
    """
    chart_data = scenario_summary.sort_values(
        "stress_pnl_pct_nav"
    ).copy()

    fig = px.bar(
        chart_data,
        x="stress_pnl_pct_nav",
        y="scenario_name",
        orientation="h",
        title="Portfolio Stress P&L by Scenario",
        labels={
            "stress_pnl_pct_nav": "Stress P&L (% of NAV)",
            "scenario_name": "Scenario",
        },
        text="stress_pnl_pct_nav",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig.add_vline(
        x=0,
        line_width=1,
        line_dash="dash",
    )

    fig.update_layout(
        xaxis_title="Stress P&L (% of NAV)",
        yaxis_title="",
        showlegend=False,
    )

    return fig