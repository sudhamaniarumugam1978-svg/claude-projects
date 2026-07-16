#!/usr/bin/env python3
"""One-shot build for the BuildWise Business Plan Report.

Regenerates everything from the single shared content model:

    1. buildwise_diagrams.py  -> figures/fig01..fig43.png   (43 navy diagrams)
    2. render_pdf.py          -> BuildWise_Business_Plan_Report.pdf   (30 pages)
    3. render_docx.py         -> BuildWise_Business_Plan_Report.docx

Run:  python build_report.py
"""

import importlib


def main():
    print("[1/3] Generating diagrams ...")
    diagrams = importlib.import_module("buildwise_diagrams")
    diagrams.build_all()

    print("[2/3] Rendering PDF ...")
    import render_pdf
    render_pdf.build()

    print("[3/3] Rendering DOCX ...")
    import render_docx
    render_docx.build()

    print("\nDone. Outputs:")
    print("  BuildWise_Business_Plan_Report.pdf")
    print("  BuildWise_Business_Plan_Report.docx")


if __name__ == "__main__":
    main()
