import math


# ==========================================
# 1. SURYA SIDDHANTA METHOD (Algorithmic & Trigonometric Correction)
# ==========================================
def surya_siddhanta_longitude(day, orbital_period=365.25, manda_radius=1.91):
  """Computes celestial longitude using Surya Siddhanta's approach:

  1. Mean Longitude: Uniform linear motion based on period.
  2. Manda Correction: A trigonometric sine-based correction (Equation of the Center)
     to account for distance/speed variations using a manda epicycle radius.
  """
  # Mean daily motion in degrees
  mean_daily_motion = 360.0 / orbital_period
  mean_longitude = (mean_daily_motion * day) % 360.0

  # Manda anomaly (distance from apogee, assumed here proportional to mean longitude)
  # In Surya Siddhanta, this uses sine tables (jya) to apply the manda-phala correction.
  manda_anomaly_rad = math.radians(mean_longitude)
  manda_correction = manda_radius * math.sin(manda_anomaly_rad)

  # True longitude is mean longitude + correction
  true_longitude = (mean_longitude + manda_correction) % 360.0
  return true_longitude


# ==========================================
# 2. MODERN METHOD (Kepler's Elliptical Laws)
# ==========================================
def kepler_true_longitude(day, orbital_period=365.25, eccentricity=0.0167):
  """Computes true longitude using Kepler's Laws:

  1. Mean Anomaly (M): Uniform linear progression.
  2. Kepler's Equation: Solved iteratively for Eccentric Anomaly (E).
  3. True Anomaly (v): Converted from E to find exact elliptical position.
  """
  mean_motion = 360.0 / orbital_period
  M_deg = (mean_motion * day) % 360.0
  M = math.radians(M_deg)

  # Initial guess for Eccentric Anomaly (E)
  E = M

  # Solve Kepler's Equation: M = E - e * sin(E) using Newton-Raphson
  for _ in range(10):
    delta = (E - eccentricity * math.sin(E) - M) / (
        1 - eccentricity * math.cos(E)
    )
    E -= delta
    if abs(delta) < 1e-6:
      break

  # Compute True Anomaly (v) from Eccentric Anomaly (E)
  v = 2 * math.atan(
      math.sqrt((1 + eccentricity) / (1 - eccentricity)) * math.tan(E / 2)
  )
  true_anomaly_deg = math.degrees(v) % 360.0
  return true_anomaly_deg


# ==========================================
# 3. COMPARISON EXECUTION
# ==========================================
def run_comparison():
  print(
      f"{'Day':<6} | {'Surya Siddhanta (deg)':<22} | {'Keplerian (deg)':<18} |"
      f" {'Difference (deg)':<16}"
  )
  print("-" * 70)

  # Sample check points across a 365-day year
  check_days = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]

  for day in check_days:
    ss_long = surya_siddhanta_longitude(day)
    kep_long = kepler_true_longitude(day)
    diff = abs(ss_long - kep_long)

    # Normalize difference for wrap-around at 360 degrees
    if diff > 180:
      diff = 360 - diff

    print(f"{day:<6} | {ss_long:<22.4f} | {kep_long:<18.4f} | {diff:<16.4f}")


if __name__ == "__main__":
  run_comparison()