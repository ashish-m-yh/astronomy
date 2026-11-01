import math

# ==========================================
# CONSTANTS & GLOBAL PARAMETERS
# ==========================================
R = 3438.0  # Siddhantic Radius in arc-minutes (1 radian)
MAHAYUGA_DAYS = 1577917828.0
MAHAYUGA_YEARS = 4320000.0


def siddhanta_sine(angle_deg):
  """Computes R-sine using Siddhantic scale R = 3438."""
  return R * math.sin(math.radians(angle_deg))


def siddhanta_arcsine(val):
  """Inverse R-sine returning degrees."""
  val_clamped = max(-1.0, min(1.0, val / R))
  return math.degrees(math.asin(val_clamped))


# ==========================================
# 1. AHARGANA (Elapsed Days Calculation)
# ==========================================
def compute_ahargana(solar_years_elapsed):
  """Computes the total number of civil days elapsed (Ahargana)

  from the beginning of the current Mahayuga epoch.
  """
  # Proportion of Mahayuga elapsed scaled by total civil days
  ahargana = (solar_years_elapsed / MAHAYUGA_YEARS) * MAHAYUGA_DAYS
  return ahargana


# ==========================================
# 2. MANDA-PHALA (Equation of the Center)
# ==========================================
def compute_manda_correction(mean_longitude, manda_radius):
  """Applies the Manda (slow/distance) correction.

  Accounts for orbital eccentricity (distance variation from apogee).
  """
  # Assume mean anomaly is longitude relative to apogee
  anomaly_rad = math.radians(mean_longitude)

  # Manda equation of the center using R-sine table method
  # Phala = (R * sin(anomaly) * manda_radius) / R (simplified proportional form)
  sine_val = math.sin(anomaly_rad)
  manda_correction_deg = siddhanta_arcsine(manda_radius * sine_val) / 60.0

  true_longitude = (mean_longitude + manda_correction_deg) % 360.0
  return true_longitude, manda_correction_deg


# ==========================================
# 3. SIGHRA-PHALA (Conjunction & Retrograde)
# ==========================================
def compute_sighra_correction(manda_longitude, sighra_radius, elongation):
  """Applies the Sighra (speed/conjunction) correction.

  Accounts for Earth's motion and produces apparent retrograde loops.
  """
  elongation_rad = math.radians(elongation)

  # Compute sighra anomaly offset using R-sine
  sine_val = math.sin(elongation_rad)
  sighr_correction_deg = (
      siddhanta_arcsine(sighra_radius * sine_val) / 60.0
  )  # Simplified adjustment

  apparent_longitude = (manda_longitude + sighr_correction_deg) % 360.0
  return apparent_longitude


# ==========================================
# 4. SANKU (Gnomon Shadow & Local Time)
# ==========================================
def compute_gnomon_shadow(gnomon_height, sun_altitude_deg):
  """Calculates the shadow length (Chhaya) cast by a vertical gnomon

  and determines local solar time indicators.
  """
  alt_rad = math.radians(sun_altitude_deg)

  # Shadow Length = Gnomon Height / tan(Altitude)
  if sun_altitude_deg <= 0:
    shadow_length = float("inf")
  else:
    shadow_length = gnomon_height / math.tan(alt_rad)

  # Hypotenuse of shadow triangle (Karna)
  karna = math.sqrt(gnomon_height**2 + shadow_length**2)
  return shadow_length, karna


# ==========================================
# 5. GRAHANA (Solar/Lunar Eclipse Prediction)
# ==========================================
def predict_eclipse(moon_longitude, sun_longitude, node_longitude):
  """Determines if an eclipse condition is met based on node proximity

  (Rahu/Ketu) and computes basic obscuration limits.
  """
  # Distance from Moon to the nearest node (Rahu/Ketu)
  distance_to_node = min(
      abs(moon_longitude - node_longitude),
      360 - abs(moon_longitude - node_longitude),
  )

  # Surya Siddhanta eclipse threshold limits (approximate arc-limits)
  solar_eclipse_limit = 18.0  # degrees from node for solar eclipse
  lunar_eclipse_limit = 12.0  # degrees from node for lunar eclipse

  is_solar = distance_to_node <= solar_eclipse_limit
  is_lunar = distance_to_node <= lunar_eclipse_limit

  return {
      "distance_to_node_deg": distance_to_node,
      "solar_eclipse_possible": is_solar,
      "lunar_eclipse_possible": is_lunar,
  }


# ==========================================
# MAIN EXECUTION: DEMONSTRATING ALL MODULES
# ==========================================
if __name__ == "__main__":
  print("=" * 60)
  print("SURYA SIDDHANTA COMPUTATIONAL ENGINE DEMO")
  print("=" * 60)

  # 1. Ahargana Demo
  years_elapsed = 1950500.5  # arbitrary point in a Mahayuga cycle
  ahargana_days = compute_ahargana(years_elapsed)
  print(
      f"1. Ahargana (Elapsed Days for {years_elapsed} years):"
      f" {ahargana_days:,.2f} days"
  )

  # 2. Manda Phala Demo
  mean_long = 120.0
  manda_rad = 13.0  # e.g., Mars manda epicycle parameter
  true_long, manda_corr = compute_manda_correction(mean_long, manda_rad)
  print(f"\n2. Manda-phala (Equation of Center):")
  print(
      f"   Mean Longitude: {mean_long}° | Correction: {manda_corr:.4f}° | True"
      f" Longitude: {true_long:.4f}°"
  )

  # 3. Sighra Phala Demo
  sighra_rad = 235.0  # Mars sighra epicycle parameter
  elongation = 45.0
  apparent_long = compute_sighra_correction(true_long, sighra_rad, elongation)
  print(f"\n3. Sighra-phala (Conjunction/Retrograde Correction):")
  print(f"   Apparent Geocentric Longitude: {apparent_long:.4f}°")

  # 4. Sanku (Gnomon) Demo
  g_height = 12.0  # e.g., 12 angulas
  sun_alt = 30.0  # degrees altitude
  shadow, karna = compute_gnomon_shadow(g_height, sun_alt)
  print(f"\n4. Sanku (Gnomon Shadow Mathematics):")
  print(
      f"   Gnomon Height: {g_height} | Sun Altitude: {sun_alt}°"
      f" \n   Shadow Length (Chhaya): {shadow:.4f} | Hypotenuse (Karna):"
      f" {karna:.4f}"
  )

  # 5. Grahana (Eclipse) Demo
  m_long = 150.5
  s_long = 150.0
  n_long = 145.0  # near the lunar node
  eclipse_status = predict_eclipse(m_long, s_long, n_long)
  print(f"\n5. Grahana (Eclipse Prediction):")
  print(f"   Distance to Node: {eclipse_status['distance_to_node_deg']:.2f}°")
  print(
      f"   Solar Eclipse Possible: {eclipse_status['solar_eclipse_possible']}"
  )
  print(
      f"   Lunar Eclipse Possible: {eclipse_status['lunar_eclipse_possible']}"
  )
  print("=" * 60)