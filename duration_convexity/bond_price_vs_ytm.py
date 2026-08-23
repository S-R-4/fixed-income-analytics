import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Bond pricing function
def bond_price(face, coupon_rate, years, ytm):
    coupon = face * coupon_rate
    # Present value of coupons + face
    pv_coupons = sum(coupon / (1 + ytm) ** t for t in range(1, years + 1))
    pv_face    = face / (1 + ytm) ** years
    return pv_coupons + pv_face

# Parameters
face_value  = 100
ytm_values  = np.linspace(0, 0.10, 101)  # 0% to 10% in 0.1% steps

# Compute prices
data = {
    "Yield-to-Maturity (%)": ytm_values * 100,
    "Romanian Bond (30yr, 4.625%)": [
        bond_price(face_value, 0.04625, 30, y) for y in ytm_values
    ],
    "MAKE Bond (5yr, 3.2%)": [
        bond_price(face_value, 0.032, 5, y) for y in ytm_values
    ],
    "Australian Bond (1yr, 0%)": [
        face_value / (1 + y) for y in ytm_values
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display DataFrame (for copy/paste into Excel)
EXCEL_OUTPUT = OUTPUT_DIR / "bond_price_vs_ytm.xlsx"
df.to_excel(EXCEL_OUTPUT, index=False)

print(f"Excel file created: {EXCEL_OUTPUT}")
#print(df)

# Plot
plt.figure(figsize=(8,5))
plt.plot(df["Yield-to-Maturity (%)"], df["Romanian Bond (30yr, 4.625%)"], label="Romanian Bond (30yr, 4.625%)")
plt.plot(df["Yield-to-Maturity (%)"], df["MAKE Bond (5yr, 3.2%)"],      label="MAKE Bond (5yr, 3.2%)")
plt.plot(df["Yield-to-Maturity (%)"], df["Australian Bond (1yr, 0%)"], label="Australian Bond (1yr, 0%)")
plt.xlabel("Yield-to-Maturity (%)")
plt.ylabel("Bond Price (% of Par)")
plt.title("Bond Prices vs Yield-to-Maturity")
plt.legend()
plt.grid(True)
plt.show()