import math

def generate_surya_siddhanta_sine_table():
    # Radius defined in the Surya Siddhanta (Trijya)
    R = 3438
    
    # The 24 exact historical integer R-Sine values from Surya Siddhanta (Ch. 2, vv. 17-27)
    surya_siddhanta_values = [
        225,  449,  671,  890,  1105, 1315, 1520, 1719, 
        1910, 2093, 2267, 2431, 2585, 2728, 2859, 2978, 
        3084, 3177, 3256, 3321, 3372, 3409, 3431, 3438
    ]
    
    print(f"{'Step':<5} | {'Angle (°)':<10} | {'SS R-Sine':<10} | {'Modern R-Sine':<14} | {'Difference':<10}")
    print("-" * 60)
    
    table_data = []
    for i, ss_val in enumerate(surya_siddhanta_values, start=1):
        angle_deg = i * 3.75
        angle_rad = math.radians(angle_deg)
        modern_val = round(R * math.sin(angle_rad))
        diff = ss_val - modern_val
        
        table_data.append({
            "step": i,
            "angle": angle_deg,
            "ss_sine": ss_val,
            "modern_sine": modern_val
        })
        
        print(f"{i:<5} | {angle_deg:<10.2f} | {ss_val:<10} | {modern_val:<14} | {diff:<10}")

    return table_data

if __name__ == "__main__":
    generate_surya_siddhanta_sine_table()