# OBOS · Composite Overbought/Oversold Indicator

[中文说明](README.zh-CN.md)

A TradingView Pine Script indicator combining RSI, Stochastic, CCI and Bollinger %B into a 0–100 state score, with trend, volatility and recovery conditions for alerts.

This is an `indicator()`, not a complete trading strategy. It does not place orders, define a full exit system or provide strategy performance results. No win rate or profitability is claimed.

## Installation

1. Open [OBOS.pine](OBOS.pine), select **Raw**, and copy the complete source.
2. Open TradingView's Pine Editor and replace a new indicator's contents with this source.
3. Save and add it to the chart. It appears in a separate pane.
4. Review the timeframe preset and settings before use.

This repository distributes source code. It does not include a TradingView community publication link.

## Default components

| Component | Transformation | Weight |
| --- | --- | ---: |
| RSI | RSI value | 35 |
| Stochastic | Stochastic value | 20 |
| CCI | `50 + CCI / 4`, clamped to 0–100 | 20 |
| Bollinger %B | Position within the bands × 100, clamped to 0–100 | 25 |

Weights are normalized before calculation. The internal score is EMA-smoothed according to settings. Default reference levels are 20, 30, 50, 70 and 80.

## Display and signals

The displayed curve applies additional smoothing to the internal score: by default, a 6-period EMA followed by a 2-period EMA. Extreme fills follow this displayed curve, while line colors depend on the internal score. The yellow background represents convergence conditions based on band width, ATR% and EMA spread.

**The displayed `displayScore` and the internal signal `score` differ.** Fills, colors and alerts can therefore change on different bars.

**Buying while oversold is a different rule from buying when an upward recovery alert occurs.** Alerts require pending-state, timing, price, momentum, cooldown and enabled environment conditions. Trend-pullback and mean-reversion lanes are evaluated separately and arbitrated when both qualify.

The Q score is an internal heuristic quality score, not a calibrated probability or win rate. Enhanced signals require additional quality and context conditions. This snapshot renders the curve, fills and backgrounds; it does not plot BUY/SELL arrows.

## Settings and alerts

- Automatic, 5m, 15m, 1H, 4H and custom presets are provided; their existence is not evidence of equal performance across timeframes.
- Defaults include US-equity intraday assumptions: regular-session signals, time-of-day ATR/RVOL baselines and shock protection. Check these settings before using other markets or sessions.
- Higher-timeframe context must be strictly above the chart timeframe. It uses completed higher-timeframe data and therefore involves confirmation delay.
- Volume filtering is disabled by default. Other enabled modules affect alert eligibility.
- Close-only confirmation is enabled by default. Intrabar conditions may change if it is disabled.

Create an alert in TradingView and select the indicator's upward/downward recovery or enhanced conditions. For dynamic messages, enable dynamic alerts and choose `Any alert() function call`. Adding the indicator alone does not create an alert.

## Verification status

The published source uses English comments, input labels and options, plot titles, error messages and alert text. Outdated section-version labels and decorative separators were cleaned up. Formulas, thresholds, state transitions, numeric defaults and plot styling were preserved. Existing saved settings and alerts should be reviewed or recreated after switching to the English version.

The published source has a different byte hash from the Chinese original. Static checks verified every string substitution and confirmed that reversing the translations and excluding comments and blank lines reproduces the original code. This is a localization integrity check, not a compiler or runtime test. Release preparation also checked common sensitive-data patterns. No new official TradingView compilation, runtime execution or strategy backtest was performed for this release.

Performance requires explicit entry, exit, holding, cost and data-split definitions. Report issues with the symbol, timeframe, session, settings and exact bar time.

## License and provenance

[MIT License](LICENSE). The maintainer confirmed that this version was written with AI assistance without copying third-party scripts. The required Pine compiler directive is preserved; cosmetic version labels are removed.

See [CHANGELOG.md](CHANGELOG.md) for the release record and [SOURCE.sha256](SOURCE.sha256) for the source checksum.

