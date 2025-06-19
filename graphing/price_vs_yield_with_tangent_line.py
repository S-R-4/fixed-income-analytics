import matplotlib.pyplot as plt
import numpy as np

# Original data arrays
ytm = np.array([
    -0.100, -0.090, -0.080, -0.070, -0.060, -0.050,
    -0.040, -0.030, -0.020, -0.010,  0.000,  0.010,
     0.020,  0.030,  0.040,  0.050,  0.060,  0.070,
     0.080,  0.090,  0.100
])
price = np.array([
    1131850.226, 886912.7467, 701229.4064, 559515.8354,
    450620.842 , 366364.9667, 300716.3388, 249202.9769,
    208491.6397, 176084.558 , 150100.    , 129112.7334,
    112037.4848,  98043.40542, 86490.99837, 76885.39288,
    68841.56677, 62058.34623, 56298.85445, 51375.80733,
    47140.30319
])
duration_est = np.array([
    382403.6414, 359173.2525, 335942.8636, 312712.4746,
    289482.0857, 266251.6968, 243021.3079, 219790.9189,
    196560.53  , 173330.1411, 150099.7521, 126868.9632,
    103638.9743,  80408.5854,  57178.1964,  33947.8075,
     10717.4186, -12512.9703, -35743.3593, -58973.7482,
    -82204.1371
])

# 1) Compute offset so the lowest value is at zero
orig_min    = min(price.min(), duration_est.min())
offset      = -orig_min

# 2) Add a small buffer above zero (5% of the data range)
total_range = price.max() - orig_min
margin      = 0.05 * total_range

# 3) Shift both series up by (offset + margin)
price_adj = price + offset + margin
dur_adj   = duration_est + offset + margin

# 4) Find the intersection point (x0, y0_adj)
x0      = -0.010
y0_adj  = np.interp(x0, ytm, price_adj)

# 5) Plot everything
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(ytm, price_adj, label='PRICE (offset + buffer)')
ax.plot(ytm, dur_adj,   label='DURATION ESTIMATE (offset + buffer)')
ax.fill_between(ytm, price_adj, dur_adj, alpha=0.3)

# 6) Add dashed H and V lines
ax.axhline(y=y0_adj, linestyle='--', label='H')
ax.vlines(x0, ymin=0, ymax=y0_adj, linestyle='--', label='V')

# 7) Force the y-axis to start at zero
ax.set_ylim(bottom=0)

# 8) Labels, title, legend
ax.set_xlabel('Yield-to-maturity')
ax.set_ylabel('Value (offset + buffer)')
ax.set_title('Price vs Yield (Buffered Above Zero)')
ax.legend(loc='upper right')

plt.tight_layout()
plt.show()
