# Market Risk Stress Testing

## Portfolio-Level Stress Testing, P&L Attribution, and Cross-Scenario Risk Profiling

---

## 2. Portfolio Composition and Risk Exposure

### 2.1 Portfolio Overview

The stress-testing framework is applied to a hypothetical multi-asset portfolio with a total net asset value (NAV) of **$100 million**. The portfolio contains ten positions spanning five broad asset classes: Equity, Rates, Credit, Commodity, and Foreign Exchange (FX). The portfolio is designed to provide exposure to several major market risk channels, including equity-market movements, interest-rate changes, credit-spread movements, commodity prices, and foreign-exchange rates.

The portfolio contains $50 million of equity exposure through U.S. and European equity ETFs, $25 million of rates exposure through intermediate- and long-duration U.S. Treasury ETFs, $15 million of credit exposure through investment-grade and high-yield corporate bond ETFs, $5 million of gold exposure, and $5 million of foreign-exchange exposure. Total position exposure therefore equals the portfolio's $100 million NAV.

**Table 1. Portfolio Positions**

| Instrument | Asset Class | Exposure (USD) | % NAV |
|---|---|---:|---:|
| SPY | Equity | $25,000,000 | 25.0% |
| QQQ | Equity | $15,000,000 | 15.0% |
| VGK | Equity | $10,000,000 | 10.0% |
| IEF | Rates | $15,000,000 | 15.0% |
| TLT | Rates | $10,000,000 | 10.0% |
| LQD | Credit | $10,000,000 | 10.0% |
| HYG | Credit | $5,000,000 | 5.0% |
| GLD | Commodity | $5,000,000 | 5.0% |
| EURUSD | FX | $3,000,000 | 3.0% |
| USDJPY | FX | $2,000,000 | 2.0% |
| **Total** |  | **$100,000,000** | **100.0%** |

The portfolio is intentionally multi-asset, but its exposure is not evenly distributed across risk categories. Equity represents the largest allocation at 50% of NAV, followed by Rates at 25%, Credit at 15%, Commodity at 5%, and FX at 5%. This composition provides the foundation for the stress-testing analysis: portfolio outcomes will depend not only on the magnitude of shocks to individual markets, but also on how losses and gains across these asset classes interact under different market regimes.

### 2.2 Asset-Class Allocation

At the asset-class level, the portfolio is concentrated primarily in Equity and Rates, which together account for **75% of NAV**. Credit represents an additional 15%, while Commodity and FX exposures each represent 5%. The resulting allocation is:

- **Equity — 50% of NAV:** The portfolio's largest allocation consists of SPY (25%), QQQ (15%), and VGK (10%). These positions provide exposure to broad U.S. equities, technology-oriented U.S. equities, and European equities, respectively. Equity therefore represents the portfolio's principal source of directional growth-market exposure.

- **Rates — 25% of NAV:** IEF (15%) and TLT (10%) provide exposure to intermediate- and long-duration U.S. Treasury securities. These positions introduce sensitivity to changes in U.S. interest rates. Because TLT has greater duration than IEF, its price response to a given yield shock is expected to be larger.

- **Credit — 15% of NAV:** LQD (10%) and HYG (5%) provide investment-grade and high-yield corporate credit exposure. Unlike pure Treasury positions, these instruments are exposed to both underlying interest-rate movements and changes in corporate credit spreads. Credit stress can therefore arise from multiple risk channels simultaneously.

- **Commodity — 5% of NAV:** GLD represents the portfolio's gold exposure. Gold is modeled as a direct-return risk factor and provides a potential source of diversification because its behavior can differ from that of equities, rates, and corporate credit across market regimes.

- **FX — 5% of NAV:** EURUSD (3%) and USDJPY (2%) represent the portfolio's foreign-exchange exposures. These positions introduce sensitivity to movements in the euro and Japanese yen relative to the U.S. dollar. Given their relatively small portfolio weights, their direct contribution to total portfolio stress is expected to be smaller than that of Equity, Rates, or Credit, although their direction of contribution can vary across scenarios.

This allocation creates an important distinction between **portfolio weight** and **portfolio risk**. An asset class with a large NAV allocation does not necessarily generate a proportionally large stress loss, while a smaller position can become important if it has high sensitivity to the shocked risk factor. For fixed-income instruments in particular, duration and spread sensitivity influence stress P&L in addition to the size of the underlying exposure.

The portfolio should therefore be viewed not simply as a set of asset-class weights, but as a collection of exposures to different underlying market risk factors. The mapping between individual positions and those risk factors is presented in the following subsection.

### 2.3 Risk-Factor Mapping

The hypothetical stress-testing framework translates each portfolio position into one or more underlying market risk factors. This mapping allows scenario shocks to be specified at the risk-factor level and subsequently translated into position-level and portfolio-level stressed P&L.

Three broad types of risk-factor exposure are modeled:

1. **Direct-return factors**, where the scenario shock is applied directly as a percentage return to the associated position.
2. **Interest-rate factors**, where changes in yields affect fixed-income positions through modified duration.
3. **Credit-spread factors**, where changes in corporate credit spreads affect credit positions through spread duration.

**Table 2. Instrument-to-Risk-Factor Mapping**

| Instrument | Asset Class | Risk Factor(s) | Risk-Factor Type |
|---|---|---|---|
| SPY | Equity | SPX | Direct return |
| QQQ | Equity | NASDAQ | Direct return |
| VGK | Equity | EU_EQUITY, EURUSD | Direct return |
| IEF | Rates | USD_7Y_RATE | Interest rate |
| TLT | Rates | USD_20Y_RATE | Interest rate |
| LQD | Credit | USD_10Y_RATE, IG_SPREAD | Interest rate + credit spread |
| HYG | Credit | USD_5Y_RATE, HY_SPREAD | Interest rate + credit spread |
| GLD | Commodity | GOLD | Direct return |
| EURUSD | FX | EURUSD | Direct return |
| USDJPY | FX | USDJPY | Direct return |

For most Equity, Commodity, and FX positions, the mapping is direct. The model generally assumes a unit sensitivity of 1.0 between each instrument and its designated primary risk factor. For example, a shock to the SPX factor is transmitted to SPY, while a shock to GOLD is transmitted to GLD. VGK is modeled with two sources of risk: a primary sensitivity of 1.0 to European equities (EU_EQUITY) and an additional sensitivity of 0.35 to EURUSD. This allows the hypothetical framework to capture a partial foreign-exchange effect alongside the underlying European equity-market shock. The magnitude of the resulting position return depends on the scenario shock and the position's assigned sensitivity to the relevant risk factor.

Rates positions are mapped to representative points on the U.S. Treasury yield curve. IEF is associated with the USD 7-year rate factor, while TLT is associated with the USD 20-year rate factor. Their stressed price changes are estimated using modified duration, so a given change in yield does not translate directly into an equal percentage change in price.

Credit positions require a two-factor representation. LQD is exposed to both the USD 10-year interest-rate factor and the investment-grade credit-spread factor, while HYG is exposed to the USD 5-year interest-rate factor and the high-yield credit-spread factor. The total stressed P&L of each credit position therefore reflects the combined contribution of interest-rate and spread movements.

This structure allows the hypothetical stress framework to distinguish between different economic sources of loss even when they affect the same instrument. For example, a corporate bond ETF may lose value because Treasury yields rise, because credit spreads widen, or because both occur simultaneously. The position-level P&L can therefore be decomposed into individual risk-factor contributions before being aggregated to the asset-class and portfolio levels.

The mapping can be summarized as:

$$
\mathrm{Scenario\ Shock}
\rightarrow
\mathrm{Risk\ Factor}
\rightarrow
\mathrm{Position\ P\&L}
\rightarrow
\mathrm{Asset\text{-}Class\ P\&L}
\rightarrow
\mathrm{Portfolio\ P\&L}
$$

This risk-factor mapping is specific to the hypothetical stress-testing framework. Historical stress testing does not require the same factor mapping because it applies observed historical returns directly to each portfolio instrument.

### 2.4 Fixed-Income Sensitivity Assumptions

Fixed-income positions require additional sensitivity parameters because their stressed returns cannot be represented adequately by applying interest-rate or credit-spread shocks as direct percentage price changes. The hypothetical stress framework therefore uses **modified duration** for interest-rate risk and **spread duration** for credit-spread risk.

#### Modified Duration

Modified duration measures the approximate percentage change in the price of a fixed-income instrument for a change in its underlying yield. For a small change in yield, the first-order relationship is:

$$
\frac{\Delta P}{P}
\approx
-D_{\mathrm{mod}}\Delta y
$$

where:

- $P$ is the instrument price;
- $D_{\mathrm{mod}}$ is modified duration;
- $\Delta y$ is the change in yield, expressed in decimal form.

The negative sign reflects the inverse relationship between bond prices and yields. An increase in yield produces an estimated decline in price, while a decrease in yield produces an estimated increase in price.

For example, an instrument with a modified duration of 8 would experience an approximate price change of:

$$
-8 \times 0.01 = -8\%
$$

for a 100-basis-point increase in its underlying yield, before incorporating any additional sensitivity scaling used by the stress model.

#### Spread Duration

Corporate credit positions are exposed not only to changes in Treasury yields but also to changes in credit spreads. Spread duration approximates the percentage price response to a change in the relevant credit spread:

$$
\frac{\Delta P}{P}
\approx
-SD\Delta s
$$

where:

- $SD$ is spread duration;
- $\Delta s$ is the change in credit spread, expressed in decimal form.

A widening of credit spreads therefore produces a negative price effect, while spread tightening produces a positive price effect.

In this portfolio, LQD and HYG contain both interest-rate and credit-spread exposure. Their hypothetical stressed P&L can therefore reflect two separate channels:

$$
\mathrm{Credit\ Position\ Stress}
=
\mathrm{Interest\text{-}Rate\ Contribution}
+
\mathrm{Credit\text{-}Spread\ Contribution}
$$

This decomposition is important because the two components need not move in the same direction. In a conventional risk-off environment, falling Treasury yields may partially offset losses caused by widening credit spreads. In an inflationary stress, rising Treasury yields and widening credit spreads may instead generate losses simultaneously.

**Table 3. Fixed-Income Sensitivity Assumptions**

| Instrument | Asset Class | Rate Factor | Modified Duration | Spread Factor | Spread Duration |
|---|---|---|---:|---|---:|
| IEF | Rates | USD_7Y_RATE | 7.3 | — | — |
| TLT | Rates | USD_20Y_RATE | 15.8 | — | — |
| LQD | Credit | USD_10Y_RATE | 8.1 | IG_SPREAD | 7.6 |
| HYG | Credit | USD_5Y_RATE | 3.5 | HY_SPREAD | 3.3 |

The duration parameters are treated as **static model inputs** for the purpose of the stress analysis. They are not dynamically calculated from the underlying bond cash flows or ETF holdings during each scenario. This approach keeps the stress framework transparent and allows the contribution of interest-rate and spread shocks to be isolated clearly.

The duration-based approach is a first-order approximation. It does not incorporate convexity or other nonlinear effects that may become material under sufficiently large yield or spread movements. These limitations are discussed further in Section 8.

In addition to duration, the hypothetical stress framework applies position-specific risk-factor sensitivities when translating scenario shocks into stressed P&L. These sensitivities are specified as model assumptions rather than estimated through statistical calibration. The distinction between scenario shocks, sensitivities, and duration parameters is developed formally in the stress-testing methodology in Section 3.

## 3. Stress Testing Methodology

### 3.1 Stress Testing Framework

The stress-testing framework evaluates the portfolio under two complementary approaches: **hypothetical stress testing** and **historical stress testing**. Both approaches estimate the impact of adverse market conditions on the portfolio's current exposures, but they differ in how the stressed market movements are defined and transmitted to individual positions.

**Hypothetical stress testing** begins with a predefined set of shocks to underlying market risk factors. These shocks represent economically coherent but deliberately constructed market environments, such as a global risk-off event, a stagflation shock, or a sustained increase in interest rates. Each risk-factor shock is translated into position-level P&L using the instrument's assigned sensitivity and, where applicable, modified duration or spread duration. The resulting factor contributions are then aggregated from the risk-factor level to the position, asset-class, and portfolio levels.

The hypothetical framework therefore follows the structure:

$$
\mathrm{Scenario}
\rightarrow
\mathrm{Risk\text{-}Factor\ Shocks}
\rightarrow
\mathrm{Position\ Sensitivities}
\rightarrow
\mathrm{Position\ P\&L}
\rightarrow
\mathrm{Portfolio\ P\&L}
$$

**Historical stress testing**, by contrast, does not specify risk-factor shocks or sensitivities. Instead, it measures the actual returns experienced by the portfolio's instruments over selected historical stress windows and applies those observed returns to the portfolio's current exposures. The approach therefore asks how the current portfolio would perform if the selected historical pattern of market movements were replayed.

The historical framework follows:

$$
\mathrm{Historical\ Stress\ Window}
\rightarrow
\mathrm{Observed\ Instrument\ Returns}
\rightarrow
\mathrm{Current\ Position\ Exposures}
\rightarrow
\mathrm{Position\ P\&L}
\rightarrow
\mathrm{Portfolio\ P\&L}
$$

The two approaches provide different but complementary perspectives on portfolio risk. Hypothetical scenarios provide greater control over the economic structure of a stress event and allow losses to be decomposed into individual modeled risk factors. Historical scenarios preserve the joint market behavior observed during actual periods of stress, including relationships across asset classes that do not need to be specified individually by the model.

Neither approach should be interpreted as a forecast of future portfolio performance. Rather, each represents a conditional analysis of the portfolio under a particular stressed market environment. Hypothetical stress asks **"What would happen if these specified risk-factor shocks occurred?"**, while historical stress asks **"What would happen to today's portfolio if these observed historical market movements were repeated?"**

Using both approaches reduces reliance on a single view of stress. Hypothetical scenarios can examine economically relevant conditions that may not correspond exactly to a past episode, while historical scenarios provide an empirical reference based on realized market behavior. Their combined use therefore provides a broader basis for assessing portfolio vulnerabilities, loss concentration, and diversification behavior across different market regimes.

### 3.2 Hypothetical Stress Methodology

The hypothetical stress-testing framework estimates portfolio P&L by applying predefined scenario shocks to the risk factors mapped to each position. For position $i$ and risk factor $f$, the stressed P&L contribution depends on four components: the position exposure, the scenario shock, the assigned factor sensitivity, and, for fixed-income exposures, the relevant duration measure.

Let:

- $E_i$ = USD exposure of position $i$;
- $\beta_{i,f}$ = sensitivity of position $i$ to risk factor $f$;
- $\Delta F_f$ = direct-return shock to risk factor $f$;
- $D_i$ = modified duration of position $i$;
- $SD_i$ = spread duration of position $i$;
- $\Delta y_f$ = interest-rate shock for factor $f$;
- $\Delta s_f$ = credit-spread shock for factor $f$.

All percentage-return shocks are represented in decimal form. Interest-rate and credit-spread shocks are also converted to decimal yield or spread changes before entering the duration-based calculations. For example, a 100-basis-point increase corresponds to:

$$
100\,\mathrm{bps} = 0.01
$$

#### 3.2.1 Direct-Return Risk Factors

For direct-return factors, stressed P&L is calculated by applying the specified percentage shock to the position exposure, adjusted by the assigned factor sensitivity:

$$
P\&L_{i,f}
=
E_i
\times
\beta_{i,f}
\times
\Delta F_f
$$

This methodology is used for the modeled Equity, Commodity, and FX factors, including `SPX`, `NASDAQ`, `EU_EQUITY`, `GOLD`, `EURUSD`, and `USDJPY`.

For example, if a $25 million SPY position has a sensitivity of 1.0 to the SPX factor and the scenario specifies a -20% SPX shock:

$$
P\&L_{\mathrm{SPY}}
=
\$25\,\mathrm{m}
\times 1.0
\times (-0.20)
=
-\$5\,\mathrm{m}
$$

The same framework accommodates partial factor sensitivity. VGK, for example, has a primary sensitivity of 1.0 to `EU_EQUITY` and an additional sensitivity of 0.35 to `EURUSD`. Its total hypothetical P&L is therefore the sum of the contributions generated by both factors.

#### 3.2.2 Interest-Rate Risk Factors

For interest-rate exposures, the framework uses a first-order modified-duration approximation. The factor-level P&L is estimated as:

$$
P\&L_{i,f}
\approx
-E_i
\times D_i
\times \beta_{i,f}
\times \Delta y_f
$$

The negative sign captures the inverse relationship between bond prices and yields. A positive yield shock therefore generates a negative estimated P&L, while a decline in yields generates a positive estimated P&L.

For example, consider the $10 million TLT position with a modified duration of 15.8 and a sensitivity of 1.0 to the USD 20-year rate factor. Under a hypothetical 100-basis-point increase in the 20-year yield:

$$
P\&L_{\mathrm{TLT}}
\approx
-\$10\,\mathrm{m}
\times 15.8
\times 1.0
\times 0.01
=
-\$1.58\,\mathrm{m}
$$

The same methodology is applied to IEF and to the interest-rate components of LQD and HYG using their respective rate factors and modified-duration assumptions.

#### 3.2.3 Credit-Spread Risk Factors

Credit instruments are additionally exposed to changes in corporate credit spreads. The spread component of stressed P&L is estimated using spread duration:

$$
P\&L_{i,f}
\approx
-E_i
\times SD_i
\times \beta_{i,f}
\times \Delta s_f
$$

A positive spread shock represents spread widening and therefore produces a negative price effect. Spread tightening produces the opposite result.

Because LQD and HYG are exposed to both interest-rate and credit-spread factors, their total stressed P&L combines the two effects. For a credit position $i$:

$$
P\&L_i
=
P\&L_{i,\mathrm{rate}}
+
P\&L_{i,\mathrm{spread}}
$$

This allows the framework to distinguish between losses caused by movements in the underlying Treasury curve and losses caused by changes in credit risk premia.

#### 3.2.4 Position and Portfolio Aggregation

A position may be exposed to one or more modeled risk factors. Its total stressed P&L is calculated by summing all factor-level contributions:

$$
P\&L_i
=
\sum_f P\&L_{i,f}
$$

The position's stressed return is then:

$$
R_i^{\mathrm{stress}}
=
\frac{P\&L_i}{E_i}
$$

Portfolio-level stressed P&L is obtained by aggregating across all positions:

$$
P\&L_{\mathrm{portfolio}}
=
\sum_i P\&L_i
$$

To make scenario severity directly comparable across scenarios and asset classes, portfolio P&L is also expressed relative to portfolio NAV:

$$
P\&L_{\%\mathrm{NAV}}
=
\frac{P\&L_{\mathrm{portfolio}}}
{\mathrm{NAV}}
\times 100
$$

With a portfolio NAV of $100 million, a stress loss of $15 million therefore corresponds to:

$$
\frac{-\$15\,\mathrm{m}}
{\$100\,\mathrm{m}}
\times 100
=
-15.0\%
$$

The same normalization is applied to position-level, asset-class, and risk-factor contributions when they are reported as percentages of NAV.

#### 3.2.5 Hypothetical P&L Attribution

Because hypothetical stress is calculated initially at the risk-factor level, the resulting portfolio loss can be decomposed through several analytical layers:

$$
\mathrm{Risk\text{-}Factor\ P\&L}
\rightarrow
\mathrm{Position\ P\&L}
\rightarrow
\mathrm{Asset\text{-}Class\ P\&L}
\rightarrow
\mathrm{Portfolio\ P\&L}
$$

Risk-factor attribution identifies the modeled economic shocks responsible for the result. Position attribution identifies the individual instruments through which those shocks affect the portfolio, while asset-class attribution aggregates the same P&L into broader portfolio risk categories.

This decomposition is additive. Subject to rounding:

$$
\sum_f P\&L_f
=
\sum_i P\&L_i
=
\sum_a P\&L_a
=
P\&L_{\mathrm{portfolio}}
$$

where $a$ denotes asset class.

The hypothetical scenario shocks and factor sensitivities used in this framework are deterministic model inputs. The primary risk-factor sensitivities are generally set to 1.0, with VGK additionally assigned a 0.35 sensitivity to EURUSD. These sensitivities are not statistically calibrated to historical factor relationships or estimated betas. Consequently, the hypothetical stress results should be interpreted as conditional scenario estimates under the specified assumptions rather than as forecasts or probabilistic loss estimates.

### 3.3 Historical Stress Methodology

Historical stress testing evaluates how the current portfolio would have performed under market movements observed during selected historical periods of stress. Unlike the hypothetical framework, historical stress does not construct shocks at the risk-factor level. Instead, it measures the realized return of each portfolio instrument over a predefined historical window and applies that return directly to the instrument's current exposure.

This approach preserves the cross-asset market movements that occurred during the selected episode and provides an empirical complement to the assumption-driven hypothetical scenarios.

#### 3.3.1 Historical Scenario Definition

Each historical scenario is defined by a start date and an end date corresponding to a selected period of market stress. The framework evaluates three historical episodes:

- COVID-19 Market Crash;
- 2022 Inflation / Rates Sell-Off;
- 2023 Regional Banking Stress.

For each scenario, historical market prices are obtained for the instruments represented in the portfolio. The same current portfolio exposures are used across all historical scenarios, so differences in stressed P&L reflect differences in the historical market movements rather than changes in portfolio composition.

The historical framework therefore represents a replay analysis:

$$
\mathrm{Historical\ Stress\ Window}
\rightarrow
\mathrm{Observed\ Instrument\ Returns}
\rightarrow
\mathrm{Current\ Portfolio\ Exposures}
\rightarrow
\mathrm{Stress\ P\&L}
$$

#### 3.3.2 Historical Return and P&L Calculation

For instrument $i$, the historical return over scenario window $h$ is calculated from its observed market prices:

$$
R_{i,h}
=
\frac{P_{i,h}^{\mathrm{end}}}
{P_{i,h}^{\mathrm{start}}}
-1
$$

where:

- $R_{i,h}$ is the historical return of instrument $i$ during scenario $h$;
- $P_{i,h}^{\mathrm{start}}$ is the instrument price at the beginning of the historical window;
- $P_{i,h}^{\mathrm{end}}$ is the instrument price at the end of the historical window.

The observed historical return is then applied directly to the current USD exposure of the position:

$$
P\&L_{i,h}
=
E_i
\times
R_{i,h}
$$

where $E_i$ is the current USD exposure of position $i$.

For example, if a position currently has an exposure of $25 million and its instrument experienced a -30% return during the selected historical window, its historical stress P&L would be:

$$
P\&L
=
\$25\,\mathrm{m}
\times (-0.30)
=
-\$7.5\,\mathrm{m}
$$

The calculation therefore answers a counterfactual question: how would the portfolio's current exposures perform if the instrument-level market movements observed during the historical episode were repeated?

#### 3.3.3 Portfolio Aggregation and Attribution

Historical position-level P&L is aggregated to obtain total portfolio stress P&L:

$$
P\&L_{\mathrm{portfolio},h}
=
\sum_i P\&L_{i,h}
$$

As in the hypothetical framework, the portfolio result is normalized by current portfolio NAV:

$$
P\&L_{\%\mathrm{NAV},h}
=
\frac{P\&L_{\mathrm{portfolio},h}}
{\mathrm{NAV}}
\times 100
$$

Position-level results can also be aggregated by asset class:

$$
P\&L_{a,h}
=
\sum_{i \in a} P\&L_{i,h}
$$

where $a$ denotes an asset class.

The resulting decomposition therefore follows:

$$
\mathrm{Observed\ Instrument\ Returns}
\rightarrow
\mathrm{Position\ P\&L}
\rightarrow
\mathrm{Asset\text{-}Class\ P\&L}
\rightarrow
\mathrm{Portfolio\ P\&L}
$$

Historical stress attribution is reported at the position and asset-class levels. Risk-factor attribution is not applied to historical scenarios because the framework directly uses realized instrument returns rather than decomposing those returns into modeled factor shocks. This distinction preserves the methodological separation between the historical and hypothetical approaches.

#### 3.3.4 Interpretation of Historical Stress

Historical stress results should be interpreted as conditional replay estimates rather than forecasts. They show the estimated effect on the current portfolio if the selected historical pattern of instrument returns were repeated, holding current portfolio exposures constant.

A key advantage of this approach is that the historical returns jointly reflect market relationships that actually occurred during the selected episode. For example, an historical stress period may simultaneously contain equity declines, changes in Treasury prices, credit-market repricing, currency movements, and changes in commodity prices. These relationships are captured through the observed instrument returns without requiring the model to specify each relationship separately.

Historical replay nevertheless depends on the selected scenario window. Different start and end dates can materially change measured returns and therefore estimated portfolio losses. In addition, a past episode does not necessarily represent the structure or severity of a future crisis. Historical stress should therefore be viewed as an empirical reference scenario rather than a complete representation of the portfolio's possible future loss distribution.

Used together, the historical and hypothetical methodologies provide complementary information: historical stress anchors the analysis in realized market behavior, while hypothetical stress allows specific economic shocks and risk-factor relationships to be examined explicitly.

### 3.4 Scenario Design and Selection

The stress-testing framework contains seven scenarios: four hypothetical scenarios and three historical scenarios. The scenario set is designed to expose the portfolio to materially different sources of market risk rather than variations of a single adverse environment. Together, the scenarios examine equity drawdowns, interest-rate shocks, credit-spread widening, inflationary pressure, safe-haven behavior, and changes in cross-asset diversification.

The scenarios are not assigned probabilities. Their purpose is to evaluate the conditional behavior of the current portfolio under a range of economically distinct market environments.

#### 3.4.1 Hypothetical Scenario Design

Four hypothetical scenarios are used in the analysis:

**Table 4. Hypothetical Scenario Set**

| Scenario | Primary Stress Theme | Key Risk Channels | Intended Portfolio Test |
|---|---|---|---|
| Global Risk-Off | Broad deterioration in investor risk appetite | Equity declines, credit-spread widening, safe-haven rate and gold behavior, FX movements | Tests portfolio performance during a conventional flight-to-quality environment |
| Stagflation Shock | Weak growth combined with persistent inflation | Equity losses, higher interest rates, wider credit spreads, commodity and FX movements | Tests vulnerability when both growth-sensitive and duration-sensitive assets are under pressure |
| Rates Higher for Longer | Persistent upward pressure on interest rates | Treasury yield increases, duration losses, credit repricing, pressure on rate-sensitive equities | Tests sensitivity to sustained restrictive monetary conditions |
| Growth / Risk-On Rally | Improving growth and investor risk appetite | Equity gains, higher yields, credit-spread tightening, weaker defensive assets | Tests upside participation and the behavior of defensive positions in a favorable risk environment |

The hypothetical scenarios are designed at the risk-factor level. Each scenario specifies shocks to the factors relevant to the portfolio, including equity indices, Treasury rates, credit spreads, foreign-exchange rates, and gold. These shocks are then transmitted to positions using the methodology described in Section 3.2.

The scenarios are intentionally differentiated in their economic structure. Global Risk-Off represents a more conventional defensive market regime in which risky assets decline while high-quality duration and gold can provide offsets. Stagflation Shock is designed to challenge this diversification mechanism by combining equity weakness with rising rates and wider credit spreads. Rates Higher for Longer isolates the portfolio's vulnerability to sustained interest-rate pressure, while Growth / Risk-On Rally provides a positive scenario that tests whether the portfolio participates in improving risk sentiment and identifies which defensive exposures become performance drags.

Including a positive scenario is useful because stress analysis need not be restricted to portfolio losses. Examining the portfolio under a risk-on environment provides additional information about asymmetry, diversification, and the opportunity cost of defensive exposures.

The hypothetical shock magnitudes are deterministic scenario assumptions rather than forecasts or statistically estimated tail events. They are selected to create economically interpretable stress environments and should therefore be evaluated as conditional model inputs.

#### 3.4.2 Historical Scenario Selection

Three historical episodes are used to complement the hypothetical scenarios:

**Table 5. Historical Scenario Set**

| Scenario | Stress Window | Primary Market Theme | Intended Portfolio Test |
|---|---|---|---|
| COVID-19 Market Crash | 19 Feb 2020 – 23 Mar 2020 | Rapid global risk-asset sell-off and flight to safety | Tests the portfolio against an extreme growth and liquidity shock |
| 2022 Inflation / Rates Sell-Off | 3 Jan 2022 – 14 Oct 2022 | Inflation shock, aggressive monetary tightening, and simultaneous equity/bond weakness | Tests the portfolio in an environment where traditional equity-rate diversification weakened |
| 2023 Regional Banking Stress | 8 Mar 2023 – 24 Mar 2023 | Banking-sector stress accompanied by falling rates and defensive asset demand | Tests portfolio behavior during a financial-sector shock with offsetting performance across asset classes |

These episodes were selected because they represent distinct forms of realized market stress. The COVID-19 episode captures a rapid and severe risk-off shock. The 2022 episode captures an inflation-driven regime in which equities and fixed income experienced substantial simultaneous losses. The 2023 regional banking episode provides a different stress structure in which declines in interest rates and gains in defensive assets could offset weakness elsewhere in the portfolio.

The selected windows are applied consistently across the instruments in each historical scenario. Historical returns are measured over each specified window and then applied to the portfolio's current exposures using the methodology described in Section 3.3.

#### 3.4.3 Complementarity of the Scenario Set

The seven scenarios are designed to provide complementary rather than redundant information. In particular, the scenario set allows the portfolio to be examined under several different relationships between equity and interest-rate risk.

A conventional risk-off environment can produce:

$$
\mathrm{Equity\ Losses}
+
\mathrm{Rate\ Gains}
$$

while an inflationary or stagflationary environment can instead produce:

$$
\mathrm{Equity\ Losses}
+
\mathrm{Rate\ Losses}
$$

This distinction is particularly important for the portfolio because Equity and Rates represent its two largest asset-class allocations. The effectiveness of fixed-income exposure as a portfolio diversifier therefore depends materially on the economic structure of the stress event.

The historical and hypothetical scenarios also provide useful points of comparison. The 2022 Inflation / Rates Sell-Off offers a realized example of simultaneous equity and fixed-income weakness, while the hypothetical Stagflation Shock and Rates Higher for Longer scenarios examine related vulnerabilities under explicitly defined factor shocks. Conversely, the historical COVID-19 and Regional Banking Stress episodes provide examples in which falling rates can support fixed-income positions during periods of market stress.

The scenario framework therefore evaluates not only the magnitude of portfolio losses, but also how the sources of those losses and the effectiveness of diversification change across different market environments.



