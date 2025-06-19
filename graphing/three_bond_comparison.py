import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# Identify bonds

bond_1 = "Bulgarian Bond (30yr, 4.625%)"
bond_2 = "Loews Corp Bond (5yr, 3.2%)"
bond_3 = "Japan Bond (1yr, 0%)" #zero-coupon

# Compute prices
data = {
    "Yield-to-Maturity (%)": ytm_values * 100,
    bond_1: [bond_price(face_value, 0.04625, 30, y) for y in ytm_values],
    bond_2: [bond_price(face_value, 0.032, 5, y) for y in ytm_values],
    bond_3: [face_value / (1 + y) for y in ytm_values]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display DataFrame (for copy/paste into Excel)
#display(df) #works in jupyter
print(df) #works in vscode

# Plot
plt.figure(figsize=(8,5))
plt.plot(df["Yield-to-Maturity (%)"], df[bond_1], label=bond_1)
plt.plot(df["Yield-to-Maturity (%)"], df[bond_2], label=bond_2)
plt.plot(df["Yield-to-Maturity (%)"], df[bond_3], label=bond_3)
plt.xlabel("Yield-to-Maturity (%)")
plt.ylabel("Bond Price (% of Par)")
plt.title("Bond Prices vs Yield-to-Maturity")
plt.legend()
plt.grid(True)
plt.show()
