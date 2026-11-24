# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime

# # ── BRAND ────────────────────────────────────────────────────────────────────
# NAVY   = "#081b31"
# GOLD   = "#8e6d2d"
# LIGHT  = "#f5f3ef"
# RED    = "#c0392b"
# GREEN  = "#1e8449"
# AMBER  = "#d4ac0d"
# BLUE   = "#1a5276"

# st.set_page_config(page_title="FinPay | May 2026 Monthly Report", layout="wide", page_icon="📊")

# st.markdown(f"""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
# html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; background:{LIGHT}; }}
# h1,h2,h3 {{ font-family:'DM Serif Display', serif; color:{NAVY}; }}
# [data-testid="stMetricValue"] {{ font-size:22px; color:{NAVY}; font-weight:600; }}
# [data-testid="stMetricLabel"] {{ font-size:12px; color:#666; }}
# .header-band {{
#     background: linear-gradient(135deg, {NAVY} 0%, #0d2d52 60%, #112240 100%);
#     padding:28px 32px; border-radius:12px; margin-bottom:24px; color:white;
#     border-left: 5px solid {GOLD};
# }}
# .section-title {{
#     font-family:'DM Serif Display',serif; font-size:20px; color:{NAVY};
#     border-bottom: 2px solid {GOLD}; padding-bottom:8px; margin: 28px 0 16px;
# }}
# .obs-card {{
#     background:white; padding:14px 18px; border-radius:8px;
#     border-left:4px solid {GOLD}; margin-bottom:12px;
#     box-shadow:0 2px 8px rgba(0,0,0,0.06); font-size:13px; color:#333;
# }}
# .crit-card {{
#     background:#fdf0f0; padding:14px 18px; border-radius:8px;
#     border-left:4px solid {RED}; margin-bottom:12px;
#     box-shadow:0 2px 8px rgba(0,0,0,0.06); font-size:13px; color:#333;
# }}
# .scorecard {{
#     background:white; padding:16px; border-radius:10px;
#     box-shadow:0 2px 12px rgba(0,0,0,0.08); margin-bottom:12px;
#     border-top:3px solid {GOLD};
# }}
# .badge-high {{ background:{RED}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
# .badge-med  {{ background:{AMBER}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
# .badge-low  {{ background:{GREEN}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
# .kpi-box {{
#     background:white; border-radius:10px; padding:16px 20px;
#     border-top:3px solid {GOLD}; box-shadow:0 2px 8px rgba(0,0,0,0.07);
#     text-align:center;
# }}
# .flag-banner {{
#     background:#fff3cd; border:1px solid #ffc107; border-radius:8px;
#     padding:10px 16px; margin-bottom:10px; font-size:12px; color:#856404;
# }}
# </style>
# """, unsafe_allow_html=True)

# # ── DATA ─────────────────────────────────────────────────────────────────────
# merchants = [
#     {
#         "code": "REDSEA",
#         "name": "RED SEA",
#         "country": "United Kingdom",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
#         "channel": "Bank",
#         "total_txns": 1374, "successful": 1370, "failed": 4, "pending": 0,
#         "volume": 302232247.00,
#         "revenue": 954322.47,
#         "avg_charge": 696.59,
#         "avg_txn_value": 220607.48,
#         "failed_value": 202150.00,
#         "top_failures": "XML validation failed; reversed (2), Missing data; reversed (2)",
#         "banks_used": 12,
#         "top_bank": "Commercial Bank of Ethiopia (69%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 0,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 0,
#         "notes": "100% of failures were auto-reversed. ACCOUNT_DEBIT (17 txns, ETB 206.8M) are bulk/treasury transfers carrying zero charges. Broadest bank spread: 12 institutions, CBE at 69%.",
#     },
#     {
#         "code": "REDSEADIRECTDEPOSITS",
#         "name": "RED SEA DIRECT DEPOSITS",
#         "country": "United Kingdom",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank",
#         "total_txns": 4402, "successful": 4207, "failed": 195, "pending": 0,
#         "volume": 192700775.95,
#         "revenue": 1927008.63,
#         "avg_charge": 458.05,
#         "avg_txn_value": 45804.80,
#         "failed_value": 9911320.30,
#         "top_failures": "Insufficient balance (63), Unknown error (42), System Error (28), CIF harmonization block (26), Missing data; reversed (4), XML validation (3)",
#         "banks_used": 11,
#         "top_bank": "Commercial Bank of Ethiopia (70%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 26,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 99113.00,
#         "notes": "Highest revenue merchant. ETB 9.9M in failed value — highest in portfolio. CIF harmonization block (26 cases) is CBE compliance sweep — needs escalation. ETB 99,113 charged on failed txns requires refund review.",
#     },
#     {
#         "code": "JUBAEXPRESS",
#         "name": "JUBA EXPRESS",
#         "country": "Ethiopia",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank",
#         "total_txns": 8042, "successful": 7923, "failed": 119, "pending": 0,
#         "volume": 252050695.00,
#         "revenue": 1008230.09,
#         "avg_charge": 127.25,
#         "avg_txn_value": 31812.53,
#         "failed_value": 3534649.00,
#         "top_failures": "System Error (24), Insufficient balance (24), XML validation (21), CIF harmonization block (21), Unknown error (12), Missing data; reversed (5)",
#         "banks_used": 17,
#         "top_bank": "Commercial Bank of Ethiopia (77%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 21,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 14138.93,
#         "notes": "Highest transaction volume (bank channel). Broadest bank network — 17 institutions. CIF harmonization block (21 cases) confirms portfolio-wide CBE compliance event. ETB 14,138 charged on failed txns.",
#     },
#     {
#         "code": "FINPAYAPPLICATION",
#         "name": "FINPAY APPLICATION (EMAAL)",
#         "country": "Kenya",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
#         "channel": "Bank + Mobile",
#         "total_txns": 4756, "successful": 4749, "failed": 7, "pending": 0,
#         "volume": 358351263.38,
#         "revenue": 427063.00,
#         "avg_charge": 89.93,
#         "avg_txn_value": 75458.26,
#         "failed_value": 538144.00,
#         "top_failures": "Transaction Failed generic (3), Missing data; reversed (1), ERRR; reversed (1), Insufficient balance (1), CreditParty invalid state/mobile (1)",
#         "banks_used": 15,
#         "top_bank": "Commercial Bank of Ethiopia (88%)",
#         "mobile": True,
#         "mobile_networks": ["Safaricom (M-Pesa)", "Airtel", "MTN"],
#         "mobile_txns": 51, "mobile_successful": 49, "mobile_failed": 2,
#         "mobile_volume": 6120284.00,
#         "mobile_revenue": 0.00,
#         "cif_issues": 0,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 455.00,
#         "notes": "Highest total value moved (ETB 358M) and best success rate (99.85%). No CIF harmonization failures — only major merchant unaffected. Mobile: 3 networks, Airtel handling largest avg value (ETB 540K/txn). Mobile generates ETB 0 revenue — confirm if intentional.",
#     },
#     {
#         "code": "BIRRLINK",
#         "name": "BIRR LINK",
#         "country": "Ethiopia",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank",
#         "total_txns": 52, "successful": 50, "failed": 2, "pending": 0,
#         "volume": 1841316.53,
#         "revenue": 0.00,
#         "avg_charge": 0.00,
#         "avg_txn_value": 36826.33,
#         "failed_value": 28297.90,
#         "top_failures": "Exception on bank transfer (1), Insufficient balance (1)",
#         "banks_used": 4,
#         "top_bank": "Commercial Bank of Ethiopia (79%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 0,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 0,
#         "notes": "CRITICAL: 4th consecutive period of ETB 0.00 revenue. Zero charges on all 52 transactions. Commercial team must resolve fee arrangement urgently — this merchant consumes operational resources at zero revenue.",
#     },
#     {
#         "code": "DEEROSERVICES",
#         "name": "DEERO SERVICES",
#         "country": "USA",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
#         "channel": "Bank",
#         "total_txns": 955, "successful": 796, "failed": 159, "pending": 0,
#         "volume": 188381403.00,
#         "revenue": 67431.00,
#         "avg_charge": 84.71,
#         "avg_txn_value": 236660.05,
#         "failed_value": 3607806.00,
#         "top_failures": "BLCK Account Blocked; reversed (87), XML validation failed; reversed (63), System Error (7), Currency mismatch (2)",
#         "banks_used": 10,
#         "top_bank": "Commercial Bank of Ethiopia (50%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 0,
#         "cbo_failures": 71,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 14469.00,
#         "notes": "Worst success rate (83.35%). 100% of failures concentrated at 2 banks: Kaafi MFI (84 failures, BLCK errors) and Cooperative Bank of Oromia (71 failures, XML validation). ACCOUNT_DEBIT (55 txns, ETB 157.8M) all succeeded. ETB 14,469 charged on failed txns. Refund required.",
#     },
#     {
#         "code": "REMITLYGLOBAL",
#         "name": "REMITLY GLOBAL",
#         "country": "USA",
#         "period": "May 1–31, 2026",
#         "full_month": True,
#         "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
#         "channel": "Bank + Mobile",
#         "total_txns": 15066, "successful": 14773, "failed": 293, "pending": 0,
#         "volume": 467019428.75,
#         "revenue": 0.00,
#         "avg_charge": 0.00,
#         "avg_txn_value": 31613.04,
#         "failed_value": 17625789.27,
#         "top_failures": "Creditor Agent error; reversed (57), System Error (52), Transaction not found (33), Insufficient balance (32), CIF harmonization block (22), Unknown error (16)",
#         "banks_used": 12,
#         "top_bank": "Commercial Bank of Ethiopia (66%)",
#         "mobile": True,
#         "mobile_networks": ["Safaricom (M-Pesa)", "Ethiotelecom (Telebirr)"],
#         "mobile_txns": 245, "mobile_successful": 200, "mobile_failed": 45,
#         "mobile_volume": 5039597.00,
#         "mobile_revenue": 0.00,
#         "cif_issues": 22,
#         "cbo_failures": 8,
#         "telebirr_failures": 42,
#         "kyc_status": "Complete",
#         "charges_on_failed": 0,
#         "notes": "Highest volume (15,066 txns) and highest value moved (ETB 467M). ETB 0 revenue. International model, but arrangement must be documented. CRITICAL: Ethiotelecom/Telebirr 100% failure rate (42/42). 22 customers blocked due to CBE data mismatch. Cooperative Bank of Oromia: 57% failure rate (8/14). ETB 17.6M in failed value.",
#     },
#     {
#         "code": "RAFIKILTD",
#         "name": "RAFIKI LTD (NALA)",
#         "country": "United Kingdom",
#         "period": "May 6–28, 2026",
#         "full_month": False,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank + Mobile",
#         "total_txns": 27, "successful": 6, "failed": 21, "pending": 0,
#         "volume": 45023.08,
#         "revenue": 546.00,
#         "avg_charge": 91.00,
#         "avg_txn_value": 7503.85,
#         "failed_value": 313918.31,
#         "top_failures": "Transaction not found (14), Transaction Failed generic (3), Transaction state Cancelled (2), Customer not registered (1), JDBC Connection error (1)",
#         "banks_used": 3,
#         "top_bank": "Commercial Bank of Ethiopia (100% success on bank)",
#         "mobile": True,
#         "mobile_networks": ["Ethiotelecom (Telebirr)", "Safaricom (M-Pesa)"],
#         "mobile_txns": 22, "mobile_successful": 1, "mobile_failed": 21,
#         "mobile_volume": 14018.31,
#         "mobile_revenue": 0.00,
#         "cif_issues": 0,
#         "cbo_failures": 0,
#         "telebirr_failures": 21,
#         "kyc_status": "Complete",
#         "charges_on_failed": 1911.00,
#         "notes": "CRITICAL: 77.78% failure rate — worst in portfolio. Ethiotelecom 100% failure (21/21). Bank channel: 100% success (5/5). ETB 1,911 charged on failed txns — full refund required. Likely still in onboarding/testing phase.",
#     },
#     {
#         "code": "BAKAALEXPRESS",
#         "name": "BAKAAL EXPRESS",
#         "country": "Somalia",
#         "period": "May 9–30, 2026",
#         "full_month": False,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank",
#         "total_txns": 300, "successful": 296, "failed": 4, "pending": 0,
#         "volume": 4873318.00,
#         "revenue": 17384.07,
#         "avg_charge": 58.73,
#         "avg_txn_value": 16463.91,
#         "failed_value": 89920.00,
#         "top_failures": "XML validation; reversed (1), Currency mismatch; reversed (1), Missing data; reversed (1), Unknown (1)",
#         "banks_used": 6,
#         "top_bank": "Commercial Bank of Ethiopia (91%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 0,
#         "cbo_failures": 1,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 314.74,
#         "notes": "Percentage-based charge model — unique in portfolio. Charges scale with transaction size (ETB 0.12–ETB 315). Solid 98.67% success rate. Bank of Abyssinia showing 12.5% failure rate (2/16) — monitor. ETB 314.74 on failed txns for refund.",
#     },
#     {
#         "code": "MELAFINANCE",
#         "name": "MELA FINANCE",
#         "country": "United Kingdom",
#         "period": "May 18–31, 2026",
#         "full_month": False,
#         "txn_types": ["DISBURSEMENTS"],
#         "channel": "Bank",
#         "total_txns": 60, "successful": 57, "failed": 3, "pending": 0,
#         "volume": 2065210.76,
#         "revenue": 6200.99,
#         "avg_charge": 108.79,
#         "avg_txn_value": 36231.77,
#         "failed_value": 82425.00,
#         "top_failures": "Failed to obtain auth token (2), No reason recorded (1)",
#         "banks_used": 1,
#         "top_bank": "Commercial Bank of Ethiopia (100%)",
#         "mobile": False,
#         "mobile_networks": [],
#         "cif_issues": 0,
#         "cbo_failures": 0,
#         "telebirr_failures": 0,
#         "kyc_status": "Complete",
#         "charges_on_failed": 247.28,
#         "notes": "New merchant (onboarded May 11). Percentage-based fee model. Auth token failures (2) are integration/connectivity issues. 100% CBE concentration — single point of failure risk. ETB 247.28 on failed txns for refund.",
#     },
# ]

# df = pd.DataFrame(merchants)
# df["success_rate"] = (df["successful"] / df["total_txns"]) * 100
# df["failure_rate"] = (df["failed"] / df["total_txns"]) * 100
# df["rev_bps"] = (df["revenue"] / df["volume"].replace(0, 1)) * 10000

# # ── FX DATA ──────────────────────────────────────────────────────────────────
# fx_data = {
#     "ETB/USD": {"date": "22 May 2026", "opening": 184.00, "closing": "Not received", "note": "Confirmed opening rate. Closing rate not submitted by Finance."},
#     "KES/USD": {"date": "22 May 2026", "opening": 129.00, "closing": "Not received", "note": "Confirmed opening rate. Same rate confirmed as of 25 May."},
#     "UGX/USD": {"date": "22 May 2026", "opening": 3772.00, "closing": "Not received", "note": "Confirmed opening rate only."},
# }

# # ── RISK SCORECARD ────────────────────────────────────────────────────────────
# def compute_risk(m):
#     score = 0
#     # Success rate
#     sr = (m["successful"] / m["total_txns"]) * 100
#     if sr < 85:   score += 40
#     elif sr < 95: score += 20
#     elif sr < 99: score += 10
#     # Revenue
#     if m["revenue"] == 0: score += 30
#     # Failed value
#     if m["failed_value"] > 5000000: score += 25
#     elif m["failed_value"] > 1000000: score += 15
#     # Charges on failed
#     if m["charges_on_failed"] > 10000: score += 20
#     elif m["charges_on_failed"] > 0: score += 10
#     # Telebirr failures
#     if m["telebirr_failures"] > 10: score += 30
#     # CIF issues
#     if m["cif_issues"] > 15: score += 20
#     elif m["cif_issues"] > 0: score += 10
#     # CBO failures
#     if m["cbo_failures"] > 30: score += 15
#     elif m["cbo_failures"] > 0: score += 8
#     # Full month
#     if not m["full_month"]: score += 5

#     if score >= 55:   return "High", score
#     elif score >= 25: return "Medium", score
#     else:             return "Low", score

# for m in merchants:
#     risk, score = compute_risk(m)
#     m["risk_level"] = risk
#     m["risk_score"] = score

# df["risk_level"] = [m["risk_level"] for m in merchants]
# df["risk_score"]  = [m["risk_score"]  for m in merchants]

# # ── PORTFOLIO AGGREGATES (needed by header) ───────────────────────────────
# total_vol    = df["volume"].sum()
# total_rev    = df["revenue"].sum()
# total_txns   = df["total_txns"].sum()
# total_failed = df["failed"].sum()
# total_fail_val = df["failed_value"].sum()
# avg_sr       = df["success_rate"].mean()
# total_charged_on_failed = sum(m["charges_on_failed"] for m in merchants)

# # ════════════════════════════════════════════════════════════════════════════
# # HEADER
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown(f"""
# <div class="header-band">
#   <div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;opacity:0.7;margin-bottom:6px;color:{GOLD};">
#     FINPAY TECH · INTERNAL ANALYTICS
#   </div>
#   <div style="font-size:28px;font-family:'DM Serif Display',serif;font-weight:400;color:white;margin-bottom:4px;">
#     Monthly Merchant Performance & Risk Report
#   </div>
#   <div style="font-size:13px;opacity:0.85;color:white;">
#     Reporting Period: May 1 – 31, 2026 &nbsp;
#     |&nbsp; Active Merchants: {len(merchants)} active &nbsp;|&nbsp; Total value monitored: ETB {total_vol/1e6:.1f}M &nbsp;|&nbsp;
#   Total revenue: ETB {total_rev:,.0f}
#   </div>
# </div>
# """, unsafe_allow_html=True)




# # ════════════════════════════════════════════════════════════════════════════
# # PORTFOLIO KPIs
# # ════════════════════════════════════════════════════════════════════════════
# # Portfolio aggregates for critical flags
# total_cif = sum(m["cif_issues"] for m in merchants)
# total_telebirr = sum(m["telebirr_failures"] for m in merchants)

# st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

# c1,c2,c3,c4,c5,c6 = st.columns(6)
# c1.metric("Total Value Moved", f"ETB {total_vol/1e6:.1f}M")
# c2.metric("Total Revenue", f"ETB {total_rev:,.0f}")
# c3.metric("Total Transactions", f"{total_txns:,}")
# c4.metric("Total Failed", f"{total_failed:,}", delta=f"{(total_failed/total_txns*100):.1f}% of all txns", delta_color="inverse")
# c5.metric("Est. Failed Value", f"ETB {total_fail_val/1e6:.1f}M")
# c6.metric("Charges on Failed Txns", f"ETB {total_charged_on_failed:,.0f}", help="Requires refund review across portfolio")
# st.markdown(f"""
# <div class="obs-card">
#   In May 2026, we processed transactions for <strong>{len(merchants)} active merchants</strong> moving a combined
#   <strong>ETB {total_vol/1e6:.2f} billion</strong> across <strong>{total_txns:,} total transactions</strong>,
#   generating <strong>ETB {total_rev:,.0f}</strong> in revenue.<br><br>
#   Overall platform success rate was <strong>{avg_sr:.1f}%</strong>
#   ({df['successful'].sum():,} successful of {total_txns:,} total),
#   with <strong>FINPAY APPLICATION (EMAAL)</strong> delivering the strongest individual performance at <strong>99.85%</strong>
#   and <strong>RAFIKI LTD (NALA)</strong> the weakest at <strong>22.2%</strong>.
# </div>
# """, unsafe_allow_html=True)
# # ════════════════════════════════════════════════════════════════════════════
# # CHART ROW 1 — Volume & Revenue
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Volume & Revenue Analysis</div>', unsafe_allow_html=True)

# CHART_COLORS = [NAVY, GOLD, BLUE, "#2e86c1", "#117a65", "#6c3483", "#784212", "#1a5276", "#0b5345", "#4a235a"]

# ch1, ch2 = st.columns(2)
# with ch1:
#     fig_vol = px.bar(
#         df.sort_values("volume"),
#         x="volume", y="name", orientation="h",
#         color_discrete_sequence=[NAVY],
#         title="Total Value Moved by Merchant (ETB)",
#         text=df.sort_values("volume")["volume"].apply(lambda v: f"{v/1e6:.1f}M" if v > 0 else "N/A"),
#     )
#     fig_vol.update_traces(textposition="outside")
#     fig_vol.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                           margin=dict(t=40,b=10,l=10,r=80), xaxis_title="ETB", yaxis_title="")
#     st.plotly_chart(fig_vol, use_container_width=True)

# with ch2:
#     fig_rev = px.bar(
#         df.sort_values("revenue"),
#         x="name", y="revenue",
#         color_discrete_sequence=[GOLD],
#         title="Total Revenue Collected by Merchant (ETB)",
#         text=df.sort_values("revenue")["revenue"].apply(lambda v: f"{v:,.0f}"),
#     )
#     fig_rev.update_traces(textposition="outside")
#     fig_rev.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                           margin=dict(t=40,b=10,l=10,r=10), xaxis_title="", yaxis_title="ETB")
#     fig_rev.update_xaxes(tickangle=30)
#     st.plotly_chart(fig_rev, use_container_width=True)

# # ════════════════════════════════════════════════════════════════════════════
# # CHART ROW 2 — Success Rates & Revenue per Transaction
# # ════════════════════════════════════════════════════════════════════════════
# ch3, ch4 = st.columns(2)
# with ch3:
#     color_map = {"High": RED, "Medium": AMBER, "Low": GREEN}
#     fig_sr = px.bar(
#         df.sort_values("success_rate"),
#         x="success_rate", y="name", orientation="h",
#         color="risk_level",
#         color_discrete_map=color_map,
#         title="Success Rate by Merchant (%)",
#         text=df.sort_values("success_rate")["success_rate"].apply(lambda v: f"{v:.1f}%"),
#     )
#     fig_sr.update_traces(textposition="outside")
#     fig_sr.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                          margin=dict(t=40,b=10,l=10,r=60),
#                          xaxis=dict(range=[0,105]), xaxis_title="%", yaxis_title="")
#     st.plotly_chart(fig_sr, use_container_width=True)

# with ch4:
#     df_rev_per = df[df["revenue"] > 0].copy()
#     df_rev_per["rev_per_txn"] = df_rev_per["revenue"] / df_rev_per["total_txns"]
#     fig_rpt = px.scatter(
#         df_rev_per,
#         x="total_txns", y="rev_per_txn", size="revenue",
#         color="risk_level",
#         color_discrete_map=color_map,
#         hover_name="name",
#         title="Revenue per Transaction vs Volume",
#         labels={"total_txns": "Total Transactions", "rev_per_txn": "Revenue per Txn (ETB)"},
#     )
#     fig_rpt.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                           margin=dict(t=40,b=10,l=10,r=10))
#     st.plotly_chart(fig_rpt, use_container_width=True)
#     st.caption("Bubble size = total revenue. Merchants with ETB 0 revenue excluded.")

# # ════════════════════════════════════════════════════════════════════════════
# # CHART ROW 3 — Revenue BPS & Avg Transaction Value
# # ════════════════════════════════════════════════════════════════════════════
# ch5, ch6 = st.columns(2)
# with ch5:
#     df_bps = df[df["rev_bps"] > 0].sort_values("rev_bps").reset_index(drop=True)
#     fig_bps = go.Figure()
#     fig_bps.add_trace(go.Scatter(
#         x=df_bps["rev_bps"], y=df_bps["name"],
#         mode="markers+text",
#         marker=dict(color=GOLD, size=14, line=dict(color=NAVY, width=1.5)),
#         text=df_bps["rev_bps"].apply(lambda v: f"{v:.1f} bps"),
#         textposition="middle right",
#         name="",
#     ))
#     for _, row in df_bps.iterrows():
#         fig_bps.add_shape(type="line",
#             x0=0, x1=row["rev_bps"], y0=row["name"], y1=row["name"],
#             line=dict(color=GOLD, width=2, dash="dot"))
#     fig_bps.update_layout(
#         title="Revenue Earned per ETB Moved (Basis Points)",
#         plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#         margin=dict(t=40, b=10, l=10, r=90),
#         xaxis=dict(title="BPS", showgrid=True, gridcolor="#eee", zeroline=True),
#         yaxis=dict(title=""),
#         showlegend=False,
#     )
#     st.plotly_chart(fig_bps, use_container_width=True)
#     st.caption(
#         "I have used basis points (BPS) here because transaction volumes are very large and the revenue percentages are relatively small. "
#         "Expressing performance in percentages (e.g., 0.31%) can make the figures appear insignificant, while BPS provides a clearer and more precise way to show revenue efficiency per unit processed. "
#         "In this context, 1 BPS equals ETB 1 earned for every ETB 10,000 processed, making it easier to compare how effectively each merchant converts transaction volume into revenue. "
#         "Merchants with ETB 0 revenue have been excluded from the analysis."
#     )

# with ch6:
#     df_ticket = df.sort_values("avg_txn_value", ascending=False).reset_index(drop=True)
#     fig_ticket = go.Figure(go.Treemap(
#         labels=df_ticket["name"],
#         parents=[""] * len(df_ticket),
#         values=df_ticket["avg_txn_value"],
#         text=df_ticket["avg_txn_value"].apply(lambda v: f"ETB {v:,.0f}"),
#         textinfo="label+text",
#         marker=dict(
#             colors=df_ticket["avg_txn_value"],
#             colorscale=[[0, "#d6e4f0"], [1, NAVY]],
#             showscale=False,
#         ),
#     ))
#     fig_ticket.update_layout(
#         title="Average Transaction Value - Successful Txns (ETB)",
#         font=dict(family="DM Sans", size=11),
#         margin=dict(t=40, b=10, l=10, r=10),
#     )
#     st.plotly_chart(fig_ticket, use_container_width=True)


# # ════════════════════════════════════════════════════════════════════════════
# # FAILURE DEEP DIVE
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Failure Analysis Deep Dive</div>', unsafe_allow_html=True)

# fail_data = {
#     "DEERO SERVICES":      {"BLCK/Account Blocked; reversed": 87, "XML validation failed; reversed": 63, "System Error": 7, "Currency mismatch": 2},
#     "REMITLY GLOBAL":      {"Creditor Agent error; reversed": 57, "System Error": 52, "Transaction not found": 33, "Insufficient balance": 32, "CIF harmonization block": 22, "Unknown error": 16},
#     "RED SEA DIRECT DEPOSITS": {"Insufficient balance": 63, "Unknown error": 42, "System Error": 28, "CIF harmonization block": 26, "Missing data; reversed": 4},
#     "JUBA EXPRESS":        {"System Error": 24, "Insufficient balance": 24, "XML validation failed": 21, "CIF harmonization block": 21, "Unknown error": 12},
#     "RAFIKI (NALA)":       {"Transaction not found": 14, "Transaction Failed": 3, "State Cancelled": 2, "Customer not registered": 1, "JDBC Error": 1},
#     "FINPAY APP (EMAAL)":  {"Transaction Failed": 3, "Missing data": 1, "ERRR reversed": 1, "Insufficient balance": 1, "CreditParty invalid": 1},
#     "BAKAAL EXPRESS":      {"XML validation": 1, "Currency mismatch": 1, "Missing data": 1, "Unknown": 1},
#     "MELA FINANCE":        {"Auth token failure": 2, "No reason recorded": 1},
#     "BIRR LINK":           {"Exception on bank transfer": 1, "Insufficient balance": 1},
#     "RED SEA":             {"XML validation; reversed": 2, "Missing data; reversed": 2},
# }

# fail_rows = []
# for merchant, reasons in fail_data.items():
#     for reason, count in reasons.items():
#         fail_rows.append({"Merchant": merchant, "Reason": reason, "Count": count})
# fail_df = pd.DataFrame(fail_rows)

# fig_fd = px.bar(
#     fail_df, x="Count", y="Reason", color="Merchant", orientation="h",
#     color_discrete_sequence=CHART_COLORS,
#     title="Failure Reasons Across All Merchants — May 2026",
#     text="Count",
# )
# fig_fd.update_traces(textposition="outside")
# fig_fd.update_layout(
#     plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#     margin=dict(t=40,b=10,l=10,r=10), height=480,
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
# )
# st.plotly_chart(fig_fd, use_container_width=True)

# # CIF + Telebirr summary
# col_a, col_b = st.columns(2)
# with col_a:
#     cif_data = {m["name"]: m["cif_issues"] for m in merchants if m["cif_issues"] > 0}
#     fig_cif = px.bar(
#         x=list(cif_data.keys()), y=list(cif_data.values()),
#         color_discrete_sequence=[RED],
#         title="Customers Blocked (CBE data mismatch) by Merchant",
#         text=list(cif_data.values()),
#     )
#     fig_cif.update_traces(textposition="outside")
#     fig_cif.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                           xaxis_title="", yaxis_title="Customers", margin=dict(t=40,b=10,l=10,r=10))
#     st.plotly_chart(fig_cif, use_container_width=True)
#     st.caption(f"Total {sum(m['cif_issues'] for m in merchants)} customers blocked because their info doesn't match CBE's system. CBE contact needed.")

# with col_b:
#     tel_data = {m["name"]: m["telebirr_failures"] for m in merchants if m["telebirr_failures"] > 0}
#     fig_tel = px.bar(
#         x=list(tel_data.keys()), y=list(tel_data.values()),
#         color_discrete_sequence=[AMBER],
#         title="Ethiotelecom/Telebirr Failures by Merchant (100% failure rate)",
#         text=list(tel_data.values()),
#     )
#     fig_tel.update_traces(textposition="outside")
#     fig_tel.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
#                           xaxis_title="", yaxis_title="Failed Txns", margin=dict(t=40,b=10,l=10,r=10))
#     st.plotly_chart(fig_tel, use_container_width=True)
#     st.caption("Telebirr integration is completely non-functional. Must be suspended platform-wide until resolved.")

# # ════════════════════════════════════════════════════════════════════════════
# # FX SECTION
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">FX Rate Monitoring</div>', unsafe_allow_html=True)

# fx_cols = st.columns(3)
# fx_items = [
#     ("ETB/USD", "184.00", "Not received", "22 May 2026", "Ethiopian Birr — primary transaction currency. Historically volatile. Confirmed opening rate only."),
#     ("KES/USD", "129.00", "Not received", "22 May 2026", "Kenyan Shilling. Confirmed opening rate; same as of 25 May 2026 per Finance team."),
#     ("UGX/USD", "3,772.00", "Not received", "22 May 2026", "Ugandan Shilling. Opening rate confirmed only."),
# ]
# for col, (pair, opening, closing, date, note) in zip(fx_cols, fx_items):
#     col.markdown(f"""
#     <div class="scorecard">
#       <div style="font-size:11px;color:{GOLD};font-weight:600;letter-spacing:1px;">{pair}</div>
#       <div style="font-size:20px;font-weight:600;color:{NAVY};margin:4px 0;">{opening}</div>
#       <div style="font-size:11px;color:#888;">Opening Rate · {date}</div>
#       <div style="font-size:11px;color:{RED};margin-top:4px;">Closing: {closing}</div>
#       <div style="font-size:11px;color:#666;margin-top:6px;">{note}</div>
#     </div>
#     """, unsafe_allow_html=True)

# st.divider()

# # ════════════════════════════════════════════════════════════════════════════
# # PER-MERCHANT EXPANDERS
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Per-Merchant Detail</div>', unsafe_allow_html=True)

# risk_badge = {"High": "badge-high", "Medium": "badge-med", "Low": "badge-low"}

# for m in merchants:
#     sr = (m["successful"] / m["total_txns"]) * 100
#     badge = risk_badge[m["risk_level"]]
#     with st.expander(f"{m['name']}  ·  {m['channel']}  ·  {sr:.1f}% success  ·  {m['period']}"):
#         d1,d2,d3,d4,d5 = st.columns(5)
#         d1.metric("Total Transactions", f"{m['total_txns']:,}")
#         d2.metric("Successful", f"{m['successful']:,}")
#         d3.metric("Failed", f"{m['failed']:,}")
#         d4.metric("Value Moved (ETB)", f"{m['volume']/1e6:.1f}M")
#         d5.metric("Revenue (ETB)", f"{m['revenue']:,.0f}")

#         d6,d7,d8,d9 = st.columns(4)
#         d6.metric("Avg Charge", f"ETB {m['avg_charge']:,.2f}")
#         d7.metric("Avg Txn Value", f"ETB {m['avg_txn_value']:,.0f}")
#         d8.metric("Est. Failed Value", f"ETB {m['failed_value']:,.0f}")
#         d9.metric("Charges on Failed", f"ETB {m['charges_on_failed']:,.0f}" if m['charges_on_failed'] > 0 else "—")

#         st.markdown(f"**Country:** {m['country']} &nbsp;|&nbsp; **Channel:** {m['channel']} &nbsp;|&nbsp; **Transaction Types:** {', '.join(m['txn_types'])} &nbsp;|&nbsp; **Banks Used:** {m['banks_used']} &nbsp;|&nbsp; **Top Bank:** {m['top_bank']}")
#         if m["mobile"]:
#             st.markdown(f"**Mobile Networks:** {', '.join(m['mobile_networks'])} &nbsp;|&nbsp; **Mobile Txns:** {m.get('mobile_txns',0)} &nbsp;|&nbsp; **Mobile Value:** ETB {m.get('mobile_volume',0):,.0f} &nbsp;|&nbsp; **Mobile Revenue:** ETB {m.get('mobile_revenue',0):,.0f}")
#         if m["cif_issues"] > 0:
#             st.warning(f"⚠️ {m['cif_issues']} customers blocked: their details on file don't match what CBE has. Needs to be raised with CBE to unblock.")
#         if m["telebirr_failures"] > 0:
#             st.error(f"🚨 Telebirr/Ethiotelecom: {m['telebirr_failures']} failures — 100% failure rate on this channel")
#         st.markdown(f"**Top Failure Reasons:** {m['top_failures']}")
#         st.info(m["notes"])

# # ════════════════════════════════════════════════════════════════════════════
# # RISK SCORECARD
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Monthly Merchant Risk Scorecard</div>', unsafe_allow_html=True)
# st.caption("Each merchant scored across 6 dimensions: Transaction Volume, Revenue, Failure/Reversal Performance, FX Exposure, KYC Compliance, and Overall Risk.")

# score_data = []
# for m in merchants:
#     sr = (m["successful"] / m["total_txns"]) * 100
#     score_data.append({
#         "Merchant": m["name"],
#         "Volume Score": "🟢 High" if m["volume"] > 100e6 else ("🟡 Med" if m["volume"] > 10e6 else "🔴 Low"),
#         "Revenue": "🚨 Zero" if m["revenue"] == 0 else ("🟢 Strong" if m["revenue"] > 500000 else "🟡 Moderate"),
#         "Success Rate": f"{sr:.1f}%",
#         "Failure Risk": "🔴 High" if sr < 85 else ("🟡 Med" if sr < 97 else "🟢 Low"),
#         "FX Exposure": "🟡 Medium" if m["channel"] in ["Bank", "Bank + Mobile"] else "🟢 Low",
#         "KYC Status": "🟢 Complete",
#         "Charges on Failed": f"ETB {m['charges_on_failed']:,.0f}" if m["charges_on_failed"] > 0 else "—",
#         "Overall Risk": m["risk_level"],
#     })

# score_df = pd.DataFrame(score_data)

# def color_risk(val):
#     if val == "High":   return f"background-color:{RED};color:white;font-weight:bold"
#     if val == "Medium": return f"background-color:{AMBER};color:white;font-weight:bold"
#     if val == "Low":    return f"background-color:{GREEN};color:white;font-weight:bold"
#     return ""

# styled = score_df.style.applymap(color_risk, subset=["Overall Risk"])
# st.dataframe(styled, use_container_width=True, height=380)

# risk_col1, risk_col2 = st.columns(2)
# with risk_col1:
#     risk_counts = df["risk_level"].value_counts().reset_index()
#     risk_counts.columns = ["Risk Level", "Count"]
#     fig_risk = px.pie(risk_counts, names="Risk Level", values="Count",
#                       color="Risk Level",
#                       color_discrete_map={"High": RED, "Medium": AMBER, "Low": GREEN},
#                       title="Portfolio Risk Distribution",
#                       hole=0.4)
#     fig_risk.update_layout(font=dict(family="DM Sans", size=11), margin=dict(t=40,b=10,l=10,r=10))
#     st.plotly_chart(fig_risk, use_container_width=True)

# with risk_col2:
#     heat_merchants = [m["name"] for m in merchants]
#     heat_metrics = ["Success Rate", "Revenue (ETB)", "Volume (ETB)", "Avg Txn Value", "Charges on Failed"]
#     sr_vals      = [round((m["successful"]/m["total_txns"])*100, 1) for m in merchants]
#     rev_vals     = [m["revenue"] for m in merchants]
#     vol_vals     = [m["volume"] for m in merchants]
#     txn_vals     = [m["avg_txn_value"] for m in merchants]
#     fail_vals    = [m["charges_on_failed"] for m in merchants]

#     def norm(lst):
#         mx = max(lst) if max(lst) > 0 else 1
#         return [round(v / mx, 3) for v in lst]

#     heat_z = [
#         norm(sr_vals),
#         norm(rev_vals),
#         norm(vol_vals),
#         norm(txn_vals),
#         [round(1 - v, 3) for v in norm(fail_vals)],
#     ]

#     fig_heat = go.Figure(go.Heatmap(
#         z=heat_z,
#         x=heat_merchants,
#         y=heat_metrics,
#         colorscale=[[0, "#fdf0f0"], [0.5, GOLD], [1, NAVY]],
#         text=[
#             [f"{sr_vals[i]:.1f}%" for i in range(len(merchants))],
#             [f"ETB {rev_vals[i]:,.0f}" for i in range(len(merchants))],
#             [f"ETB {vol_vals[i]/1e6:.1f}M" for i in range(len(merchants))],
#             [f"ETB {txn_vals[i]:,.0f}" for i in range(len(merchants))],
#             [f"ETB {fail_vals[i]:,.0f}" for i in range(len(merchants))],
#         ],
#         texttemplate="%{text}",
#         textfont=dict(size=9),
#         showscale=False,
#     ))
#     fig_heat.update_layout(
#         title="Merchant Performance Heatmap",
#         font=dict(family="DM Sans", size=10),
#         margin=dict(t=40, b=10, l=130, r=10),
#         xaxis=dict(tickangle=30),
#     )
#     st.plotly_chart(fig_heat, use_container_width=True)
#     st.caption("Each row is normalized relative to the top performer in that category. Darker = stronger. Charges on Failed is inverted so darker = fewer charges (better).")

# st.divider()

# # ════════════════════════════════════════════════════════════════════════════
# # AUDIT TABLE
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Comprehensive Monthly Audit Trail</div>', unsafe_allow_html=True)

# audit_df = df[[
#     "name","channel","risk_level","total_txns","successful","failed","pending",
#     "volume","revenue","avg_charge","avg_txn_value","success_rate","failed_value"
# ]].copy()
# audit_df.columns = [
#     "Merchant","Channel","Risk","Total Txns","Successful","Failed","Pending",
#     "Volume (ETB)","Revenue (ETB)","Avg Charge","Avg Txn Value","Success Rate %","Est Failed Value"
# ]

# st.dataframe(
#     audit_df.style
#     .format({
#         "Volume (ETB)":     "{:,.0f}",
#         "Revenue (ETB)":    "{:,.0f}",
#         "Avg Charge":       "{:,.2f}",
#         "Avg Txn Value":    "{:,.0f}",
#         "Success Rate %":   "{:.2f}%",
#         "Est Failed Value": "{:,.0f}",
#     })
#     .applymap(lambda v: f"background-color:{RED};color:white" if isinstance(v,str) and v=="High"
#               else (f"background-color:{AMBER}" if isinstance(v,str) and v=="Medium"
#               else (f"background-color:{GREEN};color:white" if isinstance(v,str) and v=="Low" else "")),
#               subset=["Risk"])
#     .bar(subset=["Success Rate %"], color=["#c0392b","#1e8449"], vmin=0, vmax=100)
#     .bar(subset=["Volume (ETB)"], color="#d6e4f0"),
#     use_container_width=True, height=380,
# )

# st.divider()

# # ════════════════════════════════════════════════════════════════════════════
# # CRITICAL FLAGS & ACTIONS
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="section-title">Key Observations & Actions Required</div>', unsafe_allow_html=True)

# critical_items = [
#     ("Telebirr channel has 100% failure across REMITLY (42 txns) and RAFIKI (21 txns). ETB 661K blocked. Urgent technical resolution needed.",
#      f"{total_telebirr} transactions blocked. Integration broken at API level."),
#     (f"{total_cif} customers blocked across 3 merchants because their info doesn't match CBE's system. Need to contact CBE to unblock them.",
#      "Affects RED SEA DIRECT DEPOSITS (26), JUBA EXPRESS (21), REMITLY GLOBAL (22). Compile account list and raise with CBE relationship manager."),
#     ("DEEROSERVICES has been failing 1 in every 6 transactions for at least 4 months in a row. Every single failure is coming from their Kaafi MFI and Cooperative Bank of Oromia connections.",
#      "159 failures (16.65%). Reroute from Kaafi MFI and Cooperative Bank of Oromia immediately. ETB 14,469 charged on failed txns needs refund."),
#     ("BIRRLINK zero revenue for 4th consecutive period. ETB 0 on all transactions.",
#      "52 transactions processed at zero revenue."),
#     ("RAFIKI/NALA 77.78% failure rate. Integration not production ready. ETB 1,911 charged on failed transactions.",
#      "21 of 27 transactions failed. Telebirr channel 100% failure. Bank channel 100% success. Still in testing phase."),
# ]

# for headline, detail in critical_items:
#     st.markdown(f"""
#     <div class="crit-card">
#       <strong>🔴 CRITICAL:</strong> {headline}<br>
#       <span style="font-size:12px;color:#666;">{detail}</span>
#     </div>
#     """, unsafe_allow_html=True)

# st.divider()
# st.markdown('<div class="section-title">Strenghts</div>', unsafe_allow_html=True)

# positive_obs = [
#     ("🟢 FINPAYAPPLICATION (EMAAL) & JUBAEXPRESS Lead Performance",
#      "FINPAYAPPLICATION delivered highest total value (ETB 358M), best success rate (99.85%), and highest avg transaction value (ETB 75,458) with only 7 failures across 4,756 transactions. "
#      "JUBAEXPRESS leads on transaction count (8,042) and revenue (ETB 1,008,230). Both merchants show clean operations with broad bank diversification. "
#      "FINPAYAPPLICATION is the only major merchant with zero blocked customers, understanding why could help protect other merchants."),
#     ("🟢 New Merchants BAKAALEXPRESS & MELAFINANCE Performing Well",
#      "Both new merchants show strong early performance: BAKAALEXPRESS at 98.67% success (300 txns), MELAFINANCE at 95% (60 txns in first 2 weeks). "
#      "Both use percentage based fee models. MELAFINANCE's auth token failures (2 cases) should be resolved quickly."),
# ]

# for title, body in positive_obs:
#     st.markdown(f'<div class="obs-card"><strong>{title}</strong><br><br>{body}</div>', unsafe_allow_html=True)

# st.divider()

# # ════════════════════════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════════════════════════
# st.markdown(f"""
# <div style="background:{NAVY};color:white;padding:20px 28px;border-radius:8px;margin-top:20px;font-size:12px;opacity:0.9;">
#   <strong style="font-family:'DM Serif Display',serif;font-size:16px;">FinPay Tech · Monthly Report · May 2026</strong><br>
#   <span style="opacity:0.6;font-size:10px;">
#   FX data gap: Finance submitted 22 May opening rates only. Daily FX tracking Excel established for June onwards.
#   Data source: FinPay transaction portal exports. Analysis by Gladys W.
#   </span>
# </div>
# """, unsafe_allow_html=True)

# # streamlit run app.py

# # ── SIDEBAR ───────────────────────────────────────────────────────────────────
# # st.sidebar.markdown("### FinPay Analytics")
# # st.sidebar.markdown("**Cycle:** Apr 27 to May 3, 2026")
# # st.sidebar.markdown(f"**Merchants:** {len(df)}")
# # st.sidebar.markdown(f"**Total Volume (Excl. REMITLY):** ETB {volume_excl_remitly/1e6:.2f}M")
# # st.sidebar.markdown(f"**Total Revenue:** ETB {df['Revenue'].sum():,.2f}")
# # st.sidebar.divider()
# # st.sidebar.markdown("⚠ **REMITLYGLOBAL** volume = 0 due to data tag issue in source dataset. See report for details.")
# # st.sidebar.divider()

# # if st.sidebar.button("Download Strategic PDF"):
# #     try:
# #         pdf_bytes = generate_pdf(
# #             df, df_prev,
# #             fig_vol, fig_rev, fig_sr, fig_fail,
# #             fig_margin, fig_ticket,
# #             fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail
# #         )
# #         if isinstance(pdf_bytes, str):
# #             pdf_bytes = pdf_bytes.encode("latin-1")
# #         b64 = base64.b64encode(pdf_bytes).decode()
# #         href = (
# #             f'<a href="data:application/octet-stream;base64,{b64}" '
# #             f'download="Merchant360_Apr27_May3_2026.pdf" '
# #             f'style="text-decoration:none; color:white; background:{MAIN_COLOR}; '
# #             f'padding:12px 16px; border-radius:5px; display:inline-block; font-size:13px;">'
# #             f'Save PDF Report</a>'
# #         )
# #         st.sidebar.markdown(href, unsafe_allow_html=True)
# #     except Exception as e:
# #         st.sidebar.error(f"PDF error: {e}")

# # st.sidebar.divider()
# # st.sidebar.markdown("**Risk Legend**")
# # st.sidebar.markdown("🔴 Red; Revenue or failure anomaly")
# # st.sidebar.markdown("🟡 Yellow; Elevated failure rate")
# # st.sidebar.markdown("🟢 Green; Normal operating range")

# # streamlit run app.py


# # streamlit run app.py
# # .\venv\Scripts\activate



AS_OF = "23 Nov 2026"

# key, merchant, channel, first, last, status, total, success, failed, volume, revenue, refunds, failvalue, charge model, cbe %, main issue
ROWS = [
 ("FINPAYAPPLICATION_BANK","Finpay App (Emaal)","Bank","3 Jan","23 Nov","Active",85045,84822,223,4563607425.25,7351526.00,12194.00,11474887.90,"Free Jan to Feb, ETB 91 flat from Apr",86.92,"Ethio Telecom outage 30 Aug to 1 Sep, CBE branch block 26 Sep to 6 Oct"),
 ("FINPAYAPPLICATION_MOBILE","Finpay App (Emaal)","Mobile","Jan","22 Nov","Active",1063,979,84,27275947.26,88816.00,7644.00,2821582.28,"About 0.33% of value",None,"70 of 100 mobile failures are System error from 30 Aug to 1 Sep"),
 ("JUBAEXPRESS_BANK","Juba Express","Bank","31 Dec","23 Nov","Active",82752,80465,2287,2609051151.00,4097781.61,139309.47,80795941.00,"0.40% until 5 Jun, none since",76.67,"Charging stopped 5 Jun, about ETB 6.34M not collected (estimate)"),
 ("JUBAEXPRESS_MOBILE","Juba Express","Mobile","10 Aug","4 Nov","Quiet since 4 Nov",313,238,75,4232460.00,0.00,0.00,1514197.00,"No charge",None,"Never charged, 24% failure rate, no traffic for 19 days"),
 ("THUNES","Thunes","Bank","20 Aug","23 Nov","Active",40320,39635,685,1435021463.13,0.00,0.00,25975002.39,"No charge",81.30,"Failure rate rising 0.90% (Sep) to 2.03% (Nov), export is 4 successes behind the portal"),
 ("REMITLYGLOBAL","Remitly Global","Bank (incl. CBE Birr, HCash)","27 Mar","23 Nov","Active",127785,124600,3184,3537067166.70,0.00,0.00,108844569.38,"No charge",66.83,"One payment stuck as INSERTED since 25 Jun, Telebirr and M-Pesa file not in this pull"),
 ("REDSEADIRECTDEPOSITS","Red Sea Direct Deposits","Bank","1 Apr","23 Jul","Stopped 23 Jul",13470,13007,463,587149915.13,5871501.73,220608.27,22060817.59,"1.00% of value",70.45,"No traffic for four months, 82 GL-not-allowed failures all in June"),
 ("REDSEA","Red Sea","Bank","15 Feb","14 Aug","Stopped 14 Aug",8684,8563,121,473876646.50,4685305.18,58968.51,6120570.00,"1.00% (0.50% on launch day)",67.63,"Funds Red Sea Direct Deposits through account debits, 101 days quiet"),
 ("DEEROSERVICES","Deero Services","Bank","27 Feb","7 May","Disbursements stopped",7231,6416,815,245539122.00,449904.00,69524.00,25897510.00,"Free to 19 Mar, then ETB 91 flat",58.65,"No disbursements since 7 May, Kaafi fails 26.6%, Cooperative Bank of Oromia 44.5%"),
 ("FLEXYREMIT","FlexyRemit","Bank","4 Sep","23 Nov","Active",4312,4080,232,206978944.57,0.00,0.00,8427308.71,"No charge",72.84,"November volume 443 vs 2,399 in October, Coopay-eBirr failed 12 of 12"),
 ("USWYRE","USWYRE","Bank","Aug","23 Nov","Active",2630,2427,203,74092743.39,370466.29,31752.14,6350390.87,"0.50% flat",60.19,"No activity in October, Kaafi fails 13.4%, Cooperative Bank of Oromia 65.5%"),
 ("MELAFINANCE","Mela Finance","Bank","15 May","23 Nov","Active",3064,2952,112,123184802.28,369564.56,8765.47,2921763.27,"0.30% of value",70.79,"October failure rate 5.18%, two charge anomalies on CBE payments"),
 ("BAKAALEXPRESS","Bakaal Express (Remittel)","Bank","9 May","23 Nov","Active",3103,2995,108,107464442.78,376466.27,16560.10,4731301.87,"0.35% of value",80.60,"Cooperative Bank of Oromia fails 69%, possible double payment on reference 7321317"),
 ("RAFIKILTD_BANK","Rafiki Ltd (Nala)","Bank","17 Feb","23 Nov","Active",1852,1134,718,20292468.29,103194.00,65338.00,5238525.07,"ETB 91 flat, also on failed",31.10,"Three repeated payments are 605 of 718 failures, Addis International failed 146 of 146"),
 ("RAFIKILTD_MOBILE","Rafiki Ltd (Nala)","Mobile","17 Feb","23 Nov","Active",913,542,371,5605332.28,49322.00,33761.00,56380162.82,"ETB 91 flat, also on failed",None,"Two repeated Safaricom payments are 220 of 371 failures"),
 ("BIRRLINK","Birr Link","Bank","27 Feb","15 Nov","Near dormant",350,333,17,9118224.28,0.00,0.00,622928.22,"No charge",85.14,"Almost no traffic since July, zero revenue throughout"),
]

# other currencies (Finpay): channel, currency, total, success, failed, value, revenue, refunds
OTHER_CCY = [
 ("Finpay bank","KES",41,40,1,2033806.00,1110.00,30.00),
 ("Finpay bank","UGX",11,7,4,3978828.00,1000.00,0.00),
 ("Finpay mobile","KES",399,386,13,10089338.35,19800.00,600.00),
 ("Finpay mobile","UGX",147,144,3,82150810.00,2000.00,0.00),
]

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov"]

# successful disbursement value, ETB millions (Juba Dec 2025 folded into Jan, EAT dates)
VALUE_M = {
 "Finpay App (bank)":[86.75,103.32,98.02,152.46,259.87,440.91,548.47,659.75,847.89,751.63,614.54],
 "Juba Express (bank)":[173.73,135.50,182.91,237.18,252.25,266.92,300.04,323.10,287.90,274.95,174.58],
 "Remitly Global":[0,0,2.507,286.6,457.3,355.3,474.3,563.2,607.9,471.7,318.1],
 "Thunes":[0,0,0,0,0,0,0,0.001,177.4,717.1,540.6],
 "Red Sea":[0,93.461,179.423,57.730,95.432,38.521,9.199,0.109,0,0,0],
 "Red Sea Direct Deposits":[0,0,0,193.111,193.587,136.050,64.401,0,0,0,0],
 "Deero Services":[0,7.433,81.691,126.139,30.277,0,0,0,0,0,0],
 "FlexyRemit":[0,0,0,0,0,0,0,0,66.75,125.60,14.62],
 "Mela Finance":[0,0,0,0,2.065,14.924,26.070,20.188,20.713,22.273,16.951],
 "Bakaal Express":[0,0,0,0,4.873,16.927,12.408,20.523,24.572,17.427,10.734],
 "USWYRE":[0,0,0,0,0,0,0,0.003,36.630,0,37.459],
 "Birr Link":[0,0.106,2.131,2.499,1.838,1.593,0.941,0.007,0,0,0.002],
}

# revenue by month, ETB (Rafiki and Finpay mobile not available by month)
REVENUE = {
 "Finpay App (bank)":[0,0,64610,305760,427336,613977,889343,1087996,1532531,1369550,1060423],
 "Juba Express (bank)":[694926.36,541997.30,731646.99,948751.60,1009026.55,171432.81,0,0,0,0,0],
 "Red Sea":[0,881146.73,1794233.45,577303.43,954322.47,385214.34,91994.73,1090.03,0,0,0],
 "Red Sea Direct Deposits":[0,0,0,1931109.49,1935874.59,1360503.23,644014.42,0,0,0,0],
 "Deero Services":[0,0,91546,291473,66885,0,0,0,0,0,0],
 "Mela Finance":[0,0,0,0,6200.99,44772.94,78210.49,60564.03,62141.33,66821.06,50853.72],
 "Bakaal Express":[0,0,0,0,17384.07,59248.28,43428.18,71832.19,86006.27,60997.58,37569.70],
 "USWYRE":[0,0,0,0,0,0,0,17.05,183152.89,0,187296.35],
}

# merchant, channel, failed txns charged, amount ETB, note
REFUNDS = [
 ("Red Sea Direct Deposits","Bank",463,220608.27,"Includes 11 duplicate-payment rejections that were still charged"),
 ("Juba Express","Bank",970,139309.47,"All from before 6 Jun, later failures were not charged"),
 ("Rafiki Ltd (Nala)","Bank",718,65338.00,"Retry loops alone account for most of this"),
 ("Rafiki Ltd (Nala)","Mobile",371,33761.00,"Retry loops on two Safaricom payments"),
 ("Deero Services","Bank",764,69524.00,"Kaafi and Cooperative Bank of Oromia are 91% of it"),
 ("Red Sea","Bank",121,58968.51,"105 of 121 payments were later retried and succeeded, charge is still owed"),
 ("USWYRE","Bank",203,31752.14,"BLCK failures are ETB 12,522.06 of this"),
 ("Finpay App (Emaal)","Bank",None,12194.00,"Also KES 30 on bank"),
 ("Finpay App (Emaal)","Mobile",None,7644.00,"Also KES 600 on mobile"),
 ("Bakaal Express (Remittel)","Bank",108,16560.10,"CBE and Cooperative Bank of Oromia are 89% of it"),
 ("Mela Finance","Bank",112,8765.47,"CBE is about two thirds of it"),
]

# priority, issue, merchants, evidence, action, suggested owner
FLAGS = [
 ("P1","Zero revenue on very large volumes","Remitly, Thunes, FlexyRemit, Birr Link, Juba mobile","About ETB 5.19 billion moved with no charge on any transaction (Remitly 3.54B, Thunes 1.44B, FlexyRemit 207M, Birr Link 9.1M). Portal confirms FlexyRemit shows ETB 0.00.","Confirm in writing whether fees are billed off platform (FX margin, invoice) or the charge setup is missing.","Commercial and Finance"),
 ("P1","Juba Express stopped charging on 5 Jun","Juba Express bank","Rate was exactly 0.40% until 5 Jun, then zero on 48,184 successes. About ETB 6.34M not collected if charging should have continued (estimate).","Find out if this was a deliberate waiver or a configuration fault, then fix or document.","Finance, Peneal"),
 ("P1","Refunds owed on charges taken from failed transactions","9 merchants","ETB 664,424.96 plus KES 630 across the year. Largest: Red Sea Direct Deposits 220,608, Juba bank 139,309, Rafiki 99,099.","Confirm none were already refunded, then run the refund batch. Failed rows have no Transaction ID, match on Reference.","Finance"),
 ("P1","Rafiki retry loops","Rafiki bank and mobile","Three bank payments were retried 436, 143 and 26 times, two mobile payments 173 and 47 times, each attempt charged ETB 91. November failure rates 73% bank, 96% mobile.","Stop the retries at source, add a duplicate and retry limit, and tell Rafiki.","Peneal, Gladys"),
 ("P1","Cooperative Bank of Oromia failing across the platform","10 merchants","Failure rates 40% to 69% at Flexy, Thunes, Deero, Bakaal, Remitly, USWYRE, Juba, Red Sea Direct. The XML validation failures are only at this bank.","Tech to fix the message format or route traffic away until fixed.","Peneal"),
 ("P1","Kaafi Microfinance BLCK failures","Deero, USWYRE, FlexyRemit","Deero 426 and USWYRE 78 BLCK failures, FlexyRemit all 20 BLCK failures.","Ask Kaafi what BLCK means for these accounts and whether account checks can run before sending.","Peneal"),
 ("P1","Idle and stopped connections","Red Sea Direct, Red Sea, Deero, Birr Link, Juba mobile","Red Sea Direct stopped 23 Jul, Red Sea 14 Aug, Deero disbursements 7 May, Birr Link near dormant, Juba mobile quiet since 4 Nov. Red Sea and Red Sea Direct are one operation (ETB 1.06B combined).","Send the management directive emails. Ask whether volume moved to another provider.","Gladys"),
 ("P2","Payment stuck as INSERTED","Remitly","ETB 4,779 to a CBE account, reference R30378308885, no final status since 25 Jun.","Check whether the customer was paid and close it.","Peneal"),
 ("P2","Possible double payment","Bakaal Express","Two successful ETB 12,411.24 payments on reference 7321317, one second apart on 25 Aug.","Check with the bank whether the customer was paid twice.","Peneal, Finance"),
 ("P2","Thunes export behind the portal","Thunes","Portal has 4 more successes worth ETB 174,153.58 than the export.","Re-pull the export and re-check. Use portal figures until then.","PM"),
 ("P2","FlexyRemit volume drop in November","FlexyRemit","443 disbursements in 23 days against 2,399 in October. Coopay-eBirr failed 12 of 12.","Check whether the limit increase request or Cooperative Bank of Oromia failures are holding traffic back.","Backend, Gladys"),
 ("P2","Float running short","Remitly, Juba, Red Sea Direct, Bakaal","Insufficient balance is the top failure at Remitly (623) and Juba (564). Bakaal had 14 in one day on 29 Jun.","Set a low-balance alert and tell merchants to prefund earlier.","Gladys"),
 ("P2","Merchants not yet pulled","Amal Express and sub-accounts, TapTapSend, Revenue Proceeds, Overdraft account, Deero sub-accounts, Mamlaka, HoneyCoin, Kotani","Amal Express had 11 transactions in June but has no pull here. Remitly file has no Telebirr or M-Pesa rows although June showed about 1,459.","Pull bank and mobile exports for these and the Remitly mobile file.","PM"),
 ("P2","Earlier June report needs restating","Bakaal, Red Sea Direct, Finpay, Juba","June report showed Bakaal ETB 129.8M (full pull says 16.9M), Red Sea Direct revenue 810K (full pull 1.36M), Finpay bank 566M (full pull 441M), Juba 303M (full pull 267M).","Restate June using this pull. The Bakaal '26x growth' headline was wrong, real May to June growth is 3.5x.","PM"),
]

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FinPay Jan to Nov 2026", layout="wide")

GREEN  = "#1a6b3c"
GREEN2 = "#27ae60"
RED    = "#c0392b"
AMBER  = "#e67e22"
GRAY   = "#f4f6f4"
TEXT   = "#1a1a1a"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background: {GRAY};
    color: {TEXT};
}}

[data-testid="stMetricValue"] {{
    font-size: clamp(20px, 2.5vw, 32px) !important;
    font-weight: 700 !important;
    color: {GREEN} !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: clamp(13px, 1.2vw, 16px) !important;
    color: #444 !important;
    font-weight: 500 !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: clamp(12px, 1vw, 14px) !important;
}}
[data-testid="stTab"] p {{
    font-size: clamp(14px, 1.3vw, 17px) !important;
    font-weight: 600 !important;
}}
.stDataFrame td, .stDataFrame th {{
    font-size: clamp(13px, 1.1vw, 15px) !important;
    padding: 8px 12px !important;
}}
p, li, div {{
    font-size: clamp(14px, 1.2vw, 16px);
    line-height: 1.7;
}}
.info-box {{
    background: #e8f5ee;
    border-left: 4px solid {GREEN};
    border-radius: 6px;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
    font-size: clamp(14px, 1.2vw, 16px);
    color: #0d3320;
    line-height: 1.75;
}}
.warn-box {{
    background: #fef3e2;
    border-left: 4px solid {AMBER};
    border-radius: 6px;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
    font-size: clamp(14px, 1.2vw, 16px);
    color: #5a3000;
    line-height: 1.75;
}}
.crit-box {{
    background: #fdf0f0;
    border-left: 4px solid {RED};
    border-radius: 6px;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
    font-size: clamp(14px, 1.2vw, 16px);
    color: #5a0000;
    line-height: 1.75;
}}
.good-box {{
    background: #e8f5ee;
    border-left: 4px solid {GREEN2};
    border-radius: 6px;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
    font-size: clamp(14px, 1.2vw, 16px);
    color: #0b3d1f;
    line-height: 1.75;
}}
.section-title {{
    font-size: clamp(18px, 1.8vw, 22px);
    font-weight: 700;
    color: {GREEN};
    border-bottom: 2px solid {GREEN2};
    padding-bottom: 8px;
    margin: 28px 0 16px;
}}
.header-band {{
    background: linear-gradient(135deg, {GREEN} 0%, #145a32 60%, #0d3d22 100%);
    padding: 28px 32px;
    border-radius: 10px;
    margin-bottom: 24px;
    color: white;
    border-left: 5px solid {GREEN2};
}}
.detail-card {{
    background: white;
    border-radius: 10px;
    padding: 20px 24px;
    margin-top: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    font-size: clamp(14px, 1.2vw, 16px);
    line-height: 2;
}}
</style>
""", unsafe_allow_html=True)

df = pd.DataFrame(ROWS, columns=["key","Merchant","Channel","First","Last","Status","Total","Success","Failed","Value","Revenue","Refunds","FailedValue","ChargeModel","CBE","Issue"])
df["Label"] = df["Merchant"] + " (" + df["Channel"].str.split(" ").str[0].str.lower() + ")"
df["SuccessRate"] = df["Success"]/df["Total"]*100
df["ChargeRate"] = (df["Revenue"]/df["Value"]*100).round(3)

total_val   = df.Value.sum()
total_rev   = df.Revenue.sum()
total_txns  = df.Total.sum()
total_succ  = df.Success.sum()
total_ref   = df.Refunds.sum()

st.markdown(f"""
<div class="header-band">
  <div style="font-size:clamp(22px,3vw,34px);font-weight:700;color:white;margin-bottom:8px;">Merchant Performance Report</div>
  <div style="font-size:clamp(13px,1.3vw,16px);opacity:0.9;color:white;">01 January to {AS_OF} &nbsp; {len(df)} merchant connections &nbsp; Disbursements only, ETB &nbsp; Source: Our portal</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="info-box"><strong>Value moved</strong> is the total ETB disbursed to end recipients. <strong>Revenue</strong> is what FinPay earned in fees   the blended rate shows how many cents we earn per ETB 100 processed. <strong>Success rate</strong> is the share of transactions that reached the recipient. <strong>"Refunds owed" </strong> means fees we charged merchants on payments that failed.</div>', unsafe_allow_html=True)

k = st.columns(5)
k[0].metric("Value moved", f"ETB {total_val/1e9:.2f}B")
k[1].metric("Revenue", f"ETB {total_rev:,.0f}", f"{total_rev/total_val*100:.2f}% of value", delta_color="off")
k[2].metric("Transactions", f"{total_txns:,}")
k[3].metric("Success rate", f"{total_succ/total_txns*100:.2f}%")
k[4].metric("Refunds owed", f"ETB {total_ref:,.0f}")

t1,t2,t3,t4,t5,t6 = st.tabs(["📊 Volume & Revenue","✅ Success & Failures","📈 Monthly Trend","💸 Refunds Owed","🔍 Merchant Detail","🚩 Flags & Gaps"])

with t1:
    st.markdown('<div class="section-title">Volume & Revenue Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>The left chart:</strong>  ranks every merchant by the total ETB they disbursed to recipients. Bigger bars mean more money flowing through our gateway. <strong>The right chart</strong> shows only merchants who are actually generating fees. Merchants with ETB 0 revenue are excluded because they either have a zero-fee arrangement/charges. The formular: the exact charge model for each merchant and the blended rate (total revenue divided by total value times 100).</div>', unsafe_allow_html=True)
    a,b = st.columns(2)
    d = df.sort_values("Value")
    fig_val = px.bar(d, x="Value", y="Label", orientation="h", title="Total Value Moved by Merchant (ETB)",
                     color_discrete_sequence=[GREEN],
                     text=d["Value"].apply(lambda v: f"{v/1e9:.2f}B" if v>=1e9 else f"{v/1e6:.0f}M"))
    fig_val.update_traces(textposition="outside", textfont_size=13)
    fig_val.update_layout(height=540, yaxis_title="", xaxis_title="ETB",
                          font=dict(family="DM Sans", size=14), margin=dict(t=50,b=20,l=10,r=90))
    a.plotly_chart(fig_val, use_container_width=True)

    d2 = df[df.Revenue>0].sort_values("Revenue")
    fig_rev = px.bar(d2, x="Revenue", y="Label", orientation="h",
                     title="Revenue Earned   Fee-Charging Merchants Only (ETB)",
                     color_discrete_sequence=[GREEN],
                     text=d2["Revenue"].apply(lambda v: f"{v/1e6:.2f}M" if v>=1e6 else f"{v:,.0f}"))
    fig_rev.update_traces(textposition="outside", textfont_size=13)
    fig_rev.update_layout(height=540, yaxis_title="", xaxis_title="ETB",
                          font=dict(family="DM Sans", size=14), margin=dict(t=50,b=20,l=10,r=90))
    b.plotly_chart(fig_rev, use_container_width=True)

    st.markdown('<div class="warn-box"><strong>Zero-revenue merchants (No charges):</strong> Remitly (ETB 3.54B), Thunes (ETB 1.44B), FlexyRemit (ETB 207M), Birr Link (ETB 9.1M), and Juba mobile are processing significant value with no fee income recorded...we have a different billing arrangement (e.g. FX margin)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Charge Model Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>Contracted rate</strong> is what the agreement says (e.g. 1.00% or ETB 91 flat). <strong>Blended rate</strong> is what we actually earned: total revenue divided by total value times 100. For flat-fee merchants the blended rate varies with transaction size. <strong>Revenue per txn</strong> is the average ETB earned per successful transaction. Merchants showing 0.000% blended rate have no fee recorded on the platform.</div>', unsafe_allow_html=True)

    charge_df = df[["Label","ChargeModel","Value","Revenue","ChargeRate","Success"]].copy()
    charge_df["Rev per txn (ETB)"] = (charge_df["Revenue"] / charge_df["Success"].replace(0,1)).round(2)
    charge_df["Fee type"] = charge_df["ChargeModel"].apply(
        lambda x: "No charge" if "No charge" in str(x)
        else "Flat fee" if "ETB" in str(x) and "%" not in str(x)
        else "Percentage" if "%" in str(x)
        else "Mixed"
    )
    charge_df = charge_df.rename(columns={
        "Label": "Merchant",
        "ChargeModel": "Contracted rate",
        "Value": "Value moved (ETB)",
        "Revenue": "Revenue earned (ETB)",
        "ChargeRate": "Blended rate %",
    })[["Merchant","Fee type","Contracted rate","Value moved (ETB)","Revenue earned (ETB)","Blended rate %","Rev per txn (ETB)"]]

    def color_fee(val):
        if val == "No charge": return f"background-color:#fef3e2;color:#5a3000"
        if val == "Flat fee":  return f"background-color:#e8f5ee;color:#0d3320"
        if val == "Percentage": return f"background-color:#eaf4fb;color:#0a3d62"
        return ""

    st.dataframe(
        charge_df.style
        .format({"Value moved (ETB)":"{:,.0f}","Revenue earned (ETB)":"{:,.2f}","Blended rate %":"{:.3f}%","Rev per txn (ETB)":"{:,.2f}"})
        .map(color_fee, subset=["Fee type"]),
        use_container_width=True, hide_index=True
    )

with t2:
    st.markdown('<div class="section-title">Transaction Success Rates</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>What this shows:</strong> Each bar is the percentage of transactions that successfully reached the recipient. Red means below 85% (critical), amber means 85 to 96% (elevated, monitor closely), green means 97% or above (healthy). The platform target is 97% or above.</div>', unsafe_allow_html=True)
    d = df.sort_values("SuccessRate")
    colors = [RED if v<85 else AMBER if v<97 else GREEN for v in d.SuccessRate]
    fig_sr = go.Figure(go.Bar(
        x=d.SuccessRate, y=d.Label, orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in d.SuccessRate],
        textfont=dict(size=14),
    ))
    fig_sr.update_layout(
        title="Success Rate by Merchant (%)",
        height=540, xaxis=dict(range=[0,105], title="%"),
        yaxis_title="", font=dict(family="DM Sans", size=14),
        margin=dict(t=50,b=20,l=10,r=60),
        plot_bgcolor="white",
    )
    st.plotly_chart(fig_sr, use_container_width=True)

    deero = df[df.key=="DEEROSERVICES"].iloc[0]
    st.markdown(f'<div class="crit-box"><strong>Merchants needing attention:</strong><br><br>'
        f'<strong>Rafiki Ltd</strong> bank (38.7%) and mobile (59.4%) are critically low. Root cause: retry loops where the same payment is sent hundreds of times, each attempt failing and being charged ETB 91.<br><br>'
        f'<strong>Deero Services</strong> (88.7%) has persistent failures concentrated at two specific banks: '
        f'<strong>Kaafi Microfinance</strong> (26.6% failure rate, BLCK account-blocked errors) and '
        f'<strong>Cooperative Bank of Oromia</strong> (44.5% failure rate, XML validation errors). '
        f'These two banks account for virtually all of Deero\'s 815 failures.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Failure Hot Spots by Bank</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>What this shows:</strong> This table looks at failures per bank. The two most critical banks are Cooperative Bank of Oromia (XML validation errors affecting 7 or more merchants) and Kaafi Microfinance (BLCK account blocked errors).</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        ["Cooperative Bank of Oromia","Flexy 59%, Thunes 54%, Deero 45%, Bakaal 69%, Remitly 51%, USWYRE 66%, Juba 39%","XML validation failures   only at this bank","P1   Fix message format or reroute"],
        ["Kaafi Microfinance","Deero 27%, USWYRE 13%, FlexyRemit all BLCK","BLCK (account blocked at source)","P1   Ask Kaafi what BLCK means, add pre-send check"],
        ["Bank of Abyssinia","Rafiki 70%, Remitly 437 Creditor Agent errors","Mixed error types","P2   Investigate per merchant"],
        ["Addis International","Rafiki 146 of 146 failed, Juba 52%","Mixed error types","P2   Investigate"],
        ["CBE Birr (mobile)","Juba 22 of 22 since Sep","Technical errors","P2   Check integration"],
    ], columns=["Bank","Failure rate by merchant","Main reason","Action"]),
    use_container_width=True, hide_index=True)

with t3:
    st.markdown('<div class="section-title">Monthly Volume & Revenue Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>What this shows:</strong> The top chart tracks how much ETB each merchant disbursed each month. Rising lines mean growing activity; flat or falling lines mean the merchant is slowing down or has stopped. The bottom chart shows monthly revenue. Juba Express revenue drops to zero after June because charging stopped on 5 June.</div>', unsafe_allow_html=True)
    mv = pd.DataFrame(VALUE_M, index=MONTHS).T.reset_index().melt(id_vars="index", var_name="Month", value_name="ETB millions")
    fig_mv = px.line(mv, x="Month", y="ETB millions", color="index", markers=True,
                     title="Successful Disbursement Value by Month (ETB millions)")
    fig_mv.update_layout(height=500, legend_title="", font=dict(family="DM Sans", size=14),
                         margin=dict(t=50,b=20,l=10,r=10))
    fig_mv.update_traces(line=dict(width=2.5), marker=dict(size=8))
    st.plotly_chart(fig_mv, use_container_width=True)

    rv = pd.DataFrame(REVENUE, index=MONTHS).T.reset_index().melt(id_vars="index", var_name="Month", value_name="ETB")
    fig_rv = px.bar(rv, x="Month", y="ETB", color="index",
                    title="Revenue by Month (ETB)   Rafiki and Finpay mobile have no month split")
    fig_rv.update_layout(height=500, legend_title="", font=dict(family="DM Sans", size=14),
                         margin=dict(t=50,b=20,l=10,r=10))
    st.plotly_chart(fig_rv, use_container_width=True)

    st.markdown('<div class="warn-box"><strong>Key trend to watch:</strong> Juba Express revenue falls to zero after June because charging stopped on 5 Jun. FlexyRemit dropped from 2,399 transactions in October to 443 in the first 23 days of November..</div>', unsafe_allow_html=True)

with t4:
    st.markdown('<div class="section-title">Refunds Owed to Merchants</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>What this shows:</strong> When a transaction fails, the recipient does not receive money. If FinPay already collected a fee on that transaction, we owe that fee back to the merchant. This table lists every merchant where we charged a fee on a failed transaction and the total amount owed. The largest exposure is Red Sea Direct Deposits (ETB 220,608) and Juba Express (ETB 139,309). Failed transactions have no Transaction ID in the export, so match on the Reference field when processing refunds.</div>', unsafe_allow_html=True)
    rf = pd.DataFrame(REFUNDS, columns=["Merchant","Channel","Failed txns charged","Amount owed (ETB)","Note"])
    total_owed = rf["Amount owed (ETB)"].sum()
    st.metric("Total refunds owed", f"ETB {total_owed:,.2f}", "plus KES 630 on Finpay", delta_color="off")
    st.dataframe(
        rf.style.format({"Amount owed (ETB)":"{:,.2f}"})
          .bar(subset=["Amount owed (ETB)"], color="#f5c6c6"),
        use_container_width=True, hide_index=True
    )

with t5:
    st.markdown('<div class="section-title">Per-Merchant Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">The metrics show cumulative totals from first activity to last recorded transaction. The charge model explains how fees are calculated. The main issue is the single most important thing to resolve for that merchant.</div>', unsafe_allow_html=True)
    pick = st.selectbox("Select a merchant", df.Label.tolist(), label_visibility="visible")
    r = df[df.Label==pick].iloc[0]
    sr_color = RED if r.SuccessRate < 85 else AMBER if r.SuccessRate < 97 else GREEN
    c = st.columns(5)
    c[0].metric("Total transactions", f"{r.Total:,}")
    c[1].metric("Success rate", f"{r.SuccessRate:.2f}%")
    c[2].metric("Value moved (ETB)", f"{r.Value/1e6:.1f}M")
    c[3].metric("Revenue (ETB)", f"{r.Revenue:,.0f}")
    c[4].metric("Refunds owed (ETB)", f"{r.Refunds:,.0f}")
    st.markdown(f"""
    <div class="detail-card">
      <div><strong>Status:</strong> {r.Status} &nbsp; First activity: {r.First} &nbsp; Last activity: {r.Last}</div>
      <div><strong>Channel:</strong> {r.Channel}</div>
      <div><strong>Charge model:</strong> {r.ChargeModel}</div>
      <div><strong>Failed value (ETB):</strong> {r.FailedValue:,.0f}</div>
      {'<div><strong>CBE share of transactions:</strong> ' + str(r.CBE) + '%</div>' if pd.notna(r.CBE) else ''}
    </div>
    """, unsafe_allow_html=True)
    issue_color = "crit-box" if r.SuccessRate < 85 else "warn-box" if r.SuccessRate < 97 else "good-box"
    st.markdown(f'<div class="{issue_color}" style="margin-top:16px;"><strong>Main issue to resolve:</strong> {r.Issue}</div>', unsafe_allow_html=True)

with t6:
    st.markdown('<div class="section-title">Merchant Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">All 16 merchant connections, Jan to Nov 2026. Value in ETB millions. Success rate is transactions that reached the recipient. Refunds owed are fees charged on failed transactions that must be returned.</div>', unsafe_allow_html=True)

    summary_df = df[["Label","Total","SuccessRate","Value","Revenue","Refunds","Status"]].copy()
    summary_df["Value (ETB m)"] = (summary_df["Value"] / 1e6).round(1)
    summary_df["Success rate"] = summary_df["SuccessRate"].apply(lambda v: f"{v:.2f}%")
    summary_df = summary_df.rename(columns={"Label":"Merchant","Total":"Txns","Revenue":"Revenue (ETB)","Refunds":"Refunds owed (ETB)"})
    summary_df = summary_df[["Merchant","Txns","Success rate","Value (ETB m)","Revenue (ETB)","Refunds owed (ETB)","Status"]]

    totals = pd.DataFrame([{
        "Merchant": "TOTAL",
        "Txns": df.Total.sum(),
        "Success rate": f"{total_succ/total_txns*100:.2f}%",
        "Value (ETB m)": round(df.Value.sum()/1e6, 1),
        "Revenue (ETB)": df.Revenue.sum(),
        "Refunds owed (ETB)": df.Refunds.sum(),
        "Status": "",
    }])
    summary_display = pd.concat([summary_df, totals], ignore_index=True)

    st.dataframe(
        summary_display.style
        .format({"Txns":"{:,}", "Value (ETB m)":"{:,.1f}", "Revenue (ETB)":"{:,.0f}", "Refunds owed (ETB)":"{:,.0f}"})
        .apply(lambda row: [
            "font-weight:bold;background:#e8f5ee" if row["Merchant"]=="TOTAL" else ""
            for _ in row], axis=1),
        use_container_width=True, hide_index=True
    )

    st.markdown(f'<div class="warn-box"><strong>Red Sea and Red Sea Direct Deposits are one operation.</strong> Red Sea funds the Direct Deposits account. Read them together: ETB 1.06 billion moved and ETB 10.6 mmillion in revenue. Red Sea stopped 14 Aug, Direct Deposits stopped 23 Jul.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Flags, Gaps & Actions Required</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>What this shows:</strong> Every issue found in the data, ranked by priority. P1 means it needs to be resolved this week because it is either losing money, creating refund liability, or blocking transactions at scale. P2 means it needs to be investigated and resolved within the month. Each row includes what the data shows, what needs to happen, and who should own it.</div>', unsafe_allow_html=True)
    fl = pd.DataFrame(FLAGS, columns=["Priority","Issue","Merchants affected","What the data shows","What to do","Suggested owner"])
    p1 = fl[fl.Priority=="P1"]
    p2 = fl[fl.Priority=="P2"]
    st.markdown(f'<div class="crit-box"><strong>{len(p1)} Priority 1 issues</strong>   require action this week</div>', unsafe_allow_html=True)
    st.dataframe(
        p1.drop(columns="Priority").style.set_properties(**{"font-size":"14px"}),
        use_container_width=True, hide_index=True
    )
    st.markdown(f'<div class="warn-box" style="margin-top:20px;"><strong>{len(p2)} Priority 2 issues</strong>   investigate and resolve within the month</div>', unsafe_allow_html=True)
    st.dataframe(
        p2.drop(columns="Priority").style.set_properties(**{"font-size":"14px"}),
        use_container_width=True, hide_index=True
    )

st.divider()
st.markdown(f"""
<div style="background:{GREEN};color:white;padding:20px 28px;border-radius:8px;margin-top:10px;font-size:clamp(13px,1.1vw,15px);">
  <strong style="font-size:clamp(16px,1.5vw,20px);">FinPay Tech   Jan to Nov 2026 Report</strong><br>
  <span style="opacity:0.75;font-size:clamp(11px,1vw,13px);">Source: portal data exports - pulled 23 Nov 2026. Prepared by Gladys. Confidential</span>
</div>
""", unsafe_allow_html=True)