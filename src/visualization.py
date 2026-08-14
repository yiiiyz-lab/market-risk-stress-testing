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

def plot_asset_class_attribution(asset_class_summary, scenario_name):
    """
    Plot stress P&L contribution by asset class.
    """
    chart_data = asset_class_summary.sort_values(
        "pnl_pct_nav"
    ).copy()

    fig = px.bar(
        chart_data,
        x="pnl_pct_nav",
        y="asset_class",
        orientation="h",
        title=f"Stress P&L Attribution by Asset Class — {scenario_name}",
        labels={
            "pnl_pct_nav": "P&L Contribution (% of NAV)",
            "asset_class": "Asset Class",
        },
        text="pnl_pct_nav",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig.add_vline(
        x=0,
        line_width=1,
        line_dash="dash",
    )

    fig.update_layout(
        xaxis_title="P&L Contribution (% of NAV)",
        yaxis_title="",
        showlegend=False,
    )

    return fig


def plot_factor_attribution(factor_summary, scenario_name):
    """
    Plot stress P&L contribution by risk factor.
    """
    chart_data = factor_summary.sort_values(
        "pnl_pct_nav"
    ).copy()

    fig = px.bar(
        chart_data,
        x="pnl_pct_nav",
        y="risk_factor",
        orientation="h",
        title=f"Stress P&L Attribution by Risk Factor — {scenario_name}",
        labels={
            "pnl_pct_nav": "P&L Contribution (% of NAV)",
            "risk_factor": "Risk Factor",
        },
        text="pnl_pct_nav",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig.add_vline(
        x=0,
        line_width=1,
        line_dash="dash",
    )

    fig.update_layout(
        xaxis_title="P&L Contribution (% of NAV)",
        yaxis_title="",
        showlegend=False,
    )

    return fig


def plot_scenario_heatmap(heatmap_data):
    """
    Plot asset-class P&L contribution across stress scenarios.
    """
    fig = px.imshow(
        heatmap_data,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        title="Stress P&L Heatmap — Scenario × Asset Class",
        labels={
            "x": "Scenario",
            "y": "Asset Class",
            "color": "P&L (% NAV)",
        },
    )

    fig.update_traces(
        texttemplate="%{z:.2f}%"
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
    )

    return fig

def plot_stress_comparison(comparison):
    """
    Compare historical and hypothetical portfolio stress scenarios.
    """
    chart_data = comparison.sort_values(
        "stress_pnl_pct_nav"
    ).copy()

    fig = px.bar(
        chart_data,
        x="stress_pnl_pct_nav",
        y="scenario_name",
        orientation="h",
        color="scenario_type",
        title="Historical vs Hypothetical Stress Test Results",
        labels={
            "stress_pnl_pct_nav": "Stress P&L (% of NAV)",
            "scenario_name": "Scenario",
            "scenario_type": "Scenario Type",
        },
        text="stress_pnl_pct_nav",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
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
        legend_title_text="Scenario Type",
    )

    return fig