import pandas as pd
from datetime import datetime

def daycount_30_360(start, end):
    """
    30/360 US day‐count convention for computing remaining periods.
    """
    d1, m1, y1 = start.day, start.month, start.year
    d2, m2, y2 = end.day,   end.month,   end.year

    if d1 == 31:           
        d1 = 30
    if d2 == 31 and d1 == 30:
        d2 = 30

    return 360*(y2 - y1) + 30*(m2 - m1) + (d2 - d1)

# === 1) User inputs ===
coupon_rate = float(input("Annual coupon rate % (e.g. 3.2): "))
freq        = int(  input("Coupons per year (e.g. 2): "))
price       = float(input("Price per 100 par (e.g. 100): "))
ytm         = float(input("YTM % (e.g. 3.2): "))
par         = 100

fmt         = "%m/%d/%Y"
issuance    = datetime.strptime(input("Issuance date  (MM/DD/YYYY): "), fmt)
settlement  = datetime.strptime(input("Settlement date(MM/DD/YYYY): "), fmt)
maturity    = datetime.strptime(input("Maturity date (MM/DD/YYYY): "), fmt)

# === 2) Compute actual t and 30/360 T ===
t       = (settlement - issuance).days    # actual calendar days, e.g. 57
T       = 360.0 / freq                    # days per coupon period
offset  = t / T                            # fraction of first period elapsed

# === 3) Number of remaining periods N ===
days_to_mat = daycount_30_360(settlement, maturity)
N = int(round(days_to_mat / T))
if N < 1:
    raise ValueError("No remaining coupon periods; check your dates.")

# === 4) Build cash‐flow schedule & timings ===
times_to_receipt = [(p+1) - offset for p in range(N)]
coupon_pmt       = coupon_rate/100 * par / freq
cash_flows       = [coupon_pmt]*N
cash_flows[-1]  += par

# === 5) Discount & compute PVs ===
r_period = ytm/100/freq
pv       = [
    cf * (1 + r_period)**(-tpr)
    for cf, tpr in zip(cash_flows, times_to_receipt)
]

# === 6) Weights & time‐weights ===
theo_price      = sum(pv)
weights         = [v/theo_price for v in pv]
time_weights    = [tpr * w for tpr, w in zip(times_to_receipt, weights)]

# === 7) Durations in periods & annualized ModDur ===
mac_dur_periods = sum(time_weights)
mod_dur_periods = mac_dur_periods / (1 + r_period)
mod_dur_annual  = mod_dur_periods / freq

# === 8) Output ===
df = pd.DataFrame({
    "Period":           list(range(1, N+1)),
    "Time to Receipt":  [round(x, 4) for x in times_to_receipt],
    "Cash Flow":        [round(cf, 4) for cf in cash_flows],
    "PV":               [round(v, 4) for v in pv],
    "Weight":           [round(w, 6) for w in weights],
    "Time × Weight":    [round(tw, 6) for tw in time_weights],
})

from IPython.display import display
display(df)

print(f"Actual days between issuance → settlement (t):  {t}")
print(f"Days per period (T):                           {T:.1f}")
print(f"Macaulay Duration (periods):                   {mac_dur_periods:.6f}")
print(f"Modified Duration (periods):                   {mod_dur_periods:.6f}")
print(f"Annualized Modified Duration (years):          {mod_dur_annual:.6f}")
