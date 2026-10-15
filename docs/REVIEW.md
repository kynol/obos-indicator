# Review of the published snapshot

Review date: 2026-10-15. Audited base: [`7be1779`](https://github.com/kynol/obos-indicator/tree/7be1779d6baf0b654d169ca96da0babb374ff046).

This is a source-level review supported by TradingView's documented execution semantics and local integrity/arithmetic checks. It is not an official Pine compilation, realtime parity test, backtest or calibration study. The accompanying update changes comments and documentation, not indicator calculations, inputs, plots or signal conditions.

## Findings

### P0-1: stale source checksum — not reproduced

The audited snapshot's `OBOS.pine` hashes to:

```text
0088e564c479b97824704bb12306e19fc90a13368cfb64ae2103a9e9a43564d7
```

Its `SOURCE.sha256` contains the same value. The cosmetic-label cleanup updated both files together. Commit ordering does not demonstrate a mismatch.

This hash above explicitly refers to the audited base, not subsequent source comments. The current checkout's `SOURCE.sha256` is refreshed with the source in the same commit. Use [the integrity utility](../scripts/check_integrity.py) on both files from one revision. A checksum from an earlier revision must not be presented as applying to later edited bytes.

### P0-2: static alerts bypass close confirmation — not reproduced

The current dependency chain is:

```text
barConfirmed = not confirmOnClose or barstate.isconfirmed
  -> rawBuySignal / rawSellSignal (logical AND with barConfirmed)
  -> baseBuySignal / baseSellSignal
  -> trend and mean-reversion lanes
  -> lane pass and selection
  -> buyBaseQualityOK / sellBaseQualityOK
  -> normal and enhanced final signals
  -> alertcondition() and alert()
```

With the switch enabled and the current chart bar unconfirmed, the raw signals are false; no lane can qualify and no final signal becomes true. The normal and enhanced static conditions therefore inherit close gating even though their call sites do not repeat it.

Static alert frequency is still selected by the user. Dynamic frequency is set in the code. Existing running alerts retain their script/input snapshots and must be recreated after changes. These points are documented in [TradingView alerts](https://www.tradingview.com/pine-script-docs/concepts/alerts/) and [bar states](https://www.tradingview.com/pine-script-docs/concepts/bar-states/).

### P0-3: current volume contaminates its own baseline — not reproduced

The code reads `todVolumeBaseline` from the array, computes `todRvol`, then updates the array only in the confirmed-bar block. The retrieved baseline is a scalar value, not a live alias into the array. The ATR path follows the same read-before-write pattern.

For a prior baseline of 100 and current volume of 200, RVOL is 2.0. With the default alpha `2 / 21`, the baseline committed afterward is approximately 109.5238. Moving the update before the division would lower that ratio to approximately 1.8261: that proposed fix would introduce the self-contamination being alleged.

The arrays use ordinary `var`, not `varip`; open-bar changes roll back. Moreover, their update block runs only when the bar is confirmed. There is no repeated tick-by-tick accumulation in that block. See [TradingView execution model](https://www.tradingview.com/pine-script-docs/language/execution-model/). This reasoning does not substitute for an end-to-end live execution test.

### P1-1: session-dependent baseline availability — documentation improved

Historical bars are confirmed, so the baseline is built from historical regular-session bars as well as realtime closing updates. Within an eligible open bar, the minimum-observation check and stored baseline come from previously committed observations. The cited code does not establish a baseline selector that flips repeatedly because of current ticks.

Availability can change with symbol/session, warm-up, data coverage and the chart period. This is a real usage limitation, now documented with the actual fallback branches. No universal live-versus-history equivalence is claimed.

`session.ismarket` does not mean "US equity". For symbols without extended sessions, such as BTCUSD, it is always true; many futures use electronic hours as their regular session. It does not remain false merely because a symbol is outside the US equity market. See [TradingView sessions](https://www.tradingview.com/pine-script-docs/concepts/sessions/#session-states).

### P1-2: Q calibration sensitivity — valid evidence gap; claimed fixed bounds unsupported

`QualityRaw` is a normalized weighted mean multiplied by 100. Macro and structure votes are only some of its components. Their values alone cannot establish a universal 55.1–76.6 raw-score interval.

As an algebraic check, setting every enabled normalized component to 1 makes the weighted raw score 100. This is a scoring-formula bound, not proof that an actual OHLC path can attain all components together or pass every lane gate.

For a less extreme scoring-only example using the default non-volume mean-reversion contributions, set depth/dwell/exhaustion/breadth/price/momentum to 1, range to 0.8, structure to 0.9, timing to 0.7 and dispersion to 0.8. The numerator is 84 and denominator 92, giving raw Q approximately 91.3043. At core minimum 0.8 and zero volatility/mode penalties, final Q is approximately 92.3043. This exceeds the 1H/4H thresholds algebraically. It is synthetic component arithmetic, not a real trade, market sample or evidence of an observed distribution.

The mean-reversion weak penalty is zero at `coreMin >= 0.52`; it saturates at four points at `coreMin <= 0.40`. It is not inevitably active. Regime and signal gates also affect which scores ever become eligible.

The empirical concern remains: no new SPY 5m/15m/1H/4H Q quantile and lane-frequency table has been produced for this publication. Changes to inputs/modules are not automatically recalibrated. This is explicitly documented. No debug table, filter, threshold optimization or fabricated sample statistics are added.

### P1-3: additional wick filter — untested strategy hypothesis

Both close-location variables use `(close - low) / (high - low)`. Their values are the same on a given nonzero-range bar; opposite comparisons implement the two directions.

Buy confirmation requires close location at least 0.62, which already limits the upper wick to at most 38% of the range. Sell confirmation requires close location at most 0.38, limiting the lower wick similarly. This does not guarantee that all such candles are desirable. A stricter wick rule would change the trading hypothesis and needs independent evaluation; its benefit cannot be assumed from the candle's appearance.

### P1-4: shared absolute body magnitude — explanatory comment added

`signalBodyAtr` uses `abs(close - open)`. Body magnitude and its excess above the minimum are direction-independent. Assigning the sell excess from the buy excess is intentional; candle direction and location checks differ.

### P2-1: alert-message format differences — documented compatibility boundary

The static and dynamic channels expose different contracts. Downstream parsers should select one consistently. TradingView's `{{time}}` placeholder is UTC bar-open time; dynamic `signalTime` is exchange-local bar-close time. They are different timestamps as well as different formats. No breaking payload change is made without an explicit message-schema migration.

### P2-3: Auto fallback — confirmed and documented

Auto applies only to minute charts through 240 minutes. Other chart periods use Custom values while the selector remains Auto. The README now states the exact mapping. No new Daily preset is invented or calibrated.

### P2-4: market/session assumptions — confirmed limitation, documented

The default time-of-day and regular-session settings are intended for US-equity research, while their implementation follows the symbol's exchange session. There is no US-market detector. The README makes this explicit.

### P3: preset refactor and dispersion display — no functional refactor

Centralizing presets could improve maintainability, but is not required to correct a demonstrated failure and would expand this patch unnecessarily. `maxDispersion` already has `display=display.none` in the audited source, so the alleged missing display flag does not apply to this snapshot.

## Verification boundaries

- Retrieve source and checksum from the same pinned snapshot before comparing.
- Verify the current exact-byte checksum with `python scripts/check_integrity.py`.
- Check that intentionally corrupted source is rejected by that utility.
- Compare source before/after excluding comments and blank lines; formulas and conditions must remain identical.
- Treat baseline and Q numerical examples as arithmetic checks, not Pine runtime tests.
- Do not claim new compilation, runtime, live-parity or strategy-performance results.
