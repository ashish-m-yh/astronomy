import math

# ==========================================
# 1. SURYA SIDDHANTA SMALL-ANGLE APPROXIMATION
# ==========================================


def surya_siddhanta_jya(theta_minutes):
  """Computes the R-sine (Jya) using Surya Siddhanta's radius R = 3438 arc-min.

  For small angles in arc-minutes, R * sin(theta) approximately equals theta.
  """
  R = 3438.0  # 1 radian in arc-minutes (21600 / 2pi)
  theta_rad = math.radians(theta_minutes / 60.0)

  # Exact Siddhantic R-sine: R * sin(theta)
  r_sin = R * math.sin(theta_rad)

  # Small angle linear shortcut: if theta is very small, R * sin(theta) ≈ theta (in min)
  small_angle_approx = theta_minutes

  return r_sin, small_angle_approx


# ==========================================
# 2. GREEK ASTRONOMY (PTOLEMY) CHORD APPROXIMATION
# ==========================================


def ptolemy_chord(theta_degrees):
  """Computes Ptolemy's Chord function Crd(theta) for R = 60 base circle.

  Formula: Crd(theta) = 120 * sin(theta / 2)
  For small angles, Crd(theta) ≈ 60 * math.radians(theta).
  """
  R = 60.0
  # Exact chord formula
  chord = 2 * R * math.sin(math.radians(theta_degrees / 2.0))

  # Small angle linear shortcut for chords
  small_angle_approx = 2 * R * math.radians(theta_degrees / 2.0)

  return chord, small_angle_approx


# ==========================================
# 3. RUN COMPARISON
# ==========================================
def run_small_angle_comparison():
  print("=== SURYA SIDDHANTA (R = 3438' Scale) ===")
  print(
      f"{'Angle (arc-min)':<18} | {'Exact R-Sine':<16} |"
      f" {'Small-Angle Shortcut':<22} | {'Error (%)':<10}"
  )
  print("-" * 75)

  # Test small arc-minute intervals (e.g., 5', 10', 30', 60')
  test_minutes = [5, 10, 30, 60, 120]
  for m in test_minutes:
    exact, approx = surya_siddhanta_jya(m)
    error = abs(exact - approx) / exact * 100
    print(f"{m:<18} | {exact:<16.4f} | {approx:<22.4f} | {error:<10.4f}%")

  print("\n=== GREEK ASTRONOMY / PTOLEMY (R = 60 Scale) ===")
  print(
      f"{'Angle (degrees)':<18} | {'Exact Chord':<16} |"
      f" {'Small-Angle Shortcut':<22} | {'Error (%)':<10}"
  )
  print("-" * 75)

  # Test small degree intervals (e.g., 0.5°, 1°, 2°, 5°)
  test_degrees = [0.5, 1.0, 2.0, 5.0]
  for d in test_degrees:
    exact_c, approx_c = ptolemy_chord(d)
    error_c = abs(exact_c - approx_c) / exact_c * 100
    print(f"{d:<18} | {exact_c:<16.4f} | {approx_c:<22.4f} | {error_c:<10.4f}%")


if __name__ == "__main__":
  run_small_angle_comparison()