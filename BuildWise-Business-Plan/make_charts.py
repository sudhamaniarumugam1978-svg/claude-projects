#!/usr/bin/env python3
"""Generate professional navy-themed charts for the BuildWise business plan report."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT_DIR = "/projects/sandbox/claude-projects/BuildWise-Business-Plan"

NAVY = "#163A6B"
NAVY_LIGHT = "#4E77B0"
GREY = "#8A8A8A"
GRID = "#DDDDDD"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#BBBBBB",
    "axes.linewidth": 0.8,
    "figure.dpi": 150,
})


# ---------- Figure 1: Startup Budget Allocation (horizontal bar) ----------
budget = [
    ("Working capital (project float)", 25),
    ("Salaries (6-month runway)", 24),
    ("Office setup", 12),
    ("Construction equipment & tools", 10),
    ("Emergency / contingency reserve", 8),
    ("Utility vehicle (pre-owned)", 6),
    ("Laptops & IT equipment", 5),
    ("Marketing & branding", 5),
    ("Engineering & design software", 3),
    ("Legal registration & compliance", 2),
]
labels = [b[0] for b in budget]
values = [b[1] for b in budget]

fig, ax = plt.subplots(figsize=(7.4, 4.0))
ypos = range(len(labels))
bars = ax.barh(list(ypos), values, color=NAVY, height=0.62)
ax.invert_yaxis()
ax.set_yticks(list(ypos))
ax.set_yticklabels(labels, fontsize=9.5)
ax.set_xlabel("Allocation (\u20b9 Lakhs)", fontsize=10, color="#333333")
ax.set_xlim(0, max(values) + 5)
for b, v in zip(bars, values):
    ax.text(v + 0.4, b.get_y() + b.get_height() / 2,
            f"\u20b9{v}L  ({v}%)", va="center", ha="left",
            fontsize=8.8, color=NAVY)
ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Startup Capital Allocation \u2014 \u20b91.00 Crore",
             fontsize=12, fontweight="bold", color=NAVY, pad=10)
fig.tight_layout()
fig.savefig(f"{OUT_DIR}/budget_allocation.png", bbox_inches="tight", facecolor="white")
plt.close(fig)


# ---------- Figure 2: Revenue & Net Profit Growth (grouped bars) ----------
years = ["Year 1", "Year 2", "Year 3"]
revenue = [2.02, 4.94, 8.76]      # Rs Crore
net_profit = [0.078, 0.343, 0.658]

x = range(len(years))
w = 0.38
fig, ax = plt.subplots(figsize=(7.4, 3.8))
b1 = ax.bar([i - w / 2 for i in x], revenue, width=w, label="Total Revenue", color=NAVY)
b2 = ax.bar([i + w / 2 for i in x], net_profit, width=w, label="Net Profit", color=NAVY_LIGHT)
ax.set_xticks(list(x))
ax.set_xticklabels(years, fontsize=10.5)
ax.set_ylabel("\u20b9 Crore", fontsize=10, color="#333333")
ax.set_ylim(0, max(revenue) + 1.6)
for b, v in zip(b1, revenue):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.12, f"\u20b9{v:.2f} Cr",
            ha="center", va="bottom", fontsize=8.8, color=NAVY, fontweight="bold")
for b, v in zip(b2, net_profit):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.12, f"\u20b9{v:.2f} Cr",
            ha="center", va="bottom", fontsize=8.2, color=NAVY_LIGHT)
ax.grid(axis="y", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, fontsize=9.5, loc="upper left")
ax.set_title("Projected Revenue and Net Profit (Years 1\u20133)",
             fontsize=12, fontweight="bold", color=NAVY, pad=10)
fig.tight_layout()
fig.savefig(f"{OUT_DIR}/revenue_growth.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------- Break-even visualization ----------
import numpy as np
from matplotlib.patches import FancyBboxPatch

rev = np.linspace(0, 3, 200)
fixed = 0.30                      # Rs Crore fixed operating cost (Year 1)
total_cost = fixed + 0.80 * rev   # 80% variable (20% contribution margin)
be = 1.5                          # break-even revenue (Rs Crore)

fig, ax = plt.subplots(figsize=(7.8, 4.3))
ax.fill_between(rev, rev, total_cost, where=(rev >= be), color=NAVY, alpha=0.13,
                label="Profit zone", zorder=1)
ax.fill_between(rev, rev, total_cost, where=(rev <= be), color=GREY, alpha=0.20,
                label="Loss zone", zorder=1)
ax.plot(rev, rev, color=NAVY, lw=2.6, label="Total Revenue", zorder=3)
ax.plot(rev, total_cost, color=NAVY_LIGHT, lw=2.6, label="Total Cost", zorder=3)
ax.axhline(fixed, color=GREY, lw=1.3, ls=":", zorder=2)
ax.text(0.03, fixed + 0.05, "Fixed cost \u20b90.30 Cr", fontsize=8.5, color=GREY)
ax.axvline(be, color="#B0433B", ls="--", lw=1.2, zorder=2)
ax.plot([be], [be], "o", color="#B0433B", ms=9, zorder=5)
ax.annotate("Break-even\n\u20b91.50 Crore", (be, be), xytext=(be + 0.18, be - 0.72),
            fontsize=9.5, color="#B0433B", fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color="#B0433B"))
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_xlabel("Revenue (\u20b9 Crore)", fontsize=10, color="#333333")
ax.set_ylabel("Revenue / Cost (\u20b9 Crore)", fontsize=10, color="#333333")
ax.grid(color=GRID, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper left", ncol=2)
ax.set_title("Break-Even Analysis (Year 1)", fontsize=12, fontweight="bold",
             color=NAVY, pad=10)
fig.tight_layout()
fig.savefig(f"{OUT_DIR}/breakeven_chart.png", bbox_inches="tight", facecolor="white")
plt.close(fig)


# ---------- Financial summary KPI cards ----------
cards = [
    ("STARTUP CAPITAL", "\u20b91.00 Cr", "Self / informal funding"),
    ("BREAK-EVEN", "\u20b91.50 Cr", "Reached within Year 1"),
    ("YEAR 3 REVENUE", "\u20b98.76 Cr", "From \u20b92.02 Cr in Year 1"),
    ("YEAR 3 NET PROFIT", "\u20b965.8 L", "~7.5% net margin"),
]
fig, ax = plt.subplots(figsize=(10.2, 2.5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 26)
ax.axis("off")
cw, gap = 22.5, 3.0
x0 = (100 - (cw * 4 + gap * 3)) / 2
colors = [NAVY, "#24548F", NAVY, "#24548F"]
for i, (title, value, sub) in enumerate(cards):
    x = x0 + i * (cw + gap)
    ax.add_patch(FancyBboxPatch((x, 1), cw, 24, boxstyle="round,pad=0.02,rounding_size=1.6",
                 facecolor=colors[i], edgecolor=colors[i], zorder=2))
    ax.text(x + cw / 2, 19.5, title, ha="center", va="center", color="#D6E0EE",
            fontsize=9.5, fontweight="bold", zorder=3)
    ax.text(x + cw / 2, 12.5, value, ha="center", va="center", color="white",
            fontsize=17, fontweight="bold", zorder=3)
    ax.text(x + cw / 2, 5.5, sub, ha="center", va="center", color="#C9D6E8",
            fontsize=8, zorder=3)
fig.savefig(f"{OUT_DIR}/financial_summary.png", bbox_inches="tight", facecolor="white", dpi=200)
plt.close(fig)

print("charts written")
