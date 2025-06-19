import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Bond Parameters ---
#face_value = 100
#coupon_rate = 0.05         # 5%
#frequency = 2              # Semiannual
#years = 10                 # 10-year bond
#y0 = 0.04                  # Base yield (4%)
#delta_y = 0.0001           # 1 bp

# --- Prompt for Inputs (Bond Parameters) ---
face_value = float(input("Face value (e.g., 100): "))
coupon_rate = float(input("Annual coupon rate (e.g., 0.05 for 5%): "))
frequency = int(input("Payments per year (e.g., 2 for semiannual): "))
years = int(input("Years to maturity: "))
y0 = float(input("Base yield (e.g., 0.04 for 4%): "))
delta_y = float(input("Delta y for duration/convexity (e.g., 0.0001 for 1 bp): "))

# --- Derived Values ---
N = years * frequency
coupon = face_value * coupon_rate / frequency
ytms = np.linspace(-0.02, 0.10, 1000)  # YTM from -2% to 10%

# --- Bond Pricing Function
def bond_price(y):
    r = y / frequency
    cashflows = np.array([coupon] * (N - 1) + [coupon + face_value])
    times = np.arange(1, N + 1)
    return np.sum(cashflows / (1 + r) ** times)

# --- Generate Actual Price Curve ---
price_curve = np.array([bond_price(y) for y in ytms])

# --- P0, P+, P- (Base Price and Sensitivity Estimates) ---
P0 = bond_price(y0)
P_minus = bond_price(y0 - delta_y)
P_plus = bond_price(y0 + delta_y)

# --- Duration and Convexity ---
mod_duration = (P_minus - P_plus) / (2 * P0 * delta_y)
convexity = (P_minus + P_plus - 2 * P0) / (P0 * delta_y**2)

# --- Duration Line (Tangent) ---
duration_line = P0 - mod_duration * P0 * (ytms - y0)

# --- Convexity-Adjusted Estimate ---
convexity_line = P0 - mod_duration * P0 * (ytms - y0) + 0.5 * convexity * P0 * (ytms - y0)**2

# --- Plotting ---
plt.figure(figsize=(10,6))
plt.plot(ytms * 100, price_curve, label="Actual Bond Price", linewidth=2)
plt.plot(ytms * 100, duration_line, label="Duration Estimate", linestyle='--')
plt.plot(ytms * 100, convexity_line, label="Convexity-Adjusted Estimate", linestyle=':')
plt.axvline(x=y0 * 100, color='gray', linestyle='--', alpha=0.5)
plt.title("Bond Price vs Yield")
plt.xlabel("Yield to Maturity (%)")
plt.ylabel("Bond Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()