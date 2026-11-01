import math


def generate_ancient_sine_table():
  R = 3438.0  # Standard radius in arc-minutes
  n_steps = 24
  step_minutes = 225.0  # 3.75 degrees = 225 arc-minutes

  sines = [0.0] * (n_steps + 1)
  differences = [0.0] * (n_steps + 1)

  # Initial conditions for the first step (n = 1)
  differences[1] = step_minutes
  sines[1] = differences[1]

  print(
      f"{'Step':<5} | {'Angle':<8} | {'Ancient R-Sine':<16} |"
      f" {'Difference (d_n)':<18} | {'Modern R-Sine':<16}"
  )
  print("-" * 75)

  # Print Step 0
  print(f"{0:<5} | {0.0:>6.2f}° | {sines[0]:<16.2f} | {'-':<18} | {0.0:<16.2f}")

  # Print Step 1
  mod_val_1 = R * math.sin(math.radians(3.75))
  print(
      f"{1:<5} | {3.75:>6.2f}° | {sines[1]:<16.2f} | {differences[1]:<18.2f} |"
      f" {mod_val_1:<16.2f}"
  )

  # Generate remaining steps using the ancient recursive algorithm
  for n in range(2, n_steps + 1):
    # Ancient recurrence relation: d_n = d_{n-1} - (s_{n-1} / 225)
    d_n = differences[n - 1] - (sines[n - 1] / step_minutes)
    differences[n] = d_n
    sines[n] = sines[n - 1] + d_n

    angle_deg = n * 3.75
    modern_r_sine = R * math.sin(math.radians(angle_deg))

    print(
        f"{n:<5} | {angle_deg:>6.2f}° | {sines[n]:<16.2f} |"
        f" {differences[n]:<18.2f} | {modern_r_sine:<16.2f}"
    )


if __name__ == "__main__":
  generate_ancient_sine_table()