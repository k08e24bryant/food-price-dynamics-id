# Decisions log

Assumptions and methodology decisions. Each entry is **Locked** (owner confirmed) or
**Proposed** (default to be confirmed by the owner at the named phase gate).

## Scope

| ID | Decision | Status |
|---|---|---|
| D01 | Period: 2021-01-01 to 2026-09-30, all provinces. | Locked (CLAUDE.md) |
| D02 | Commodities: cabai merah besar, cabai merah keriting, cabai rawit merah, cabai rawit hijau, bawang merah, bawang putih, beras (all quality tiers). Exact PIHPS names to be recorded after ingestion. | Locked (CLAUDE.md) |
| D03 | The fact table keeps all market types; marts filter to traditional markets (`pasar tradisional`). | Proposed (Phase 3 gate) |
| D04 | Each beras quality tier is a separate commodity with `commodity_group = 'beras'`; chilies roll up to `cabai` and shallot/garlic to `bawang`. | Proposed (Phase 3 gate) |

## Sources and reference data

| ID | Decision | Status |
|---|---|---|
| D10 | Source: PIHPS Bank Indonesia (https://www.bi.go.id/hargapangan). Ingestion method decided after a site inspection session; manual Excel download is the fallback. | Locked (2026-10-18) |
| D11 | Eid al-Fitr and Ramadan dates: government (Kemenag sidang isbat) dates only, entered by the owner into `dbt/seeds/ramadan_calendar.csv` from official sources. Source per year: _TODO (owner)_. | Locked (2026-10-18) |
| D12 | Provinces: kept as reported by PIHPS. `provinces.csv` adds `parent_province_34`, which maps Papua Selatan, Papua Tengah and Papua Pegunungan to Papua, and Papua Barat Daya to Papua Barat (2022 split), so trends can use a stable 34-province panel. | Locked (2026-10-18) |
| D13 | Java = DKI Jakarta, Jawa Barat, Jawa Tengah, DI Yogyakarta, Jawa Timur, Banten. All other provinces (including Bali) are non-Java. | Proposed (owner review of `provinces.csv`) |
| D14 | Prices stored as integer Rupiah per kg (or the PIHPS unit, recorded here once confirmed). Unit: _TODO after ingestion_. | Locked (CLAUDE.md) |

## Data quality

| ID | Decision | Status |
|---|---|---|
| D20 | Staging keeps raw nulls. No forward-fill anywhere. | Locked (CLAUDE.md) |
| D21 | Imputation (intermediate layer only): linear interpolation for gaps of 3 or fewer consecutive days per province × commodity × market type, flagged `is_imputed = true`. Longer gaps stay null. | Proposed (Phase 2 gate) |
| D22 | Outliers: `is_outlier = true` when the price falls outside the rolling 15-day median ± 5 × MAD per province × commodity × market type. Flagged, never deleted. | Proposed (Phase 2 gate) |

## Metric definitions

| ID | Metric | Definition | Status |
|---|---|---|---|
| M01 | Ramadan spike | % change of the mean price over H-30..H-1 before Eid al-Fitr against the baseline mean over H-90..H-61. Per year × commodity × province. | Locked (CLAUDE.md) |
| M02 | Spike onset | Daily index = price / baseline mean (H-90..H-61). Onset = the earliest day in H-60..H-1 from which the 7-day rolling index stays at or above 1.10 through H-1. Reported as days before Eid; null if the threshold is never sustained. | Proposed (Phase 3 gate) |
| M03 | Java vs non-Java disparity | Monthly median price per group (unweighted median across provinces of each province's monthly median). Ratio = Java ÷ non-Java; absolute gap = Java − non-Java (nominal Rp). | Locked (CLAUDE.md); median construction Proposed |
| M04 | Disparity trend | Headline = the monthly ratio on the stable 34-province panel. Trend = linear slope of the ratio over time, plus year-over-year change. The absolute gap is labeled nominal (not inflation-adjusted). | Proposed (Phase 3 gate) |
| M05 | Volatility (CV) | Coefficient of variation (std / mean) of daily prices within each month, per province × commodity. Observed (non-imputed) prices only. | Locked (CLAUDE.md); exclusion of imputed values Proposed |
| M06 | Volatility (rolling) | 30-calendar-day rolling std of daily log returns, observed prices only, requiring at least 15 observations in the window (otherwise null). | Locked (CLAUDE.md); window rules Proposed |
| M07 | Date helpers | `days_to_eid` = signed days to the nearest Eid al-Fitr (negative = before Eid). `ramadan_window` = H-30..H-1; `is_spike_window` = H-30..H-1; `is_baseline_window` = H-90..H-61. | Proposed (Phase 3 gate) |

## Exports

| ID | Decision | Status |
|---|---|---|
| E01 | Exports as Parquet (committed) and CSV (gitignored, since daily facts may exceed GitHub's 100 MB file limit). | Proposed (Phase 4 gate) |
| E02 | CSV format: UTF-8 with BOM, ISO dates, `.` decimal separator. Open in Excel via Data → From Text/CSV with locale "English (United States)". | Proposed (Phase 4 gate) |

## Interpretation notes (for the owner's narrative)

- 2021 and 2022 Lebaran fell under COVID-era mobility restrictions (mudik limits), which may dampen or shift the spike in those years.
- Lebaran public holidays (cuti bersama) can create reporting gaps right around Eid; the coverage profile in Phase 2 measures this.
