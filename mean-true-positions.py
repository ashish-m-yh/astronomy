"""
The constants in the code represent foundational epochs, cosmic cycles, orbital frequencies, and geometric correction factors across all three astronomical systems.

---

### 1. Global & Time-Reference Constants

* **`target_jd = 2460676.5`**: The Julian Date (JD) for January 1, 2026. This is the target point in time for which all three models calculate planetary positions.
* **`ayanamsa = 24.18`**: The **Lahiri Ayanamsa** value for 2026. Because Indian astronomy calculates *sidereal* positions (relative to fixed background stars) and Greek/modern systems calculate *tropical* positions (relative to the vernal equinox), this constant shifts the Surya Siddhanta output by ~24.18° so they can be compared apples-to-apples.

---

### 2. Surya Siddhanta Constants

Ancient Indian astronomy models time using massive cosmic cycles called **Mahayugas** (4.32 million solar years).

* **`kali_yuga_jd = 588465.5`**: The starting Julian Date for the current cosmic age (*Kali Yuga*), traditionally set at midnight on February 18, 3102 BCE. The script measures time elapsed (*ahargana*) from this exact moment.
* **`CIVIL_DAYS_IN_MAHAYUGA = 1577917828`**: The total number of civil (sunrise-to-sunrise) days in one complete Mahayuga according to the Surya Siddhanta.
* **`revs` (Revolutions)**: The exact integer number of times a planet orbits the zodiac in one Mahayuga. For example, the Sun (`4,320,000`) completes 4.32 million orbits, matching the number of solar years in a Mahayuga.
* **`m_apo` (Manda Apogee)**: The position in degrees where a planet is farthest from the Earth (apogee/aphelion). This establishes the asymmetry of the orbit.
* **`m_max` (Maximum Manda Equation)**: The maximum angular correction (in degrees) caused by orbital eccentricity (the equivalent of Kepler's equation of center).
* **`s_revs`, `s_apo`, `s_max` (Sighra Parameters)**: Constants handling **synodic motion** (the planet's apparent loop-de-loops caused by Earth's own motion around the Sun). `s_revs` represents the planet's synodic/epicyclic revolutions in a Mahayuga, and `s_max` is the maximum size of the epicyclic correction.

---

### 3. Greek (Ptolemaic / Almagest) Constants

* **`1448638.2` (Epoch of Nabonassar)**: February 26, 747 BCE. Ptolemy and ancient Babylonian astronomers anchored their planetary tables to the reign of King Nabonassar.
* **`greek_params` lists `[daily_motion_deg, base_long, max_eq]**`:
* **Daily Motion**: The average number of degrees the planet moves across the sky each day.
* **Base Longitude**: The planet's calculated position at the exact moment of Nabonassar's epoch.
* **Max Equation (`max_eq`)**: The peak amplitude of the epicyclic correction used to shift uniform circular motion into a variable speed matching observations.


* **Anomaly offsets (e.g., `45.0`, `70.0`, `110.0`)**: Geometric phase shifts used in the script to approximate the angular distance between the planet's deferent center and its epicycle or solar alignment.

---

### 4. Modern IAU Constants

* **`2451545.0` (J2000.0 Epoch)**: Noon on January 1, 2000. Modern dynamical astronomy uses this exact Julian Date as the zero-point for all time calculations.
* **`36525.0`**: The number of days in a **Julian century** ($365.25 \times 100$). The variable `d_centuries` measures how many centuries have passed since January 1, 2000.
* **Polynomial Coefficients (e.g., `280.46646 + 36000.76983 * d_centuries`)**: Empirical formulas derived from high-precision numerical integration of the solar system. The first number is the planet's mean longitude at J2000.0, and the second number is its secular rate of motion per century, accounting for long-term gravitational interactions.

### 1. The Greek (Ptolemaic) Constants

The numbers in `greek_params` originate directly from **Claudius Ptolemy’s *Almagest*** (written around 150 CE) and the centuries of Babylonian observational data that preceded it.

* **The Epoch (Nabonassar):** The baseline date used in the script (`Feb 26, 747 BCE`, Julian Date `1448638.2`) is the **Era of Nabonassar**. Ptolemy chose this historical starting point because it marked the beginning of reliable, continuous Babylonian king-lists and eclipse records available to Greek astronomers.
* **Daily Motions & Max Equations:** In the *Almagest* (specifically Books III through XIII), Ptolemy calculated precise tables of mean motion for each planet and the maximum angular deviations (equations) caused by their epicycles and eccentric paths.
* **In the Script:** The author of this script extracted or approximated Ptolemy’s tabulated daily rates (e.g., the Sun’s mean motion of ~0.9856°/day) and maximum equations (e.g., Mars' whopping 39.5° maximum equation) and hardcoded them into a compact Python dictionary to simulate a simplified geocentric calculation.

---

### 2. The Modern IAU Constants

The numbers in `modern_planets` come from **modern analytical planetary theories** adopted by the **International Astronomical Union (IAU)**.

* **The Foundation (Newcomb & VSOP):** In the late 19th century, Canadian-American astronomer **Simon Newcomb** calculated comprehensive analytical theories for the motions of all the major planets. In the late 20th century, these were refined by modern theories like **VSOP87** (Variations Séculaires des Orbites Planétaires), developed by French astronomers at the Bureau des Longitudes.
* **Where You Find Them Today:** These exact polynomial coefficients (e.g., the Sun's formula `280.46646 + 36000.76983 * d_centuries`) are standard reference formulas published in astronomical handbooks, most notably **Jean Meeus’s *Astronomical Algorithms*** and the *Explanatory Supplement to the Astronomical Almanac*.
* **How They Work:**
* The **first constant** (e.g., `280.46646°` for the Sun) is the planet's exact geometric mean longitude at the J2000.0 epoch (January 1, 2000, at 12:00 Terrestrial Time).
* The **second constant** (multiplied by `d_centuries`) is the planet's mean speed expressed in degrees per Julian century, incorporating long-term gravitational perturbations from other planets.

"""

import numpy as np

target_jd = 2460676.5  # January 1, 2026
kali_yuga_jd = 588465.5
ahargana = target_jd - kali_yuga_jd
CIVIL_DAYS_IN_MAHAYUGA = 1577917828
ayanamsa = 24.18  # Lahiri Ayanāṃśa for 2026

# =====================================================================
# 1. Surya Siddhanta Pipeline (Sidereal -> Tropical)
# =====================================================================
ss_planets = {
    "Sun":     { "revs": 4320000,  "m_apo": 77.0,  "m_max": 2.14,  "s_revs": 4320000,  "s_apo": 77.0,  "s_max": 0.0 },
    "Mercury": { "revs": 17937060, "m_apo": 220.0, "m_max": 6.33,  "s_revs": 4322680,  "s_apo": 30.0,  "s_max": 28.0 },
    "Venus":   { "revs": 7022388,  "m_apo": 80.0,  "m_max": 1.16,  "s_revs": 575764,   "s_apo": 70.0,  "s_max": 47.0 },
    "Mars":    { "revs": 2296832,  "m_apo": 130.0, "m_max": 11.0,  "s_revs": 4320000 - 2296832, "s_apo": 130.0, "s_max": 40.0 },
    "Jupiter": { "revs": 364220,   "m_apo": 170.0, "m_max": 5.0,   "s_revs": 4320000 - 364220,  "s_apo": 170.0, "s_max": 11.5 },
    "Saturn":  { "revs": 146568,   "m_apo": 240.0, "m_max": 6.5,   "s_revs": 4320000 - 146568,  "s_apo": 240.0, "s_max": 6.5 }
}

def compute_surya_planet(params):
    revs = (ahargana * params["revs"]) / CIVIL_DAYS_IN_MAHAYUGA
    mean_long = (revs % 1.0) * 360.0
    manda_anomaly = mean_long - params["m_apo"]
    manda_eq = params["m_max"] * np.sin(np.radians(manda_anomaly))
    mandaspasta = (mean_long + manda_eq) % 360.0

    if params["s_max"] > 0 and params["revs"] != params["s_revs"]:
        s_revs = (ahargana * params["s_revs"]) / CIVIL_DAYS_IN_MAHAYUGA
        sighra_long = (s_revs % 1.0) * 360.0
        sighra_anomaly = sighra_long - mandaspasta
        sighra_eq = params["s_max"] * np.sin(np.radians(sighra_anomaly))
        true_sidereal = (mandaspasta + sighra_eq) % 360.0
    else:
        true_sidereal = mandaspasta
    return (true_sidereal + ayanamsa) % 360.0

# =====================================================================
# 2. Greek (Ptolemaic / Almagest) Method (Tropical Frame)
# =====================================================================
# Epoch of Nabonassar: Feb 26, 747 BCE = JD 1448638.2
days_nabonassar = target_jd - 1448638.2

# Ptolemaic mean daily motions and base parameters (Almagest tables approximation)
# Format: { Planet: [daily_motion_deg, epoch_base_long, max_equation_deg] }
greek_params = {
    "Sun":     [0.98564735, 266.25, 2.383],
    "Mercury": [3.09841460, 185.00, 22.00],  # Combined eccentric/epicyclic anomaly effect
    "Venus":   [0.98564735, 266.25, 47.10],  # Tied to solar mean motion (sun-centered anomaly)
    "Mars":    [0.52403300, 312.00, 39.50],
    "Jupiter": [0.08309120, 168.00, 11.50],
    "Saturn":  [0.03345970, 298.00, 6.50]
}

def compute_greek_planet(name):
    motion, base_long, max_eq = greek_params[name]
    mean_long = (base_long + days_nabonassar * motion) % 360.0

    # For inner planets (Mercury/Venus) and outer planets, Ptolemy used an eccentric/epicycle model 
    # where the anomaly oscillates relative to the solar/center position.
    if name == "Mercury":
        anomaly = (mean_long - 45.0) % 360.0 # Approximate deferent/epicycle center offset
    elif name == "Venus":
        anomaly = (mean_long - 70.0) % 360.0
    else:
        anomaly = (mean_long - 110.0) % 360.0

    eq = max_eq * np.sin(np.radians(anomaly))
    return (mean_long + eq) % 360.0

# =====================================================================
# 3. Modern IAU Method (Tropical Frame)
# =====================================================================
d_centuries = (target_jd - 2451545.0) / 36525.0

modern_planets = {
    "Sun":     (280.46646 + 36000.76983 * d_centuries) % 360.0,
    "Mercury": (252.250906 + 149474.072246 * d_centuries) % 360.0,
    "Venus":   (181.979801 + 58517.815676 * d_centuries) % 360.0,
    "Mars":    (355.45332 + 19140.299331 * d_centuries) % 360.0,
    "Jupiter": (34.351519 + 3034.905674 * d_centuries) % 360.0,
    "Saturn":  (50.077444 + 1222.113794 * d_centuries) % 360.0
}

# =====================================================================
# Print Synchronized Multi-Model Comparison Table
# =====================================================================
print(f"{'Planet':<10} | {'Surya Siddhanta':<18} | {'Ptolemaic (Greek)':<18} | {'Modern IAU':<15}")
print("-" * 69)
for planet in ss_planets:
    ss_val = compute_surya_planet(ss_planets[planet])
    greek_val = compute_greek_planet(planet)
    mod_val = modern_planets[planet]
    print(f"{planet:<10} | {ss_val:>14.2f}°    | {greek_val:>14.2f}°    | {mod_val:>10.2f}°")
