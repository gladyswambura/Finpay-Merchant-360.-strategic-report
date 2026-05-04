import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import base64
import io
import datetime

# ── BRANDING ──────────────────────────────────────────────────────────────────
MAIN_COLOR = "#081b31"
GOLD_COLOR = "#8e6d2d"
LIGHT_BG   = "#f5f3ef"


def safe(text):
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "*", "\u26a0": "!",
        "\u2705": "[OK]", "\u274c": "[X]", "\u2714": "[v]",
    }
    for k, v in replacements.items():
        text = str(text).replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

MAIN_RGB = hex_to_rgb(MAIN_COLOR)
GOLD_RGB = hex_to_rgb(GOLD_COLOR)


st.set_page_config(page_title="Merchant 360 | Weekly Strategic Report", layout="wide")

st.markdown(f"""
<style>
.main {{ background-color: {LIGHT_BG}; }}
[data-testid="stMetricValue"] {{ font-size: 22px; color: {MAIN_COLOR}; font-weight: bold; }}
[data-testid="stMetricLabel"] {{ font-size: 13px; color: #555; }}
h1, h2 {{ color: {MAIN_COLOR} !important; }}
h3 {{ color: {MAIN_COLOR} !important; font-size: 16px !important; font-weight: bold; margin-bottom: 2px; }}
.observation-box {{
    background-color: #ffffff; padding: 12px 14px;
    border-left: 4px solid {GOLD_COLOR};
    font-size: 12px; color: #333;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 14px; border-radius: 0 6px 6px 0;
}}
.flag-box {{
    background-color: #fdf6e3; padding: 10px 14px;
    border-left: 4px solid {GOLD_COLOR};
    font-size: 12px; color: #555;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 10px; border-radius: 0 6px 6px 0;
}}
.header-band {{
    background: linear-gradient(90deg, {MAIN_COLOR} 0%, #0d2d52 100%);
    padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;
    color: white;
}}
.wow-up   {{ color: #1e8449; font-weight: bold; }}
.wow-down {{ color: #c0392b; font-weight: bold; }}
.wow-flat {{ color: #888;    font-weight: normal; }}
.compare-header {{
    background: linear-gradient(90deg, {GOLD_COLOR} 0%, #b8960e 100%);
    padding: 14px 24px; border-radius: 8px; margin-bottom: 16px; color: white;
}}
.chart-note {{
    font-size: 11px; color: #666; font-style: italic;
    margin-top: -10px; margin-bottom: 10px; padding-left: 4px;
}}
.data-note {{
    background-color: #fff8e1; padding: 10px 14px;
    border-left: 4px solid #f39c12;
    font-size: 12px; color: #555;
    margin-bottom: 14px; border-radius: 0 6px 6px 0;
}}
</style>
""", unsafe_allow_html=True)


# ── THIS WEEK DATA (Apr 27 – May 3, 2026) ─────────────────────────────────────
def load_current():
    records = [
        {
            "Merchant":       "REDSEA",
            "TxnTypes":       "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 01 May 2026",
            "Volume":         40_970_043.00,
            "Revenue":        97_700.43,
            "Successful":     46,
            "Failed":         0,
            "Pending":        0,
            "Avg_Charge":     2_123.92,
            "Avg_Txn_Value":  890_653.11,
            "Risk":           "Low",
            "Top_Failures":   "None",
            "Notes":          "100% success rate across all 46 transactions. No pending or failed records. All processed through bank channels. Revenue of ETB 97,700.43 collected.",
        },
        {
            "Merchant":       "REDSEADIRECTDEPOSITS",
            "TxnTypes":       "DIRECT_DEPOSIT, ACCOUNT_CREDIT",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 02 May 2026",
            "Volume":         52_884_310.00,
            "Revenue":        126_184.31,
            "Successful":     115,
            "Failed":         3,
            "Pending":        1,
            "Avg_Charge":     1_090.57,
            "Avg_Txn_Value":  456_761.12,
            "Risk":           "Low",
            "Top_Failures":   "Account Not Found (2), Insufficient Balance (1)",
            "Notes":          "115 successful transactions used for value and revenue calculations. 3 failures and 1 pending noted. Failure rate ~2.5% (3/118); within acceptable range.",
        },
        {
            "Merchant":       "JUBAEXPRESS",
            "TxnTypes":       "DISBURSEMENTS",
            "Channel":        "Bank",
            "DateRange":      "01 May – 03 May 2026",
            "Volume":         53_305_536.00,
            "Revenue":        213_227.96,
            "Successful":     1_713,
            "Failed":         42,
            "Pending":        0,
            "Avg_Charge":     124.48,
            "Avg_Txn_Value":  31_118.23,
            "Risk":           "Medium",
            "Top_Failures":   "Insufficient balance (19), System Error (9), Unknown error (8), XML validation failed reversed (2), Creditor Agent error reversed (2)",
            "Notes":          "1,755 total transactions. Failure rate ~2.4% (42/1755). Top failure is insufficient balance; may indicate funding gaps. System errors (9) also need investigation.",
        },
        {
            "Merchant":       "FINPAYAPPLICATION",
            "TxnTypes":       "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 03 May 2026",
            "Volume":         55_973_997.51,
            "Revenue":        74_893.00,
            "Successful":     826,
            "Failed":         2,
            "Pending":        0,
            "Avg_Charge":     90.67,
            "Avg_Txn_Value":  67_765.13,
            "Risk":           "Low",
            "Top_Failures":   "Insufficient balance (1), XML validation failed reversed (1)",
            "Notes":          "828 total transactions. Failure rate extremely low (0.24%). Charges are very consistent (~91 ETB); near-flat fee structure. Operationally strong week.",
        },
        {
            "Merchant":       "BIRRLINK",
            "TxnTypes":       "DISBURSEMENTS",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 03 May 2026",
            "Volume":         641_020.50,
            "Revenue":        0.00,
            "Successful":     20,
            "Failed":         1,
            "Pending":        0,
            "Avg_Charge":     0.00,
            "Avg_Txn_Value":  32_051.03,
            "Risk":           "High",
            "Top_Failures":   "Insufficient balance (1)",
            "Notes":          "Zero revenue recorded again; likely zero-fee or absorbed-cost arrangement. Failure rate 4.76% (1/21). Fee arrangement still unconfirmed; documentation urgently needed.",
        },
        {
            "Merchant":       "DEEROSERVICES",
            "TxnTypes":       "DISBURSEMENTS",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 03 May 2026",
            "Volume":         40_875_745.00,
            "Revenue":        88_179.00,
            "Successful":     853,
            "Failed":         116,
            "Pending":        0,
            "Avg_Charge":     91.00,  # flat fee
            "Avg_Txn_Value":  47_919.98,
            "Risk":           "High",
            "Top_Failures":   "BLCK reversed (58), XML validation failed reversed (45), System Error (7), Currency mismatch (5), Missing reversed (1)",
            "Notes":          "CRITICAL: 969 total transactions. Failure rate ~12% (116/969); significantly above acceptable thresholds. Main issue cluster: reversals + validation errors. Escalation required immediately.",
        },
        {
            "Merchant":       "REMITLYGLOBAL",
            "TxnTypes":       "DISBURSEMENTS",
            "Channel":        "Bank",
            "DateRange":      "27 Apr – 03 May 2026",
            "Volume":         0.00,   # data quality issue; no 'successful' tag found
            "Revenue":        0.00,
            "Successful":     2_735,  # 2834 - 99 failed
            "Failed":         99,
            "Pending":        0,
            "Avg_Charge":     0.00,
            "Avg_Txn_Value":  0.00,
            "Risk":           "Medium",
            "Top_Failures":   "System Error (35), Insufficient balance (31), Creditor Agent error reversed (18), Unknown error (9), Failed to obtain auth token (3)",
            "Notes":          "DATA QUALITY FLAG: No transactions tagged 'successful' in dataset; volume and avg transaction value show 0. Actual volume cannot be confirmed. 2,834 total transactions; 99 failed (3.5% failure rate). Zero charges; international remittance model confirmed. Recommend data pipeline review.",
        },
    ]
    df = pd.DataFrame(records)
    df["Total_Txns"]       = df["Successful"] + df["Failed"] + df["Pending"]
    df["Success_Rate"]     = (df["Successful"] / df["Total_Txns"].replace(0, 1)) * 100
    df["Est_Failed_Value"] = df["Failed"] * df["Avg_Txn_Value"]
    df["Rev_Margin_BPS"]   = (df["Revenue"] / df["Volume"].replace(0, 1)) * 10_000
    return df


# ── PRIOR WEEK DATA (Apr 20–26, 2026) ─────────────────────────────────────────
def load_prior():
    records = [
        {"Merchant": "REDSEA",               "Volume": 41_981_936.00, "Revenue": 49_819.36,   "Successful": 27,    "Failed": 0,   "Total_Txns": 27,   "Avg_Txn_Value": 1_554_886.52, "Success_Rate": 100.0},
        {"Merchant": "REDSEADIRECTDEPOSITS",  "Volume": 45_195_396.45, "Revenue": 451_954.15,  "Successful": 1_000, "Failed": 3,   "Total_Txns": 1_003,"Avg_Txn_Value": 45_195.40,    "Success_Rate": 99.70},
        {"Merchant": "JUBAEXPRESS",           "Volume": 46_886_467.00, "Revenue": 187_550.80,  "Successful": 1_460, "Failed": 3,   "Total_Txns": 1_463,"Avg_Txn_Value": 32_114.02,    "Success_Rate": 99.79},
        {"Merchant": "FINPAYAPPLICATION",     "Volume": 28_026_347.40, "Revenue": 60_879.00,   "Successful": 670,   "Failed": 1,   "Total_Txns": 671,  "Avg_Txn_Value": 41_830.37,    "Success_Rate": 99.85},
        {"Merchant": "BIRRLINK",              "Volume": 615_078.00,    "Revenue": 0.00,          "Successful": 24,    "Failed": 0,   "Total_Txns": 24,   "Avg_Txn_Value": 25_628.25,    "Success_Rate": 100.0},
        {"Merchant": "DEEROSERVICES",         "Volume": 23_453_278.00, "Revenue": 56_966.00,   "Successful": 626,   "Failed": 154, "Total_Txns": 780,  "Avg_Txn_Value": 37_465.30,    "Success_Rate": 80.26},
        {"Merchant": "REMITLYGLOBAL",         "Volume": 71_061_908.98, "Revenue": 0.00,          "Successful": 2_322, "Failed": 13,  "Total_Txns": 2_335,"Avg_Txn_Value": 30_603.75,    "Success_Rate": 99.44},
    ]
    return pd.DataFrame(records)


df      = load_current()
df_prev = load_prior()


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-band">
  <span style="font-size:22px; font-weight:700; letter-spacing:1px; color:white;">
    MERCHANT 360 &nbsp;|&nbsp; WEEKLY STRATEGIC REPORT
  </span><br>
  <span style="font-size:13px; opacity:0.85; color:white;">
    Analytics Cycle: April 27 to May 3, 2026 &nbsp;&middot;&nbsp;
    7 Merchants &nbsp;&middot;&nbsp; Ethiopia (ETB)
  </span>
</div>
""", unsafe_allow_html=True)



# ── TOP KPIs ──────────────────────────────────────────────────────────────────
# Exclude REMITLYGLOBAL from volume total due to data quality issue
volume_excl_remitly = df[df["Merchant"] != "REMITLYGLOBAL"]["Volume"].sum()
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Weekly Revenue",           f"ETB {df['Revenue'].sum():,.2f}")
k2.metric("Total Money Moved (Excl. REMITLY)", f"ETB {volume_excl_remitly:,.2f}",
          help="REMITLYGLOBAL excluded due to data quality issue (no successful transaction tags found). Volume = 0 for that merchant.")
k3.metric("Total Transactions",             f"{df['Total_Txns'].sum():,}")
k4.metric("Average Success Rate",           f"{df['Success_Rate'].mean():.2f}%")
k5.metric(
    "Est. Value in Failed Transactions",
    f"ETB {df['Est_Failed_Value'].sum():,.2f}",
    help="Failed count × Average Transaction Value. REMITLYGLOBAL not included (avg txn value = 0 due to data issue).",
)

st.divider()

# ── CHART ROW 1: Volume + Revenue ─────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    df_vol = df.copy()
    fig_vol = px.bar(
        df_vol.sort_values("Volume"),
        x="Volume", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Total Money Moved by Merchant (ETB); REMITLY = 0 due to data issue",
        text=df_vol.sort_values("Volume")["Volume"].apply(
            lambda v: f"{v/1e6:.1f}M" if v > 0 else "Data N/A"
        ),
    )
    fig_vol.update_traces(textposition="outside")
    fig_vol.update_layout(plot_bgcolor="white", font=dict(size=10),
                          margin=dict(t=50, b=10, l=10, r=90), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_vol, use_container_width=True)

with c2:
    fig_rev = px.bar(
        df.sort_values("Revenue"),
        x="Merchant", y="Revenue",
        color_discrete_sequence=[GOLD_COLOR],
        title="Total Revenue / Charges Collected (ETB)",
        text=df.sort_values("Revenue")["Revenue"].apply(lambda v: f"{v:,.0f}"),
    )
    fig_rev.update_traces(textposition="outside")
    fig_rev.update_layout(plot_bgcolor="white", font=dict(size=10),
                          margin=dict(t=40, b=10, l=10, r=10), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_rev, use_container_width=True)

# ── CHART ROW 2: Success Rate Donut + Failed bar ──────────────────────────────
c3, c4 = st.columns(2)

with c3:
    pie_colors = [MAIN_COLOR, GOLD_COLOR, "#1a5276", "#b8860b", "#2e86c1", "#c0a060", "#0d2d52"]
    fig_sr = px.pie(
        df,
        names="Merchant",
        values="Success_Rate",
        title="Success Rate by Merchant (%)",
        color_discrete_sequence=pie_colors,
        hole=0.35,
    )
    fig_sr.update_traces(
        textinfo="label+percent",
        texttemplate="<b>%{label}</b><br>%{customdata:.1f}%",
        customdata=df["Success_Rate"],
        hovertemplate="<b>%{label}</b><br>Success Rate: %{customdata:.2f}%<extra></extra>",
    )
    fig_sr.update_layout(
        plot_bgcolor="white", font=dict(size=10),
        margin=dict(t=40, b=10, l=10, r=10), showlegend=True,
    )
    st.plotly_chart(fig_sr, use_container_width=True)

with c4:
    fig_fail = px.bar(
        df.sort_values("Failed", ascending=False),
        x="Merchant", y="Failed", color="Risk",
        color_discrete_map={"High": "#c0392b", "Medium": "#d4ac0d", "Low": "#1e8449"},
        title="Number of Failed Transactions by Merchant",
        text="Failed",
    )
    fig_fail.update_traces(textposition="outside")
    fig_fail.update_layout(plot_bgcolor="white", font=dict(size=10),
                           margin=dict(t=40, b=10, l=10, r=10),
                           xaxis_title="", yaxis_title="Number of Failed Transactions")
    st.plotly_chart(fig_fail, use_container_width=True)

# ── CHART ROW 3: Revenue Margin + Avg Transaction Value ───────────────────────
c5, c6 = st.columns(2)

with c5:
    fig_margin = px.bar(
        df.sort_values("Rev_Margin_BPS"),
        x="Rev_Margin_BPS", y="Merchant", orientation="h",
        color_discrete_sequence=[GOLD_COLOR],
        title="Revenue Earned per ETB Moved (Basis Points)",
        text=df.sort_values("Rev_Margin_BPS")["Rev_Margin_BPS"].apply(lambda v: f"{v:.1f} bps"),
    )
    fig_margin.update_traces(textposition="outside")
    fig_margin.update_layout(plot_bgcolor="white", font=dict(size=10),
                             margin=dict(t=40, b=10, l=10, r=90),
                             xaxis_title="Basis Points (BPS)", yaxis_title="")
    st.plotly_chart(fig_margin, use_container_width=True)
    st.markdown(
        '<p class="chart-note">'
        '<b>1 BPS = 0.01%.</b> Revenue ÷ Volume × 10,000. '
        'Higher BPS = more revenue earned per ETB moved. '
        'REDSEA leads this week at ~23.8 BPS (ETB 97,700 on ETB 40.97M).'
        '</p>',
        unsafe_allow_html=True,
    )

with c6:
    fig_ticket = px.bar(
        df.sort_values("Avg_Txn_Value"),
        x="Avg_Txn_Value", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Average Transaction Value by Merchant (ETB)",
        text=df.sort_values("Avg_Txn_Value")["Avg_Txn_Value"].apply(
            lambda v: f"{v:,.0f}" if v > 0 else "Data N/A"
        ),
    )
    fig_ticket.update_traces(textposition="outside")
    fig_ticket.update_layout(plot_bgcolor="white", font=dict(size=10),
                             margin=dict(t=40, b=10, l=10, r=90),
                             xaxis_title="ETB", yaxis_title="")
    st.plotly_chart(fig_ticket, use_container_width=True)
    st.markdown(
        '<p class="chart-note">'
        '<b>Average Transaction Value</b> = Total money moved ÷ Number of successful transactions. '
        'REMITLYGLOBAL shows 0 due to data quality issue (no successful tag in dataset).'
        '</p>',
        unsafe_allow_html=True,
    )

st.divider()

# ── FAILURE BREAKDOWN CHART ───────────────────────────────────────────────────
st.markdown("#### Top Failure Reasons")

failure_data = {
    "DEEROSERVICES":      {"BLCK / reversed": 58, "XML validation failed": 45, "System Error": 7, "Currency mismatch": 5, "Missing / reversed": 1},
    "JUBAEXPRESS":        {"Insufficient balance": 19, "System Error": 9, "Unknown error": 8, "XML validation failed": 2, "Creditor Agent error": 2},
    "REMITLYGLOBAL":      {"System Error": 35, "Insufficient balance": 31, "Creditor Agent error": 18, "Unknown error": 9, "Auth token failure": 3},
    "REDSEADIRECTDEPOSITS": {"Account Not Found": 2, "Insufficient Balance": 1},
    "FINPAYAPPLICATION":  {"Insufficient balance": 1, "XML validation failed": 1},
    "BIRRLINK":           {"Insufficient balance": 1},
    "REDSEA":             {},
}

fail_rows = []
for merchant, reasons in failure_data.items():
    for reason, count in reasons.items():
        fail_rows.append({"Merchant": merchant, "Reason": reason, "Count": count})

fail_df = pd.DataFrame(fail_rows)

if not fail_df.empty:
    fig_fail_detail = px.bar(
        fail_df,
        x="Count", y="Reason", color="Merchant",
        orientation="h",
        color_discrete_sequence=[MAIN_COLOR, GOLD_COLOR, "#1a5276", "#b8860b", "#2e86c1", "#c0a060", "#0d2d52"],
        title="Failure Reasons Across All Merchants; Count of Occurrences",
        text="Count",
    )
    fig_fail_detail.update_traces(textposition="outside")
    fig_fail_detail.update_layout(
        plot_bgcolor="white", font=dict(size=10),
        margin=dict(t=40, b=10, l=10, r=10),
        xaxis_title="Count", yaxis_title="",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_fail_detail, use_container_width=True)

st.divider()

# ── AUDIT TABLE ───────────────────────────────────────────────────────────────
st.markdown("#### Comprehensive Weekly Audit Trail")

audit_df = df[[
    "Merchant", "Channel", "Risk", "Total_Txns", "Successful", "Failed",
    "Pending", "Volume", "Revenue", "Avg_Charge", "Avg_Txn_Value",
    "Success_Rate", "Est_Failed_Value",
]].copy()
audit_df.columns = [
    "Merchant", "Channel", "Risk", "Total Txns", "Successful", "Failed",
    "Pending", "Volume (ETB)", "Revenue (ETB)", "Avg Charge (ETB)",
    "Avg Transaction Value (ETB)", "Success Rate (%)", "Est. Value in Failed Txns (ETB)",
]

st.dataframe(
    audit_df.style
    .format({
        "Volume (ETB)":                    "{:,.2f}",
        "Revenue (ETB)":                   "{:,.2f}",
        "Avg Charge (ETB)":                "{:,.2f}",
        "Avg Transaction Value (ETB)":     "{:,.2f}",
        "Success Rate (%)":                "{:.2f}%",
        "Est. Value in Failed Txns (ETB)": "{:,.2f}",
    })
    .applymap(
        lambda v: "background-color:#fdecea" if isinstance(v, str) and v == "High"
        else ("background-color:#fef9e7" if isinstance(v, str) and v == "Medium" else ""),
        subset=["Risk"],
    )
    .bar(subset=["Success Rate (%)"], color=["#c0392b", "#1e8449"], vmin=75, vmax=100)
    .bar(subset=["Volume (ETB)"], color="#d6e4f0"),
    use_container_width=True, height=320,
)

st.divider()

# ── STRATEGIC OBSERVATIONS ────────────────────────────────────────────────────
st.markdown("#### Strategic Observations & Flags")

observations = [
    ("⚠ CRITICAL; DEEROSERVICES: High Failure Rate Persists",
     "116 out of 969 transactions failed (~12% failure rate). Compared to last week's 154 failures (19.7%), this is an improvement, "
     "but still significantly above acceptable thresholds. Key failure clusters: BLCK reversals (58 cases), XML validation failures (45), "
     "System Errors (7), Currency mismatches (5). Escalation is still required; improvement is not enough."),
    ("Top Revenue Generator; JUBAEXPRESS",
     "ETB 213,227.96 in charges this week; up 13.7% from ETB 187,550.80 last week. "
     "Highest revenue earner this cycle. 1,755 total transactions with 42 failures (2.4% failure rate). "
     "Insufficient balance (19 cases) is the top failure driver; funding adequacy should be reviewed."),
    ("REDSEA; Revenue More Than Doubled",
     "Revenue jumped to ETB 97,700.43 this week from ETB 49,819.36 last week; a 96.1% increase. "
     "All 46 transactions were successful (100% success rate). Volume slightly dipped to ETB 40.97M from ETB 41.98M. "
     "Avg charge rose to ETB 2,123.92 from ETB 1,845.16; worth confirming if fee structure changed."),
    ("REDSEADIRECTDEPOSITS; Revenue Drop, Volume Up",
     "Revenue dropped sharply to ETB 126,184.31 from ETB 451,954.15 last week; a 72% decline. "
     "Volume increased to ETB 52.88M from ETB 45.2M. 3 failures (Account Not Found x2, Insufficient Balance x1) and 1 pending transaction noted. "
     "The revenue drop may reflect a different transaction mix (DIRECT_DEPOSIT vs DISBURSEMENTS); review billing logic."),
    ("FINPAYAPPLICATION; Strong Week, Revenue Up",
     "ETB 74,893.00 revenue; up from ETB 60,879 last week. 828 transactions with only 2 failures (0.24%); near-perfect performance. "
     "Volume surged to ETB 55.97M from ETB 28.03M last week; a 99.7% increase in money moved. "
     "Avg charge remains flat at ~91 ETB; consistent flat-fee model confirmed."),
    ("⚠ FLAG; BIRRLINK: Zero Revenue Continues (3rd Consecutive Week)",
     "ETB 0.00 charges again across 20 successful transactions. 1 failure (insufficient balance). "
     "This is now the third week in a row with zero revenue. Fee arrangement documentation is critically overdue. "
     "Volume also declined slightly; ETB 641,020 vs ETB 615,078 last week."),
    ("Zero-Revenue Merchants; BIRRLINK and REMITLYGLOBAL",
     "Both posted ETB 0.00 again this week. REMITLYGLOBAL's zero revenue is expected (international remittance model). "
     "BIRRLINK's zero revenue remains unexplained. Formal confirmation of fee waiver or absorbed-cost arrangement must be documented."),
    ("Overall Portfolio Success Rate",
     "Average success rate this week: ~96.6% (excluding REMITLYGLOBAL data quality issue). "
     "REDSEA (100%), FINPAYAPPLICATION (99.76%), and REDSEADIRECTDEPOSITS (97.5%) are the top performers. "
     "DEEROSERVICES remains the single largest drag on portfolio performance at ~88% success rate."),
]

for title, body in observations:
    st.markdown(f"""
    <div class="observation-box">
      <strong style="color:{MAIN_COLOR};">{title}</strong><br>{body}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── PER-MERCHANT EXPANDERS ────────────────────────────────────────────────────
st.markdown("#### Per-Merchant Detail")

for _, row in df.iterrows():
    with st.expander(f"{row['Merchant']}  |  {row['Risk']} Risk  |  Success Rate: {row['Success_Rate']:.2f}%  |  Period: {row['DateRange']}"):
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Transactions", f"{row['Total_Txns']:,}")
        d2.metric("Total Moved (ETB)",  f"{row['Volume']:,.2f}" if row["Volume"] > 0 else "Data N/A")
        d3.metric("Revenue (ETB)",      f"{row['Revenue']:,.2f}")
        d4.metric("Failed Transactions", str(int(row["Failed"])))

        d5, d6, d7 = st.columns(3)
        d5.metric("Avg Transaction Value (ETB)", f"{row['Avg_Txn_Value']:,.2f}" if row["Avg_Txn_Value"] > 0 else "Data N/A")
        d6.metric("Avg Charge per Transaction",  f"ETB {row['Avg_Charge']:,.2f}")
        d7.metric("Channel", row["Channel"])

        st.markdown(f"**Transaction Types:** {row['TxnTypes']}")
        st.markdown(f"**Top Failure Reasons:** {row['Top_Failures']}")
        if row["Notes"]:
            st.markdown(f'<div class="flag-box">{row["Notes"]}</div>', unsafe_allow_html=True)

st.divider()

# ── WEEK-ON-WEEK COMPARISON ───────────────────────────────────────────────────
st.markdown(f"""
<div class="compare-header">
  <span style="font-size:18px; font-weight:700; color:white;">
    Week-on-Week Comparison &nbsp;|&nbsp; Apr 20–26 vs Apr 27–May 3, 2026
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="chart-note" style="font-size:12px; color:#444;">'
    '<b>What does "Change vs Last Week" mean?</b> It shows how much a number went up or down compared to the previous week. '
    'A <span style="color:#1e8449;font-weight:bold;">green positive number</span> means improvement. '
    'A <span style="color:#c0392b;font-weight:bold;">red negative number</span> means it got worse. '
    'For failed transactions, fewer failures = better, so a decrease is shown in green. '
    'Note: REMITLYGLOBAL volume comparison is unreliable due to data quality issue in current week.'
    '</p>',
    unsafe_allow_html=True,
)

# Build merged comparison dataframe
comp = df[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed", "Success_Rate", "Avg_Txn_Value"]].copy()
comp.columns = ["Merchant", "Vol_CW", "Rev_CW", "Txns_CW", "Failed_CW", "SR_CW", "Ticket_CW"]
prev_cols = df_prev[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed", "Success_Rate", "Avg_Txn_Value"]].copy()
prev_cols.columns = ["Merchant", "Vol_PW", "Rev_PW", "Txns_PW", "Failed_PW", "SR_PW", "Ticket_PW"]
merged = comp.merge(prev_cols, on="Merchant", how="left")

# Portfolio-level KPI changes
cw_vol  = df[df["Merchant"] != "REMITLYGLOBAL"]["Volume"].sum()
pw_vol  = df_prev[df_prev["Merchant"] != "REMITLYGLOBAL"]["Volume"].sum()
cw_rev  = df["Revenue"].sum()
pw_rev  = df_prev["Revenue"].sum()
cw_txns = df["Total_Txns"].sum()
pw_txns = df_prev["Total_Txns"].sum()
cw_fail = df["Failed"].sum()
pw_fail = df_prev["Failed"].sum()

def delta_pct(cw, pw):
    if pw == 0:
        return None
    return ((cw - pw) / pw) * 100

st.markdown("##### Portfolio Totals; Change vs Last Week")
w1, w2, w3, w4 = st.columns(4)
d_vol  = delta_pct(cw_vol, pw_vol)
d_rev  = delta_pct(cw_rev, pw_rev)
d_txns = delta_pct(cw_txns, pw_txns)
d_fail = delta_pct(cw_fail, pw_fail)

w1.metric("Total Money Moved (Excl. REMITLY)", f"ETB {cw_vol/1e6:.1f}M",
          delta=f"{'+' if d_vol>=0 else ''}{d_vol:.1f}% vs last week")
w2.metric("Total Revenue",        f"ETB {cw_rev:,.0f}",
          delta=f"{'+' if d_rev>=0 else ''}{d_rev:.1f}% vs last week")
w3.metric("Total Transactions",   f"{cw_txns:,}",
          delta=f"{'+' if d_txns>=0 else ''}{d_txns:.1f}% vs last week")
w4.metric("Total Failed",         f"{int(cw_fail)}",
          delta=f"{'+' if d_fail>=0 else ''}{d_fail:.1f}% vs last week", delta_color="inverse")

st.markdown("---")
st.markdown("##### Merchant-by-Merchant Breakdown")

# Volume WoW
fig_wow_vol = go.Figure()
fig_wow_vol.add_trace(go.Bar(
    name="Apr 20–26 (Last Week)",
    x=merged["Merchant"], y=merged["Vol_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v/1e6:.1f}M" for v in merged["Vol_PW"]], textposition="outside",
))
fig_wow_vol.add_trace(go.Bar(
    name="Apr 27–May 3 (This Week)",
    x=merged["Merchant"], y=merged["Vol_CW"],
    marker_color=MAIN_COLOR,
    text=[f"{v/1e6:.1f}M" if v > 0 else "N/A" for v in merged["Vol_CW"]], textposition="outside",
))
fig_wow_vol.update_layout(
    barmode="group", title="Money Moved; Last Week vs This Week (ETB)",
    plot_bgcolor="white", font=dict(size=10),
    margin=dict(t=40, b=10, l=10, r=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Revenue WoW
fig_wow_rev = go.Figure()
fig_wow_rev.add_trace(go.Bar(
    name="Apr 20–26 (Last Week)",
    x=merged["Merchant"], y=merged["Rev_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v:,.0f}" for v in merged["Rev_PW"]], textposition="outside",
))
fig_wow_rev.add_trace(go.Bar(
    name="Apr 27–May 3 (This Week)",
    x=merged["Merchant"], y=merged["Rev_CW"],
    marker_color=MAIN_COLOR,
    text=[f"{v:,.0f}" for v in merged["Rev_CW"]], textposition="outside",
))
fig_wow_rev.update_layout(
    barmode="group", title="Revenue; Last Week vs This Week (ETB)",
    plot_bgcolor="white", font=dict(size=10),
    margin=dict(t=40, b=10, l=10, r=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

wc1, wc2 = st.columns(2)
with wc1:
    st.plotly_chart(fig_wow_vol, use_container_width=True)
with wc2:
    st.plotly_chart(fig_wow_rev, use_container_width=True)

# Success Rate WoW
fig_wow_sr = go.Figure()
fig_wow_sr.add_trace(go.Bar(
    name="Apr 20–26 (Last Week)",
    x=merged["Merchant"], y=merged["SR_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v:.1f}%" for v in merged["SR_PW"]], textposition="outside",
))
fig_wow_sr.add_trace(go.Bar(
    name="Apr 27–May 3 (This Week)",
    x=merged["Merchant"], y=merged["SR_CW"],
    marker_color=MAIN_COLOR,
    text=[f"{v:.1f}%" for v in merged["SR_CW"]], textposition="outside",
))
fig_wow_sr.update_layout(
    barmode="group", title="Success Rate; Last Week vs This Week (%)",
    plot_bgcolor="white", font=dict(size=10),
    yaxis=dict(range=[70, 105]),
    margin=dict(t=40, b=10, l=10, r=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Failed Transactions WoW
fig_wow_fail = go.Figure()
fig_wow_fail.add_trace(go.Bar(
    name="Apr 20–26 (Last Week)",
    x=merged["Merchant"], y=merged["Failed_PW"],
    marker_color=GOLD_COLOR,
    text=[str(int(v)) for v in merged["Failed_PW"]], textposition="outside",
))
fig_wow_fail.add_trace(go.Bar(
    name="Apr 27–May 3 (This Week)",
    x=merged["Merchant"], y=merged["Failed_CW"],
    marker_color="#c0392b",
    text=[str(int(v)) for v in merged["Failed_CW"]], textposition="outside",
))
fig_wow_fail.update_layout(
    barmode="group", title="Failed Transactions; Last Week vs This Week",
    plot_bgcolor="white", font=dict(size=10),
    margin=dict(t=40, b=10, l=10, r=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

wc3, wc4 = st.columns(2)
with wc3:
    st.plotly_chart(fig_wow_sr, use_container_width=True)
with wc4:
    st.plotly_chart(fig_wow_fail, use_container_width=True)

# ── Detailed WoW Summary Table ────────────────────────────────────────────────
st.markdown("##### Detailed Change vs Last Week; Summary Table")
st.markdown(
    '<p class="chart-note">'
    'PW = Previous Week (Apr 20–26) | CW = Current Week (Apr 27–May 3) | '
    'Change = how much it moved up or down | SR = Success Rate | '
    '"Change in SR" = percentage point change in success rate | '
    '* REMITLYGLOBAL volume flagged; data quality issue'
    '</p>',
    unsafe_allow_html=True,
)

rows = []
for _, r in merged.iterrows():
    dv  = delta_pct(r["Vol_CW"],    r["Vol_PW"])
    drv = delta_pct(r["Rev_CW"],    r["Rev_PW"])
    dt  = delta_pct(r["Txns_CW"],   r["Txns_PW"])
    df_ = delta_pct(r["Failed_CW"], r["Failed_PW"])
    dsr = r["SR_CW"] - r["SR_PW"] if pd.notna(r["SR_PW"]) else None

    def fmt(v, pct=True, invert=False):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return "n/a"
        sign = "+" if v >= 0 else ""
        unit = "%" if pct else " pts"
        good = (v > 0) if not invert else (v < 0)
        color = "#1e8449" if good else "#c0392b"
        return f'<span style="color:{color};font-weight:bold">{sign}{v:.1f}{unit}</span>'

    vol_note = " *" if r["Merchant"] == "REMITLYGLOBAL" else ""

    rows.append({
        "Merchant":                      r["Merchant"],
        "Vol Last Wk (M)":               f"{r['Vol_PW']/1e6:.1f}",
        "Vol This Wk (M)":               f"{r['Vol_CW']/1e6:.1f}{vol_note}",
        "Volume Change":                 fmt(dv) if r["Merchant"] != "REMITLYGLOBAL" else '<span style="color:#888">Data Issue</span>',
        "Rev Last Wk":                   f"{r['Rev_PW']:,.0f}",
        "Rev This Wk":                   f"{r['Rev_CW']:,.0f}",
        "Revenue Change":                fmt(drv) if r["Rev_PW"] > 0 else "n/a",
        "Txns Last Wk":                  str(int(r["Txns_PW"])),
        "Txns This Wk":                  str(int(r["Txns_CW"])),
        "Txns Change":                   fmt(dt),
        "Failed Last Wk":                str(int(r["Failed_PW"])),
        "Failed This Wk":                str(int(r["Failed_CW"])),
        "Failed Change":                 fmt(df_, invert=True),
        "Success Rate Last Wk":          f"{r['SR_PW']:.1f}%",
        "Success Rate This Wk":          f"{r['SR_CW']:.1f}%",
        "Change in Success Rate":        fmt(dsr, pct=False),
    })

wow_df = pd.DataFrame(rows)
st.write(wow_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()

# ── PDF ENGINE ────────────────────────────────────────────────────────────────
def generate_pdf(dataframe, prev_df, fig_vol, fig_rev, fig_sr, fig_fail,
                 fig_margin, fig_ticket, fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail):

    def img(fig, w=700, h=380):
        return io.BytesIO(fig.to_image(format="png", width=w, height=h, scale=2))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)

    def header_band(title_text, subtitle=""):
        pdf.set_fill_color(*MAIN_RGB)
        pdf.rect(0, 0, 210, 30, "F")
        pdf.set_fill_color(*GOLD_RGB)
        pdf.rect(0, 30, 210, 2, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.text(10, 13, safe(title_text))
        if subtitle:
            pdf.set_font("Arial", size=8)
            pdf.text(10, 21, safe(subtitle))
            pdf.text(10, 27, safe(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"))

    # PAGE 1: KPIs + Charts + Audit
    pdf.add_page()
    header_band(
        "MERCHANT 360 | WEEKLY STRATEGIC REPORT",
        "Analytics Cycle: April 27 - May 3, 2026  |  7 Merchants  |  Ethiopia (ETB)"
    )

    kpi_items = [
        ("Total Revenue",          f"ETB {dataframe['Revenue'].sum():,.2f}"),
        ("Total Money Moved",      f"ETB {dataframe[dataframe['Merchant']!='REMITLYGLOBAL']['Volume'].sum()/1e6:.2f}M*"),
        ("Total Txns",             f"{dataframe['Total_Txns'].sum():,}"),
        ("Avg Success Rate",       f"{dataframe['Success_Rate'].mean():.1f}%"),
        ("Est. Failed Value",      f"ETB {dataframe['Est_Failed_Value'].sum():,.0f}"),
    ]
    x = 10
    for lbl, val in kpi_items:
        pdf.set_fill_color(245, 246, 250)
        pdf.rect(x, 35, 37, 18, "F")
        pdf.set_fill_color(*GOLD_RGB)
        pdf.rect(x, 35, 37, 1.5, "F")
        pdf.set_xy(x, 38); pdf.set_font("Arial", "B", 6); pdf.set_text_color(110, 110, 110)
        pdf.cell(37, 4, safe(lbl), 0, 1, "C")
        pdf.set_xy(x, 43); pdf.set_font("Arial", "B", 8); pdf.set_text_color(*MAIN_RGB)
        pdf.cell(37, 4, safe(val), 0, 1, "C")
        x += 39

    # Data quality note in PDF
    pdf.set_xy(10, 56)
    pdf.set_font("Arial", "I", 6); pdf.set_text_color(180, 100, 0)
    pdf.cell(190, 4, safe("* REMITLYGLOBAL excluded from volume total; data quality issue (no successful transaction tag found in dataset)."), ln=True)

    imgs4 = [img(f) for f in (fig_vol, fig_rev, fig_sr, fig_fail)]
    pdf.image(imgs4[0], x=10,  y=63,  w=93)
    pdf.image(imgs4[1], x=107, y=63,  w=93)
    pdf.image(imgs4[2], x=10,  y=114, w=93)
    pdf.image(imgs4[3], x=107, y=114, w=93)

    pdf.set_xy(10, 168)
    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", "B", 9)
    pdf.cell(190, 7, safe("Comprehensive Weekly Audit Trail"), ln=True)

    hdrs   = ["Merchant", "Vol (M ETB)", "Revenue (ETB)", "Txns", "Failed", "Success %", "Avg Txn Value"]
    widths = [36, 27, 27, 15, 15, 24, 33]
    pdf.set_font("Arial", "B", 7); pdf.set_fill_color(*MAIN_RGB); pdf.set_text_color(255, 255, 255)
    for h, w in zip(hdrs, widths):
        pdf.cell(w, 7, safe(h), 1, 0, "C", True)
    pdf.ln()

    pdf.set_font("Arial", size=7)
    for i, (_, row) in enumerate(dataframe.iterrows()):
        if row["Risk"] == "High":      pdf.set_fill_color(253, 235, 233)
        elif row["Risk"] == "Medium":  pdf.set_fill_color(254, 249, 231)
        else:
            pdf.set_fill_color(248, 250, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(0, 0, 0)
        vol_str = f"{row['Volume']/1e6:.2f}" if row["Volume"] > 0 else "N/A*"
        cells = [
            str(row["Merchant"]),
            vol_str,
            f"{row['Revenue']:,.0f}",
            str(int(row["Total_Txns"])),
            str(int(row["Failed"])),
            f"{row['Success_Rate']:.1f}%",
            f"{row['Avg_Txn_Value']:,.0f}" if row["Avg_Txn_Value"] > 0 else "N/A*",
        ]
        for val, w in zip(cells, widths):
            pdf.cell(w, 6, safe(val), 1, 0, "C", True)
        pdf.ln()

    # PAGE 2: Observations
    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB); pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB); pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Strategic Observations & Flags | Week of April 27 - May 3, 2026"))

    obs_pdf = [
        ("CRITICAL - DEEROSERVICES: Failure Rate Still High",
         "116/969 transactions failed (~12%); improvement from 19.7% last week but still unacceptable. "
         "BLCK reversals (58), XML validation failures (45), System Errors (7), Currency mismatches (5). Escalation required."),
        ("DATA FLAG - REMITLYGLOBAL: Dataset Quality Issue",
         "2,834 transactions processed, 99 failures (3.5%). No successful tag found - volume shows 0. "
         "Data pipeline review required before next reporting cycle."),
        ("Top Revenue Generator - JUBAEXPRESS",
         "ETB 213,227.96 in charges (+13.7% vs last week). 1,755 transactions, 42 failures (2.4%). "
         "Insufficient balance (19 cases) is top failure - review funding adequacy."),
        ("REDSEA - Revenue Nearly Doubled",
         "ETB 97,700.43 revenue (+96.1% vs ETB 49,819 last week). All 46 transactions successful. "
         "Avg charge rose to ETB 2,123.92 - confirm if fee structure changed."),
        ("REDSEADIRECTDEPOSITS - Revenue Drop, Volume Up",
         "Revenue dropped 72% to ETB 126,184 from ETB 451,954 last week. Volume grew to ETB 52.88M. "
         "Mix changed to DIRECT_DEPOSIT / ACCOUNT_CREDIT this week - review billing logic."),
        ("FINPAYAPPLICATION - Strong Week",
         "ETB 74,893 revenue (+23%). Volume near doubled to ETB 55.97M. Only 2 failures (0.24%). Flat fee ~91 ETB confirmed."),
        ("BIRRLINK - Zero Revenue: 3rd Week",
         "ETB 0.00 charges for third consecutive week. Fee arrangement documentation is critically overdue."),
    ]

    y_pos = 27
    for title, body in obs_pdf:
        if y_pos > 265:
            pdf.add_page(); y_pos = 15
        pdf.set_fill_color(*GOLD_RGB); pdf.rect(10, y_pos, 2.5, 16, "F")
        pdf.set_xy(15, y_pos + 1); pdf.set_font("Arial", "B", 9); pdf.set_text_color(*MAIN_RGB)
        pdf.cell(183, 5, safe(title), ln=True)
        pdf.set_xy(15, y_pos + 8); pdf.set_font("Arial", size=8); pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(183, 4, safe(body))
        y_pos += 26

    # PAGE 3: Week-on-Week charts
    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB); pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB); pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Week-on-Week Comparison | Apr 20-26 vs Apr 27 - May 3, 2026"))

    merged_loc = dataframe[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed"]].copy()
    merged_loc.columns = ["Merchant", "Vol_CW", "Rev_CW", "Txns_CW", "Failed_CW"]
    pv = prev_df[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed"]].copy()
    pv.columns = ["Merchant", "Vol_PW", "Rev_PW", "Txns_PW", "Failed_PW"]
    mg = merged_loc.merge(pv, on="Merchant", how="left")

    pw_vol_t  = prev_df[prev_df["Merchant"] != "REMITLYGLOBAL"]["Volume"].sum()
    pw_rev_t  = prev_df["Revenue"].sum()
    pw_txn_t  = prev_df["Total_Txns"].sum()
    pw_fail_t = prev_df["Failed"].sum()
    cw_vol_t  = dataframe[dataframe["Merchant"] != "REMITLYGLOBAL"]["Volume"].sum()
    cw_rev_t  = dataframe["Revenue"].sum()
    cw_txn_t  = dataframe["Total_Txns"].sum()
    cw_fail_t = dataframe["Failed"].sum()

    def dpdf(cw, pw):
        if pw == 0: return "n/a"
        v = ((cw - pw) / pw) * 100
        return f"{'+'if v>=0 else ''}{v:.1f}% vs last week"

    kpi2 = [
        ("Total Money Moved*", f"ETB {cw_vol_t/1e6:.1f}M",    dpdf(cw_vol_t, pw_vol_t)),
        ("Total Revenue",      f"ETB {cw_rev_t:,.0f}",         dpdf(cw_rev_t, pw_rev_t)),
        ("Total Txns",         f"{int(cw_txn_t):,}",           dpdf(cw_txn_t, pw_txn_t)),
        ("Total Failed",       str(int(cw_fail_t)),             dpdf(cw_fail_t, pw_fail_t)),
    ]
    x = 10
    for lbl, val, delta in kpi2:
        pdf.set_fill_color(245, 246, 250); pdf.rect(x, 25, 45, 22, "F")
        pdf.set_fill_color(*GOLD_RGB); pdf.rect(x, 25, 45, 1.5, "F")
        pdf.set_xy(x, 28); pdf.set_font("Arial", "B", 6); pdf.set_text_color(110, 110, 110)
        pdf.cell(45, 4, safe(lbl), 0, 1, "C")
        pdf.set_xy(x, 33); pdf.set_font("Arial", "B", 8); pdf.set_text_color(*MAIN_RGB)
        pdf.cell(45, 4, safe(val), 0, 1, "C")
        pdf.set_xy(x, 39); pdf.set_font("Arial", size=6); pdf.set_text_color(80, 80, 80)
        pdf.cell(45, 4, safe(delta), 0, 1, "C")
        x += 47

    wow_imgs = [img(f) for f in (fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail)]
    pdf.image(wow_imgs[0], x=10,  y=52,  w=93)
    pdf.image(wow_imgs[1], x=107, y=52,  w=93)
    pdf.image(wow_imgs[2], x=10,  y=105, w=93)
    pdf.image(wow_imgs[3], x=107, y=105, w=93)

    pdf.set_xy(10, 160)
    pdf.set_font("Arial", "B", 8); pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 6, safe("Merchant Change vs Last Week; Summary Table"), ln=True)

    th2 = ["Merchant", "Vol PW(M)", "Vol CW(M)", "Vol Chg", "Rev PW", "Rev CW", "Rev Chg",
           "SR Last Wk", "SR This Wk", "SR Change", "Failed PW", "Failed CW"]
    tw2 = [32, 16, 16, 14, 21, 21, 14, 16, 16, 14, 16, 16]
    pdf.set_font("Arial", "B", 6); pdf.set_fill_color(*MAIN_RGB); pdf.set_text_color(255, 255, 255)
    for h, w in zip(th2, tw2):
        pdf.cell(w, 6, safe(h), 1, 0, "C", True)
    pdf.ln()

    pdf.set_font("Arial", size=6)
    for _, r in mg.iterrows():
        dv_  = ((r["Vol_CW"] - r["Vol_PW"]) / r["Vol_PW"] * 100) if r["Vol_PW"] else 0
        drv_ = ((r["Rev_CW"] - r["Rev_PW"]) / r["Rev_PW"] * 100) if r["Rev_PW"] else 0
        sr_cw  = df.loc[df["Merchant"] == r["Merchant"], "Success_Rate"].values
        sr_cw  = sr_cw[0] if len(sr_cw) else 0
        sr_pw2 = df_prev.loc[df_prev["Merchant"] == r["Merchant"], "Success_Rate"].values
        sr_pw2 = sr_pw2[0] if len(sr_pw2) else 0

        pdf.set_fill_color(255, 255, 255); pdf.set_text_color(0, 0, 0)
        vol_note = "*" if r["Merchant"] == "REMITLYGLOBAL" else ""
        row_cells = [
            str(r["Merchant"]),
            f"{r['Vol_PW']/1e6:.1f}", f"{r['Vol_CW']/1e6:.1f}{vol_note}",
            f"{'+'if dv_>=0 else ''}{dv_:.0f}%" if r["Merchant"] != "REMITLYGLOBAL" else "N/A*",
            f"{r['Rev_PW']:,.0f}", f"{r['Rev_CW']:,.0f}",
            f"{'+'if drv_>=0 else ''}{drv_:.0f}%",
            f"{sr_pw2:.1f}%", f"{sr_cw:.1f}%",
            f"{'+'if (sr_cw-sr_pw2)>=0 else ''}{(sr_cw-sr_pw2):.1f}",
            str(int(r["Failed_PW"])), str(int(r["Failed_CW"])),
        ]
        for val, w in zip(row_cells, tw2):
            pdf.cell(w, 5, safe(val), 1, 0, "C", True)
        pdf.ln()

    # PAGE 4: Per-Merchant Detail
    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB); pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB); pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Per-Merchant Breakdown | April 27 - May 3, 2026"))

    y_pos = 27
    for _, row in dataframe.iterrows():
        if y_pos > 248:
            pdf.add_page(); y_pos = 15
        pdf.set_fill_color(*MAIN_RGB); pdf.rect(10, y_pos, 190, 7, "F")
        pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 8)
        pdf.text(12, y_pos + 5,
                 safe(f"{row['Merchant']}  |  [{row['Risk']} Risk]  |  {row['DateRange']}  |  Success: {row['Success_Rate']:.1f}%"))

        vol_str  = f"ETB {row['Volume']:,.0f}" if row["Volume"] > 0 else "Data N/A*"
        tick_str = f"ETB {row['Avg_Txn_Value']:,.2f}" if row["Avg_Txn_Value"] > 0 else "Data N/A*"

        detail_rows = [
            [("Channel", row["Channel"]), ("Txn Types", row["TxnTypes"]),
             ("Total Txns", f"{int(row['Total_Txns']):,}"), ("Failed", str(int(row["Failed"]))),
             ("Total Moved", vol_str)],
            [("Revenue", f"ETB {row['Revenue']:,.2f}"),
             ("Avg Transaction Value", tick_str),
             ("Avg Charge per Txn", f"ETB {row['Avg_Charge']:,.2f}"),
             ("Top Failures", str(row["Top_Failures"])[:45])],
        ]
        row_y = y_pos + 9
        for drow in detail_rows:
            cw = 190 // len(drow); x_pos = 10
            for lbl, val in drow:
                pdf.set_xy(x_pos, row_y); pdf.set_font("Arial", "B", 6)
                pdf.set_text_color(120, 120, 120); pdf.cell(cw, 3.5, safe(lbl + ":"), 0, 0)
                pdf.set_xy(x_pos, row_y + 3.5); pdf.set_font("Arial", size=7)
                pdf.set_text_color(0, 0, 0); pdf.cell(cw, 4, safe(str(val)), 0, 0)
                x_pos += cw
            row_y += 9

        if row["Notes"]:
            pdf.set_fill_color(253, 248, 235); pdf.rect(10, row_y, 190, 8, "F")
            pdf.set_fill_color(*GOLD_RGB);     pdf.rect(10, row_y, 2, 8, "F")
            pdf.set_xy(14, row_y + 2); pdf.set_font("Arial", size=7); pdf.set_text_color(80, 60, 20)
            pdf.cell(184, 4, safe(str(row["Notes"])[:115]), 0, 0)
            row_y += 8
        y_pos = row_y + 5

    return pdf.output(dest="S")


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