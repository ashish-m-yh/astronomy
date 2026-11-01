# Project plan: historical astronomy compared with JPL DE440 and DE441

Prepared: 1 November 2026. Status: proposal and feasibility review; implementation awaits user confirmation. This document does not authorize or claim completion of code changes, dependency installation, kernel downloads, or numerical benchmarking.

## Objective

Build a reproducible comparison of a documented Sūrya Siddhānta reconstruction, selected historical alternatives, and explicitly labeled modern approximations against JPL DE440 for the initial 1900–2026 benchmark, with DE441 for historical-era and long-term studies. First deliver a reliable data pipeline and a solar-longitude benchmark. Extend to the Moon, planets, events, and local observations only after their prerequisites pass.

Maintain three separate assessments:

1. Textual fidelity: whether the implementation follows the selected edition and cited verses.
2. Numerical correctness: whether the software evaluates those rules correctly.
3. Astronomical accuracy: agreement with a specified modern reference under matched conventions.

The JPL reference addresses the third assessment. It cannot establish authorship, textual priority, transmission, or fidelity to a Sanskrit passage. It is a fitted dynamical model, not an independent observation at every requested date. JPL describes DE440 as more accurate for the current century and DE441 as the longer-span solution; use DE440 as the primary modern-interval reference and DE441 for historical epochs outside DE440 coverage. Compare both over a shared sample to measure reference sensitivity. [JPL paper](https://ssd.jpl.nasa.gov/doc/de440_de441.html)

## Feasibility review and corrections to the initial proposal

**Assessment:** the reference pipeline and modern-interval solar benchmark are technically feasible. The historical reconstruction is conditional on resolving the source edition, epoch, and longitude origin. Full planetary and eclipse validation requires substantial additional work; the present demonstrations do not supply those models.

| Area | Checked finding | Consequence |
| --- | --- | --- |
| Primary DE440 coverage | The full `de440.bsp` covers approximately 1550–2650. | One kernel covers the initial 1900–2026 interval; no cross-part routing is needed for the primary benchmark. |
| Historical DE441 coverage | NAIF lists part 1 through 1969-07-30 and part 2 from 1969-06-28, with an overlap. | For later DE441 work, choose parts by the actual study dates. Both parts are needed for a full 1900–2026 DE441 replication; a shared sensitivity sample can use a single part if its dates fit. |
| Disk and transfer | The full DE440 kernel is approximately 114 MB in the directory listing; DE441 parts are roughly 1.5 GB each. | Start with DE440. Acquire DE441 only for selected sensitivity/historical dates; budget up to roughly 3 GB if both parts are needed, plus cache/output overhead. Exclude kernels from Git. |
| Astropy integration | Astropy accepts an explicit local kernel path, but its ordinary ephemeris state represents one kernel at a time. | Use an explicit DE440 path initially. For later multi-part DE441 runs, route date batches by coverage and validate overlap; a single `set('de441')` must not be assumed to load both parts. |
| Target identity | Astropy's mappings for Mars, Jupiter, and Saturn resolve to system barycenters 4, 5, and 6. | Store explicit target IDs. Planet-center positions require additional satellite kernels and a separate provenance description. |
| Workload | The proposed half-open date interval contains 46,021 daily epochs. | Seven targets produce 322,147 body-time records. Chunked processing and ordinary CSV outputs are reasonable; runtime and memory remain to be measured. |
| Local environment | Read-only module discovery found no Astropy, jplephem, NumPy, pandas, Matplotlib, or SpiceyPy installed. | A project environment and pinned dependencies are prerequisites. No installation has been attempted. |
| Historical model | README documents missing epoch/origin choices and defective corrections. | A successful download does not make the repository ready for historical accuracy claims. |

Coverage and body availability were checked against [NAIF's kernel summaries](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/aa_summaries.txt); sizes against the [kernel directory](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/). Astropy behavior was checked in its [official source](https://docs.astropy.org/en/stable/_modules/astropy/coordinates/solar_system.html). These are documentation checks, not successful local kernel evaluations.

### Problems with the supplied sample

- `de432s` is a different ephemeris with approximately 1950–2050 coverage; it cannot cover the requested start in 1900. Explicit local kernel paths are supported. [Astropy ephemeris reference](https://docs.astropy.org/en/stable/api/astropy.coordinates.solar_system_ephemeris.html)
- `get_body_barycentric` returns barycentric positions, despite the sample's heliocentric comment. Geometric geocentric vectors require subtracting Earth's barycentric position at the same time; heliocentric vectors subtract the Sun. [Function reference](https://docs.astropy.org/en/stable/api/astropy.coordinates.get_body_barycentric.html)
- Cartesian coordinate construction must specify its representation. Observation time and equinox must be supplied deliberately for time-dependent transformations. Do not rely on default `SkyCoord` interpretation or default frame dates. [SkyCoord](https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html), [GeocentricMeanEcliptic](https://docs.astropy.org/en/stable/api/astropy.coordinates.GeocentricMeanEcliptic.html)
- A general frame transformation can include more than a simple rotation. The geometric baseline must use an explicitly specified rotation of same-time relative vectors; apparent-coordinate products belong to a separately documented pipeline.
- Adding bare day counts obscures units; use explicit time intervals. Output paths must be relative to a documented project location, with directories created deliberately.
- The paper mentioned in the sample is unidentified. Replication of its analysis is outside the verified scope until its citation and methods are supplied.

## Comparisons and prerequisites

| Comparison | Repository readiness | Verification benefit and limitation |
| --- | --- | --- |
| Mean-motion rates and accumulated drift | Constants and ratio function exist; epoch missing. | Measures rate-related drift after origin alignment. JPL instantaneous longitude is not the historical mean longitude; define any averaged/fitted rate explicitly. |
| True solar longitude | Requires sourced manda reconstruction. | First substantive historical benchmark; separates mean-motion, table, and correction effects. |
| Lunar longitude and latitude | Full lunar model absent. | Measures lunar periodic errors and node treatment after implementation. |
| Mercury through Saturn longitude | Full historical models absent. | Assesses manda/śīghra geometry and correction sequence. Record barycenter-versus-center approximation. |
| Full sky separation and equatorial coordinates | Latitude and documented obliquity/frame conversion needed. | Evaluates combined directional errors; longitude alone cannot establish this. |
| Stations and retrograde duration | Need continuous time-dependent longitude model. | Measures reversals and timing; a single angular adjustment cannot demonstrate a loop. |
| Conjunctions, oppositions, lunar phases | Need validated solar/lunar/planetary longitude functions. | Gives interpretable event-time differences using finer sampling and root finding. |
| Gnomon shadows | Triangle calculation exists; solar altitude pipeline absent. | Requires location, rotation/time convention, and refraction policy. Cannot infer local time uniquely from shadow length alone. |
| Eclipse screening and circumstances | Current flags are defective. | Screening first; contacts, magnitude, and local visibility require separate geometry and validation. Ephemeris vectors alone are insufficient. |
| Sine and chord approximations | Direct mathematical checks possible. | Compare with modern trigonometry and the selected historical table; A JPL ephemeris is unnecessary. |
| Kepler approximation | Solver exists; physical elements/orientation absent. | Measures a specified two-body model against the dynamical reference; fitted variants must be labeled. |
| Ptolemaic predictions | Only generic circular vectors exist. | Requires a named construction, planet, parameters, epoch, and textual source before historical comparison. |

Do not transfer a finding for the Sun to the entire Sūrya Siddhānta or transfer a finding for arbitrary epicycles to Ptolemy. Keep unsupported attributions unresolved.

## Experimental specification

### Time and coordinates

- Initial interval: 1900-01-01 00:00:00 TDB inclusive to 2026-01-01 00:00:00 TDB exclusive; 46,021 samples at one-day intervals. Calendar dates are Gregorian. These are TDB timestamps, not local civil midnights.
- Preserve two-part Julian dates internally where supported; exports must identify `jd_tdb` explicitly.
- Kernel reference: ICRF-oriented positions and velocities; retain raw vectors in stated units, preferably km and km/day.
- Geometric baseline: body minus Earth at the same TDB epoch, with no light-time, aberration, refraction, or topocentric displacement. Derive longitude, latitude, and distance by an explicit documented rotation.
- Retain fixed J2000 ecliptic results for transformation checks. For historical comparisons, specify the ecliptic/equinox and the mapping of the text's longitude origin. A J2000 longitude must not be directly compared with an unconverted historical sidereal longitude.
- Do not select a modern ayanāṃśa silently. If historical origin mapping is unresolved, present declared alternative conventions as sensitivity cases and withhold a unique absolute-accuracy conclusion.
- For historical ahargaṇa, document epoch, day boundary, reference meridian, calendar interpretation, and relation of the model's civil day to the modern time argument. Reference-position generation can proceed while this is researched; the historical benchmark cannot claim completion without it.
- UT1/ΔT and Earth orientation become required for Earth-rotation-dependent event/local calculations. Early dates need a documented historical treatment rather than an assumption that modern IERS data or UTC conversions cover the entire interval.

### Target identity

Use Earth center 399 as the observer origin. Initial reference targets: Sun 10, Moon 301, Mercury 199, Venus 299, Mars-system barycenter 4, Jupiter-system barycenter 5, Saturn-system barycenter 6. Earth itself must be reconstructed from its proper segment chain, not confused with Earth–Moon barycenter 3.

Keep human-readable names and numerical target IDs together. When later adding centers 499/599/699, obtain the appropriate additional kernels, quantify the differences, and label the result as a combined-kernel reference.

### Reference acquisition and independent checks

Primary route: the verified full local `de440.bsp`, read with Astropy/jplephem through an explicit file path, for every date in the initial benchmark. Do not substitute `de440s`: its approximately 1849–2150 coverage includes the initial interval, but the full DE440 kernel is the chosen baseline and also supports wider modern-period studies. Record exact segment coverage from the acquired file.

DE441 has two separate roles:

1. Reference-sensitivity check: before interpreting historical-model errors, compare DE440 and DE441 at a fixed, recorded set of shared epochs with identical target IDs and conventions. A sample confined to dates supported by one DE441 part avoids downloading both for this check. Report vector and angular differences separately, including the Moon; do not treat exact equality as a requirement.
2. Historical/long-term extension: choose dated study windows after the textual epoch is settled, then acquire the required DE441 part(s). If an interval crosses the part boundary, validate overlap and use deterministic coverage-based routing.

Never silently blend ephemerides or fall back to another solution. A DE441 result must retain its own manifest and reference label; it must not be merged into a dataset labeled DE440.

Cross-check selected raw vectors with Horizons using matching target IDs, Earth center, TDB epochs, ICRF axes, explicit units, and `VEC_CORR=NONE`. Its vector API exposes these settings. Save queries, raw responses, and actual source headers; service defaults or future source updates must not silently change the reference. [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html)

Horizons is a check on extraction and conventions, not an independent astronomical theory when it uses the same underlying ephemeris. Horizons commonly uses DE441 for these targets, so a Horizons result must not be presented as an exact DE440 extraction check. Verify its actual source header: for DE441, compare like-for-like with the local DE441 sensitivity sample; compare against DE440 separately as a reference-solution difference. An exact DE440 extraction check should use a second reading path to the same kernel or an explicitly DE440-derived fixture. If local downloads are impractical, a cached Horizons-based alternative can be proposed, but it must identify its actual ephemerides and service constraints; it does not automatically satisfy the DE440 baseline requirement.

### Metrics and interpretation

- Signed longitude residual wrapped to `[-180°, 180°)`; report in degrees and arcminutes.
- Median absolute error, RMSE, 95th percentile absolute error, maximum absolute error, and signed bias with a defined circular convention. Do not average wrapped angles across the discontinuity naively.
- Plot residuals over time and by decade. Estimate drift only with documented unwrapping and a justified interval; distinguish drift from periodic structure.
- Use full angular separation only when both models supply longitude and latitude in the same frame.
- Refine event brackets using continuous model evaluation; daily samples alone cannot establish precise event timing. Verify event correspondence and identify missed/extra events.
- Report original sourced parameters separately from fitted variants. Prespecify training/evaluation intervals before fitting; never optimize and report accuracy on the same dates without disclosure.
- Separate software tolerances, coordinate-convention sensitivity, parameter uncertainty, and model discrepancy. Do not invent an acceptable historical error threshold.

## Implementation phases and acceptance gates

| Phase | Work and artifacts | Completion gate |
| --- | --- | --- |
| 1. Research specification | Edition/translation choice; verse-to-rule and parameter tables; epoch/origin definitions; ambiguity log. Start with I.15–16, I.29, I.37, I.53; II.15–22, II.29, II.31–39, II.45 as mapped in README. | Every implemented historical operation has an explicit citation or an explicit reconstruction assumption. Unresolved choices that affect absolute longitude are documented and resolved or treated as alternatives. |
| 2. Reference pipeline | Pinned environment, full DE440 acquisition/manifest, coverage checks, cached fixtures, raw/derived exports, and a fixed DE440–DE441 sensitivity sample. | DE440 smoke tests succeed for 1900, J2000, and the final sample; same-kernel extraction/frame checks pass declared tolerances. Archive DE440–DE441 differences and check local DE441 against matching-source Horizons results. Cross-part tests apply only when both DE441 parts are used. |
| 3. Solar reconstruction | Historical mean motion, sine table/interpolation policy, apsidal motion/position, manda periphery, inverse lookup, signs, and elapsed-day conversion. Preserve demonstration model separately. | Edition-based worked examples where available; otherwise explicit rule-by-rule independent calculations. Numerical checks cover quadrants, wrap, interpolation boundaries, and units. Do not invent a worked example. |
| 4. First benchmark | Solar residual dataset against DE440, summary tables, plots, coordinate-convention and reference-solution sensitivity, and README/report updates. Compare historical reconstruction and existing approximation separately. | Exactly aligned dates/frames; no unexplained missing rows; reproducible metrics; all defects affecting interpretation disclosed. If epoch/origin remains unresolved, label the artifact provisional and do not mark the historical benchmark complete. |
| 5. Moon and planets | Sourced body constants, latitude where supported, node/apsidal handling, śīghra geometry and II.43–44 sequence. Add phases/stations. | Per-body textual and numerical checks pass before publishing positional or event accuracy claims. |
| 6. Other systems | A sourced Ptolemaic construction; specified Keplerian elements, orientation, and evolution assumptions. | Each model predicts the same defined observable; calibration and historical fidelity remain separately reported. |
| 7. Local geometry and eclipses | Solar altitude/shadows; conjunction/opposition and both-node screening; disc/shadow geometry, parallax, contact/visibility calculations as separate increments. | Validate against independent event catalogs or worked cases with matched definitions; quantify misses/false positives for screening. Detailed eclipse results wait for complete geometry. |
| 8. Research release | Reproduction commands, dependency lock, source manifest, charts, methodology, defects, and open points. | A clean rerun reproduces archived results within declared tolerances without silently changing kernels or parameters. |

The first implementation milestone is phases 1–4. A seven-body reference export is useful in phase 2 but does not imply seven historical models are implemented. DE441 becomes the primary reference for later ancient-date studies; a long-term series spanning ancient and modern dates should use DE441 consistently and retain the DE440 comparison separately. Historical-era comparisons require a separate date/calendar/precession/ΔT feasibility review; DE441's long coverage is not proof of equal accuracy at all epochs.

## Proposed artifacts and dependencies

Proposed layout, to be created only during implementation:

- `docs/methodology.md`, `docs/source_map.md`, and `docs/open_points.md` for conventions, verse mappings, and research decisions.
- `src/astronomy/` for reference access, time/frame conversions, historical models, metrics, and event calculations.
- `scripts/` for reference generation and reproducible comparisons.
- `tests/` with small local fixtures and meaningful numerical/textual cases; large network tests remain explicit integration checks.
- `data/manifests/` for URLs, checksums, segment/coverage inventory, and target maps; ignored local kernel/raw-data directories.
- `results/` for residual CSVs, summary tables, figures, and a run manifest. Commit compact reviewable artifacts; exclude multi-GB kernels.

Expected core packages: Astropy, jplephem, NumPy, and Matplotlib. Use pandas only if its table operations justify it; add SciPy for event root finding if needed. SpiceyPy is optional, not required for the initial Astropy route. Select mutually compatible released versions and pin them after a smoke test; no versions have been tested here.

Reference records should include time, body label, target/center IDs, raw vectors, derived coordinates, units, and a manifest identifier. Historical records should identify model/edition/parameter set, elapsed-day convention, and output frame. The run manifest must record kernel hashes, software versions, code revision, input settings, transformation definitions, and any fitted parameters. Unsupported outputs remain absent with an explicit reason, never fabricated or silently zero-filled.

## Risks, open decisions, and effort boundaries

| Risk/open decision | Handling |
| --- | --- |
| No selected edition or reliable worked example | Resolve in phase 1; use README's transcriptions as leads, not a critical edition. |
| Epoch/meridian/day and longitude origin unresolved | Allow reference extraction and relative-motion studies to proceed; block unique absolute historical accuracy claims. |
| Recurrence rounding differs from listed table | Keep explicit tabulated values and recurrence experiment distinct; document evidence for any rounding policy. |
| Download size or unavailable network | Start with the approximately 114 MB DE440 file; reserve multi-GB DE441 transfers for the selected sensitivity/historical windows. Inspect capacity, resume safely, and hash files. |
| Reference-solution, cross-part, or target mismatch | Keep DE440/DE441 outputs distinct; test coverage and any DE441 overlap, log numerical IDs, and reject unsupported segments/dates. |
| Frame transformation introduces observational corrections | Check raw vectors first; separate geometric rotation from apparent/topocentric pipelines. |
| Modern fitting disguises historical error | Preserve unmodified historical baseline and use held-out dates for fitted variants. |
| Eclipses dominate scope | Keep eclipse work outside the first milestone and require independent geometry/event validation. |
| Unknown paper's methods | Obtain citation before claiming reproduction. |

No reliable wall-clock delivery estimate follows from the current evidence: package setup, transfer speed, selected edition, and interpretive work are unresolved. Measure reference-pipeline runtime on a small batch before estimating the full run. The data volume is feasible; historical research and later eclipse implementation are the main scope uncertainties.

## Checks completed for this plan

- Rechecked the file inventory when preparing the plan. This plan update changes documentation only.
- Inspected official kernel coverage, target mappings, Astropy loading behavior, and Horizons vector settings. Updated the reference choice to DE440 for 1900–2026 and DE441 for historical/long-term work based on the cited JPL guidance.
- Counted 46,021 daily epochs using standard-library date arithmetic; seven targets yield 322,147 records.
- Checked installed-package availability without installing anything.
- No kernels downloaded, no supplied sample executed, and no astronomical accuracy results generated. Documentation feasibility is established; operational feasibility still requires the phase 2 smoke tests.

The existing [README audit](README.md) remains the defect and source-mapping baseline. Implementation begins only after the user confirms the plan.
