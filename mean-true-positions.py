"""
Computes the mean longitudes of planets based on elapsed days (Ahargana) since epoch (Kaliyuga, Feb 18, 3102 BCE).
    • Surya Siddhanta: Uses integer proportions based on planetary revolutions in a Mahayuga (4,320,000 solar years).
    • Greek: Uses mean motion tables with sexagesimal additions per day.
    • Modern: Polynomial time functions L(T) = L0 + L1*T + L2*T².

Why a Residual Difference Still Exists Here

Even when synchronized to the exact same calendar date, you will notice a difference of a few degrees between the Surya Siddhanta and modern outputs. This residual gap is caused by:

    Ayanāṃśa (Reference Frame Shift): Modern astronomy measures longitude from the dynamical equinox, whereas ancient Indian astronomy traditionally measured from fixed sidereal markers (like the star Revati / Zeta Piscium), introducing a precession offset that grows over millennia.

    Secular Acceleration: The constant mean motion ratio in the Surya Siddhanta cannot replicate the subtle gravitational wobbles and variations baked into the modern IAU polynomial.
"""

import numpy as np

def surya_mean_longitude(ahargana: float, rev_per_mahayuga: int) -> float:
    """Surya Siddhanta: Mean longitude (in degrees) from Ahargana (elapsed civil days).
    Civil days in Mahayuga = 1,577,917,828
    """
    CIVIL_DAYS_IN_MAHAYUGA = 1577917828
    revs = (ahargana * rev_per_mahayuga) / CIVIL_DAYS_IN_MAHAYUGA
    return (revs % 1.0) * 360.0

def greek_mean_longitude(ahargana: float, daily_motion_deg: float, epoch_long: float) -> float:
    """Ptolemaic: Mean motion accumulated linearly from a reference epoch."""
    return (epoch_long + ahargana * daily_motion_deg) % 360.0

def modern_mean_longitude(d_centuries: float) -> float:
    """Modern (IAU): Polynomial expansion for Sun's mean longitude."""
    # T = centuries from J2000.0
    L0 = 280.46646 + 36000.76983 * d_centuries + 0.0003032 * (d_centuries**2)
    return L0 % 360.0

# 1. Choose a target date (e.g., January 1, 2026)
# Julian Date for 2026-01-01 00:00 UTC is approximately 2460676.5
target_jd = 2460676.5

# 2. Modern IAU input: Centuries from J2000.0 (JD 2451545.0)
j2000_epoch = 2451545.0
d_centuries = (target_jd - j2000_epoch) / 36525.0
modern_sun = modern_mean_longitude(d_centuries)

# 3. Surya Siddhanta input: Ahargana (Days elapsed since Kali Yuga Epoch: Feb 18, 3102 BCE = JD 588465.5)
kali_yuga_epoch_jd = 588465.5
ahargana_val = target_jd - kali_yuga_epoch_jd
ss_sun = surya_mean_longitude(ahargana_val, 4320000)

print(f"Target Julian Date            : {target_jd}")
print(f"Surya Siddhanta Sun Longitude : {ss_sun:.2f}°")
print(f"Modern IAU Sun Longitude      : {modern_sun:.2f}°")
