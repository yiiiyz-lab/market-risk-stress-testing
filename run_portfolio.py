from src.portfolio import (
    load_portfolio,
    portfolio_summary,
    validate_portfolio,
)


portfolio_info, positions = load_portfolio()

validate_portfolio(portfolio_info, positions)

summary = portfolio_summary(positions)

print("\nPortfolio:")
print(portfolio_info)

print("\nPositions:")
print(positions[["instrument", "asset_class", "exposure_usd"]])

print("\nAsset Class Summary:")
print(summary)