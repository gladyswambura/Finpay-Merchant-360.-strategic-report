import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── BRAND ────────────────────────────────────────────────────────────────────
NAVY   = "#081b31"
GOLD   = "#8e6d2d"
LIGHT  = "#f5f3ef"
RED    = "#c0392b"
GREEN  = "#1e8449"
AMBER  = "#d4ac0d"
BLUE   = "#1a5276"

st.set_page_config(page_title="FinPay | May 2026 Monthly Report", layout="wide", page_icon="📊")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; background:{LIGHT}; }}
h1,h2,h3 {{ font-family:'DM Serif Display', serif; color:{NAVY}; }}
[data-testid="stMetricValue"] {{ font-size:22px; color:{NAVY}; font-weight:600; }}
[data-testid="stMetricLabel"] {{ font-size:12px; color:#666; }}
.header-band {{
    background: linear-gradient(135deg, {NAVY} 0%, #0d2d52 60%, #112240 100%);
    padding:28px 32px; border-radius:12px; margin-bottom:24px; color:white;
    border-left: 5px solid {GOLD};
}}
.section-title {{
    font-family:'DM Serif Display',serif; font-size:20px; color:{NAVY};
    border-bottom: 2px solid {GOLD}; padding-bottom:8px; margin: 28px 0 16px;
}}
.obs-card {{
    background:white; padding:14px 18px; border-radius:8px;
    border-left:4px solid {GOLD}; margin-bottom:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06); font-size:13px; color:#333;
}}
.crit-card {{
    background:#fdf0f0; padding:14px 18px; border-radius:8px;
    border-left:4px solid {RED}; margin-bottom:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06); font-size:13px; color:#333;
}}
.scorecard {{
    background:white; padding:16px; border-radius:10px;
    box-shadow:0 2px 12px rgba(0,0,0,0.08); margin-bottom:12px;
    border-top:3px solid {GOLD};
}}
.badge-high {{ background:{RED}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
.badge-med  {{ background:{AMBER}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
.badge-low  {{ background:{GREEN}; color:white; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
.kpi-box {{
    background:white; border-radius:10px; padding:16px 20px;
    border-top:3px solid {GOLD}; box-shadow:0 2px 8px rgba(0,0,0,0.07);
    text-align:center;
}}
.flag-banner {{
    background:#fff3cd; border:1px solid #ffc107; border-radius:8px;
    padding:10px 16px; margin-bottom:10px; font-size:12px; color:#856404;
}}
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────
merchants = [
    {
        "code": "REDSEA",
        "name": "RED SEA",
        "country": "United Kingdom",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
        "channel": "Bank",
        "total_txns": 1374, "successful": 1370, "failed": 4, "pending": 0,
        "volume": 302232247.00,
        "revenue": 954322.47,
        "avg_charge": 696.59,
        "avg_txn_value": 220607.48,
        "failed_value": 202150.00,
        "top_failures": "XML validation failed; reversed (2), Missing data; reversed (2)",
        "banks_used": 12,
        "top_bank": "Commercial Bank of Ethiopia (69%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 0,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 0,
        "notes": "100% of failures were auto-reversed. ACCOUNT_DEBIT (17 txns, ETB 206.8M) are bulk/treasury transfers carrying zero charges. Broadest bank spread: 12 institutions, CBE at 69%.",
    },
    {
        "code": "REDSEADIRECTDEPOSITS",
        "name": "RED SEA DIRECT DEPOSITS",
        "country": "United Kingdom",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank",
        "total_txns": 4402, "successful": 4207, "failed": 195, "pending": 0,
        "volume": 192700775.95,
        "revenue": 1927008.63,
        "avg_charge": 458.05,
        "avg_txn_value": 45804.80,
        "failed_value": 9911320.30,
        "top_failures": "Insufficient balance (63), Unknown error (42), System Error (28), CIF harmonization block (26), Missing data; reversed (4), XML validation (3)",
        "banks_used": 11,
        "top_bank": "Commercial Bank of Ethiopia (70%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 26,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 99113.00,
        "notes": "Highest revenue merchant. ETB 9.9M in failed value — highest in portfolio. CIF harmonization block (26 cases) is CBE compliance sweep — needs escalation. ETB 99,113 charged on failed txns requires refund review.",
    },
    {
        "code": "JUBAEXPRESS",
        "name": "JUBA EXPRESS",
        "country": "Ethiopia",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank",
        "total_txns": 8042, "successful": 7923, "failed": 119, "pending": 0,
        "volume": 252050695.00,
        "revenue": 1008230.09,
        "avg_charge": 127.25,
        "avg_txn_value": 31812.53,
        "failed_value": 3534649.00,
        "top_failures": "System Error (24), Insufficient balance (24), XML validation (21), CIF harmonization block (21), Unknown error (12), Missing data; reversed (5)",
        "banks_used": 17,
        "top_bank": "Commercial Bank of Ethiopia (77%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 21,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 14138.93,
        "notes": "Highest transaction volume (bank channel). Broadest bank network — 17 institutions. CIF harmonization block (21 cases) confirms portfolio-wide CBE compliance event. ETB 14,138 charged on failed txns.",
    },
    {
        "code": "FINPAYAPPLICATION",
        "name": "FINPAY APPLICATION (EMAAL)",
        "country": "Kenya",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
        "channel": "Bank + Mobile",
        "total_txns": 4756, "successful": 4749, "failed": 7, "pending": 0,
        "volume": 358351263.38,
        "revenue": 427063.00,
        "avg_charge": 89.93,
        "avg_txn_value": 75458.26,
        "failed_value": 538144.00,
        "top_failures": "Transaction Failed generic (3), Missing data; reversed (1), ERRR; reversed (1), Insufficient balance (1), CreditParty invalid state/mobile (1)",
        "banks_used": 15,
        "top_bank": "Commercial Bank of Ethiopia (88%)",
        "mobile": True,
        "mobile_networks": ["Safaricom (M-Pesa)", "Airtel", "MTN"],
        "mobile_txns": 51, "mobile_successful": 49, "mobile_failed": 2,
        "mobile_volume": 6120284.00,
        "mobile_revenue": 0.00,
        "cif_issues": 0,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 455.00,
        "notes": "Highest total value moved (ETB 358M) and best success rate (99.85%). No CIF harmonization failures — only major merchant unaffected. Mobile: 3 networks, Airtel handling largest avg value (ETB 540K/txn). Mobile generates ETB 0 revenue — confirm if intentional.",
    },
    {
        "code": "BIRRLINK",
        "name": "BIRR LINK",
        "country": "Ethiopia",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank",
        "total_txns": 52, "successful": 50, "failed": 2, "pending": 0,
        "volume": 1841316.53,
        "revenue": 0.00,
        "avg_charge": 0.00,
        "avg_txn_value": 36826.33,
        "failed_value": 28297.90,
        "top_failures": "Exception on bank transfer (1), Insufficient balance (1)",
        "banks_used": 4,
        "top_bank": "Commercial Bank of Ethiopia (79%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 0,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 0,
        "notes": "CRITICAL: 4th consecutive period of ETB 0.00 revenue. Zero charges on all 52 transactions. Commercial team must resolve fee arrangement urgently — this merchant consumes operational resources at zero revenue.",
    },
    {
        "code": "DEEROSERVICES",
        "name": "DEERO SERVICES",
        "country": "USA",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
        "channel": "Bank",
        "total_txns": 955, "successful": 796, "failed": 159, "pending": 0,
        "volume": 188381403.00,
        "revenue": 67431.00,
        "avg_charge": 84.71,
        "avg_txn_value": 236660.05,
        "failed_value": 3607806.00,
        "top_failures": "BLCK Account Blocked; reversed (87), XML validation failed; reversed (63), System Error (7), Currency mismatch (2)",
        "banks_used": 10,
        "top_bank": "Commercial Bank of Ethiopia (50%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 0,
        "cbo_failures": 71,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 14469.00,
        "notes": "Worst success rate (83.35%). 100% of failures concentrated at 2 banks: Kaafi MFI (84 failures, BLCK errors) and Cooperative Bank of Oromia (71 failures, XML validation). ACCOUNT_DEBIT (55 txns, ETB 157.8M) all succeeded. ETB 14,469 charged on failed txns. Refund required.",
    },
    {
        "code": "REMITLYGLOBAL",
        "name": "REMITLY GLOBAL",
        "country": "USA",
        "period": "May 1–31, 2026",
        "full_month": True,
        "txn_types": ["DISBURSEMENTS", "ACCOUNT_DEBIT"],
        "channel": "Bank + Mobile",
        "total_txns": 15066, "successful": 14773, "failed": 293, "pending": 0,
        "volume": 467019428.75,
        "revenue": 0.00,
        "avg_charge": 0.00,
        "avg_txn_value": 31613.04,
        "failed_value": 17625789.27,
        "top_failures": "Creditor Agent error; reversed (57), System Error (52), Transaction not found (33), Insufficient balance (32), CIF harmonization block (22), Unknown error (16)",
        "banks_used": 12,
        "top_bank": "Commercial Bank of Ethiopia (66%)",
        "mobile": True,
        "mobile_networks": ["Safaricom (M-Pesa)", "Ethiotelecom (Telebirr)"],
        "mobile_txns": 245, "mobile_successful": 200, "mobile_failed": 45,
        "mobile_volume": 5039597.00,
        "mobile_revenue": 0.00,
        "cif_issues": 22,
        "cbo_failures": 8,
        "telebirr_failures": 42,
        "kyc_status": "Complete",
        "charges_on_failed": 0,
        "notes": "Highest volume (15,066 txns) and highest value moved (ETB 467M). ETB 0 revenue. International model, but arrangement must be documented. CRITICAL: Ethiotelecom/Telebirr 100% failure rate (42/42). 22 customers blocked due to CBE data mismatch. Cooperative Bank of Oromia: 57% failure rate (8/14). ETB 17.6M in failed value.",
    },
    {
        "code": "RAFIKILTD",
        "name": "RAFIKI LTD (NALA)",
        "country": "United Kingdom",
        "period": "May 6–28, 2026",
        "full_month": False,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank + Mobile",
        "total_txns": 27, "successful": 6, "failed": 21, "pending": 0,
        "volume": 45023.08,
        "revenue": 546.00,
        "avg_charge": 91.00,
        "avg_txn_value": 7503.85,
        "failed_value": 313918.31,
        "top_failures": "Transaction not found (14), Transaction Failed generic (3), Transaction state Cancelled (2), Customer not registered (1), JDBC Connection error (1)",
        "banks_used": 3,
        "top_bank": "Commercial Bank of Ethiopia (100% success on bank)",
        "mobile": True,
        "mobile_networks": ["Ethiotelecom (Telebirr)", "Safaricom (M-Pesa)"],
        "mobile_txns": 22, "mobile_successful": 1, "mobile_failed": 21,
        "mobile_volume": 14018.31,
        "mobile_revenue": 0.00,
        "cif_issues": 0,
        "cbo_failures": 0,
        "telebirr_failures": 21,
        "kyc_status": "Complete",
        "charges_on_failed": 1911.00,
        "notes": "CRITICAL: 77.78% failure rate — worst in portfolio. Ethiotelecom 100% failure (21/21). Bank channel: 100% success (5/5). ETB 1,911 charged on failed txns — full refund required. Likely still in onboarding/testing phase.",
    },
    {
        "code": "BAKAALEXPRESS",
        "name": "BAKAAL EXPRESS",
        "country": "Somalia",
        "period": "May 9–30, 2026",
        "full_month": False,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank",
        "total_txns": 300, "successful": 296, "failed": 4, "pending": 0,
        "volume": 4873318.00,
        "revenue": 17384.07,
        "avg_charge": 58.73,
        "avg_txn_value": 16463.91,
        "failed_value": 89920.00,
        "top_failures": "XML validation; reversed (1), Currency mismatch; reversed (1), Missing data; reversed (1), Unknown (1)",
        "banks_used": 6,
        "top_bank": "Commercial Bank of Ethiopia (91%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 0,
        "cbo_failures": 1,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 314.74,
        "notes": "Percentage-based charge model — unique in portfolio. Charges scale with transaction size (ETB 0.12–ETB 315). Solid 98.67% success rate. Bank of Abyssinia showing 12.5% failure rate (2/16) — monitor. ETB 314.74 on failed txns for refund.",
    },
    {
        "code": "MELAFINANCE",
        "name": "MELA FINANCE",
        "country": "United Kingdom",
        "period": "May 18–31, 2026",
        "full_month": False,
        "txn_types": ["DISBURSEMENTS"],
        "channel": "Bank",
        "total_txns": 60, "successful": 57, "failed": 3, "pending": 0,
        "volume": 2065210.76,
        "revenue": 6200.99,
        "avg_charge": 108.79,
        "avg_txn_value": 36231.77,
        "failed_value": 82425.00,
        "top_failures": "Failed to obtain auth token (2), No reason recorded (1)",
        "banks_used": 1,
        "top_bank": "Commercial Bank of Ethiopia (100%)",
        "mobile": False,
        "mobile_networks": [],
        "cif_issues": 0,
        "cbo_failures": 0,
        "telebirr_failures": 0,
        "kyc_status": "Complete",
        "charges_on_failed": 247.28,
        "notes": "New merchant (onboarded May 11). Percentage-based fee model. Auth token failures (2) are integration/connectivity issues. 100% CBE concentration — single point of failure risk. ETB 247.28 on failed txns for refund.",
    },
]

df = pd.DataFrame(merchants)
df["success_rate"] = (df["successful"] / df["total_txns"]) * 100
df["failure_rate"] = (df["failed"] / df["total_txns"]) * 100
df["rev_bps"] = (df["revenue"] / df["volume"].replace(0, 1)) * 10000

# ── FX DATA ──────────────────────────────────────────────────────────────────
fx_data = {
    "ETB/USD": {"date": "22 May 2026", "opening": 184.00, "closing": "Not received", "note": "Confirmed opening rate. Closing rate not submitted by Finance."},
    "KES/USD": {"date": "22 May 2026", "opening": 129.00, "closing": "Not received", "note": "Confirmed opening rate. Same rate confirmed as of 25 May."},
    "UGX/USD": {"date": "22 May 2026", "opening": 3772.00, "closing": "Not received", "note": "Confirmed opening rate only."},
}

# ── RISK SCORECARD ────────────────────────────────────────────────────────────
def compute_risk(m):
    score = 0
    # Success rate
    sr = (m["successful"] / m["total_txns"]) * 100
    if sr < 85:   score += 40
    elif sr < 95: score += 20
    elif sr < 99: score += 10
    # Revenue
    if m["revenue"] == 0: score += 30
    # Failed value
    if m["failed_value"] > 5000000: score += 25
    elif m["failed_value"] > 1000000: score += 15
    # Charges on failed
    if m["charges_on_failed"] > 10000: score += 20
    elif m["charges_on_failed"] > 0: score += 10
    # Telebirr failures
    if m["telebirr_failures"] > 10: score += 30
    # CIF issues
    if m["cif_issues"] > 15: score += 20
    elif m["cif_issues"] > 0: score += 10
    # CBO failures
    if m["cbo_failures"] > 30: score += 15
    elif m["cbo_failures"] > 0: score += 8
    # Full month
    if not m["full_month"]: score += 5

    if score >= 55:   return "High", score
    elif score >= 25: return "Medium", score
    else:             return "Low", score

for m in merchants:
    risk, score = compute_risk(m)
    m["risk_level"] = risk
    m["risk_score"] = score

df["risk_level"] = [m["risk_level"] for m in merchants]
df["risk_score"]  = [m["risk_score"]  for m in merchants]

# ── PORTFOLIO AGGREGATES (needed by header) ───────────────────────────────
total_vol    = df["volume"].sum()
total_rev    = df["revenue"].sum()
total_txns   = df["total_txns"].sum()
total_failed = df["failed"].sum()
total_fail_val = df["failed_value"].sum()
avg_sr       = df["success_rate"].mean()
total_charged_on_failed = sum(m["charges_on_failed"] for m in merchants)

# ════════════════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="header-band">
  <div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;opacity:0.7;margin-bottom:6px;color:{GOLD};">
    FINPAY TECH · INTERNAL ANALYTICS
  </div>
  <div style="font-size:28px;font-family:'DM Serif Display',serif;font-weight:400;color:white;margin-bottom:4px;">
    Monthly Merchant Performance & Risk Report
  </div>
  <div style="font-size:13px;opacity:0.85;color:white;">
    Reporting Period: May 1 – 31, 2026 &nbsp;
    |&nbsp; Active Merchants: {len(merchants)} active &nbsp;|&nbsp; Total value monitored: ETB {total_vol/1e6:.1f}M &nbsp;|&nbsp;
  Total revenue: ETB {total_rev:,.0f}
  </div>
</div>
""", unsafe_allow_html=True)




# ════════════════════════════════════════════════════════════════════════════
# PORTFOLIO KPIs
# ════════════════════════════════════════════════════════════════════════════
# Portfolio aggregates for critical flags
total_cif = sum(m["cif_issues"] for m in merchants)
total_telebirr = sum(m["telebirr_failures"] for m in merchants)

st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Total Value Moved", f"ETB {total_vol/1e6:.1f}M")
c2.metric("Total Revenue", f"ETB {total_rev:,.0f}")
c3.metric("Total Transactions", f"{total_txns:,}")
c4.metric("Total Failed", f"{total_failed:,}", delta=f"{(total_failed/total_txns*100):.1f}% of all txns", delta_color="inverse")
c5.metric("Est. Failed Value", f"ETB {total_fail_val/1e6:.1f}M")
c6.metric("Charges on Failed Txns", f"ETB {total_charged_on_failed:,.0f}", help="Requires refund review across portfolio")
st.markdown(f"""
<div class="obs-card">
  In May 2026, we processed transactions for <strong>{len(merchants)} active merchants</strong> moving a combined
  <strong>ETB {total_vol/1e6:.2f} billion</strong> across <strong>{total_txns:,} total transactions</strong>,
  generating <strong>ETB {total_rev:,.0f}</strong> in revenue.<br><br>
  Overall platform success rate was <strong>{avg_sr:.1f}%</strong>
  ({df['successful'].sum():,} successful of {total_txns:,} total),
  with <strong>FINPAY APPLICATION (EMAAL)</strong> delivering the strongest individual performance at <strong>99.85%</strong>
  and <strong>RAFIKI LTD (NALA)</strong> the weakest at <strong>22.2%</strong>.
</div>
""", unsafe_allow_html=True)
# ════════════════════════════════════════════════════════════════════════════
# CHART ROW 1 — Volume & Revenue
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Volume & Revenue Analysis</div>', unsafe_allow_html=True)

CHART_COLORS = [NAVY, GOLD, BLUE, "#2e86c1", "#117a65", "#6c3483", "#784212", "#1a5276", "#0b5345", "#4a235a"]

ch1, ch2 = st.columns(2)
with ch1:
    fig_vol = px.bar(
        df.sort_values("volume"),
        x="volume", y="name", orientation="h",
        color_discrete_sequence=[NAVY],
        title="Total Value Moved by Merchant (ETB)",
        text=df.sort_values("volume")["volume"].apply(lambda v: f"{v/1e6:.1f}M" if v > 0 else "N/A"),
    )
    fig_vol.update_traces(textposition="outside")
    fig_vol.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                          margin=dict(t=40,b=10,l=10,r=80), xaxis_title="ETB", yaxis_title="")
    st.plotly_chart(fig_vol, use_container_width=True)

with ch2:
    fig_rev = px.bar(
        df.sort_values("revenue"),
        x="name", y="revenue",
        color_discrete_sequence=[GOLD],
        title="Total Revenue Collected by Merchant (ETB)",
        text=df.sort_values("revenue")["revenue"].apply(lambda v: f"{v:,.0f}"),
    )
    fig_rev.update_traces(textposition="outside")
    fig_rev.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                          margin=dict(t=40,b=10,l=10,r=10), xaxis_title="", yaxis_title="ETB")
    fig_rev.update_xaxes(tickangle=30)
    st.plotly_chart(fig_rev, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# CHART ROW 2 — Success Rates & Revenue per Transaction
# ════════════════════════════════════════════════════════════════════════════
ch3, ch4 = st.columns(2)
with ch3:
    color_map = {"High": RED, "Medium": AMBER, "Low": GREEN}
    fig_sr = px.bar(
        df.sort_values("success_rate"),
        x="success_rate", y="name", orientation="h",
        color="risk_level",
        color_discrete_map=color_map,
        title="Success Rate by Merchant (%)",
        text=df.sort_values("success_rate")["success_rate"].apply(lambda v: f"{v:.1f}%"),
    )
    fig_sr.update_traces(textposition="outside")
    fig_sr.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                         margin=dict(t=40,b=10,l=10,r=60),
                         xaxis=dict(range=[0,105]), xaxis_title="%", yaxis_title="")
    st.plotly_chart(fig_sr, use_container_width=True)

with ch4:
    df_rev_per = df[df["revenue"] > 0].copy()
    df_rev_per["rev_per_txn"] = df_rev_per["revenue"] / df_rev_per["total_txns"]
    fig_rpt = px.scatter(
        df_rev_per,
        x="total_txns", y="rev_per_txn", size="revenue",
        color="risk_level",
        color_discrete_map=color_map,
        hover_name="name",
        title="Revenue per Transaction vs Volume",
        labels={"total_txns": "Total Transactions", "rev_per_txn": "Revenue per Txn (ETB)"},
    )
    fig_rpt.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                          margin=dict(t=40,b=10,l=10,r=10))
    st.plotly_chart(fig_rpt, use_container_width=True)
    st.caption("Bubble size = total revenue. Merchants with ETB 0 revenue excluded.")

# ════════════════════════════════════════════════════════════════════════════
# CHART ROW 3 — Revenue BPS & Avg Transaction Value
# ════════════════════════════════════════════════════════════════════════════
ch5, ch6 = st.columns(2)
with ch5:
    df_bps = df[df["rev_bps"] > 0].sort_values("rev_bps").reset_index(drop=True)
    fig_bps = go.Figure()
    fig_bps.add_trace(go.Scatter(
        x=df_bps["rev_bps"], y=df_bps["name"],
        mode="markers+text",
        marker=dict(color=GOLD, size=14, line=dict(color=NAVY, width=1.5)),
        text=df_bps["rev_bps"].apply(lambda v: f"{v:.1f} bps"),
        textposition="middle right",
        name="",
    ))
    for _, row in df_bps.iterrows():
        fig_bps.add_shape(type="line",
            x0=0, x1=row["rev_bps"], y0=row["name"], y1=row["name"],
            line=dict(color=GOLD, width=2, dash="dot"))
    fig_bps.update_layout(
        title="Revenue Earned per ETB Moved (Basis Points)",
        plot_bgcolor="white", font=dict(family="DM Sans", size=10),
        margin=dict(t=40, b=10, l=10, r=90),
        xaxis=dict(title="BPS", showgrid=True, gridcolor="#eee", zeroline=True),
        yaxis=dict(title=""),
        showlegend=False,
    )
    st.plotly_chart(fig_bps, use_container_width=True)
    st.caption(
        "I have used basis points (BPS) here because transaction volumes are very large and the revenue percentages are relatively small. "
        "Expressing performance in percentages (e.g., 0.31%) can make the figures appear insignificant, while BPS provides a clearer and more precise way to show revenue efficiency per unit processed. "
        "In this context, 1 BPS equals ETB 1 earned for every ETB 10,000 processed, making it easier to compare how effectively each merchant converts transaction volume into revenue. "
        "Merchants with ETB 0 revenue have been excluded from the analysis."
    )

with ch6:
    df_ticket = df.sort_values("avg_txn_value", ascending=False).reset_index(drop=True)
    fig_ticket = go.Figure(go.Treemap(
        labels=df_ticket["name"],
        parents=[""] * len(df_ticket),
        values=df_ticket["avg_txn_value"],
        text=df_ticket["avg_txn_value"].apply(lambda v: f"ETB {v:,.0f}"),
        textinfo="label+text",
        marker=dict(
            colors=df_ticket["avg_txn_value"],
            colorscale=[[0, "#d6e4f0"], [1, NAVY]],
            showscale=False,
        ),
    ))
    fig_ticket.update_layout(
        title="Average Transaction Value - Successful Txns (ETB)",
        font=dict(family="DM Sans", size=11),
        margin=dict(t=40, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_ticket, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# FAILURE DEEP DIVE
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Failure Analysis Deep Dive</div>', unsafe_allow_html=True)

fail_data = {
    "DEERO SERVICES":      {"BLCK/Account Blocked; reversed": 87, "XML validation failed; reversed": 63, "System Error": 7, "Currency mismatch": 2},
    "REMITLY GLOBAL":      {"Creditor Agent error; reversed": 57, "System Error": 52, "Transaction not found": 33, "Insufficient balance": 32, "CIF harmonization block": 22, "Unknown error": 16},
    "RED SEA DIRECT DEPOSITS": {"Insufficient balance": 63, "Unknown error": 42, "System Error": 28, "CIF harmonization block": 26, "Missing data; reversed": 4},
    "JUBA EXPRESS":        {"System Error": 24, "Insufficient balance": 24, "XML validation failed": 21, "CIF harmonization block": 21, "Unknown error": 12},
    "RAFIKI (NALA)":       {"Transaction not found": 14, "Transaction Failed": 3, "State Cancelled": 2, "Customer not registered": 1, "JDBC Error": 1},
    "FINPAY APP (EMAAL)":  {"Transaction Failed": 3, "Missing data": 1, "ERRR reversed": 1, "Insufficient balance": 1, "CreditParty invalid": 1},
    "BAKAAL EXPRESS":      {"XML validation": 1, "Currency mismatch": 1, "Missing data": 1, "Unknown": 1},
    "MELA FINANCE":        {"Auth token failure": 2, "No reason recorded": 1},
    "BIRR LINK":           {"Exception on bank transfer": 1, "Insufficient balance": 1},
    "RED SEA":             {"XML validation; reversed": 2, "Missing data; reversed": 2},
}

fail_rows = []
for merchant, reasons in fail_data.items():
    for reason, count in reasons.items():
        fail_rows.append({"Merchant": merchant, "Reason": reason, "Count": count})
fail_df = pd.DataFrame(fail_rows)

fig_fd = px.bar(
    fail_df, x="Count", y="Reason", color="Merchant", orientation="h",
    color_discrete_sequence=CHART_COLORS,
    title="Failure Reasons Across All Merchants — May 2026",
    text="Count",
)
fig_fd.update_traces(textposition="outside")
fig_fd.update_layout(
    plot_bgcolor="white", font=dict(family="DM Sans", size=10),
    margin=dict(t=40,b=10,l=10,r=10), height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_fd, use_container_width=True)

# CIF + Telebirr summary
col_a, col_b = st.columns(2)
with col_a:
    cif_data = {m["name"]: m["cif_issues"] for m in merchants if m["cif_issues"] > 0}
    fig_cif = px.bar(
        x=list(cif_data.keys()), y=list(cif_data.values()),
        color_discrete_sequence=[RED],
        title="Customers Blocked (CBE data mismatch) by Merchant",
        text=list(cif_data.values()),
    )
    fig_cif.update_traces(textposition="outside")
    fig_cif.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                          xaxis_title="", yaxis_title="Customers", margin=dict(t=40,b=10,l=10,r=10))
    st.plotly_chart(fig_cif, use_container_width=True)
    st.caption(f"Total {sum(m['cif_issues'] for m in merchants)} customers blocked because their info doesn't match CBE's system. CBE contact needed.")

with col_b:
    tel_data = {m["name"]: m["telebirr_failures"] for m in merchants if m["telebirr_failures"] > 0}
    fig_tel = px.bar(
        x=list(tel_data.keys()), y=list(tel_data.values()),
        color_discrete_sequence=[AMBER],
        title="Ethiotelecom/Telebirr Failures by Merchant (100% failure rate)",
        text=list(tel_data.values()),
    )
    fig_tel.update_traces(textposition="outside")
    fig_tel.update_layout(plot_bgcolor="white", font=dict(family="DM Sans", size=10),
                          xaxis_title="", yaxis_title="Failed Txns", margin=dict(t=40,b=10,l=10,r=10))
    st.plotly_chart(fig_tel, use_container_width=True)
    st.caption("Telebirr integration is completely non-functional. Must be suspended platform-wide until resolved.")

# ════════════════════════════════════════════════════════════════════════════
# FX SECTION
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">FX Rate Monitoring</div>', unsafe_allow_html=True)

fx_cols = st.columns(3)
fx_items = [
    ("ETB/USD", "184.00", "Not received", "22 May 2026", "Ethiopian Birr — primary transaction currency. Historically volatile. Confirmed opening rate only."),
    ("KES/USD", "129.00", "Not received", "22 May 2026", "Kenyan Shilling. Confirmed opening rate; same as of 25 May 2026 per Finance team."),
    ("UGX/USD", "3,772.00", "Not received", "22 May 2026", "Ugandan Shilling. Opening rate confirmed only."),
]
for col, (pair, opening, closing, date, note) in zip(fx_cols, fx_items):
    col.markdown(f"""
    <div class="scorecard">
      <div style="font-size:11px;color:{GOLD};font-weight:600;letter-spacing:1px;">{pair}</div>
      <div style="font-size:20px;font-weight:600;color:{NAVY};margin:4px 0;">{opening}</div>
      <div style="font-size:11px;color:#888;">Opening Rate · {date}</div>
      <div style="font-size:11px;color:{RED};margin-top:4px;">Closing: {closing}</div>
      <div style="font-size:11px;color:#666;margin-top:6px;">{note}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# PER-MERCHANT EXPANDERS
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Per-Merchant Detail</div>', unsafe_allow_html=True)

risk_badge = {"High": "badge-high", "Medium": "badge-med", "Low": "badge-low"}

for m in merchants:
    sr = (m["successful"] / m["total_txns"]) * 100
    badge = risk_badge[m["risk_level"]]
    with st.expander(f"{m['name']}  ·  {m['channel']}  ·  {sr:.1f}% success  ·  {m['period']}"):
        d1,d2,d3,d4,d5 = st.columns(5)
        d1.metric("Total Transactions", f"{m['total_txns']:,}")
        d2.metric("Successful", f"{m['successful']:,}")
        d3.metric("Failed", f"{m['failed']:,}")
        d4.metric("Value Moved (ETB)", f"{m['volume']/1e6:.1f}M")
        d5.metric("Revenue (ETB)", f"{m['revenue']:,.0f}")

        d6,d7,d8,d9 = st.columns(4)
        d6.metric("Avg Charge", f"ETB {m['avg_charge']:,.2f}")
        d7.metric("Avg Txn Value", f"ETB {m['avg_txn_value']:,.0f}")
        d8.metric("Est. Failed Value", f"ETB {m['failed_value']:,.0f}")
        d9.metric("Charges on Failed", f"ETB {m['charges_on_failed']:,.0f}" if m['charges_on_failed'] > 0 else "—")

        st.markdown(f"**Country:** {m['country']} &nbsp;|&nbsp; **Channel:** {m['channel']} &nbsp;|&nbsp; **Transaction Types:** {', '.join(m['txn_types'])} &nbsp;|&nbsp; **Banks Used:** {m['banks_used']} &nbsp;|&nbsp; **Top Bank:** {m['top_bank']}")
        if m["mobile"]:
            st.markdown(f"**Mobile Networks:** {', '.join(m['mobile_networks'])} &nbsp;|&nbsp; **Mobile Txns:** {m.get('mobile_txns',0)} &nbsp;|&nbsp; **Mobile Value:** ETB {m.get('mobile_volume',0):,.0f} &nbsp;|&nbsp; **Mobile Revenue:** ETB {m.get('mobile_revenue',0):,.0f}")
        if m["cif_issues"] > 0:
            st.warning(f"⚠️ {m['cif_issues']} customers blocked: their details on file don't match what CBE has. Needs to be raised with CBE to unblock.")
        if m["telebirr_failures"] > 0:
            st.error(f"🚨 Telebirr/Ethiotelecom: {m['telebirr_failures']} failures — 100% failure rate on this channel")
        st.markdown(f"**Top Failure Reasons:** {m['top_failures']}")
        st.info(m["notes"])

# ════════════════════════════════════════════════════════════════════════════
# RISK SCORECARD
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Monthly Merchant Risk Scorecard</div>', unsafe_allow_html=True)
st.caption("Each merchant scored across 6 dimensions: Transaction Volume, Revenue, Failure/Reversal Performance, FX Exposure, KYC Compliance, and Overall Risk.")

score_data = []
for m in merchants:
    sr = (m["successful"] / m["total_txns"]) * 100
    score_data.append({
        "Merchant": m["name"],
        "Volume Score": "🟢 High" if m["volume"] > 100e6 else ("🟡 Med" if m["volume"] > 10e6 else "🔴 Low"),
        "Revenue": "🚨 Zero" if m["revenue"] == 0 else ("🟢 Strong" if m["revenue"] > 500000 else "🟡 Moderate"),
        "Success Rate": f"{sr:.1f}%",
        "Failure Risk": "🔴 High" if sr < 85 else ("🟡 Med" if sr < 97 else "🟢 Low"),
        "FX Exposure": "🟡 Medium" if m["channel"] in ["Bank", "Bank + Mobile"] else "🟢 Low",
        "KYC Status": "🟢 Complete",
        "Charges on Failed": f"ETB {m['charges_on_failed']:,.0f}" if m["charges_on_failed"] > 0 else "—",
        "Overall Risk": m["risk_level"],
    })

score_df = pd.DataFrame(score_data)

def color_risk(val):
    if val == "High":   return f"background-color:{RED};color:white;font-weight:bold"
    if val == "Medium": return f"background-color:{AMBER};color:white;font-weight:bold"
    if val == "Low":    return f"background-color:{GREEN};color:white;font-weight:bold"
    return ""

styled = score_df.style.applymap(color_risk, subset=["Overall Risk"])
st.dataframe(styled, use_container_width=True, height=380)

risk_col1, risk_col2 = st.columns(2)
with risk_col1:
    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]
    fig_risk = px.pie(risk_counts, names="Risk Level", values="Count",
                      color="Risk Level",
                      color_discrete_map={"High": RED, "Medium": AMBER, "Low": GREEN},
                      title="Portfolio Risk Distribution",
                      hole=0.4)
    fig_risk.update_layout(font=dict(family="DM Sans", size=11), margin=dict(t=40,b=10,l=10,r=10))
    st.plotly_chart(fig_risk, use_container_width=True)

with risk_col2:
    heat_merchants = [m["name"] for m in merchants]
    heat_metrics = ["Success Rate", "Revenue (ETB)", "Volume (ETB)", "Avg Txn Value", "Charges on Failed"]
    sr_vals      = [round((m["successful"]/m["total_txns"])*100, 1) for m in merchants]
    rev_vals     = [m["revenue"] for m in merchants]
    vol_vals     = [m["volume"] for m in merchants]
    txn_vals     = [m["avg_txn_value"] for m in merchants]
    fail_vals    = [m["charges_on_failed"] for m in merchants]

    def norm(lst):
        mx = max(lst) if max(lst) > 0 else 1
        return [round(v / mx, 3) for v in lst]

    heat_z = [
        norm(sr_vals),
        norm(rev_vals),
        norm(vol_vals),
        norm(txn_vals),
        [round(1 - v, 3) for v in norm(fail_vals)],
    ]

    fig_heat = go.Figure(go.Heatmap(
        z=heat_z,
        x=heat_merchants,
        y=heat_metrics,
        colorscale=[[0, "#fdf0f0"], [0.5, GOLD], [1, NAVY]],
        text=[
            [f"{sr_vals[i]:.1f}%" for i in range(len(merchants))],
            [f"ETB {rev_vals[i]:,.0f}" for i in range(len(merchants))],
            [f"ETB {vol_vals[i]/1e6:.1f}M" for i in range(len(merchants))],
            [f"ETB {txn_vals[i]:,.0f}" for i in range(len(merchants))],
            [f"ETB {fail_vals[i]:,.0f}" for i in range(len(merchants))],
        ],
        texttemplate="%{text}",
        textfont=dict(size=9),
        showscale=False,
    ))
    fig_heat.update_layout(
        title="Merchant Performance Heatmap",
        font=dict(family="DM Sans", size=10),
        margin=dict(t=40, b=10, l=130, r=10),
        xaxis=dict(tickangle=30),
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Each row is normalized relative to the top performer in that category. Darker = stronger. Charges on Failed is inverted so darker = fewer charges (better).")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# AUDIT TABLE
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Comprehensive Monthly Audit Trail</div>', unsafe_allow_html=True)

audit_df = df[[
    "name","channel","risk_level","total_txns","successful","failed","pending",
    "volume","revenue","avg_charge","avg_txn_value","success_rate","failed_value"
]].copy()
audit_df.columns = [
    "Merchant","Channel","Risk","Total Txns","Successful","Failed","Pending",
    "Volume (ETB)","Revenue (ETB)","Avg Charge","Avg Txn Value","Success Rate %","Est Failed Value"
]

st.dataframe(
    audit_df.style
    .format({
        "Volume (ETB)":     "{:,.0f}",
        "Revenue (ETB)":    "{:,.0f}",
        "Avg Charge":       "{:,.2f}",
        "Avg Txn Value":    "{:,.0f}",
        "Success Rate %":   "{:.2f}%",
        "Est Failed Value": "{:,.0f}",
    })
    .applymap(lambda v: f"background-color:{RED};color:white" if isinstance(v,str) and v=="High"
              else (f"background-color:{AMBER}" if isinstance(v,str) and v=="Medium"
              else (f"background-color:{GREEN};color:white" if isinstance(v,str) and v=="Low" else "")),
              subset=["Risk"])
    .bar(subset=["Success Rate %"], color=["#c0392b","#1e8449"], vmin=0, vmax=100)
    .bar(subset=["Volume (ETB)"], color="#d6e4f0"),
    use_container_width=True, height=380,
)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# CRITICAL FLAGS & ACTIONS
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Key Observations & Actions Required</div>', unsafe_allow_html=True)

critical_items = [
    ("Telebirr channel has 100% failure across REMITLY (42 txns) and RAFIKI (21 txns). ETB 661K blocked. Urgent technical resolution needed.",
     f"{total_telebirr} transactions blocked. Integration broken at API level."),
    (f"{total_cif} customers blocked across 3 merchants because their info doesn't match CBE's system. Need to contact CBE to unblock them.",
     "Affects RED SEA DIRECT DEPOSITS (26), JUBA EXPRESS (21), REMITLY GLOBAL (22). Compile account list and raise with CBE relationship manager."),
    ("DEEROSERVICES has been failing 1 in every 6 transactions for at least 4 months in a row. Every single failure is coming from their Kaafi MFI and Cooperative Bank of Oromia connections.",
     "159 failures (16.65%). Reroute from Kaafi MFI and Cooperative Bank of Oromia immediately. ETB 14,469 charged on failed txns needs refund."),
    ("BIRRLINK zero revenue for 4th consecutive period. ETB 0 on all transactions.",
     "52 transactions processed at zero revenue."),
    ("RAFIKI/NALA 77.78% failure rate. Integration not production ready. ETB 1,911 charged on failed transactions.",
     "21 of 27 transactions failed. Telebirr channel 100% failure. Bank channel 100% success. Still in testing phase."),
]

for headline, detail in critical_items:
    st.markdown(f"""
    <div class="crit-card">
      <strong>🔴 CRITICAL:</strong> {headline}<br>
      <span style="font-size:12px;color:#666;">{detail}</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown('<div class="section-title">Strenghts</div>', unsafe_allow_html=True)

positive_obs = [
    ("🟢 FINPAYAPPLICATION (EMAAL) & JUBAEXPRESS Lead Performance",
     "FINPAYAPPLICATION delivered highest total value (ETB 358M), best success rate (99.85%), and highest avg transaction value (ETB 75,458) with only 7 failures across 4,756 transactions. "
     "JUBAEXPRESS leads on transaction count (8,042) and revenue (ETB 1,008,230). Both merchants show clean operations with broad bank diversification. "
     "FINPAYAPPLICATION is the only major merchant with zero blocked customers, understanding why could help protect other merchants."),
    ("🟢 New Merchants BAKAALEXPRESS & MELAFINANCE Performing Well",
     "Both new merchants show strong early performance: BAKAALEXPRESS at 98.67% success (300 txns), MELAFINANCE at 95% (60 txns in first 2 weeks). "
     "Both use percentage based fee models. MELAFINANCE's auth token failures (2 cases) should be resolved quickly."),
]

for title, body in positive_obs:
    st.markdown(f'<div class="obs-card"><strong>{title}</strong><br><br>{body}</div>', unsafe_allow_html=True)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:{NAVY};color:white;padding:20px 28px;border-radius:8px;margin-top:20px;font-size:12px;opacity:0.9;">
  <strong style="font-family:'DM Serif Display',serif;font-size:16px;">FinPay Tech · Monthly Report · May 2026</strong><br>
  <span style="opacity:0.6;font-size:10px;">
  FX data gap: Finance submitted 22 May opening rates only. Daily FX tracking Excel established for June onwards.
  Data source: FinPay transaction portal exports. Analysis by Gladys W.
  </span>
</div>
""", unsafe_allow_html=True)

# streamlit run app.py

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
# st.sidebar.markdown("### FinPay Analytics")
# st.sidebar.markdown("**Cycle:** Apr 27 to May 3, 2026")
# st.sidebar.markdown(f"**Merchants:** {len(df)}")
# st.sidebar.markdown(f"**Total Volume (Excl. REMITLY):** ETB {volume_excl_remitly/1e6:.2f}M")
# st.sidebar.markdown(f"**Total Revenue:** ETB {df['Revenue'].sum():,.2f}")
# st.sidebar.divider()
# st.sidebar.markdown("⚠ **REMITLYGLOBAL** volume = 0 due to data tag issue in source dataset. See report for details.")
# st.sidebar.divider()

# if st.sidebar.button("Download Strategic PDF"):
#     try:
#         pdf_bytes = generate_pdf(
#             df, df_prev,
#             fig_vol, fig_rev, fig_sr, fig_fail,
#             fig_margin, fig_ticket,
#             fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail
#         )
#         if isinstance(pdf_bytes, str):
#             pdf_bytes = pdf_bytes.encode("latin-1")
#         b64 = base64.b64encode(pdf_bytes).decode()
#         href = (
#             f'<a href="data:application/octet-stream;base64,{b64}" '
#             f'download="Merchant360_Apr27_May3_2026.pdf" '
#             f'style="text-decoration:none; color:white; background:{MAIN_COLOR}; '
#             f'padding:12px 16px; border-radius:5px; display:inline-block; font-size:13px;">'
#             f'Save PDF Report</a>'
#         )
#         st.sidebar.markdown(href, unsafe_allow_html=True)
#     except Exception as e:
#         st.sidebar.error(f"PDF error: {e}")

# st.sidebar.divider()
# st.sidebar.markdown("**Risk Legend**")
# st.sidebar.markdown("🔴 Red; Revenue or failure anomaly")
# st.sidebar.markdown("🟡 Yellow; Elevated failure rate")
# st.sidebar.markdown("🟢 Green; Normal operating range")

# streamlit run app.py


# streamlit run app.py
# .\venv\Scripts\activate