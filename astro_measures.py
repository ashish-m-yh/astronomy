import math


# ==========================================
# 1. SURYA SIDDHANTA: Cosmic Cycle Mean Motion
# ==========================================
def surya_siddhanta_mean_longitude(civil_days_elapsed, revs_in_mahayuga):
  """Calculates the mean longitude of a celestial body based on

  Surya Siddhanta constants.
  1 Mahayuga = 4,320,000 solar years = 1,577,917,828 civil days.
  """
  mahayuga_days = 1577917828.0

  # Find the fractional part of the current Mahayuga cycle
  fraction = (civil_days_elapsed * revs_in_mahayuga) % mahayuga_days
  mean_long_degrees = (fraction / mahayuga_days) * 360.0
  return mean_long_degrees


# Example: Sun's mean longitude after 1,000,000 civil days
# Sun completes 4,320,000 revolutions in one Mahayuga
sun_revs = 4320000
days = 1000000.0
sun_long = surya_siddhanta_mean_longitude(days, sun_revs)
print(f"--- Surya Siddhanta ---")
print(f"Sun Mean Longitude after {days} days: {sun_long:.4f} degrees\n")


# ==========================================
# 2. GREEK ASTRONOMY: Ptolemaic Epicycle Model
# ==========================================
def ptolemaic_position(t, R_def, omega_def, r_epi, omega_epi):
  """Calculates geocentric position (x, y) using a deferent

  and an epicycle (uniform circular motion superposition).
  """
  # Position on the deferent center
  x_def = R_def * math.cos(omega_def * t)
  y_def = R_def * math.sin(omega_def * t)

  # Position on the epicycle relative to deferent center
  x_epi = r_epi * math.cos(omega_epi * t)
  y_epi = r_epi * math.sin(omega_epi * t)

  # Total geocentric vector
  x_total = x_def + x_epi
  y_total = y_def + y_epi

  distance = math.sqrt(x_total**2 + y_total**2)
  angle_deg = math.degrees(math.atan2(y_total, x_total)) % 360
  return distance, angle_deg


# Example: Planet on an epicycle at time t = 5.0 units
dist, angle = ptolemaic_position(
    t=5.0, R_def=10.0, omega_def=0.5, r_epi=2.5, omega_epi=2.0
)
print(f"--- Greek Astronomy (Ptolemaic) ---")
print(f"Geocentric Distance: {dist:.4f}, Apparent Longitude: {angle:.4f} deg\n")


# ==========================================
# 3. MODERN ASTRONOMY: Kepler's Elliptical Orbit
# ==========================================
def compute_true_anomaly(mean_anomaly_deg, eccentricity):
  """Solves Kepler's Equation (M = E - e*sin(E)) using Newton-Raphson

  to compute the true orbital anomaly (v) for an ellipse.
  """
  M = math.radians(mean_anomaly_deg)
  E = M  # Initial guess for eccentric anomaly (E)

  # Newton-Raphson iteration
  for _ in range(10):
    delta = (E - eccentricity * math.sin(E) - M) / (
        1 - eccentricity * math.cos(E)
    )
    E -= delta
    if abs(delta) < 1e-6:
      break

  # Compute true anomaly (v) from eccentric anomaly (E)
  v = 2 * math.atan(
      math.sqrt((1 + eccentricity) / (1 - eccentricity)) * math.tan(E / 2)
  )
  return math.degrees(v) % 360


# Example: Earth-like orbit with Mean Anomaly = 45 degrees, Eccentricity = 0.0167
true_anom = compute_true_anomaly(mean_anomaly_deg=45.0, eccentricity=0.0167)
print(f"--- Modern Astronomy (Keplerian) ---")
print(f"True Anomaly for Mean Anomaly 45 deg: {true_anom:.4f} degrees")