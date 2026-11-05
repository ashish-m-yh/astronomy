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
