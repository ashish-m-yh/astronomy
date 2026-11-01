# Astronomy: source and implementation audit

Research date: 1 November 2026. Reviewed baseline commit: `0e9b8f1` (`Add files via upload`).

This repository contains three Python demonstrations comparing selected Indian, Greek, and modern astronomical calculations. It does **not** currently implement a complete Sūrya Siddhānta, Ptolemaic planetary model, or observational ephemeris. None of the original scripts supplies a bibliography, edition, chapter, or verse citation. The references below are research mappings established by comparing the code with accessible texts; they do not establish the author's intended sources.

## Scope and evidence

Reviewed all three scripts and the repository's tracked-file inventory. `LICENSE` is licensing material, not astronomical evidence. No other astronomical texts, datasets, tests, or dependency specifications were present. No Python source was changed for this audit.

Chapter/verse notation below means, for example, **I.53 = chapter 1, verse 53**. Sanskrit text and English translations were checked in the linked online transcriptions. These are access copies, not a manuscript collation. Several pages contain transcription/OCR errors; conclusions below use the specific passages identified, not an assumption that every number on a hosting site is correct. Authorial provenance and edition-level verification remain open.

## Exact code-to-text references

| Repository location | Claim or operation | Textual reference and assessment |
| --- | --- | --- |
| [astro_measures.py](astro_measures.py#L7), lines 7–18 | Mean longitude from elapsed days and revolutions | **Sūrya Siddhānta I.53** gives the elapsed-days × revolutions ÷ civil-days rule. The code retains the fractional revolution and converts it to degrees. The translation states the rule with kalpa totals; using yuga totals preserves the ratio because **I.40** scales both by 1,000. This is a mathematical correspondence, subject to the missing epoch discussed below. [I.51–55](https://www.siva.sh/surya-siddhanta/1/51-55), [I.36–40](https://www.siva.sh/surya-siddhanta/1/36-40). |
| [astro_measures.py](astro_measures.py#L11), lines 11–13 | 4,320,000 solar years per great age; 1,577,917,828 civil days | **I.15–16** supplies the age's solar-year count; **I.37** explicitly supplies the civil-day count. These are different quantities, not interchangeable units without the implied year length. [Chapter I, I.15–16](https://www.swaveda.com/texts/surya-siddhanta/1/), [I.37](https://www.siva.sh/surya-siddhanta/1/37). |
| [astro_measures.py](astro_measures.py#L21), lines 21–25 | Sun: 4,320,000 revolutions per yuga | **I.29** supplies this count. The angular subdivision into 360 degrees per revolution is given in **I.28**. [I.26–30](https://www.siva.sh/surya-siddhanta/1/26-30). |
| [small-angle-formula.py](small-angle-formula.py#L8), lines 8–22 | Jya / R-sine with radius 3,438 | **II.15–16** concerns sine generation; **II.17–22** lists the 24 tabular sines, ending in **II.22** with 3,431 and 3,438. These support the traditional scale. They do not make a call to Python's `math.sin` a historical table implementation. [II.16–20](https://www.siva.sh/surya-siddhanta/2/16-20), [II.21–25](https://www.siva.sh/surya-siddhanta/2/21-25). |
| [small-angle-formula.py](small-angle-formula.py#L19), lines 19–20 | Shortcut `R*sin(theta) ≈ theta_minutes` | This is a modern small-angle interpretation. **No exact verse establishing this standalone shortcut was verified.** The relevant historical computational rules are **II.31–32**, interpolation at 225-arcminute intervals, and **II.33**, inverse interpolation. None is implemented here. [II.31–35](https://www.siva.sh/surya-siddhanta/2/31-35). |
| [surya-siddhanta-kepler.py](surya-siddhanta-kepler.py#L7), lines 7–25 | Mean longitude plus a manda correction | The relevant passages are **II.29** (kendra from apsis minus planet), **II.34** (solar/lunar manda epicycle sizes), **II.38–39** (rectified periphery and conversion of the sine result to an arc), and **II.45** (addition/subtraction by half-orbit). The implemented `1.91*sin(mean_longitude)` is only a simplified analogy, not these rules. [II.26–30](https://www.siva.sh/surya-siddhanta/2/26-30), [II.31–35](https://www.siva.sh/surya-siddhanta/2/31-35), [II.36–40](https://www.siva.sh/surya-siddhanta/2/36-40), [II.45 translation](https://www.swaveda.com/texts/surya-siddhanta/2/). |
| [small-angle-formula.py](small-angle-formula.py#L30), lines 30–43 | Ptolemaic chord, radius 60 | **Ptolemy, Almagest I.10**, establishes diameter 120 and the geometrical chord construction; **I.11** is the chord table. `120*sin(theta/2)` is a modern trigonometric expression of that geometry. The code does not reproduce the historical table construction or establish a textual source for its linear shortcut. [Toomer translation, I.10–11, printed pp. 48–60](https://www.mathship.hlevkin.com/900/Astronomy/PtolemyAlmagest.pdf). |
| [astro_measures.py](astro_measures.py#L33), lines 33–58 | “Ptolemaic” deferent and epicycle | The code sums two uniform circular vectors with arbitrary example parameters. **No exact Almagest passage or historical parameter set was established for this function.** Its name is insufficient evidence of a faithful planetary model. |
| [astro_measures.py](astro_measures.py#L66), lines 66–87; [surya-siddhanta-kepler.py](surya-siddhanta-kepler.py#L31), lines 31–59 | Kepler equation and true anomaly | Both solve `M = E - e*sin(E)` numerically and convert eccentric to true anomaly. They are modern numerical implementations. **No original Kepler passage was verified for these exact algorithms**, including Newton–Raphson. A digitized *Astronomia nova* is available for further primary-source checking; its existence does not establish this code's provenance. [1609 work and scans](https://sourcelibrary.org/book/kepler-astronomia-nova-1609-prague-kepler). |

No script names the Āryabhaṭīya, Brahmasphuṭasiddhānta, Siddhāntaśiromaṇi, or another Indian treatise. Similar mathematics alone cannot identify one of these as the source. Ptolemy and Kepler are named, but their book titles are research context supplied here, not citations found in the repository. Book/chapter references are appropriate for those works; inventing Sanskrit-style verse references for them would be misleading.

## Defects and limitations

### Historical attribution and comparison

1. **High — the “Surya Siddhanta” longitude comparison misrepresents the implemented method.** In `surya-siddhanta-kepler.py:7–25`, `manda_radius` is used as an angular amplitude in degrees, although it is described as an epicycle radius. No source for `1.91` is supplied. II.34 instead gives solar manda peripheries of 14° and 13°40′ at the specified quadrant endpoints. A periphery measured in degrees of the reference circle is not an angular correction amplitude. II.38–39 requires further operations. [II.34](https://www.swaveda.com/texts/surya-siddhanta/2/), [II.38–39](https://www.siva.sh/surya-siddhanta/2/36-40).

2. **High — apsis, phase, and sign are not aligned.** The historical kendra is apsis minus planetary place (II.29), while the script simply uses mean longitude and always adds its signed sine. It provides no apsidal longitude. The Kepler calculation starts mean anomaly at periapsis. Agreement between these arbitrarily aligned functions cannot validate a historical solar longitude calculation. [II.29](https://www.siva.sh/surya-siddhanta/2/26-30), [II.45](https://www.swaveda.com/texts/surya-siddhanta/2/).

3. **High — small differences do not demonstrate historical accuracy.** Independently expanding the implemented Kepler equation to first order in eccentricity gives `v ≈ M + 2e*sin(M)` (angles in radians). For the code's `e = 0.0167`, the coefficient in degrees is `1.9136790357`, close to `1.91`. This mathematical observation explains why the functions can agree closely; it is **not evidence** of where the author obtained the constant. There are no observations or independently sourced reference positions in the repository.

4. **Medium — inconsistent year parameters.** The mean-motion constants imply `1577917828 / 4320000 = 365.2587564815` civil days per solar revolution. The comparison instead uses `365.25` for both functions. That is a deliberate-looking simplification with no documented justification; it is not the year implied by the other script's constants.

5. **Medium — “Exact Siddhantic R-sine” is an inaccurate label.** `small-angle-formula.py:16–17` evaluates a continuous modern sine at the traditional scale. It does not implement the table, recurrence, interpolation, or historical rounding. The nearby comment also treats `3438` as exactly one radian in arcminutes, whereas `10800/pi = 3437.7467707849`. With the rounded radius, the linearization is `3438*pi/10800 * theta_minutes`, not exactly `theta_minutes`. Thus the reported error includes scale rounding as well as sine linearization.

6. **Medium — no defined astronomical epoch or initial longitude.** `astro_measures.py:7–18` assumes zero longitude at zero elapsed days, and its example does not identify a calendar date or epoch. This is sufficient for a relative-motion demonstration, not a dated prediction. Historical elapsed-day preparation and reference conventions need to be specified before interpreting the result as a planetary place.

7. **Medium — generic circles are presented as a Ptolemaic model.** `astro_measures.py:33–58` contains no identified planet, historical constants, eccentric offset, equant, or epoch. The units of angular velocities are implicitly radians per time unit, and the epicycle angle is measured in the fixed coordinate axes. These choices need documentation before comparison with a particular historical construction.

### Numerical and software behavior

8. **Medium — missing input validation.** The elliptic solvers do not enforce `0 <= eccentricity < 1`; evaluating `compute_true_anomaly(45, 1.0)` raises `ZeroDivisionError`, and `1.1` raises `ValueError`. A zero orbital period also causes division by zero. These public functions do not describe such restrictions.

9. **Medium — convergence is not reported.** Both Newton loops stop after at most ten iterations and return an angle even if tolerance was not reached. There is no residual check, failure signal, or documented supported input range. This is a robustness gap; the default demonstrations did not show a convergence failure.

10. **Low — anomaly is labeled longitude.** `kepler_true_longitude` returns true anomaly relative to periapsis; an absolute orbital longitude also needs an orientation/reference. The name and comparison heading obscure this assumption.

11. **Low — import side effects and duplicated solver.** Importing `astro_measures.py` executes and prints its examples. Its Kepler solver is duplicated in the comparison script. There is no automated regression suite. The percentage-error expressions in the small-angle driver would divide by zero if its sample lists were extended to include zero; the existing lists avoid that case.

## Reproduction and checks performed

Only Python's standard library is required:

```sh
python3 astro_measures.py
python3 small-angle-formula.py
python3 surya-siddhanta-kepler.py
```

All three commands completed successfully during the audit. Selected observed results:

| Demonstration | Output |
| --- | --- |
| Mean solar longitude after 1,000,000 input days | 282.6546° |
| Arbitrary epicycle example | distance 11.1167; angle 155.4171° |
| True anomaly at M = 45°, e = 0.0167 | 46.3733° |
| R-sine at 5 arcminutes | 5.0004; reported error 0.0073% |
| Comparison at day 60 | 60.7771° versus 60.7978°; difference 0.0207° |

These are reproducibility checks, not verification against a historical worked example or measured sky position. Arithmetic probes also confirmed the year length, radius rounding, coefficient comparison, and invalid-eccentricity exceptions described above.

## Open research points and repair priorities

- Select and record a specific Sūrya Siddhānta edition/translation, its verse numbering, and page images. Cross-check the cited passages against that edition before treating this as a critical textual apparatus. Online access copies have visible defects: for example, the II.21 transcription at siva.sh prints a parenthetical `3401` while its English list gives `3409`; neither value is used by this repository. [Example](https://www.siva.sh/surya-siddhanta/2/21-25).
- Determine the intended planet, epoch, calendar conversion, longitude origin, and apsidal convention. These cannot be recovered reliably from the present examples.
- Establish provenance for `365.25`, `1.91`, `0.0167`, and the arbitrary epicycle parameters. Do not assign a verse to an unexplained constant merely because it produces plausible output.
- Either relabel the demonstrations as simplified modern analogies, or implement and document the cited historical rules, including tabular sine handling and manda correction. Validate against a worked example from the selected edition.
- Find a precise primary-text reference for the intended Ptolemaic planetary construction and for any claimed Kepler historical algorithm. Those exact attributions remain unresolved here.
- Define valid numerical domains, report solver convergence, remove import side effects, and add meaningful reference-case checks after the intended models are settled.

No conclusions about textual priority, transmission, historical dating, or comparative observational accuracy follow from these scripts or the checks performed.
