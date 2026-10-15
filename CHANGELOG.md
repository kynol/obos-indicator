# Changelog

## Review clarifications - 2026-10-15

- Document Auto fallback, exchange-defined session states, baseline update order and both alert contracts.
- Document the lack of empirical Q calibration evidence and retain existing signal behavior.
- Explain upstream close-confirmation gating and direction-independent candle body magnitude in source comments.
- Add a checksum verification utility and a point-by-point review record.
- Refresh the source checksum in the same commit as the comment changes.

## Presentation cleanup - 2026-10-15

- Remove cosmetic version labels from alert titles, alert messages and documentation.
- Preserve the required Pine compiler directive and indicator calculations.

## Initial public snapshot — 2026-10-15

- Package the maintainer-provided indicator as `OBOS.pine` (Pine Script).
- Translate comments, input labels and options, plot titles, error messages and alert text into English.
- Remove outdated section-version labels and decorative comment separators; retain explanatory comments and the Pine version directive.
- Preserve formulas, thresholds, state transitions, numeric defaults and plot styling.
- Add Chinese and English installation, interpretation and alert documentation.
- Document the distinction between internal score, displayed score and recovery alerts.
- Add the maintainer-approved MIT License and a source SHA-256 checksum.
- Verify each literal substitution and static code equivalence after reversing localization and excluding comments and blank lines.
- Do not claim a verified win rate or a fresh TradingView compile/backtest result.

This date identifies the release preparation, not the original development date. The original Chinese source is kept locally as a backup. Saved chart settings and alerts should be reviewed after switching languages or updating alert labels.

