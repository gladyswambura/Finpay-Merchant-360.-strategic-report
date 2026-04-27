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
</style>
""", unsafe_allow_html=True)


# ── THIS WEEK DATA (Apr 20–26) ────────────────────────────────────────────────
def load_current():
    records = [
        {
            "Merchant":          "REDSEA",
            "TxnTypes":          "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":           "Bank",
            "Volume":            41_981_936.00,
            "Revenue":           49_819.36,
            "Successful":        27,
            "Failed":            0,
            "Pending":           0,
            "Avg_Charge":        1_845.16,
            "Avg_Txn_Value":     1_554_886.52,
            "Risk":              "Low",
            "Top_Failures":      "None",
            "Networks":          "CBE (16), Bank of Abyssinia (6), Dashen (1), Awash (1), CBO (1)",
            "Notes":             "100% success rate. 2 ACCOUNT_DEBIT txns (ETB 37M) carried ETB 0 charges. Highest avg transaction value in portfolio at ETB 1.55M.",
        },
        {
            "Merchant":          "REDSEADIRECTDEPOSITS",
            "TxnTypes":          "DISBURSEMENTS",
            "Channel":           "Bank",
            "Volume":            45_195_396.45,
            "Revenue":           451_954.15,
            "Successful":        1_000,
            "Failed":            3,
            "Pending":           0,
            "Avg_Charge":        451.95,
            "Avg_Txn_Value":     45_195.40,
            "Risk":              "Low",
            "Top_Failures":      "XML validation failed reversed (2), Missing reversed (1)",
            "Networks":          "CBE (677), Bank of Abyssinia (262), Awash (34), Dashen (19), Wegagen (5), CBO (4)",
            "Notes":             "99.7% success rate. All 3 failures reversed. Highest revenue ETB 451,954 — top earner this week.",
        },
        {
            "Merchant":          "JUBAEXPRESS",
            "TxnTypes":          "DISBURSEMENTS",
            "Channel":           "Bank",
            "Volume":            46_886_467.00,
            "Revenue":           187_550.80,
            "Successful":        1_460,
            "Failed":            3,
            "Pending":           0,
            "Avg_Charge":        128.46,
            "Avg_Txn_Value":     32_114.02,
            "Risk":              "Low",
            "Top_Failures":      "System Error (1), Missing reversed (1), Insufficient balance (1)",
            "Networks":          "CBE (1094), Bank of Abyssinia (281), Awash (51), Dashen (21), Wegagen (6), Abay (3), Lion (2)",
            "Notes":             "99.8% success rate across 12 networks. All 3 failures resolved. Second highest volume this week.",
        },
        {
            "Merchant":          "FINPAYAPPLICATION",
            "TxnTypes":          "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":           "Bank",
            "Volume":            28_026_347.40,
            "Revenue":           60_879.00,
            "Successful":        670,
            "Failed":            1,
            "Pending":           0,
            "Avg_Charge":        90.86,
            "Avg_Txn_Value":     41_830.37,
            "Risk":              "Low",
            "Top_Failures":      "XML validation failed reversed (1)",
            "Networks":          "CBE (578), Bank of Abyssinia (58), Awash (19), Dashen (9), Wegagen (3), CBO (1)",
            "Notes":             "99.9% success rate. Single failure reversed (ETB 60,950). Clean week.",
        },
        {
            "Merchant":          "BIRRLINK",
            "TxnTypes":          "DISBURSEMENTS",
            "Channel":           "Bank",
            "Volume":            615_078.00,
            "Revenue":           0.00,
            "Successful":        24,
            "Failed":            0,
            "Pending":           0,
            "Avg_Charge":        0.00,
            "Avg_Txn_Value":     25_628.25,
            "Risk":              "High",
            "Top_Failures":      "None",
            "Networks":          "CBE (23), Bank of Abyssinia (1)",
            "Notes":             "100% success rate. Zero charges again — waived-fee arrangement still unconfirmed. ETB 0 revenue flag persists.",
        },
        {
            "Merchant":          "DEEROSERVICES",
            "TxnTypes":          "DISBURSEMENTS",
            "Channel":           "Bank",
            "Volume":            23_453_278.00,
            "Revenue":           56_966.00,
            "Successful":        626,
            "Failed":            154,
            "Pending":           0,
            "Avg_Charge":        91.00,
            "Avg_Txn_Value":     37_465.30,
            "Risk":              "Medium",
            "Top_Failures":      "BLCK reversed (99, Kaafi MFI), XML validation failed (51, CBO), Currency mismatch (2), Missing (1), Status error (1)",
            "Networks":          "CBE (397), Kaafi Micro Finance (211), CBO (116), Bank of Abyssinia (26), Awash (21), Dashen (7)",
            "Notes":             "19.7% failure rate — worse than last week (18.67%). BLCK errors on Kaafi MFI now 99 cases. Critical — escalate immediately.",
        },
        {
            "Merchant":          "REMITLYGLOBAL",
            "TxnTypes":          "DISBURSEMENTS",
            "Channel":           "Bank + Mobile",
            "Volume":            71_061_908.98,
            "Revenue":           0.00,
            "Successful":        2_322,
            "Failed":            13,
            "Pending":           0,
            "Avg_Charge":        0.00,
            "Avg_Txn_Value":     30_603.75,
            "Risk":              "Low",
            "Top_Failures":      "Missing reversed (3), Insufficient balance (3), Unknown error (2), Currency mismatch (1), XML failed (1), Auth token (1), Creditor agent (1), ERRR (1)",
            "Networks":          "CBE (1526), Bank of Abyssinia (563), CBE Birr/Mobile (96), Dashen (65), Awash (48), Wegagen (13), Abay (9)",
            "Notes":             "Highest volume this week at ETB 71.1M. 99.4% success rate. Zero charges — international remittance model. Bank + Mobile channels.",
        },
    ]
    df = pd.DataFrame(records)
    df["Total_Txns"]        = df["Successful"] + df["Failed"] + df["Pending"]
    df["Success_Rate"]      = (df["Successful"] / df["Total_Txns"]) * 100
    # Est. Failed Value = how much ETB was tied up in failed transactions
    df["Est_Failed_Value"]  = df["Failed"] * df["Avg_Txn_Value"]
    # Revenue Margin in Basis Points: how many cents per ETB 100 moved
    # 1 basis point = 0.01%, so 100 bps = 1% of volume
    df["Rev_Margin_BPS"]    = (df["Revenue"] / df["Volume"].replace(0, 1)) * 10_000
    return df


# ── PRIOR WEEK DATA (Apr 13–19) ───────────────────────────────────────────────
def load_prior():
    records = [
        {"Merchant": "REDSEA",               "Volume": 29_400_692.00, "Revenue": 54_006.92,  "Successful": 28,    "Failed": 1,   "Total_Txns": 29, "Avg_Txn_Value": 1_088_914.52, "Success_Rate": 96.55},
        {"Merchant": "REDSEADIRECTDEPOSITS",  "Volume": 40_606_822.45, "Revenue": 406_068.40, "Successful": 869,   "Failed": 9,   "Total_Txns": 878, "Avg_Txn_Value": 46_728.22,   "Success_Rate": 98.97},
        {"Merchant": "JUBAEXPRESS",           "Volume": 39_051_740.00, "Revenue": 156_211.25, "Successful": 1_274, "Failed": 4,   "Total_Txns": 1278, "Avg_Txn_Value": 30_652.86,  "Success_Rate": 99.69},
        {"Merchant": "FINPAYAPPLICATION",     "Volume": 31_892_665.10, "Revenue": 54_054.00,  "Successful": 596,   "Failed": 0,   "Total_Txns": 596, "Avg_Txn_Value": 53_511.18,   "Success_Rate": 100.0},
        {"Merchant": "BIRRLINK",              "Volume": 663_098.79,    "Revenue": 0.00,        "Successful": 19,    "Failed": 1,   "Total_Txns": 20,  "Avg_Txn_Value": 34_899.94,   "Success_Rate": 95.0},
        {"Merchant": "DEEROSERVICES",         "Volume": 20_681_002.00, "Revenue": 49_959.00,  "Successful": 549,   "Failed": 126, "Total_Txns": 675, "Avg_Txn_Value": 37_670.31,   "Success_Rate": 81.33},
        {"Merchant": "REMITLYGLOBAL",         "Volume": 50_864_641.87, "Revenue": 0.00,        "Successful": 1_924, "Failed": 15,  "Total_Txns": 1939, "Avg_Txn_Value": 26_436.92,  "Success_Rate": 99.23},
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
    Analytics Cycle: April 20 to April 26, 2026 &nbsp;&middot;&nbsp;
    7 Merchants &nbsp;&middot;&nbsp; Ethiopia (ETB)
  </span>
</div>
""", unsafe_allow_html=True)


# ── TOP KPIs ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Weekly Revenue",           f"ETB {df['Revenue'].sum():,.2f}")
k2.metric("Total Money Moved (Successful)", f"ETB {df['Volume'].sum():,.2f}")
k3.metric("Total Transactions",             f"{df['Total_Txns'].sum():,}")
k4.metric("Average Success Rate",           f"{df['Success_Rate'].mean():.2f}%")
k5.metric(
    "Est. Value in Failed Transactions",
    f"ETB {df['Est_Failed_Value'].sum():,.2f}",
    help="This is the estimated ETB value that was tied up in failed transactions (Failed count × Average Transaction Value). These funds were not successfully delivered.",
)

st.divider()

# ── CHART ROW 1: Volume + Revenue ─────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig_vol = px.bar(
        df.sort_values("Volume"),
        x="Volume", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Total Money Moved by Merchant (ETB)",
        text=df.sort_values("Volume")["Volume"].apply(lambda v: f"{v/1e6:.1f}M"),
    )
    fig_vol.update_traces(textposition="outside")
    fig_vol.update_layout(plot_bgcolor="white", font=dict(size=10),
                          margin=dict(t=40, b=10, l=10, r=70), xaxis_title="", yaxis_title="")
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

# ── CHART ROW 2: Success Rate Bar + Failed bar ────────────────────────────────
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
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=True,
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
        '<b>1 BPS = 0.01%</b>. '
        'Revenue ÷ Volume * 10,000. '
        'Earning ETB 451,954 on ETB 45.2M moved = exactly 100.0 BPS, meaning ETB 1 earned for every ETB 100 moved. '
        'Higher BPS = more revenue earned per ETB moved.'
        '</p>',
        unsafe_allow_html=True,
    )

with c6:
    fig_ticket = px.bar(
        df.sort_values("Avg_Txn_Value"),
        x="Avg_Txn_Value", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Average Transaction Value by Merchant (ETB)",
        text=df.sort_values("Avg_Txn_Value")["Avg_Txn_Value"].apply(lambda v: f"{v:,.0f}"),
    )
    fig_ticket.update_traces(textposition="outside")
    fig_ticket.update_layout(plot_bgcolor="white", font=dict(size=10),
                             margin=dict(t=40, b=10, l=10, r=90),
                             xaxis_title="ETB", yaxis_title="")
    st.plotly_chart(fig_ticket, use_container_width=True)
    st.markdown(
        '<p class="chart-note">'
        '<b>Average Transaction Value</b> = Total money moved ÷ Number of successful transactions. '
        '</p>',
        unsafe_allow_html=True,
    )

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
    .bar(subset=["Success Rate (%)"], color=["#c0392b", "#1e8449"], vmin=80, vmax=100)
    .bar(subset=["Volume (ETB)"], color="#d6e4f0"),
    use_container_width=True, height=320,
)

st.divider()

# ── STRATEGIC OBSERVATIONS ────────────────────────────────────────────────────
st.markdown("#### Strategic Observations & Flags")

observations = [
    ("Top Revenue Generator.... REDSEADIRECTDEPOSITS",
     "ETB 451,954.15 in charges this week; an 11.3% increase from ETB 406,068.40 last week. "
     "Highest revenue margin. JUBAEXPRESS follows at ETB 187,550.80 (up from ETB 156,211.25 last week)."),
    ("CRITICAL; DEEROSERVICES Failure Rate Getting Worse",
     "19.7% of transactions failed (154 out of 780); up from 18.67% last week. "
     "Blocked account errors on Kaafi Micro Finance increased from 77 to 99 cases. "
     "XML validation failures on Cooperative Bank of Oromia rose from 49 to 51. "
     "2 new currency mismatch errors appeared this week. Escalation is overdue."),
    ("REMITLYGLOBAL; Largest Merchant by Volume",
     "ETB 71.1M moved this week; up 39.7% from ETB 50.9M last week. 2,335 transactions processed "
     "with a 99.4% success rate. Only merchant using both bank and mobile channels. Zero charges; consistent with international remittance model."),
    ("REDSEA; Big Volume Jump",
     "Volume jumped 42.8% from ETB 29.4M to ETB 41.98M. All 27 transactions succeeded (vs 1 failure last week). "
     "The 2 account debit transactions totalling ETB 37M carried no charges; worth confirming billing treatment."),
    ("Zero-Revenue Merchants; BIRRLINK and REMITLYGLOBAL",
     "BIRRLINK recorded ETB 0.00 charges again across all 24 transactions. "
     "REMITLYGLOBAL ETB 0.00 across 2,335 transactions. "
     "Both have now posted zero revenue for 2 consecutive weeks. Fee arrangement documentation needed."),
    ("FINPAYAPPLICATION; Near-Perfect Week",
     "99.9% success rate with only 1 reversed failure (ETB 60,950). Revenue up to ETB 60,879 from ETB 54,054 last week."),
    ("Overall Portfolio Success Rate",
     "Average success rate this week: 97.1% vs 96.8% last week. "
     "Improvement driven by REDSEA (100%), BIRRLINK (100%), and JUBAEXPRESS (99.8%). "
     "DEEROSERVICES remains the single largest drag on portfolio performance."),
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
    with st.expander(f"{row['Merchant']}  |  {row['Risk']} Risk  |  Success Rate: {row['Success_Rate']:.2f}%"):
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Transactions", f"{row['Total_Txns']:,}")
        d2.metric("Total Moved (ETB)",  f"{row['Volume']:,.2f}")
        d3.metric("Revenue (ETB)",      f"{row['Revenue']:,.2f}")
        d4.metric("Failed Transactions", str(int(row["Failed"])))

        d5, d6, d7 = st.columns(3)
        d5.metric("Avg Transaction Value (ETB)", f"{row['Avg_Txn_Value']:,.2f}")
        d6.metric("Avg Charge per Transaction",  f"ETB {row['Avg_Charge']:,.2f}")
        d7.metric("Channel", row["Channel"])

        st.markdown(f"**Transaction Types:** {row['TxnTypes']}")
        st.markdown(f"**Top Networks:** {row['Networks']}")
        st.markdown(f"**Top Failure Reasons:** {row['Top_Failures']}")
        if row["Notes"]:
            st.markdown(f'<div class="flag-box">{row["Notes"]}</div>', unsafe_allow_html=True)

st.divider()

# ── WEEK-ON-WEEK COMPARISON ───────────────────────────────────────────────────
st.markdown(f"""
<div class="compare-header">
  <span style="font-size:18px; font-weight:700; color:white;">
    Week-on-Week Comparison &nbsp;|&nbsp; Apr 13–19 vs Apr 20–26, 2026
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="chart-note" style="font-size:12px; color:#444;">'
    '<b>What does "Change vs Last Week" mean?</b> It shows how much a number went up or down compared to the previous week. '
    'A <span style="color:#1e8449;font-weight:bold;">green positive number</span> means improvement. '
    'A <span style="color:#c0392b;font-weight:bold;">red negative number</span> means it got worse. '
    'For failed transactions, fewer failures = better, so a decrease is shown in green.'
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
cw_vol  = df["Volume"].sum()
pw_vol  = df_prev["Volume"].sum()
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

w1.metric("Total Money Moved",    f"ETB {cw_vol/1e6:.1f}M",
          delta=f"{'+' if d_vol>=0 else ''}{d_vol:.1f}% vs last week")
w2.metric("Total Revenue",        f"ETB {cw_rev:,.0f}",
          delta=f"{'+' if d_rev>=0 else ''}{d_rev:.1f}% vs last week")
w3.metric("Total Transactions",   f"{cw_txns:,}",
          delta=f"{'+' if d_txns>=0 else ''}{d_txns:.1f}% vs last week")
w4.metric("Total Failed",         f"{int(cw_fail)}",
          delta=f"{'+' if d_fail>=0 else ''}{d_fail:.1f}% vs last week", delta_color="inverse")

st.markdown("---")
st.markdown("##### Merchant-by-Merchant Breakdown")

# Side-by-side Volume
fig_wow_vol = go.Figure()
fig_wow_vol.add_trace(go.Bar(
    name="Apr 13–19 (Last Week)",
    x=merged["Merchant"], y=merged["Vol_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v/1e6:.1f}M" for v in merged["Vol_PW"]], textposition="outside",
))
fig_wow_vol.add_trace(go.Bar(
    name="Apr 20–26 (This Week)",
    x=merged["Merchant"], y=merged["Vol_CW"],
    marker_color=MAIN_COLOR,
    text=[f"{v/1e6:.1f}M" for v in merged["Vol_CW"]], textposition="outside",
))
fig_wow_vol.update_layout(
    barmode="group", title="Money Moved; Last Week vs This Week (ETB)",
    plot_bgcolor="white", font=dict(size=10),
    margin=dict(t=40, b=10, l=10, r=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Side-by-side Revenue
fig_wow_rev = go.Figure()
fig_wow_rev.add_trace(go.Bar(
    name="Apr 13–19 (Last Week)",
    x=merged["Merchant"], y=merged["Rev_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v:,.0f}" for v in merged["Rev_PW"]], textposition="outside",
))
fig_wow_rev.add_trace(go.Bar(
    name="Apr 20–26 (This Week)",
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

# Success Rate comparison
fig_wow_sr = go.Figure()
fig_wow_sr.add_trace(go.Bar(
    name="Apr 13–19 (Last Week)",
    x=merged["Merchant"], y=merged["SR_PW"],
    marker_color=GOLD_COLOR,
    text=[f"{v:.1f}%" for v in merged["SR_PW"]], textposition="outside",
))
fig_wow_sr.add_trace(go.Bar(
    name="Apr 20–26 (This Week)",
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

# Failed transactions comparison
fig_wow_fail = go.Figure()
fig_wow_fail.add_trace(go.Bar(
    name="Apr 13–19 (Last Week)",
    x=merged["Merchant"], y=merged["Failed_PW"],
    marker_color=GOLD_COLOR,
    text=[str(int(v)) for v in merged["Failed_PW"]], textposition="outside",
))
fig_wow_fail.add_trace(go.Bar(
    name="Apr 20–26 (This Week)",
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
    'PW = Previous Week (Apr 13–19) | CW = Current Week (Apr 20–26) | '
    'Change = how much it moved up or down | '
    'SR = Success Rate | '
    '"Change in SR" = how many percentage points the success rate moved (e.g. +1.0 means it improved by 1%)'
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

    rows.append({
        "Merchant":                      r["Merchant"],
        "Vol Last Wk (M)":               f"{r['Vol_PW']/1e6:.1f}",
        "Vol This Wk (M)":               f"{r['Vol_CW']/1e6:.1f}",
        "Volume Change":                 fmt(dv),
        "Rev Last Wk":                   f"{r['Rev_PW']:,.0f}",
        "Rev This Wk":                   f"{r['Rev_CW']:,.0f}",
        "Revenue Change":                fmt(drv),
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
        "Analytics Cycle: April 20 - April 26, 2026  |  7 Merchants  |  Ethiopia (ETB)"
    )

    kpi_items = [
        ("Total Revenue",         f"ETB {dataframe['Revenue'].sum():,.2f}"),
        ("Total Money Moved",     f"ETB {dataframe['Volume'].sum()/1e6:.2f}M"),
        ("Total Txns",            f"{dataframe['Total_Txns'].sum():,}"),
        ("Avg Success Rate",      f"{dataframe['Success_Rate'].mean():.1f}%"),
        ("Est. Failed Value",     f"ETB {dataframe['Est_Failed_Value'].sum():,.0f}"),
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

    imgs4 = [img(f) for f in (fig_vol, fig_rev, fig_sr, fig_fail)]
    pdf.image(imgs4[0], x=10,  y=57,  w=93)
    pdf.image(imgs4[1], x=107, y=57,  w=93)
    pdf.image(imgs4[2], x=10,  y=108, w=93)
    pdf.image(imgs4[3], x=107, y=108, w=93)

    pdf.set_xy(10, 162)
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
        cells = [
            str(row["Merchant"]),
            f"{row['Volume']/1e6:.2f}",
            f"{row['Revenue']:,.0f}",
            str(int(row["Total_Txns"])),
            str(int(row["Failed"])),
            f"{row['Success_Rate']:.1f}%",
            f"{row['Avg_Txn_Value']:,.0f}",
        ]
        for val, w in zip(cells, widths):
            pdf.cell(w, 6, safe(val), 1, 0, "C", True)
        pdf.ln()

    # PAGE 2: Observations
    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB); pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB); pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Strategic Observations & Flags | Week of April 20-26, 2026"))

    obs_pdf = [
        ("Top Revenue Generator - REDSEADIRECTDEPOSITS",
         "ETB 451,954.15 in charges - up 11.3% from ETB 406,068.40 last week. "
         "JUBAEXPRESS follows at ETB 187,550.80 (up from ETB 156,211.25)."),
        ("CRITICAL - DEEROSERVICES Failure Rate Getting Worse",
         "19.7% failure rate (154/780 txns) - up from 18.67% last week. Blocked account errors on Kaafi MFI "
         "rose from 77 to 99. XML validation failures on CBO rose from 49 to 51. Escalation overdue."),
        ("REMITLYGLOBAL - Largest Merchant by Volume",
         "ETB 71.1M moved - up 39.7% from ETB 50.9M last week. 2,335 txns, 99.4% success rate. "
         "Only merchant using both bank and mobile channels. Zero charges."),
        ("REDSEA - Big Volume Jump",
         "Volume jumped 42.8% from ETB 29.4M to ETB 41.98M. 100% success (vs 1 failure last week). "
         "2 account debit txns (ETB 37M) carried no charges - billing treatment needs confirming."),
        ("Zero-Revenue - BIRRLINK and REMITLYGLOBAL",
         "Both posted ETB 0.00 for 2 consecutive weeks. Fee arrangement documentation needed urgently."),
        ("FINPAYAPPLICATION - Near-Perfect Week",
         "99.9% success, 1 reversed failure (ETB 60,950). Revenue ETB 60,879 - up from ETB 54,054."),
        ("Overall Portfolio Success Rate",
         "Average success rate this week: 97.1% vs 96.8% last week. "
         "DEEROSERVICES remains the single largest drag on portfolio performance."),
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
        y_pos += 25

    # PAGE 3: Week-on-Week charts
    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB); pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB); pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Week-on-Week Comparison | Apr 13-19 vs Apr 20-26, 2026"))

    # Portfolio delta boxes
    merged_loc = dataframe[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed"]].copy()
    merged_loc.columns = ["Merchant", "Vol_CW", "Rev_CW", "Txns_CW", "Failed_CW"]
    pv = prev_df[["Merchant", "Volume", "Revenue", "Total_Txns", "Failed"]].copy()
    pv.columns = ["Merchant", "Vol_PW", "Rev_PW", "Txns_PW", "Failed_PW"]
    mg = merged_loc.merge(pv, on="Merchant", how="left")

    pw_vol_t  = prev_df["Volume"].sum()
    pw_rev_t  = prev_df["Revenue"].sum()
    pw_txn_t  = prev_df["Total_Txns"].sum()
    pw_fail_t = prev_df["Failed"].sum()
    cw_vol_t  = dataframe["Volume"].sum()
    cw_rev_t  = dataframe["Revenue"].sum()
    cw_txn_t  = dataframe["Total_Txns"].sum()
    cw_fail_t = dataframe["Failed"].sum()

    def dpdf(cw, pw):
        if pw == 0: return "n/a"
        v = ((cw - pw) / pw) * 100
        return f"{'+'if v>=0 else ''}{v:.1f}% vs last week"

    kpi2 = [
        ("Total Money Moved",  f"ETB {cw_vol_t/1e6:.1f}M",    dpdf(cw_vol_t, pw_vol_t)),
        ("Total Revenue",      f"ETB {cw_rev_t:,.0f}",         dpdf(cw_rev_t, pw_rev_t)),
        ("Total Transactions", f"{int(cw_txn_t):,}",           dpdf(cw_txn_t, pw_txn_t)),
        ("Total Failed",       str(int(cw_fail_t)),             dpdf(cw_fail_t, pw_fail_t)),
    ]
    x = 10
    for lbl, val, delta in kpi2:
        pdf.set_fill_color(245, 246, 250); pdf.rect(x, 25, 45, 20, "F")
        pdf.set_fill_color(*GOLD_RGB); pdf.rect(x, 25, 45, 1.5, "F")
        pdf.set_xy(x, 28); pdf.set_font("Arial", "B", 6); pdf.set_text_color(110, 110, 110)
        pdf.cell(45, 4, safe(lbl), 0, 1, "C")
        pdf.set_xy(x, 33); pdf.set_font("Arial", "B", 8); pdf.set_text_color(*MAIN_RGB)
        pdf.cell(45, 4, safe(val), 0, 1, "C")
        pdf.set_xy(x, 39); pdf.set_font("Arial", size=6); pdf.set_text_color(80, 80, 80)
        pdf.cell(45, 4, safe(delta), 0, 1, "C")
        x += 47

    wow_imgs = [img(f) for f in (fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail)]
    pdf.image(wow_imgs[0], x=10,  y=50,  w=93)
    pdf.image(wow_imgs[1], x=107, y=50,  w=93)
    pdf.image(wow_imgs[2], x=10,  y=103, w=93)
    pdf.image(wow_imgs[3], x=107, y=103, w=93)

    # WoW text table
    pdf.set_xy(10, 158)
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
        row_cells = [
            str(r["Merchant"]),
            f"{r['Vol_PW']/1e6:.1f}", f"{r['Vol_CW']/1e6:.1f}",
            f"{'+'if dv_>=0 else ''}{dv_:.0f}%",
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
    pdf.text(10, 13, safe("Per-Merchant Breakdown | April 20-26, 2026"))

    y_pos = 27
    for _, row in dataframe.iterrows():
        if y_pos > 248:
            pdf.add_page(); y_pos = 15
        pdf.set_fill_color(*MAIN_RGB); pdf.rect(10, y_pos, 190, 7, "F")
        pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 8)
        pdf.text(12, y_pos + 5,
                 safe(f"{row['Merchant']}  |  [{row['Risk']} Risk]  |  Success: {row['Success_Rate']:.1f}%"))

        detail_rows = [
            [("Channel", row["Channel"]), ("Txn Types", row["TxnTypes"]),
             ("Total Txns", f"{int(row['Total_Txns']):,}"), ("Failed", str(int(row["Failed"]))),
             ("Total Moved", f"ETB {row['Volume']:,.0f}")],
            [("Revenue", f"ETB {row['Revenue']:,.2f}"),
             ("Avg Transaction Value", f"ETB {row['Avg_Txn_Value']:,.2f}"),
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
            pdf.cell(184, 4, safe(str(row["Notes"])[:110]), 0, 0)
            row_y += 8
        y_pos = row_y + 5

    return pdf.output(dest="S")


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("### FinPay Analytics")
st.sidebar.markdown("**Cycle:** Apr 20 to Apr 26, 2026")
st.sidebar.markdown(f"**Merchants:** {len(df)}")
st.sidebar.markdown(f"**Total Volume:** ETB {df['Volume'].sum()/1e6:.2f}M")
st.sidebar.markdown(f"**Total Revenue:** ETB {df['Revenue'].sum():,.2f}")
st.sidebar.divider()

if st.sidebar.button("Download Strategic PDF"):
    try:
        pdf_bytes = generate_pdf(
            df, df_prev,
            fig_vol, fig_rev, fig_sr, fig_fail,
            fig_margin, fig_ticket,
            fig_wow_vol, fig_wow_rev, fig_wow_sr, fig_wow_fail
        )
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode("latin-1")
        b64 = base64.b64encode(pdf_bytes).decode()
        href = (
            f'<a href="data:application/octet-stream;base64,{b64}" '
            f'download="Merchant360_Apr20_26_2026.pdf" '
            f'style="text-decoration:none; color:white; background:{MAIN_COLOR}; '
            f'padding:12px 16px; border-radius:5px; display:inline-block; font-size:13px;">'
            f'Save PDF Report</a>'
        )
        st.sidebar.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"PDF error: {e}")

st.sidebar.divider()
st.sidebar.markdown("**Risk Legend**")
st.sidebar.markdown("🔴 Red; Revenue or failure anomaly")
st.sidebar.markdown("🟡 Yellow; Elevated failure rate")
st.sidebar.markdown("🟢 Green; Normal operating range")


# streamlit run app.py
# .\venv\Scripts\activate