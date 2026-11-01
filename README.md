# Astronomy: source and implementation audit

Research updated: 1 November 2026. Reviewed baseline commit: `ae77512` (`Added Readme on current research`), including the newly added `ancient-sin-tables.py` and `surya-siddhanta.py`. The original three scripts are unchanged from the earlier audit at `0e9b8f1`.

This repository contains five Python demonstrations comparing selected Indian, Greek, and modern astronomical calculations. It does **not** currently implement a complete Sūrya Siddhānta, Ptolemaic planetary model, or observational ephemeris. None of the five scripts supplies a bibliography, edition, chapter, or verse citation. The references below are research mappings established by comparing the code with accessible texts; they do not establish the author's intended sources.

## Scope and evidence

Reviewed all five scripts and the repository's tracked-file inventory. `LICENSE` is licensing material, not astronomical evidence. No other astronomical texts, datasets, tests, or dependency specifications were present. No Python source was changed for this audit.

| File | Actual scope |
| --- | --- |
| `astro_measures.py` | Mean-motion ratio, generic circular-vector model, elliptic anomaly solver |
| `small-angle-formula.py` | Continuous sine/chord evaluations and linear approximations |
| `surya-siddhanta-kepler.py` | Simplified sinusoidal correction compared with a Kepler solver |
| `ancient-sin-tables.py` | Floating-point difference recurrence over 24 steps |
| `surya-siddhanta.py` | Proportional elapsed years, simplified angular corrections, shadow triangle, node-distance flags |

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

### References for the new files

The distinction here is between a verified matching constant, a related historical rule, and an implementation that actually follows that rule.

| Repository location | Exact reference and assessment |
| --- | --- |
| [ancient-sin-tables.py](ancient-sin-tables.py#L4), lines 4–37 | **Sūrya Siddhānta II.15–16** is the relevant sine-generation rule: initial sine 225, then successive differences. **II.17–22** supplies the explicit table. The floating-point recurrence is related to II.15–16 but does not reproduce that table. Its comment “ancient recursive algorithm” names no text; attribution to Āryabhaṭa or another author is unestablished. [II.15](https://www.siva.sh/surya-siddhanta/2/11-15), [II.16 and translation notes](https://www.siva.sh/surya-siddhanta/2/16-20), [II.22](https://www.siva.sh/surya-siddhanta/2/21-25). |
| [surya-siddhanta.py](surya-siddhanta.py#L6), lines 6–19 | The constants have the same **I.15–16, I.37, II.22** mappings as above. `siddhanta_sine` and `siddhanta_arcsine` use modern continuous functions; the corresponding historical lookup/interpolation rules are **II.31–33**. [II.31–35](https://www.siva.sh/surya-siddhanta/2/31-35). |
| [surya-siddhanta.py](surya-siddhanta.py#L25), lines 25–32 | `compute_ahargana` is a proportional conversion from fractional model solar years to days. **I.48–50** provides a calendar-based elapsed-day procedure with elapsed months, intercalations, and omitted lunar days. The function does not implement it. **No verse was verified for this exact one-line conversion.** [I.46–50](https://www.siva.sh/surya-siddhanta/1/46-50). |
| [surya-siddhanta.py](surya-siddhanta.py#L38), lines 38–52 and 142 | Manda-related references remain **II.29, II.38–39, II.45**. For the example's claimed Mars parameter, **II.35** gives manda peripheries 75°/72°, not 13°. The code does not document a conversion that could justify treating 13 as another kind of parameter. [II.35](https://www.siva.sh/surya-siddhanta/2/35), [II.38–39](https://www.siva.sh/surya-siddhanta/2/36-40). |
| [surya-siddhanta.py](surya-siddhanta.py#L58), lines 58–72 and 151 | **II.36** matches the example's Mars śīghra periphery 235°; **II.37** gives 232° at the other specified quadrant endpoints. This verifies the number as a periphery, not a radius. The related calculation is **II.38–42**, with a variable hypotenuse, and the sequence is **II.43–44**. The function does not implement these operations. [II.36–40](https://www.siva.sh/surya-siddhanta/2/36-40), [II.41–45](https://www.siva.sh/surya-siddhanta/2/41-45). |
| [surya-siddhanta.py](surya-siddhanta.py#L78), lines 78–93 and 158 | **III.21–22** describes a noon gnomon shadow and hypotenuse via sine/cosine ratios, using the gnomon's height in digits (commonly 12). The code's `height/tan(altitude)` is equivalent right-triangle geometry when the noon altitude is supplied. It accepts an arbitrary altitude and calculates no local time. This correspondence does not establish exclusive dependence on this text. [III.21–25](https://www.siva.sh/surya-siddhanta/3/21-25). |
| [surya-siddhanta.py](surya-siddhanta.py#L99), lines 99–121 | **IV.6–9** relates eclipse geometry to the node and Sun/Earth's shadow, and distinguishes new-moon conjunction from full-moon opposition. **IV.10** concerns obscuration using latitude and disc sizes; **V.1–2** concerns solar-eclipse parallax. The function implements none of those full procedures. **No exact verse or other primary-text source was verified for its fixed 18°/12° limits.** [IV.6–10](https://www.siva.sh/surya-siddhanta/4/6-10), [V.1–5](https://www.siva.sh/surya-siddhanta/5/1-5). |

The III.21–22 gnomon instruction spans the verse boundary; the hosting site's English blocks are not consistently aligned to individual Sanskrit verses. The range is intentional. The new function names `ahargana`, `manda`, `sighra`, `sanku`, and `grahana` identify subjects, not proof of textual fidelity.

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

### Defects demonstrated in the new files

12. **High — generated sine table does not reproduce the cited table.** `ancient-sin-tables.py:33–37` retains unrounded differences throughout. It gives `1717.11` at 30° and `3375.40729536156` at 90°, whereas the listed historical entries are 1719 (**II.18**) and 3438 (**II.22**). The endpoint deficit is `62.59270463844`, or about `1.8206%`. It is a recurrence experiment, not a transcription or faithful reproduction of the 24-entry table. The current source does not establish which rounding/correction policy was intended; choosing one to force agreement would require further evidence. [II.18](https://www.siva.sh/surya-siddhanta/2/18), [II.22](https://www.siva.sh/surya-siddhanta/2/21-25).

13. **High — angular units and periphery scaling are wrong in the new corrections.** `siddhanta_arcsine` already returns degrees, but both callers divide its result by 60. That extra conversion reduces their own computed angular correction by a factor of 60. Separately, they feed `parameter*sin(angle)` directly as an R-sine value, despite the example's 235 being a periphery in reference-circle degrees. II.39 instead scales the R-sine by the rectified periphery divided by 360, and śīghra requires additional geometry. Removing `/60` alone would not make either function historically correct. [II.39](https://www.siva.sh/surya-siddhanta/2/39).

14. **High — eclipse flags omit phase and the opposite node.** `sun_longitude` is unused. Inputs `(moon, sun, node) = (0, 0, 0)` and `(0, 90, 0)` both return both flags `True`; changing the Sun by 90° has no effect. This is not even a combined phase-and-node screen. The comment says “nearest node,” but the function checks only one supplied node, omitting its antipode. `(180, 180, 0)` reports node distance 180° even though the Moon is at the opposite node. The demo likewise prints both eclipse flags for a single configuration. These are defects in the advertised calculation, regardless of whether the flags are called “possible.” Compare the phase distinctions in [IV.7–9](https://www.siva.sh/surya-siddhanta/4/6-10).

15. **Medium — unnormalized angles can produce negative node distances.** `predict_eclipse(720, 0, 0)` returns distance `-360` and both flags `True`. The function needs explicit angle normalization or a documented and enforced input range.

16. **Medium — invalid inverse-sine inputs are silently accepted.** `siddhanta_arcsine(3438)` and `siddhanta_arcsine(6876)` both return 90°. Clamping can be justified for tiny floating-point overshoots, but here arbitrarily invalid R-sine values are hidden without any validation.

17. **Medium — advertised capabilities are absent.** `compute_sighra_correction` computes a single angular adjustment from supplied inputs; it supplies no time series or demonstrated retrograde loop. `predict_eclipse` returns no obscuration, contact times, or local visibility despite mentioning obscuration in its docstring. The elapsed-day function is not a calendar-to-ahargaṇa conversion. These labels need narrowing or the missing calculations need implementation.

18. **Low — shadow input domain is unchecked.** A positive gnomon and altitude between 0° and 90° give the expected elementary geometry. However, `compute_gnomon_shadow(12, 120)` returns a negative shadow, and negative heights are also accepted. At/below the horizon it returns infinity as an undocumented sentinel. It supplies no latitude, date, hour-angle, or local-time inference.

## Reproduction and checks performed

Only Python's standard library is required:

```sh
python3 astro_measures.py
python3 small-angle-formula.py
python3 surya-siddhanta-kepler.py
python3 ancient-sin-tables.py
python3 surya-siddhanta.py
```

All five commands completed successfully during the updated audit. Selected observed results:

| Demonstration | Output |
| --- | --- |
| Mean solar longitude after 1,000,000 input days | 282.6546° |
| Arbitrary epicycle example | distance 11.1167; angle 155.4171° |
| True anomaly at M = 45°, e = 0.0167 | 46.3733° |
| R-sine at 5 arcminutes | 5.0004; reported error 0.0073% |
| Comparison at day 60 | 60.7771° versus 60.7978°; difference 0.0207° |
| Generated recurrence at 90° | 3375.41 versus continuous R-sine 3438.00 |
| New elapsed-day example, 1,950,500.5 years | 712,437,387.15 days |
| New manda example, mean 120°, parameter 13 | correction 0.0031270892°; result 120.0031270892° |
| New śīghra example, parameter 235, elongation 45° | apparent longitude 120.0493° |
| Gnomon height 12, altitude 30° | shadow 20.7846; hypotenuse 24.0000 |
| New eclipse example, Moon 150.5°, Sun 150°, node 145° | distance 5.5°; both flags `True` |

These are reproducibility checks, not verification against a historical worked example or measured sky position. Arithmetic probes also confirmed the year length, radius rounding, coefficient comparison, and invalid-eccentricity exceptions described above. Direct calls reproduced the eclipse, inverse-sine, and shadow-domain defects in items 14–18. No automated test suite was added for this documentation-only update.

## Open research points and repair priorities

- Select and record a specific Sūrya Siddhānta edition/translation, its verse numbering, and page images. Cross-check the cited passages against that edition before treating this as a critical textual apparatus. Online access copies have visible defects: for example, the II.21 transcription at siva.sh prints a parenthetical `3401` while its English list gives `3409`; neither value is used by this repository. [Example](https://www.siva.sh/surya-siddhanta/2/21-25).
- Determine the intended planet, epoch, calendar conversion, longitude origin, and apsidal convention. These cannot be recovered reliably from the present examples.
- Establish provenance for `365.25`, `1.91`, `0.0167`, and the arbitrary epicycle parameters. Do not assign a verse to an unexplained constant merely because it produces plausible output.
- Either relabel the demonstrations as simplified modern analogies, or implement and document the cited historical rules, including tabular sine handling and manda correction. Validate against a worked example from the selected edition.
- Find a precise primary-text reference for the intended Ptolemaic planetary construction and for any claimed Kepler historical algorithm. Those exact attributions remain unresolved here.
- Define valid numerical domains, report solver convergence, remove import side effects, and add meaningful reference-case checks after the intended models are settled.
- Resolve the recurrence's historical rounding/correction convention against an edition and worked example. Do not infer an Āryabhaṭīya citation from shared sine-table terminology or the 225-minute step.
- Correct the new angular-unit errors and document whether each epicycle argument is a radius, a periphery, or an angular amplitude. Replace or justify the Mars manda example's `13` with an explicit derivation.
- Trace the fixed eclipse limits `18` and `12` to a specific passage if one exists; until then their Sūrya Siddhānta attribution is unverified. Require phase, both nodes, normalized angles, and appropriate geometry before describing the function as eclipse prediction.

No conclusions about textual priority, transmission, historical dating, or comparative observational accuracy follow from these scripts or the checks performed.
