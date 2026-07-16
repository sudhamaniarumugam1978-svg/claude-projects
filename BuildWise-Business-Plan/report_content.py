#!/usr/bin/env python3
"""Single source of truth for the BuildWise Business Plan Report.

The report is expressed as an ordered list of *block* dictionaries.  Two
renderers (``render_docx.py`` and ``render_pdf.py``) consume this same list so
that the generated .docx and .pdf remain identical in structure and content.

Block types
-----------
cover                           the title page (renderers hard-code its layout)
pagebreak                       force a new page
chapter   {label,title}         chapter divider page (new page + navy rule)
fmhead    {text, rule}          centred front-matter heading (Declaration/TOC)
h         {lvl,text}            section heading, lvl 2 (15pt) / 3 (13pt)
p         {text}                justified body paragraph (supports **bold**)
bullets   {items,title,check}   bullet / tick list, optional bold heading
table     {header,rows,widths}  navy-header table with alternating shading
kpis      {cards}               row of navy KPI cards  [(big, small), ...]
cards     {items,cols}          navy-title / grey-body cards  [(title, body)]
callout   {title,text}          grey insight box with navy left border
figure    {src,caption,w}       centred figure + italic caption (w = frac width)
note      {text}                small centred italic note
refs      {items}               numbered reference list
"""

NAVY = "#163A70"

# ---------------------------------------------------------------------------
# convenience builders
# ---------------------------------------------------------------------------
def ch(label, title):
    return {"t": "chapter", "label": label, "title": title}


def h(text, lvl=2):
    return {"t": "h", "lvl": lvl, "text": text}


def p(text):
    return {"t": "p", "text": text}


def pb():
    return {"t": "pagebreak"}


def tbl(header, rows, widths=None):
    return {"t": "table", "header": header, "rows": rows, "widths": widths}


def bullets(items, title=None, check=True):
    return {"t": "bullets", "items": items, "title": title, "check": check}


def kpis(cards):
    return {"t": "kpis", "cards": cards}


def cards(items, cols):
    return {"t": "cards", "items": items, "cols": cols}


def callout(title, text):
    return {"t": "callout", "title": title, "text": text}


import re as _re


def fig(n, caption, w=0.85):
    # Strip any hard-coded "Figure N." prefix; renderers assign sequential numbers.
    caption = _re.sub(r"^\s*Figure\s+\d+\.?\s*", "", caption)
    return {"t": "figure", "src": f"figures/fig{n:02d}.png", "caption": caption, "w": w}


def note(text):
    return {"t": "note", "text": text}


def fmhead(text, rule=False):
    return {"t": "fmhead", "text": text, "rule": rule}


def refs(items):
    return {"t": "refs", "items": items}


# ---------------------------------------------------------------------------
# THE REPORT
# ---------------------------------------------------------------------------
BLOCKS = []
B = BLOCKS.append

# ===================== PAGE 1 : COVER =====================
B({"t": "cover"})

# ===================== PAGE 2 : DECLARATION & ACKNOWLEDGEMENT =====================
B(pb())
B(fmhead("DECLARATION"))
B(p("We hereby declare that the Business Plan Report titled \u201cBuildWise "
    "Constructions Pvt. Ltd.\u201d is an original work prepared by our team as part "
    "of the Entrepreneurship and Family Business Management course requirements at "
    "SRM Institute of Science and Technology, Vadapalani Campus."))
B(p("The ideas, business strategies, financial projections, market analysis, and "
    "operational plans presented in this report have been developed through "
    "systematic research, critical analysis, and collaborative discussion among the "
    "team members. Every effort has been made to ensure that the information "
    "presented is accurate, realistic, and relevant to the objectives of this "
    "academic project."))
B(p("We further declare that this report has not been submitted, either wholly or "
    "partially, to any other institution or university for the award of any degree, "
    "diploma, or academic certification."))
B({"t": "hr"})
B(fmhead("ACKNOWLEDGEMENT"))
B(p("We express our sincere gratitude to our faculty members of the Department of "
    "Computer Science and Engineering (Emerging Technologies) and the Department of "
    "Computer Science and Business Systems, SRM Institute of Science and Technology, "
    "Vadapalani Campus, for their valuable guidance, encouragement, and continuous "
    "support throughout the preparation of this Business Plan Report."))
B(p("We also thank our classmates, friends, and well-wishers whose constructive "
    "suggestions and discussions helped us refine our business idea and improve the "
    "overall quality of this report. Finally, we acknowledge the collective effort "
    "of every team member in successfully planning, researching, analysing, and "
    "documenting this project."))
B(h("Prepared by", lvl=2))
B(tbl(["Team Member", "Register Number"],
      [["THILAK KUMAR K", "RA2311042040014"],
       ["ARJUN S", "RA2311042040018"],
       ["SANJAY KUMAR A M", "RA2311042040024"]],
      widths=[0.6, 0.4]))
B(p("**Place:** Chennai"))
B(p("**Date:** __________________"))

# ===================== PAGE 3 : TABLE OF CONTENTS =====================
B(pb())
B(fmhead("TABLE OF CONTENTS", rule=True))
B(tbl(["S.No", "Contents", "Page No"],
      [["1", "Executive Summary", "3"],
       ["2", "Company Overview", "5"],
       ["3", "Industry & Market Analysis", "7"],
       ["4", "Problem Statement & Solution", "9"],
       ["5", "Products & Services", "11"],
       ["6", "Business Model", "13"],
       ["7", "Competitor Analysis & SWOT", "15"],
       ["8", "Marketing Strategy", "17"],
       ["9", "Operations Plan", "19"],
       ["10", "Customer Experience Strategy", "21"],
       ["11", "Management & Organizational Structure", "22"],
       ["12", "Financial Plan", "23"],
       ["13", "Risk Assessment & Mitigation", "26"],
       ["14", "Technology Roadmap", "27"],
       ["15", "Growth Roadmap, Sustainability & Conclusion", "28"],
       ["", "References", "29"]],
      widths=[0.12, 0.70, 0.18]))
B(note("This report presents a phased business strategy for establishing BuildWise "
       "Constructions Pvt. Ltd. as a technology-enabled construction company focused "
       "on transparency, quality, and sustainable growth."))

# ===================== PAGE 4 : CHAPTER 1 EXECUTIVE SUMMARY =====================
B(ch("CHAPTER 1", "EXECUTIVE SUMMARY"))
B(h("Business Overview"))
B(p("BuildWise Constructions Pvt. Ltd. is a technology-enabled construction startup "
    "headquartered in Chennai, Tamil Nadu, established with the vision of transforming "
    "conventional construction practices through transparency, quality workmanship, "
    "disciplined project execution, and customer trust."))
B(p("Rather than competing solely on pricing, BuildWise delivers a structured "
    "construction experience supported by modern project management and a phased "
    "growth strategy that gradually introduces AI-assisted estimation, digital "
    "project management, and smart-home integration."))
B(h("Company Snapshot"))
B(tbl(["Particular", "Details"],
      [["Company Name", "BuildWise Constructions Pvt. Ltd."],
       ["Industry", "Construction & Infrastructure"],
       ["Business Model", "Technology-Enabled Construction Startup"],
       ["Headquarters", "Chennai, Tamil Nadu"],
       ["Legal Structure", "Private Limited Company"],
       ["Initial Capital", "\u20b91.00 Crore"],
       ["Target Market", "Residential & Commercial Construction"],
       ["Business Stage", "Startup (Phase 1)"]],
      widths=[0.32, 0.68]))
B(h("Financial Snapshot"))
B(kpis([("\u20b91.00 Cr", "Initial Investment"),
        ("\u20b92.02 Cr", "Projected Year-1 Revenue"),
        ("Year 1", "Expected Break-even"),
        ("\u20b98.76 Cr", "Projected Year-3 Revenue")]))
B(fig(1, "Figure 1. Overall business philosophy of BuildWise Constructions Pvt. Ltd.",
      w=0.34))
B(callout("Business Insight",
          "BuildWise positions itself not merely as a construction contractor, but as "
          "a trusted project partner delivering transparency, quality, and "
          "technology-driven construction solutions through a phased and financially "
          "sustainable growth model."))

# ===================== PAGE 5 : CH1 CONTINUED =====================
B(pb())
B(h("Business Challenge vs BuildWise Solution"))
B(tbl(["Current Industry Challenges", "BuildWise Solutions"],
      [["Lack of cost transparency", "Itemized quotations with milestone-based billing"],
       ["Delayed project completion", "Planned execution with scheduling and tracking"],
       ["Poor communication", "Weekly project updates with digital documentation"],
       ["Frequent budget overruns", "AI-assisted estimation and cost monitoring (future)"],
       ["Inconsistent quality", "Stage-wise inspections and quality checkpoints"],
       ["Weak after-sales support", "Dedicated support with 10-year structural warranty"]],
      widths=[0.42, 0.58]))
B(h("Mission \u2022 Vision \u2022 Core Values"))
B(cards([("Mission", "To deliver reliable, transparent, and high-quality construction "
          "services while building long-term customer trust through disciplined "
          "execution and responsible technology adoption."),
         ("Vision", "To become one of India's most trusted technology-enabled "
          "construction companies by combining engineering excellence, innovation, "
          "and customer satisfaction."),
         ("Core Values", ["Transparency", "Integrity", "Quality", "Innovation",
                          "Customer Commitment", "Sustainability"])], cols=3))
B(h("Target Customers"))
B(tbl(["Segment", "Primary Need"],
      [["Individual Homeowners", "Affordable, transparent home construction"],
       ["Commercial Clients", "Reliable project execution within deadlines"],
       ["SMEs", "Cost-effective office and retail infrastructure"],
       ["Property Investors", "End-to-end construction management"]],
      widths=[0.35, 0.65]))
B(fig(2, "Figure 2. Phased business growth strategy of BuildWise.", w=0.9))
B(callout("Executive Perspective",
          "BuildWise is built on the belief that trust is the foundation of every "
          "successful construction project. By combining disciplined execution, "
          "financial responsibility, and carefully adopted technology, the company "
          "focuses on sustainable growth, long-term customer relationships, and "
          "operational excellence rather than rapid expansion."))

# ===================== PAGE 6 : CHAPTER 2 COMPANY OVERVIEW =====================
B(ch("CHAPTER 2", "COMPANY OVERVIEW"))
B(h("2.1 Company Introduction"))
B(p("BuildWise Constructions Pvt. Ltd. is a technology-enabled construction startup "
    "established in Chennai to deliver transparent, reliable, and professionally "
    "managed construction services across residential and commercial projects. Unlike "
    "conventional contractors that prioritize short-term profits, BuildWise "
    "emphasizes systematic project management, ethical practices, customer trust, and "
    "sustainable growth \u2014 achieving operational excellence first, before "
    "technology adoption and geographical expansion."))
B(h("2.2 Company Snapshot"))
B(tbl(["Particular", "Details"],
      [["Company Name", "BuildWise Constructions Pvt. Ltd."],
       ["Business Type", "Private Limited Startup"],
       ["Industry", "Construction & Infrastructure"],
       ["Headquarters", "Chennai, Tamil Nadu"],
       ["Nature of Business", "Residential & Commercial Construction"],
       ["Initial Capital", "\u20b91 Crore"],
       ["Business Model", "Technology-Enabled Construction Services"],
       ["Target Market", "Homeowners, SMEs & Commercial Clients"]],
      widths=[0.34, 0.66]))
B(callout("Our Philosophy \u2014 \u201cBuilding Trust, Brick by Brick.\u201d",
          "BuildWise believes successful projects are built on trust, transparency, "
          "and consistent quality rather than aggressive pricing \u2014 treating "
          "every project as a long-term relationship where customer satisfaction and "
          "engineering excellence remain the highest priorities."))
B(h("2.4 What Makes BuildWise Different?"))
B(tbl(["Traditional Contractors", "BuildWise"],
      [["Price-focused", "Value-focused"],
       ["Limited customer updates", "Regular project communication"],
       ["Manual documentation", "Digital records & reports"],
       ["Reactive planning", "Structured project management"],
       ["Limited after-sales support", "Warranty & relationship management"],
       ["Technology only when necessary", "Planned technology adoption"]],
      widths=[0.5, 0.5]))
B(fig(3, "Figure 3. BuildWise business foundation.", w=0.30))

# ===================== PAGE 7 : CH2 CONTINUED =====================
B(pb())
B(h("2.5 Business Objectives"))
B(tbl(["Timeline", "Business Objectives"],
      [["Short Term (Year 1)", "Establish BuildWise in Chennai by completing "
        "residential projects, building customer trust, achieving operational "
        "stability, and reaching break-even."],
       ["Medium Term (Years 2\u20133)", "Expand into commercial construction, "
        "strengthen supplier partnerships, improve digital project management, and "
        "increase annual revenue through operational efficiency."],
       ["Long Term (Years 4\u20135)", "Expand into multiple cities, integrate "
        "AI-assisted estimation, drone monitoring and IoT-enabled smart buildings, "
        "and establish BuildWise as a trusted regional brand."]],
      widths=[0.26, 0.74]))
B(callout("Our Growth Strategy \u2014 \u201cTrust First, Technology Next\u201d",
          "Instead of investing heavily in advanced technologies during the startup "
          "phase, BuildWise first prioritizes quality construction, customer trust, a "
          "strong market reputation, and financial stability. Technology is "
          "introduced only when it creates measurable business value."))
B(fig(4, "Figure 4. Strategic growth philosophy adopted by BuildWise.", w=0.42))
B(h("2.7 Organizational Principles"))
B(cards([("Customer First", "Deliver long-term value rather than short-term profits."),
         ("Transparency", "Maintain open communication and milestone-based billing."),
         ("Quality", "Follow engineering standards and strict quality inspections."),
         ("Innovation", "Adopt technology only when it improves efficiency."),
         ("Sustainability", "Promote responsible construction and resource optimization."),
         ("Continuous Improvement", "Learn from every project to improve performance.")],
        cols=3))
B(callout("Strategic Insight",
          "Unlike many startups that invest heavily in technology from the beginning, "
          "BuildWise follows a financially disciplined approach by first establishing "
          "operational excellence and customer trust, minimizing financial risk while "
          "creating a strong foundation for long-term expansion."))

# ===================== PAGE 8 : CHAPTER 3 INDUSTRY & MARKET =====================
B(ch("CHAPTER 3", "INDUSTRY & MARKET ANALYSIS"))
B(h("3.1 Industry Overview"))
B(p("The Indian construction industry is one of the country's largest contributors "
    "to economic development, supporting infrastructure, manufacturing, real estate, "
    "transportation, and urban development. Rapid urbanization, population growth, and "
    "government initiatives such as the Smart Cities Mission and PMAY continue to "
    "drive demand for residential and commercial construction."))
B(p("Tamil Nadu, particularly Chennai, remains one of South India's most active "
    "construction markets due to the continuous expansion of residential communities, "
    "commercial complexes, IT corridors, and institutional infrastructure \u2014 "
    "creating favourable conditions for professionally managed construction firms."))
B(h("3.2 Industry Snapshot"))
B(tbl(["Parameter", "Market Observation"],
      [["Industry", "Construction & Infrastructure"],
       ["Primary Market", "Residential & Commercial Construction"],
       ["Growth Driver", "Urbanization & Infrastructure Development"],
       ["Focus Region", "Chennai, Tamil Nadu"],
       ["Customer Trend", "Preference for transparent, quality-focused builders"],
       ["Opportunity", "Technology-enabled project management & communication"]],
      widths=[0.30, 0.70]))
B(fig(5, "Figure 5. Major factors contributing to the growth of the Indian "
      "construction industry.", w=0.6))
B(callout("Industry Insight",
          "The construction industry is no longer driven solely by engineering "
          "capability. Customers increasingly evaluate firms on transparency, "
          "communication, timely delivery, and overall project experience \u2014 an "
          "opportunity for BuildWise to differentiate through structured project "
          "management rather than price alone."))

# ===================== PAGE 9 : CH3 CONTINUED =====================
B(pb())
B(h("3.4 Target Market"))
B(p("BuildWise focuses on customers seeking reliable, transparent, and "
    "professionally managed construction services. Rather than targeting every "
    "segment at once, the company adopts a phased customer-acquisition strategy, "
    "beginning with residential homeowners and expanding into commercial and "
    "institutional projects as capacity grows."))
B(tbl(["Customer Segment", "Requirements", "BuildWise Solution"],
      [["Individual Homeowners", "Affordable, transparent homes", "Fixed quotations, milestone billing, updates"],
       ["Commercial Businesses", "Offices, retail, warehouses", "End-to-end management with quality assurance"],
       ["SMEs", "Cost-effective expansion", "Budget-conscious construction planning"],
       ["Property Investors", "Reliable, timely delivery", "Structured execution with documentation"],
       ["Institutions", "Functional, durable facilities", "Professional planning & engineering standards"]],
      widths=[0.24, 0.34, 0.42]))
B(cards([("First-Time Homeowner",
          "Age 28\u201340. Needs an affordable home, transparent pricing, and a "
          "reliable contractor. Fears hidden costs, delays, and poor workmanship."),
         ("Small Business Owner",
          "Needs office/shop construction with budget control and quick completion. "
          "Concerned about business interruption and cost overruns."),
         ("Property Investor",
          "Needs timely delivery, professional management, and documentation. "
          "Concerned about contractor reliability and quality consistency.")], cols=3))
B(fig(6, "Figure 6. Customer segmentation framework of BuildWise.", w=0.5))
B(callout("Customer Insight",
          "Modern customers no longer evaluate construction companies solely on price. "
          "Transparency, communication, project visibility, documentation, and timely "
          "delivery have become equally important \u2014 expectations BuildWise meets "
          "by combining engineering expertise with customer-focused management."))

# ===================== PAGE 10 : CHAPTER 4 PROBLEM & SOLUTION =====================
B(ch("CHAPTER 4", "PROBLEM STATEMENT & PROPOSED SOLUTION"))
B(h("4.1 Industry Challenges"))
B(p("The construction industry has grown rapidly, yet customers continue to face "
    "recurring issues affecting project quality, cost, and satisfaction. Most "
    "problems arise from poor planning, weak communication, inadequate "
    "documentation, inconsistent quality control, and a lack of transparency across "
    "the construction lifecycle."))
B(tbl(["Existing Industry Problem", "Impact on Customer"],
      [["Hidden or changing quotations", "Budget uncertainty and financial stress"],
       ["Delayed project completion", "Increased costs and inconvenience"],
       ["Poor communication", "Lack of confidence and project confusion"],
       ["Inconsistent construction quality", "Rework and reduced building lifespan"],
       ["Manual documentation", "Difficulty tracking project progress"],
       ["No structured warranty support", "Poor post-project satisfaction"]],
      widths=[0.5, 0.5]))
B(h("4.2 BuildWise Solution Framework"))
B(tbl(["Customer Expectation", "BuildWise Solution"],
      [["Transparent Pricing", "Detailed quotations with milestone-based billing"],
       ["Timely Completion", "Structured planning and project scheduling"],
       ["Continuous Communication", "Weekly progress reports and digital records"],
       ["Quality Assurance", "Stage-wise inspections and engineering standards"],
       ["Project Visibility", "Live tracking (future phase)"],
       ["Long-Term Support", "10-year structural warranty and relationship management"]],
      widths=[0.42, 0.58]))
B(fig(8, "Figure 8. Root causes contributing to customer dissatisfaction in "
      "traditional construction projects.", w=0.4))
B(callout("Business Insight",
          "The success of BuildWise does not depend solely on constructing buildings. "
          "Its competitive advantage lies in delivering a predictable, transparent, "
          "and professionally managed construction experience that reduces customer "
          "uncertainty while improving quality and long-term satisfaction."))

# ===================== PAGE 11 : CH4 CONTINUED =====================
B(pb())
B(h("4.3 Unique Value Proposition (UVP)"))
B(p("Every construction company promises quality, affordability, and timely "
    "completion. BuildWise differentiates itself by delivering a structured "
    "construction experience that emphasizes transparency, customer involvement, and "
    "long-term trust rather than focusing solely on project completion."))
B(tbl(["Customer Expectation", "Traditional Practice", "BuildWise Approach"],
      [["Cost Estimation", "Approximate quotations", "Detailed, itemized quotations"],
       ["Billing", "Lump-sum payments", "Transparent milestone-based billing"],
       ["Communication", "Irregular updates", "Weekly reports with documentation"],
       ["Quality Assurance", "Final inspection only", "Stage-wise quality inspections"],
       ["Project Monitoring", "Manual supervision", "Structured project management"],
       ["Customer Support", "Ends after completion", "Warranty & relationship management"]],
      widths=[0.26, 0.34, 0.40]))
B(fig(10, "Figure 10. Value creation process adopted by BuildWise from planning to "
      "long-term customer relationship.", w=0.32))
B(fig(11, "Figure 11. Competitive positioning of BuildWise based on quality and "
      "transparency.", w=0.5))
B(callout("Why This Model Works",
          "BuildWise does not compete solely on price. It competes by reducing "
          "uncertainty through structured planning, transparent communication, and "
          "consistent quality control \u2014 creating higher customer satisfaction, "
          "stronger referrals, and sustainable long-term growth."))

# ===================== PAGE 12 : CHAPTER 5 PRODUCTS & SERVICES =====================
B(ch("CHAPTER 5", "PRODUCTS & SERVICES"))
B(h("5.1 Introduction"))
B(p("BuildWise offers an integrated portfolio of construction solutions for "
    "homeowners, businesses, and institutional clients. Beyond civil construction, "
    "the company provides end-to-end execution including planning, interior "
    "development, renovation, consultation, and post-construction support, introduced "
    "in phases to ensure sustainable growth."))
B(tbl(["Service Category", "Description", "Target Customers"],
      [["Residential Construction", "Houses, villas, apartments", "Homeowners"],
       ["Commercial Construction", "Offices, retail, warehouses", "SMEs & Businesses"],
       ["Interior Design & Fit-outs", "Modular interiors, office layouts", "Residential & Commercial"],
       ["Renovation & Remodeling", "Upgrades, extensions, improvements", "Property Owners"],
       ["Project Consultation", "Planning, budgeting, approvals", "All Segments"],
       ["Annual Maintenance", "Repairs and preventive maintenance", "Existing Customers"]],
      widths=[0.26, 0.42, 0.32]))
B(fig(12, "Figure 12. Comprehensive service ecosystem offered by BuildWise.", w=0.6))
B(h("Future Service Expansion"))
B(tbl(["Phase", "Future Service"],
      [["Phase 2", "Digital Project Tracking"],
       ["Phase 2", "Drone Site Monitoring"],
       ["Phase 3", "AI-Based Cost Estimation"],
       ["Phase 3", "IoT Smart Home Integration"],
       ["Phase 4", "Green Building Consultancy"],
       ["Phase 4", "Smart Facility Management"]],
      widths=[0.25, 0.75]))
B(callout("Service Strategy",
          "Rather than launching every service simultaneously, BuildWise follows a "
          "phased expansion model that strengthens operational capability, maintains "
          "quality standards, and manages financial resources effectively \u2014 "
          "reducing startup risk while ensuring sustainable growth."))

# ===================== PAGE 13 : CH5 CONTINUED =====================
B(pb())
B(h("5.3 Service Delivery Process"))
B(p("Delivering quality construction involves more than physical work. BuildWise "
    "follows a standardized service delivery process from enquiry to final handover, "
    "reducing delays, minimizing communication gaps, and ensuring consistent project "
    "outcomes."))
B(fig(13, "Figure 13. Standardized service delivery process adopted by BuildWise.",
      w=0.92))
B(cards([("Transparent Pricing", "Itemized quotations with milestone-based billing "
          "eliminate hidden costs and improve financial planning."),
         ("Dedicated Project Management", "Structured planning, scheduled reviews, "
          "and continuous customer communication for every project."),
         ("Quality Assurance", "Multiple quality inspections throughout construction "
          "rather than only at project completion."),
         ("Long-Term Support", "Warranty services, maintenance assistance, and "
          "customer relationship management after handover.")], cols=2))
B(tbl(["Feature", "Conventional Builder", "BuildWise"],
      [["Detailed Quotation", "Partial", "Comprehensive"],
       ["Progress Updates", "Occasionally", "Weekly"],
       ["Quality Checks", "Final Stage", "Every Major Stage"],
       ["Documentation", "Manual", "Digital Records"],
       ["Warranty", "Limited", "10-Year Structural Warranty"],
       ["Customer Support", "Ends after delivery", "Ongoing Relationship Management"]],
      widths=[0.28, 0.34, 0.38]))
B(callout("Customer Experience Philosophy",
          "Excellent customer experience is achieved through consistent "
          "communication, transparent pricing, disciplined execution, and dependable "
          "after-sales support \u2014 transforming satisfied customers into long-term "
          "brand advocates and generating growth through referrals."))

# ===================== PAGE 14 : CHAPTER 6 BUSINESS MODEL =====================
B(ch("CHAPTER 6", "BUSINESS MODEL"))
B(h("6.1 Introduction"))
B(p("A well-defined business model enables an organization to create value for "
    "customers while ensuring long-term profitability. BuildWise follows a "
    "customer-centric model combining quality construction, transparent execution, "
    "and phased technology adoption, focusing on operational excellence and financial "
    "discipline before scaling."))
B(fig(15, "Figure 15. Business Model Canvas illustrating how BuildWise creates, "
      "delivers, and captures value.", w=0.98))
B(h("6.3 Revenue Streams"))
B(tbl(["Revenue Source", "Description", "Contribution"],
      [["Residential Construction", "Houses, villas, apartments", "High"],
       ["Commercial Construction", "Office and retail projects", "High"],
       ["Interior Design", "Residential & commercial interiors", "Medium"],
       ["Renovation Projects", "Remodeling & extensions", "Medium"],
       ["Consultancy Services", "Planning, estimation & approvals", "Medium"],
       ["Annual Maintenance", "AMC & building maintenance", "Low (Growing)"]],
      widths=[0.30, 0.46, 0.24]))
B(callout("Sustainable Revenue Strategy",
          "BuildWise does not depend on a single source of income. Offering multiple "
          "construction-related services reduces business risk while maintaining "
          "stable cash flow, with technology-enabled services and maintenance "
          "contracts providing recurring revenue as the company grows."))

# ===================== PAGE 15 : CH6 CONTINUED =====================
B(pb())
B(h("6.4 Pricing Strategy"))
B(p("BuildWise adopts a value-based pricing strategy rather than competing solely on "
    "the lowest quotation. Every quotation is transparent, itemized, and discussed "
    "with the customer before work begins, and payments follow milestone-based "
    "billing linked to completed stages of construction."))
B(tbl(["Pricing Component", "Description"],
      [["Material Cost", "Based on current market rates and approved specifications"],
       ["Labour Charges", "Skilled and unskilled workforce allocation"],
       ["Equipment & Machinery", "Rental and operational expenses"],
       ["Project Management Fee", "Planning, supervision, documentation, coordination"],
       ["Contingency Reserve", "Allocated for unforeseen project requirements"],
       ["Profit Margin", "Sustainable margin while maintaining competitive pricing"]],
      widths=[0.32, 0.68]))
B(fig(17, "Figure 17. Standardized operational workflow from customer enquiry to "
      "post-project support.", w=0.92))
B(tbl(["Expense Category", "Estimated Share"],
      [["Construction Materials", "50%"], ["Labour & Workforce", "20%"],
       ["Equipment & Machinery", "10%"], ["Administration & Operations", "8%"],
       ["Marketing & Customer Acquisition", "5%"], ["Technology & Software", "4%"],
       ["Contingency & Miscellaneous", "3%"]],
      widths=[0.6, 0.4]))
B(fig(18, "Figure 18. Estimated allocation of operational expenses across major cost "
      "categories.", w=0.46))
B(callout("Sustainable Growth Philosophy",
          "Unlike many startups that expand aggressively, BuildWise prioritizes "
          "operational excellence before scaling. This disciplined approach minimizes "
          "financial risk, strengthens customer trust, and creates a stable platform "
          "for long-term expansion."))

# ===================== PAGE 16 : CHAPTER 7 COMPETITOR & SWOT =====================
B(ch("CHAPTER 7", "COMPETITOR ANALYSIS & SWOT"))
B(h("7.2 Market Competitor Categories"))
B(tbl(["Competitor Category", "Strengths", "Common Limitations"],
      [["Local Contractors", "Low pricing, local ties", "Inconsistent quality, poor docs"],
       ["Regional Builders", "Better resources, portfolio", "Slower comms, higher overheads"],
       ["National Companies", "Large-scale, strong brand", "Expensive, less personalized"],
       ["Interior Design Firms", "Specialized expertise", "Limited civil capabilities"],
       ["Freelance Consultants", "Affordable consultation", "Depend on third-party execution"]],
      widths=[0.26, 0.34, 0.40]))
B(h("7.3 BuildWise Competitive Position"))
B(tbl(["Feature", "Local", "Regional", "National", "BuildWise"],
      [["Transparent Pricing", "Limited", "Moderate", "Good", "Excellent"],
       ["Communication", "Low", "Moderate", "Moderate", "Excellent"],
       ["Digital Documentation", "Rare", "Partial", "Available", "Comprehensive"],
       ["Quality Monitoring", "Basic", "Good", "Excellent", "Stage-wise"],
       ["Customer Support", "Limited", "Moderate", "Moderate", "Dedicated"],
       ["Technology", "Minimal", "Moderate", "Advanced", "Phased"]],
      widths=[0.28, 0.16, 0.18, 0.18, 0.20]))
B(fig(19, "Figure 19. Competitive positioning of BuildWise relative to major "
      "categories of construction service providers.", w=0.62))
B(callout("Competing through Trust Rather than Price",
          "Instead of competing on the lowest quotation, BuildWise delivers "
          "predictable outcomes through transparent pricing, disciplined management, "
          "documented communication, and long-term relationships \u2014 creating "
          "higher confidence and stronger referral-based growth."))

# ===================== PAGE 17 : CH7 CONTINUED (SWOT) =====================
B(pb())
B(h("7.4 SWOT Analysis"))
B(fig(20, "Figure 20. SWOT analysis of BuildWise Constructions Pvt. Ltd.", w=0.82))
B(h("7.5 Strategic Interpretation"))
B(tbl(["Strategic Focus", "Action Plan"],
      [["Leverage Strengths", "Promote transparency and project management as key differentiators."],
       ["Address Weaknesses", "Build brand recognition through successful projects and referrals."],
       ["Capture Opportunities", "Expand into commercial construction and gradually adopt technology."],
       ["Mitigate Threats", "Strengthen supplier partnerships and maintain contingency reserves."]],
      widths=[0.3, 0.7]))
B(callout("Building a Sustainable Competitive Advantage",
          "Unlike competitors that differentiate through pricing or scale, BuildWise "
          "focuses on superior customer experience through transparency, disciplined "
          "execution, and quality assurance \u2014 building trust, generating repeat "
          "business, and creating an advantage difficult to replicate."))

# ===================== PAGE 18 : CHAPTER 8 MARKETING =====================
B(ch("CHAPTER 8", "MARKETING STRATEGY"))
B(h("8.1 Introduction"))
B(p("The success of a construction company depends not only on engineering expertise "
    "but on its ability to build trust, generate quality leads, and maintain "
    "long-term relationships. BuildWise adopts a relationship-driven marketing "
    "strategy combining digital marketing, referral programs, strategic partnerships, "
    "and strong customer engagement."))
B(h("8.2 Marketing Objectives"))
B(tbl(["Objective", "Expected Outcome"],
      [["Build Brand Awareness", "Establish BuildWise as a trusted builder in Chennai"],
       ["Generate Qualified Leads", "Increase enquiries via digital and offline channels"],
       ["Strengthen Customer Trust", "Improve confidence through transparency"],
       ["Increase Conversion Rate", "Convert enquiries into confirmed projects"],
       ["Build Long-Term Relationships", "Encourage referrals and repeat customers"]],
      widths=[0.4, 0.6]))
B(tbl(["Marketing Channel", "Purpose", "Priority"],
      [["Company Website", "Portfolio, enquiries, credibility", "High"],
       ["Google Business Profile", "Local visibility and reviews", "High"],
       ["Social Media", "Brand awareness and project updates", "High"],
       ["Customer Referral Program", "Generate trusted leads", "High"],
       ["Architects & Designers", "Strategic partnerships", "Medium"],
       ["Property Consultants", "Lead generation", "Medium"]],
      widths=[0.34, 0.46, 0.20]))
B(fig(22, "Figure 22. Marketing ecosystem adopted by BuildWise for customer "
      "acquisition.", w=0.62))
B(callout("Relationship-Based Marketing",
          "BuildWise believes the strongest marketing tool is customer satisfaction. "
          "Every completed project becomes a live advertisement through referrals, "
          "testimonials, and word-of-mouth \u2014 reducing acquisition costs while "
          "strengthening brand credibility."))

# ===================== PAGE 19 : CH8 CONTINUED =====================
B(pb())
B(h("8.4 Customer Acquisition Strategy"))
B(p("Acquiring construction projects requires a structured process that nurtures "
    "customer confidence from first enquiry to project confirmation. BuildWise "
    "follows a customer-acquisition funnel designed to maximize conversion while "
    "maintaining a professional experience."))
B(fig(23, "Figure 23. Customer acquisition funnel converting enquiries into confirmed "
      "projects.", w=0.5))
B(h("8.5 Branding Strategy"))
B(cards([("Brand Identity", "\u201cBuilding Trust, Brick by Brick.\u201d Consistent "
          "branding across all communication platforms."),
         ("Visual Identity", "Professional logo, navy-blue theme, branded site "
          "boards, uniforms, and digital documentation."),
         ("Customer Experience", "Prompt communication, transparent documentation, "
          "timely updates, and structured execution."),
         ("Online Presence", "Website, Google reviews, project galleries, and social "
          "media engagement.")], cols=2))
B(tbl(["Activity", "Objective"],
      [["Project Portfolio Website", "Showcase completed projects"],
       ["Social Media Campaigns", "Increase brand awareness"],
       ["Customer Testimonials", "Build credibility"],
       ["Referral Rewards", "Encourage word-of-mouth marketing"],
       ["Educational Blogs & Videos", "Demonstrate expertise"]],
      widths=[0.45, 0.55]))
B(callout("Marketing Philosophy",
          "Rather than investing heavily in expensive advertising, BuildWise focuses "
          "on delivering exceptional customer experiences that naturally generate "
          "referrals and strengthen market reputation \u2014 supporting sustainable "
          "growth while optimizing marketing spend."))

# ===================== PAGE 20 : CHAPTER 9 OPERATIONS =====================
B(ch("CHAPTER 9", "OPERATIONS PLAN"))
B(h("9.1 Introduction"))
B(p("Operational success depends on systematic planning, efficient resource "
    "utilization, quality assurance, and effective coordination among stakeholders. "
    "BuildWise follows a standardized operational framework that ensures every "
    "project progresses through clearly defined stages, minimizing delays and "
    "maintaining consistent quality."))
B(fig(25, "Figure 25. Standard operational workflow followed by BuildWise for every "
      "construction project.", w=0.92))
B(h("9.3 Resource Planning"))
B(tbl(["Resource Category", "Purpose"],
      [["Civil Engineers", "Project planning and supervision"],
       ["Site Supervisors", "Daily site management"],
       ["Skilled Labour", "Masonry, carpentry, electrical, plumbing, finishing"],
       ["Procurement Team", "Material sourcing and inventory management"],
       ["Quality Engineers", "Stage-wise inspection and compliance"],
       ["Project Manager", "Overall coordination and customer communication"]],
      widths=[0.32, 0.68]))
B(callout("Efficient Operations Drive Customer Satisfaction",
          "Construction quality depends on disciplined coordination between "
          "procurement, workforce management, scheduling, and quality control. "
          "BuildWise's standardized workflow minimizes delays while improving "
          "efficiency and customer confidence."))

# ===================== PAGE 21 : CH9 CONTINUED =====================
B(pb())
B(h("9.4 Quality Assurance Framework"))
B(fig(27, "Figure 27. Multi-stage quality assurance framework adopted by BuildWise.",
      w=0.42))
B(tbl(["Inspection Stage", "Key Verification"],
      [["Foundation", "Soil condition, reinforcement, concrete quality"],
       ["Structural Work", "Columns, beams, slab alignment"],
       ["Masonry", "Wall alignment, joint quality"],
       ["Electrical & Plumbing", "Safety compliance and leak testing"],
       ["Finishing", "Painting, flooring, fixtures"],
       ["Final Audit", "Complete project verification before handover"]],
      widths=[0.32, 0.68]))
B(cards([("Worker Safety", "Mandatory PPE, regular safety briefings, accident prevention."),
         ("Site Safety", "Hazard identification, barricading, warning signs, access."),
         ("Equipment Safety", "Routine inspection and preventive maintenance."),
         ("Environmental Safety", "Dust control, waste segregation, noise reduction.")],
        cols=2))
B(fig(28, "Figure 28. Conceptual project monitoring dashboard for tracking "
      "operational performance.", w=0.6))
B(callout("Operational Excellence Through Standardization",
          "Standardizing execution enables BuildWise to deliver consistent quality "
          "regardless of project size. Defined workflows, periodic inspections, and "
          "continuous monitoring reduce operational risks while improving customer "
          "satisfaction."))

# ===================== PAGE 22 : CHAPTER 10 CUSTOMER EXPERIENCE =====================
B(ch("CHAPTER 10", "CUSTOMER EXPERIENCE STRATEGY"))
B(h("10.1 Introduction"))
B(p("In construction, customer satisfaction is determined not only by the final "
    "structure but by the overall experience across the project lifecycle. BuildWise "
    "adopts a customer-centric approach where transparency, responsiveness, and "
    "consistent communication are core principles from first enquiry to post-handover "
    "support."))
B(fig(29, "Figure 29. Complete customer journey followed by BuildWise from enquiry to "
      "long-term relationship management.", w=0.92))
B(h("10.3 Customer Communication Framework"))
B(tbl(["Project Stage", "Customer Communication"],
      [["Initial Consultation", "Requirement gathering and project discussion"],
       ["Planning Phase", "Budget estimation, design review, project schedule"],
       ["Construction Phase", "Weekly progress reports with photographs"],
       ["Quality Inspection", "Inspection reports and customer walkthrough"],
       ["Project Handover", "Documentation, warranty certificate, guidelines"],
       ["Post-Completion", "Feedback, support assistance, referral programme"]],
      widths=[0.30, 0.70]))
B(callout("Customer Experience as a Competitive Advantage",
          "Exceptional customer experience is one of the strongest competitive "
          "advantages in construction. Transparent communication, reliable execution, "
          "timely support, and long-term engagement generate referrals, strengthen "
          "reputation, and reduce acquisition costs over time."))

# ===================== PAGE 23 : CHAPTER 11 MANAGEMENT =====================
B(ch("CHAPTER 11", "MANAGEMENT & ORGANIZATIONAL STRUCTURE"))
B(h("11.1 Introduction"))
B(p("The success of BuildWise depends on effective leadership, efficient "
    "coordination, and clearly defined responsibilities. During its startup phase the "
    "company follows a lean organizational structure enabling faster decisions, "
    "improved communication, and efficient resource utilization."))
B(fig(31, "Figure 31. Organizational hierarchy illustrating reporting relationships "
      "and responsibilities within BuildWise.", w=0.82))
B(tbl(["Position", "Primary Responsibility"],
      [["Managing Director", "Strategic planning, business growth, key decisions"],
       ["Operations Manager", "Project execution, resource allocation, quality control"],
       ["Finance & Administration", "Financial planning, budgeting, procurement, HR"],
       ["Business Development", "Client acquisition, partnerships, marketing"],
       ["Project Managers", "Planning, scheduling, monitoring, coordination"],
       ["Site Engineers", "Technical supervision, execution, inspections"]],
      widths=[0.34, 0.66]))
B(callout("Lean Management for Faster Growth",
          "During the startup phase, BuildWise adopts a lean model where communication "
          "channels are short, responsibilities clearly defined, and decision-making "
          "efficient \u2014 reducing overhead while enabling rapid response, with room "
          "to add specialized departments as the company grows."))

# ===================== PAGE 24 : CHAPTER 12 FINANCIAL PLAN =====================
B(ch("CHAPTER 12", "FINANCIAL PLAN"))
B(h("12.1 Introduction"))
B(p("Financial planning is crucial to the sustainability and profitability of any "
    "venture. BuildWise's strategy uses realistic market assumptions, phased "
    "expansion, and conservative revenue projections, beginning operations with "
    "\u20b91.00 Crore of startup capital funded through promoter investment and "
    "financial support."))
B(h("12.2 Initial Capital Requirement"))
B(tbl(["Investment Category", "Amount (\u20b9)", "Allocation"],
      [["Office Setup & Infrastructure", "12,00,000", "12%"],
       ["Construction Equipment", "18,00,000", "18%"],
       ["Initial Material Procurement", "20,00,000", "20%"],
       ["Employee Salaries & Recruitment", "15,00,000", "15%"],
       ["Marketing & Brand Development", "8,00,000", "8%"],
       ["Technology & Software", "7,00,000", "7%"],
       ["Working Capital Reserve", "15,00,000", "15%"],
       ["Legal, Registration & Misc.", "5,00,000", "5%"],
       ["Total Initial Investment", "1,00,00,000", "100%"]],
      widths=[0.52, 0.28, 0.20]))
B(fig(32, "Figure 32. Distribution of the initial \u20b91.00 Crore investment across "
      "major operational categories.", w=0.6))
B(callout("Financial Philosophy",
          "BuildWise adopts a conservative approach by investing only in essential "
          "operational requirements during the startup phase. Large technology "
          "investments are postponed until stable revenue and operational maturity "
          "are achieved, reducing financial risk."))

# ===================== PAGE 25 : CH12 CONTINUED =====================
B(pb())
B(h("12.4 Revenue Projection"))
B(tbl(["Financial Year", "Revenue (\u20b9)", "Expenses (\u20b9)", "Net Profit (\u20b9)"],
      [["Year 1", "2.02 Crore", "1.92 Crore", "10 Lakhs"],
       ["Year 2", "4.85 Crore", "4.42 Crore", "43 Lakhs"],
       ["Year 3", "8.76 Crore", "8.10 Crore", "66 Lakhs"]],
      widths=[0.28, 0.24, 0.24, 0.24]))
B(fig(33, "Figure 33. Projected financial performance during the first three years of "
      "operation.", w=0.72))
B(h("Financial Performance Indicators"))
B(kpis([("\u20b98.76 Cr", "Gross Revenue (Yr 3)"),
        ("\u20b966 L", "Net Profit (Yr 3)"),
        ("~25%", "Gross Margin"),
        ("~7.5%", "Net Margin")]))
B(fig(34, "Figure 34. Estimated contribution of each service category to overall "
      "revenue.", w=0.58))
B(callout("Business Insight",
          "Revenue growth is driven by gradual expansion into commercial "
          "construction, improved operational efficiency, and service diversification "
          "rather than aggressive price increases \u2014 supporting sustainable "
          "profitability and competitive positioning."))

# ===================== PAGE 26 : CH12 CONTINUED =====================
B(pb())
B(h("12.6 Break-even Analysis"))
B(p("The company is expected to achieve operational break-even during the first year "
    "as construction projects increase and fixed costs are distributed across a "
    "growing portfolio. Conservative assumptions and disciplined cost management "
    "reduce investment risk."))
B(fig(35, "Figure 35. Break-even analysis showing the point where projected revenue "
      "exceeds total operational costs.", w=0.72))
B(tbl(["Cost Area", "Strategy"],
      [["Material Procurement", "Bulk purchasing and approved supplier network"],
       ["Labour", "Skilled workforce allocation and productivity monitoring"],
       ["Equipment", "Preventive maintenance and efficient utilization"],
       ["Administration", "Lean organizational structure"],
       ["Technology", "Phase-wise investment based on business growth"],
       ["Marketing", "Focus on referral-based customer acquisition"]],
      widths=[0.30, 0.70]))
B(cards([("Material Price Fluctuation", "Maintain multiple supplier partnerships."),
         ("Cash Flow Management", "Milestone-based customer billing."),
         ("Emergency Reserve", "Working capital contingency fund."),
         ("Controlled Expansion", "Expand only after operational stability.")], cols=2))
B(callout("Sustainable Financial Growth",
          "Financial success depends on disciplined expenditure, transparent billing, "
          "efficient execution, and controlled expansion. Rather than rapid growth "
          "through excessive borrowing, BuildWise prioritizes stability and "
          "reinvestment for long-term resilience."))

# ===================== PAGE 27 : CHAPTER 13 RISK =====================
B(ch("CHAPTER 13", "RISK ASSESSMENT & MITIGATION"))
B(h("13.1 Introduction"))
B(p("Every business faces uncertainties affecting operations, finance, and "
    "sustainability. BuildWise adopts a proactive risk management approach, "
    "identifying potential risks early and integrating risk assessment into "
    "planning, procurement, and financial decision-making."))
B(tbl(["Risk Category", "Impact", "Likelihood", "Mitigation Strategy"],
      [["Material Price Fluctuation", "High", "High", "Long-term supplier agreements"],
       ["Labour Shortage", "Delay", "Medium", "Skilled database & subcontractors"],
       ["Project Delays", "Dissatisfaction", "Medium", "Scheduling & contingency planning"],
       ["Regulatory Changes", "Compliance", "Low", "Regular legal review"],
       ["Cash Flow Constraints", "Disruption", "Medium", "Milestone billing & reserves"],
       ["Safety Incidents", "Interruption", "Low", "PPE, audits, and training"]],
      widths=[0.28, 0.18, 0.18, 0.36]))
B(fig(37, "Figure 37. Risk assessment matrix showing the relative priority of major "
      "business risks.", w=0.6))
B(cards([("Financial Risk Management", "Adequate working capital, milestone billing, "
          "and controlled expenditure."),
         ("Operational Risk Management", "Standardized workflows, milestone monitoring, "
          "and multiple suppliers."),
         ("Safety & Compliance", "Regular safety inspections, training, and compliance "
          "verification."),
         ("Business Continuity", "Diversified services and gradual, low-dependency "
          "expansion.")], cols=2))
B(callout("Proactive Risk Management",
          "BuildWise treats risk management as a continuous business process. Regular "
          "monitoring, financial discipline, quality assurance, and structured "
          "planning minimize uncertainty while maintaining customer confidence and "
          "operational stability."))

# ===================== PAGE 28 : CHAPTER 14 TECHNOLOGY =====================
B(ch("CHAPTER 14", "TECHNOLOGY ROADMAP"))
B(h("14.1 Introduction"))
B(p("Technology is transforming construction through better planning, estimation, "
    "communication, and quality control. BuildWise believes technology should support "
    "business growth rather than become a financial burden, following a phased "
    "adoption strategy where tools are introduced only after operational stability "
    "and customer trust are achieved."))
B(tbl(["Business Phase", "Technology Introduced", "Primary Benefit"],
      [["Phase 1 \u2013 Startup", "Project management, cloud docs", "Organization & communication"],
       ["Phase 2 \u2013 Growth", "AI estimation, QR material mgmt", "Estimation accuracy & control"],
       ["Phase 3 \u2013 Expansion", "Drone monitoring, dashboards", "Monitoring & decisions"],
       ["Phase 4 \u2013 Scale", "IoT smart homes, analytics", "Premium services & differentiation"]],
      widths=[0.26, 0.40, 0.34]))
B(fig(39, "Figure 39. Phased technology adoption roadmap supporting BuildWise's "
      "long-term business growth.", w=0.92))
B(cards([("AI-Based Cost Estimation", "Improves quotation accuracy and financial planning."),
         ("QR-Based Material Management", "Tracks material from delivery to site, reducing wastage."),
         ("Drone Site Monitoring", "Aerial progress imaging and efficient site reporting."),
         ("Digital Project Dashboard", "Milestone tracking, budget monitoring, visualization."),
         ("IoT Smart Home Integration", "Energy management, automation, remote control."),
         ("Cloud Documentation", "Secure storage of quotations, contracts, and reports.")],
        cols=3))
B(callout("Technology as a Business Enabler",
          "BuildWise does not adopt technology for innovation alone. Every digital "
          "solution is selected for its ability to improve transparency, efficiency, "
          "cost control, quality, or customer satisfaction \u2014 keeping investments "
          "financially sustainable."))

# ===================== PAGE 29 : CHAPTER 15 GROWTH & SUSTAINABILITY =====================
B(ch("CHAPTER 15", "GROWTH ROADMAP, SUSTAINABILITY & CONCLUSION"))
B(h("15.1 Vision for Future Growth"))
B(p("BuildWise is designed to grow progressively through disciplined expansion, "
    "operational excellence, and continuous innovation. Rather than pursuing rapid "
    "geographical expansion, the company strengthens its reputation and refines "
    "internal processes before entering new markets."))
B(tbl(["Year", "Primary Objective", "Expected Outcome"],
      [["Year 1", "Establish BuildWise in Chennai", "Reputation & operational stability"],
       ["Year 2", "Expand residential & commercial", "Increase market share"],
       ["Year 3", "Introduce AI, drones, QR inventory", "Efficiency & transparency"],
       ["Year 4", "Expand to metropolitan cities", "Strengthen regional presence"],
       ["Year 5", "Recognized technology-enabled brand", "Sustainable profitability"]],
      widths=[0.14, 0.44, 0.42]))
B(fig(41, "Figure 41. Five-year strategic roadmap illustrating BuildWise's phased "
      "business expansion plan.", w=0.95))
B(h("15.3 Sustainability Strategy"))
B(tbl(["Sustainability Initiative", "Business Benefit"],
      [["Eco-friendly construction materials", "Reduced environmental impact"],
       ["Efficient material utilization", "Lower project wastage"],
       ["Waste segregation and recycling", "Cleaner construction sites"],
       ["Energy-efficient building practices", "Lower operational costs"],
       ["Digital documentation", "Reduced paper consumption"]],
      widths=[0.5, 0.5]))
B(callout("Sustainable Growth Philosophy",
          "BuildWise believes business growth and environmental responsibility should "
          "progress together. Sustainable practices reduce environmental impact while "
          "improving efficiency, strengthening customer trust, and creating long-term "
          "business value."))

# ===================== PAGE 30 : CONCLUSION & REFERENCES =====================
B(pb())
B(fmhead("CONCLUSION", rule=True))
B(p("BuildWise Constructions Pvt. Ltd. represents a practical and future-ready "
    "business model developed to address the evolving needs of the Indian "
    "construction industry, combining engineering expertise, structured project "
    "management, customer-centric service, and phased technology adoption to deliver "
    "reliable, transparent, and high-quality solutions."))
B(p("Unlike conventional firms that compete primarily on pricing, BuildWise "
    "differentiates itself through customer trust, disciplined execution, financial "
    "sustainability, and operational excellence \u2014 establishing a strong market "
    "presence while creating a scalable foundation for long-term expansion."))
B(kpis([("\u20b91 Cr", "Initial Startup Capital"),
        ("Res. & Comm.", "Core Business Focus"),
        ("Tech\u2011Enabled", "Future-Ready Strategy"),
        ("Multi\u2011City", "Controlled Expansion")]))
B(fig(43, "Figure 43. Strategic framework summarizing the long-term vision and "
      "success model of BuildWise.", w=0.42))
B(callout("Building Trust, Brick by Brick",
          "BuildWise is founded on the belief that lasting success in construction is "
          "achieved through integrity, transparency, engineering excellence, and "
          "meaningful customer relationships \u2014 creating sustainable value for "
          "customers, employees, partners, and society."))
B(h("References"))
B(refs([
    "Ministry of Housing and Urban Affairs (MoHUA), Government of India.",
    "Ministry of Statistics and Programme Implementation (MoSPI).",
    "National Building Code of India (NBC 2016).",
    "Construction Industry Development Council (CIDC).",
    "Invest India \u2013 Construction & Infrastructure Sector Reports.",
    "NITI Aayog \u2013 Infrastructure Development Reports.",
    "CREDAI India Publications.",
    "RICS India \u2013 Construction Market Insights.",
    "World Green Building Council.",
    "Academic journals, market reports, and publicly available industry publications.",
]))

if __name__ == "__main__":
    print(f"{len(BLOCKS)} blocks defined")
    from collections import Counter
    print(Counter(b['t'] for b in BLOCKS))
