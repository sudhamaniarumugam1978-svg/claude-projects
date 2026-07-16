#!/usr/bin/env python3
"""Generate professional, navy-themed business diagrams for the BuildWise
report: project workflow flowchart, organisation chart, customer journey,
growth roadmap, problem-to-solution framework, expansion timeline and the
phased business-model graphic. All images share one visual language so the
report looks like a single, professionally designed document."""

import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = "/projects/sandbox/claude-projects/BuildWise-Business-Plan"

NAVY = "#163A6B"
NAVY2 = "#24548F"
BLUE = "#4E77B0"
STEEL = "#6E8CB5"
GREY = "#5B6470"
LIGHT = "#EEF2F8"
LINE = "#163A6B"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def box(ax, cx, cy, w, h, text, fc=NAVY, tc="white", fs=11, bold=True,
        wrap=16, ec=None, radius=0.04):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius*100}",
        linewidth=1.2, edgecolor=ec or fc, facecolor=fc, zorder=3,
        mutation_scale=1))
    if wrap:
        text = "\n".join(textwrap.wrap(text, wrap))
    ax.text(cx, cy, text, ha="center", va="center", color=tc, fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.2)


def arrow(ax, p1, p2, color=LINE, lw=2.2, style="-|>"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=16,
                                 color=color, lw=lw, zorder=2,
                                 shrinkA=2, shrinkB=2))


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(f"{OUT}/{name}", dpi=200, bbox_inches="tight",
                facecolor="white", pad_inches=0.15)
    plt.close(fig)
    print("wrote", name)


# ============ 1. PROJECT WORKFLOW (serpentine flowchart) ============
def workflow():
    fig, ax = new_ax(9.2, 11.2)
    steps = ["Lead Generation", "Client Meeting", "Requirement Analysis",
             "Site Inspection", "Architectural Design", "Quotation",
             "Agreement", "Material Procurement", "Construction",
             "Quality Inspection", "Handover", "After-Sales Support"]
    cols = [17, 50, 83]
    rows = [90, 68, 46, 24]
    pos = []
    for r in range(4):
        order = cols if r % 2 == 0 else cols[::-1]
        for c in order:
            pos.append((c, rows[r]))
    w, h = 27, 15
    for idx, (p, s) in enumerate(zip(pos, steps)):
        fc = NAVY if idx % 2 == 0 else NAVY2
        box(ax, p[0], p[1], w, h, f"{idx+1}. {s}", fc=fc, fs=11, wrap=13)
    for a in range(len(pos) - 1):
        (x1, y1), (x2, y2) = pos[a], pos[a + 1]
        if y1 == y2:  # horizontal
            if x2 > x1:
                arrow(ax, (x1 + w / 2, y1), (x2 - w / 2, y2))
            else:
                arrow(ax, (x1 - w / 2, y1), (x2 + w / 2, y2))
        else:  # vertical turn
            arrow(ax, (x1, y1 - h / 2), (x2, y2 + h / 2))
    save(fig, "workflow_operations.png")


# ============ 2. ORGANISATION CHART ============
def org_chart():
    fig, ax = new_ax(11.5, 7.2)
    box(ax, 50, 88, 40, 15, "Founder / Managing Director", fc=NAVY, fs=13, wrap=22)
    lvl2 = [("Civil Engineer", 15), ("Site Engineer", 38.3),
            ("Finance & Administration", 61.6), ("Marketing & Client Relations", 85)]
    busy = 60
    arrow(ax, (50, 80.5), (50, busy + 6), style="-")
    ax.plot([lvl2[0][1], lvl2[-1][1]], [busy + 6, busy + 6], color=LINE, lw=2, zorder=2)
    for name, x in lvl2:
        ax.plot([x, x], [busy + 6, 52 + 7.5], color=LINE, lw=2, zorder=2)
        box(ax, x, 52, 21, 15, name, fc=NAVY2, fs=11, wrap=14)
    # third level under Civil Engineer
    arrow(ax, (lvl2[0][1], 44.5), (lvl2[0][1], 30 + 7), style="-")
    box(ax, lvl2[0][1], 24, 21, 14, "Architect (Consultant)", fc=BLUE, fs=10.5, wrap=14)
    save(fig, "org_chart.png")


# ============ 3. CUSTOMER JOURNEY ============
def customer_journey():
    fig, ax = new_ax(11.5, 5.4)
    steps = ["Enquiry", "Consultation", "Transparent Quote", "Agreement",
             "Regular Updates", "Quality Handover", "Warranty & Support", "Referral"]
    xs = [14, 40, 66, 92]
    w, h = 22, 16
    row1_y, row2_y = 74, 26
    for i in range(4):
        box(ax, xs[i], row1_y, w, h, steps[i], fc=NAVY, fs=10.5, wrap=12)
        if i < 3:
            arrow(ax, (xs[i] + w / 2, row1_y), (xs[i + 1] - w / 2, row1_y))
    # connector down from last of row1 to first of row2
    arrow(ax, (xs[3], row1_y - h / 2), (xs[3], (row1_y + row2_y) / 2 + 2))
    ax.plot([xs[0], xs[3]], [(row1_y + row2_y) / 2 + 2] * 2, color=LINE, lw=2, zorder=2)
    arrow(ax, (xs[0], (row1_y + row2_y) / 2 + 2), (xs[0], row2_y + h / 2))
    for i in range(4):
        box(ax, xs[i], row2_y, w, h, steps[i + 4], fc=NAVY2, fs=10.5, wrap=12)
        if i < 3:
            arrow(ax, (xs[i] + w / 2, row2_y), (xs[i + 1] - w / 2, row2_y))
    save(fig, "customer_journey.png")


# ============ 4. GROWTH ROADMAP (rising steps) ============
def growth_roadmap():
    fig, ax = new_ax(12.5, 7.0)
    steps = ["Start Small", "Deliver Excellent Projects", "Gain Customer Trust",
             "Generate Revenue", "Reinvest Profits", "Expand Operations",
             "Introduce Technology", "Expand Across India"]
    n = len(steps)
    xs = [6 + i * (88 / (n - 1)) for i in range(n)]
    ys = [10 + i * (74 / (n - 1)) for i in range(n)]
    w, h = 14.5, 12
    ax.plot(xs, ys, color=STEEL, lw=2, ls="--", zorder=1)
    for i in range(n):
        fc = NAVY if i % 2 == 0 else NAVY2
        box(ax, xs[i], ys[i], w, h, steps[i], fc=fc, fs=9.6, wrap=11)
        if i < n - 1:
            arrow(ax, (xs[i] + w / 2 - 1, ys[i] + h / 2 - 2),
                  (xs[i + 1] - w / 2 + 1, ys[i + 1] - h / 2 + 2), lw=1.8)
    save(fig, "growth_roadmap.png")


# ============ 5. PROBLEM -> SOLUTION FRAMEWORK ============
def problem_solution():
    fig, ax = new_ax(11.5, 9.0)
    pairs = [
        ("Hidden charges", "Transparent, itemised quotations"),
        ("Uncertain payments", "Milestone-based billing"),
        ("Poor communication", "Weekly updates & relationship manager"),
        ("Project delays", "Professional scheduling & monitoring"),
        ("Weak documentation", "Structured records & digital docs"),
        ("Quality concerns", "Defined quality-assurance checkpoints"),
        ("No after-sales support", "Warranty & after-sales service"),
    ]
    box(ax, 22, 95, 34, 8, "INDUSTRY PROBLEMS", fc=GREY, fs=12, wrap=0)
    box(ax, 78, 95, 34, 8, "BUILDWISE SOLUTIONS", fc=NAVY, fs=12, wrap=0)
    n = len(pairs)
    top = 84
    gap = (top - 6) / n
    hh = gap * 0.78
    for i, (p, s) in enumerate(pairs):
        cy = top - i * gap - hh / 2
        box(ax, 22, cy, 34, hh, p, fc="#E3E7EE", tc=GREY, fs=10, wrap=22, bold=False)
        box(ax, 78, cy, 34, hh, s, fc=NAVY2, tc="white", fs=10, wrap=24, bold=False)
        arrow(ax, (40, cy), (60, cy), lw=2)
    save(fig, "problem_solution.png")


# ============ 6. EXPANSION TIMELINE ============
def expansion_timeline():
    fig, ax = new_ax(12.6, 7.0)
    miles = [
        ("Year 1", ["Deliver first projects", "Earn referrals & trust", "Reach break-even"]),
        ("Year 2", ["Strengthen branding", "Grow the workforce", "Launch digital systems"]),
        ("Year 3", ["Open second branch", "Widen customer base", "Begin tech integration"]),
        ("Years 4–5", ["Expand across India", "Commercial & luxury", "Smart & green building"]),
    ]
    xs = [15, 40, 63, 87]
    y = 50
    ax.plot([8, 94], [y, y], color=STEEL, lw=4, zorder=1)
    for i, (label, items) in enumerate(miles):
        x = xs[i]
        ax.add_patch(plt.Circle((x, y), 2.4, color=NAVY, zorder=4))
        up = i % 2 == 0
        by = y + 20 if up else y - 20
        box(ax, x, by, 21, 26, label + "\n\n" + "\n".join("• " + t for t in items),
            fc=NAVY if up else NAVY2, fs=9.2, wrap=0)
        arrow(ax, (x, by + (-13 if up else 13)), (x, y + (2.4 if up else -2.4)), lw=1.6, style="-")
    save(fig, "expansion_timeline.png")


# ============ 7. BUSINESS MODEL PHASES (ascending) ============
def business_phases():
    fig, ax = new_ax(12.5, 6.4)
    phases = [
        ("PHASE 1", "Business Foundation", "Excellent projects, small team, transparent billing"),
        ("PHASE 2", "Digital Foundation", "Website, customer portal, CRM, digital contracts"),
        ("PHASE 3", "Technology Integration", "Material tracking, mobile app, AI estimation"),
        ("PHASE 4", "Expansion", "Multiple cities, smart & green building, enterprise scale"),
    ]
    xs = [14, 38, 62, 86]
    heights = [34, 46, 58, 72]
    w = 21
    base = 8
    for i, (ph, title, desc) in enumerate(phases):
        hh = heights[i]
        cy = base + hh / 2
        fc = NAVY if i % 2 == 0 else NAVY2
        ax.add_patch(FancyBboxPatch((xs[i] - w / 2, base), w, hh,
                     boxstyle="round,pad=0.02,rounding_size=3", facecolor=fc,
                     edgecolor=fc, zorder=3))
        ax.text(xs[i], base + hh - 6, ph, ha="center", va="center", color="white",
                fontsize=12, fontweight="bold", zorder=4)
        ax.text(xs[i], base + hh - 14, title, ha="center", va="center", color="white",
                fontsize=10, fontweight="bold", zorder=4)
        ax.text(xs[i], cy - 4, "\n".join(textwrap.wrap(desc, 20)), ha="center",
                va="center", color="white", fontsize=8.6, zorder=4, linespacing=1.3)
        if i < 3:
            arrow(ax, (xs[i] + w / 2, base + hh - 4), (xs[i + 1] - w / 2, base + heights[i + 1] - 4), lw=1.8)
    save(fig, "business_model_phases.png")


# ============ 8. INDIAN CONSTRUCTION MARKET OVERVIEW (bar chart) ============
def market_overview():
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    labels = ["Total Construction\nMarket (2025)", "Residential\nSegment (2025)"]
    values = [685, 264]
    bars = ax.bar(labels, values, color=[NAVY, NAVY2], width=0.55, zorder=3)
    ax.set_ylabel("Market Size (USD Billion)", fontsize=12, color="#333333")
    ax.set_ylim(0, 820)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 14, f"US$ {v} B",
                ha="center", va="bottom", fontsize=13, fontweight="bold", color=NAVY)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11)
    ax.set_title("Indian Construction Market Size (2025)",
                 fontsize=14, fontweight="bold", color=NAVY, pad=26)
    ax.text(0.5, 1.03,
            "Projected CAGR of about 6.9%  \u2022  overall market growing ~11% to INR 25.31 trillion",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color=GREY)
    fig.tight_layout()
    save(fig, "market_overview.png")


# ============ 9. SWOT MATRIX (2x2 quadrant) ============
def swot_matrix():
    fig, ax = new_ax(11.0, 8.4)
    quads = [
        ("STRENGTHS", NAVY, 3, 52, [
            "Transparent, customer-first model",
            "Lean, low-overhead structure",
            "Strong project-management discipline",
            "Clear phased growth strategy"]),
        ("WEAKNESSES", NAVY2, 51, 52, [
            "New brand with no track record",
            "Limited initial capital",
            "Dependent on a small founding team",
            "Limited geographic presence at launch"]),
        ("OPPORTUNITIES", "#2F6091", 3, 4, [
            "Large, growing construction market",
            "Demand for transparency & quality",
            "Rising interest in smart / green homes",
            "NRI and investor demand"]),
        ("THREATS", STEEL, 51, 4, [
            "Input-cost inflation",
            "Intense local competition",
            "Regulatory & approval delays",
            "Skilled-labour shortages"]),
    ]
    qw, qh = 46, 44
    for title, color, x, y, items in quads:
        ax.add_patch(FancyBboxPatch((x, y), qw, qh,
                     boxstyle="round,pad=0.02,rounding_size=2.0",
                     facecolor="white", edgecolor=color, linewidth=2.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + qh - 9), qw, 9,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=color, zorder=3))
        ax.text(x + qw / 2, y + qh - 4.5, title, ha="center", va="center",
                color="white", fontsize=13, fontweight="bold", zorder=4)
        for k, it in enumerate(items):
            ax.text(x + 3, y + qh - 14 - k * 7.5, "\u2022 " + it, ha="left", va="center",
                    color="#2B2B2B", fontsize=10.2, zorder=4)
    save(fig, "swot_matrix.png")


# ============ 10. TECHNOLOGY ADOPTION ROADMAP (horizontal phases) ============
def tech_roadmap():
    fig, ax = new_ax(12.8, 6.2)
    phases = [
        ("PHASE 1", "Foundation", ["Google Workspace", "WhatsApp updates", "Transparent billing"]),
        ("PHASE 2", "Digital", ["Website & portal", "Online quotations", "CRM & e-signatures"]),
        ("PHASE 3", "Integration", ["QR material tracking", "Mobile application", "AI cost estimation"]),
        ("PHASE 4", "Smart Ops", ["Drone monitoring", "IoT integration", "Predictive analytics"]),
    ]
    xs = [14, 39, 62, 86]
    y = 52
    ax.plot([8, 93], [y, y], color=STEEL, lw=4, zorder=1)
    for i, (ph, title, items) in enumerate(phases):
        x = xs[i]
        ax.add_patch(plt.Circle((x, y), 2.4, color=NAVY, zorder=4))
        fc = NAVY if i % 2 == 0 else NAVY2
        by = y + 22
        box(ax, x, by, 21, 30, ph + " \u2014 " + title + "\n\n" + "\n".join("• " + t for t in items),
            fc=fc, fs=9.4, wrap=0)
        arrow(ax, (x, by - 15), (x, y + 2.4), lw=1.6, style="-")
        ax.text(x, y - 8, ph, ha="center", va="center", color=NAVY, fontsize=10, fontweight="bold")
    save(fig, "tech_roadmap.png")


# ============ 11. MARKETING / CUSTOMER-ACQUISITION FUNNEL ============
def marketing_funnel():
    from matplotlib.patches import Polygon
    fig, ax = new_ax(11.4, 7.4)
    stages = [
        ("AWARENESS", "Google Business Profile, Instagram & Facebook, site boards", NAVY),
        ("INTEREST", "Referrals, word of mouth, customer testimonials", "#20497D"),
        ("CONSIDERATION", "Consultation & transparent, itemised quotation", NAVY2),
        ("DECISION", "Signed agreement with milestone-based billing", "#3A6098"),
        ("ADVOCACY", "Referrals & repeat business", BLUE),
    ]
    top_w, bot_w = 94, 46
    n = len(stages)
    h = 13.5
    gap = 2.0
    y = 92
    cx = 50
    for i, (title, desc, color) in enumerate(stages):
        wt = top_w - (top_w - bot_w) * (i / n)
        wb = top_w - (top_w - bot_w) * ((i + 1) / n)
        yt, yb = y, y - h
        poly = Polygon([(cx - wt / 2, yt), (cx + wt / 2, yt),
                        (cx + wb / 2, yb), (cx - wb / 2, yb)],
                       closed=True, facecolor=color, edgecolor="white", lw=2, zorder=3)
        ax.add_patch(poly)
        ax.text(cx, (yt + yb) / 2 + 1.6, title, ha="center", va="center",
                color="white", fontsize=12.5, fontweight="bold", zorder=4)
        ax.text(cx, (yt + yb) / 2 - 3.4, desc, ha="center", va="center",
                color="#EAF0F8", fontsize=8.6, zorder=4)
        y = yb - gap
    save(fig, "marketing_funnel.png")


# ============ 12. QUALITY ASSURANCE & SAFETY ============
def quality_safety():
    fig, ax = new_ax(11.6, 6.2)
    ax.text(50, 96, "Quality Assurance Checkpoints", ha="center", va="center",
            color=NAVY, fontsize=13, fontweight="bold")
    stages = ["Foundation\nInspection", "Structure\nInspection",
              "Finishing\nInspection", "Final Handover\nInspection"]
    xs = [16, 39.3, 62.6, 86]
    w, hh = 20, 18
    for i, (x, s) in enumerate(zip(xs, stages)):
        box(ax, x, 78, w, hh, s, fc=NAVY if i % 2 == 0 else NAVY2, fs=10, wrap=0)
        if i < 3:
            arrow(ax, (x + w / 2, 78), (xs[i + 1] - w / 2, 78))
    ax.text(50, 50, "Safety Standards on Every Site", ha="center", va="center",
            color=NAVY, fontsize=13, fontweight="bold")
    items = ["Personal Protective\nEquipment (PPE)", "Safe Scaffolding\n& Access",
             "On-site\nSupervision", "Regulatory\nCompliance"]
    for i, (x, s) in enumerate(zip(xs, items)):
        box(ax, x, 28, w, 20, s, fc=BLUE if i % 2 == 0 else STEEL, fs=10, wrap=0)
    save(fig, "quality_safety.png")


# ============ 13. ESG / SUSTAINABILITY PILLARS ============
def esg_sustainability():
    fig, ax = new_ax(11.6, 7.0)
    pillars = [
        ("ENVIRONMENTAL", NAVY, ["Energy-efficient design",
                                 "Responsible material sourcing",
                                 "On-site waste reduction",
                                 "Green-building certifications"]),
        ("SOCIAL", NAVY2, ["Fair wages & safe conditions",
                           "Skill development for workers",
                           "Community infrastructure support",
                           "Customer trust & transparency"]),
        ("GOVERNANCE", BLUE, ["Transparent documentation",
                              "Regulatory & RERA compliance",
                              "Quality & safety standards",
                              "Ethical business conduct"]),
    ]
    cw = 30
    xs = [8, 38, 68]
    ax.text(50, 95, "Sustainability & ESG Framework", ha="center", va="center",
            color=NAVY, fontsize=14, fontweight="bold")
    for (title, color, items), x in zip(pillars, xs):
        ax.add_patch(FancyBboxPatch((x, 6), cw, 78,
                     boxstyle="round,pad=0.02,rounding_size=2", facecolor="white",
                     edgecolor=color, linewidth=2.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, 74), cw, 10, boxstyle="square,pad=0",
                     facecolor=color, edgecolor=color, zorder=3))
        ax.text(x + cw / 2, 79, title, ha="center", va="center", color="white",
                fontsize=11.5, fontweight="bold", zorder=4)
        for k, it in enumerate(items):
            ax.text(x + cw / 2, 64 - k * 15,
                    "\n".join(textwrap.wrap(it, 20)), ha="center", va="center",
                    color="#2B2B2B", fontsize=9.6, zorder=4)
    save(fig, "esg_sustainability.png")


# ============ 14. CONCLUSION KEY TAKEAWAYS + MOTTO CALLOUT ============
def key_takeaways():
    fig, ax = new_ax(11.6, 6.8)
    ax.text(50, 93, "Key Takeaways", ha="center", va="center",
            color=NAVY, fontsize=15, fontweight="bold")
    cards = [
        ("Trust-Led Differentiation", "Transparency, quality and communication\u2014not the lowest price"),
        ("Disciplined Phased Growth", "Revenue and reputation first; technology only when affordable"),
        ("Realistic Financials", "Conservative projections with break-even inside Year 1"),
        ("Clear Expansion Path", "From Chennai to a technology-enabled national brand"),
    ]
    pos = [(6, 56), (52, 56), (6, 27), (52, 27)]
    cw, ch = 42, 24
    for (title, desc), (x, y) in zip(cards, pos):
        ax.add_patch(FancyBboxPatch((x, y), cw, ch, boxstyle="round,pad=0.02,rounding_size=2",
                     facecolor=NAVY, edgecolor=NAVY, zorder=2))
        ax.text(x + cw / 2, y + ch - 6, title, ha="center", va="center", color="white",
                fontsize=11, fontweight="bold", zorder=3)
        ax.text(x + cw / 2, y + ch / 2 - 4, "\n".join(textwrap.wrap(desc, 34)),
                ha="center", va="center", color="#D9E2F0", fontsize=8.8, zorder=3)
    # closing motto banner
    ax.add_patch(FancyBboxPatch((6, 4), 88, 13, boxstyle="round,pad=0.02,rounding_size=2",
                 facecolor="#0F2A50", edgecolor="#0F2A50", zorder=2))
    ax.text(50, 10.5, '"Building Trust, Brick by Brick."', ha="center", va="center",
            color="white", fontsize=16, fontweight="bold", style="italic", zorder=3)
    save(fig, "key_takeaways.png")


if __name__ == "__main__":
    workflow()
    org_chart()
    customer_journey()
    growth_roadmap()
    problem_solution()
    expansion_timeline()
    business_phases()
    market_overview()
    swot_matrix()
    tech_roadmap()
    marketing_funnel()
    quality_safety()
    esg_sustainability()
    key_takeaways()
    print("all diagrams done")
