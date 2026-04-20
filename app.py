import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import base64
import io
import datetime

MAIN_COLOR = "#081b31"
GOLD_COLOR = "#8e6d2d"
LIGHT_BG   = "#f5f3ef"


def safe(text):
    """Strip any character outside latin-1 so fpdf never raises a Unicode error."""
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


st.set_page_config(page_title="Merchant 360 ; Weekly Strategic Report", layout="wide")

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
</style>
""", unsafe_allow_html=True)


def load_data():
    records = [
        {
            "Merchant":     "REDSEA",
            "TxnTypes":     "DISBURSEMENTS",
            "Channel":      "Bank",
            "Volume":       29_400_692.00,
            "Revenue":      54_006.92,
            "Successful":   28,
            "Failed":       1,
            "Pending":      0,
            "Avg_Charge":   2_000.26,
            "Avg_Ticket":   1_088_914.52,
            "Risk":         "Low",
            "Top_Failures": "Payment Failed (1)",
            "Networks":     "CBE, Bank of Abyssinia + others",
            "Notes":        "1 failure ; Payment Failed. Highest avg ticket (ETB 1.09M). Low volume, high-value profile.",
        },
        {
            "Merchant":     "FINPAY APP",
            "TxnTypes":     "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":      "Bank",
            "Volume":       31_892_665.10,
            "Revenue":      54_054.00,
            "Successful":   596,
            "Failed":       0,
            "Pending":      0,
            "Avg_Charge":   90.69,
            "Avg_Ticket":   53_511.18,
            "Risk":         "Low",
            "Top_Failures": "None",
            "Networks":     "Multiple Ethiopian banks",
            "Notes":        "Perfect 100% success rate. Zero failures across 596 transactions.",
        },
        {
            "Merchant":     "JUBAEXPRESS",
            "TxnTypes":     "DISBURSEMENTS",
            "Channel":      "Bank",
            "Volume":       39_051_740.00,
            "Revenue":      156_211.25,
            "Successful":   1_274,
            "Failed":       4,
            "Pending":      0,
            "Avg_Charge":   122.61,
            "Avg_Ticket":   30_652.86,
            "Risk":         "Low",
            "Top_Failures": "XML validation failed (2), Missing reversed (1), System Error (1)",
            "Networks":     "CBE (965), Bank of Abyssinia (241), Awash (42) + 10 others",
            "Notes":        "0.31% failure rate ; well-controlled. Highest txn revenue ETB 156K. All failures reversed.",
        },
        {
            "Merchant":     "BIRRLINK",
            "TxnTypes":     "DISBURSEMENTS",
            "Channel":      "Bank",
            "Volume":       663_098.79,
            "Revenue":      0.00,
            "Successful":   19,
            "Failed":       1,
            "Pending":      0,
            "Avg_Charge":   0.00,
            "Avg_Ticket":   34_899.94,
            "Risk":         "High",
            "Top_Failures": "UNFN reversed (1) ; Abay Bank",
            "Networks":     "CBE, Bank of Abyssinia, Abay Bank, Awash",
            "Notes":        "Zero charges recorded ; possible waived-fee arrangement. Small volume merchant. ETB 0 revenue flag.",
        },
        {
            "Merchant":     "DEEROSERVICES",
            "TxnTypes":     "DISBURSEMENTS",
            "Channel":      "Bank",
            "Volume":       20_681_002.00,
            "Revenue":      49_959.00,
            "Successful":   549,
            "Failed":       126,
            "Pending":      0,
            "Avg_Charge":   91.00,
            "Avg_Ticket":   37_670.31,
            "Risk":         "Medium",
            "Top_Failures": "BLCK reversed (77, Kaafi MFI), XML validation failed (49, CBO)",
            "Networks":     "CBE (344), Kaafi Micro Finance (192), CBO (88), Bank of Abyssinia (32)",
            "Notes":        "18.67% failure rate ; highest in portfolio. BLCK errors on Kaafi MFI suggest account-level blocks. Urgent investigation needed.",
        },
        {
            "Merchant":     "REMITLYGLOBAL",
            "TxnTypes":     "DISBURSEMENTS, ACCOUNT_DEBIT",
            "Channel":      "Bank + Mobile",
            "Volume":       50_864_641.87,
            "Revenue":      0.00,
            "Successful":   1_924,
            "Failed":       15,
            "Pending":      0,
            "Avg_Charge":   0.00,
            "Avg_Ticket":   26_436.92,
            "Risk":         "Low",
            "Top_Failures": "Creditor agent error (8, Bank of Abyssinia), System error (3), Technical error (2, CBE Birr)",
            "Networks":     "CBE (1310), Bank of Abyssinia (466), CBE Birr/Mobile (77), Dashen (59)",
            "Notes":        "Only merchant using both bank & mobile channels. Zero charges ; likely net-settlement. 8 creditor agent errors on BoA need flagging.",
        },
        {
            "Merchant":     "REDSEADIRECTDEPOSITS",
            "TxnTypes":     "DISBURSEMENTS",
            "Channel":      "Bank",
            "Volume":       40_606_822.45,
            "Revenue":      406_068.40,
            "Successful":   869,
            "Failed":       9,
            "Pending":      0,
            "Avg_Charge":   467.28,
            "Avg_Ticket":   46_728.22,
            "Risk":         "Low",
            "Top_Failures": "XML validation failed (3), Exception on bank transfer (2), Missing account (2), UNFN (1), Payment Failed (1)",
            "Networks":     "CBE (583), Bank of Abyssinia (243), Awash (30), Dashen (13), CBO (5)",
            "Notes":        "Highest avg charge (ETB 467.28) and highest avg ticket (ETB 46.7K). ETB 5,696.41 charges on 9 failed txns ; verify refund status.",
        },
    ]

    df = pd.DataFrame(records)
    df["Total_Txns"]     = df["Successful"] + df["Failed"] + df["Pending"]
    df["Success_Rate"]   = (df["Successful"] / df["Total_Txns"]) * 100
    df["Leakage"]        = df["Failed"] * df["Avg_Ticket"]
    df["Rev_Margin_BPS"] = (df["Revenue"] / df["Volume"].replace(0, 1)) * 10_000
    return df


df = load_data()

st.markdown(f"""
<div class="header-band">
  <span style="font-size:22px; font-weight:700; letter-spacing:1px; color:white;">
    MERCHANT 360 &nbsp;;&nbsp; WEEKLY STRATEGIC REPORT
  </span><br>
  <span style="font-size:13px; opacity:0.85; color:white;">
    Analytics Cycle: April 13 to April 19, 2026 &nbsp;&middot;&nbsp;
    7 Merchants &nbsp;&middot;&nbsp; Ethiopia (ETB)
  </span>
</div>
""", unsafe_allow_html=True)


k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Weekly Revenue",    f"ETB {df['Revenue'].sum():,.2f}")
k2.metric("Gross Volume Moved",      f"ETB {df['Volume'].sum():,.2f}")
k3.metric("Total Transactions",      f"{df['Total_Txns'].sum():,}")
k4.metric("Avg System Success Rate", f"{df['Success_Rate'].mean():.2f}%")
k5.metric("Est. Leakage (Failed)",   f"ETB {df['Leakage'].sum():,.2f}")

st.divider()

c1, c2 = st.columns(2)

with c1:
    fig_vol = px.bar(
        df.sort_values("Volume"),
        x="Volume", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Gross Volume by Merchant (ETB)",
        text=df.sort_values("Volume")["Volume"].apply(lambda v: f"{v/1e6:.1f}M"),
    )
    fig_vol.update_traces(textposition="outside")
    fig_vol.update_layout(plot_bgcolor="white", font=dict(size=10),
                          margin=dict(t=40, b=10, l=10, r=70),
                          xaxis_title="", yaxis_title="")
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
                          margin=dict(t=40, b=10, l=10, r=10),
                          xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_rev, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    pie_colors = [
        MAIN_COLOR, GOLD_COLOR, "#1a5276", "#b8860b",
        "#2e86c1", "#c0a060", "#0d2d52",
    ]
    fig_pie = px.pie(
        df,
        names="Merchant",
        values="Success_Rate",
        title="Success Rate by Merchant (%)",
        color_discrete_sequence=pie_colors,
        hole=0.35,
    )
    fig_pie.update_traces(
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Success Rate: %{value:.2f}%<extra></extra>",
    )
    fig_pie.update_layout(
        plot_bgcolor="white", font=dict(size=10),
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=True,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c4:
    fig_fail = px.bar(
        df.sort_values("Failed", ascending=False),
        x="Merchant", y="Failed",
        color="Risk",
        color_discrete_map={"High": "#c0392b", "Medium": "#d4ac0d", "Low": "#1e8449"},
        title="Failed Transactions by Merchant",
        text="Failed",
    )
    fig_fail.update_traces(textposition="outside")
    fig_fail.update_layout(plot_bgcolor="white", font=dict(size=10),
                           margin=dict(t=40, b=10, l=10, r=10),
                           xaxis_title="", yaxis_title="# Failed Txns")
    st.plotly_chart(fig_fail, use_container_width=True)

c5, c6 = st.columns(2)

with c5:
    fig_margin = px.bar(
        df.sort_values("Rev_Margin_BPS"),
        x="Rev_Margin_BPS", y="Merchant", orientation="h",
        color_discrete_sequence=[GOLD_COLOR],
        title="Revenue Margin (Basis Points on Volume)",
        text=df.sort_values("Rev_Margin_BPS")["Rev_Margin_BPS"].apply(lambda v: f"{v:.1f} bps"),
    )
    fig_margin.update_traces(textposition="outside")
    fig_margin.update_layout(plot_bgcolor="white", font=dict(size=10),
                             margin=dict(t=40, b=10, l=10, r=90),
                             xaxis_title="BPS", yaxis_title="")
    st.plotly_chart(fig_margin, use_container_width=True)

with c6:
    fig_ticket = px.bar(
        df.sort_values("Avg_Ticket"),
        x="Avg_Ticket", y="Merchant", orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
        title="Average Transaction Value by Merchant (ETB)",
        text=df.sort_values("Avg_Ticket")["Avg_Ticket"].apply(lambda v: f"{v:,.0f}"),
    )
    fig_ticket.update_traces(textposition="outside")
    fig_ticket.update_layout(plot_bgcolor="white", font=dict(size=10),
                             margin=dict(t=40, b=10, l=10, r=90),
                             xaxis_title="ETB", yaxis_title="")
    st.plotly_chart(fig_ticket, use_container_width=True)

st.divider()

st.markdown("#### Comprehensive Weekly Audit Trail")

audit_df = df[[
    "Merchant", "Channel", "Risk", "Total_Txns", "Successful", "Failed",
    "Pending", "Volume", "Revenue", "Avg_Charge", "Avg_Ticket",
    "Success_Rate", "Leakage",
]].copy()

st.dataframe(
    audit_df.style
    .format({
        "Volume":       "{:,.2f}",
        "Revenue":      "{:,.2f}",
        "Avg_Charge":   "{:,.2f}",
        "Avg_Ticket":   "{:,.2f}",
        "Success_Rate": "{:.2f}%",
        "Leakage":      "{:,.2f}",
    })
    .applymap(
        lambda v: "background-color:#fdecea" if isinstance(v, str) and v == "High"
        else ("background-color:#fef9e7" if isinstance(v, str) and v == "Medium" else ""),
        subset=["Risk"],
    )
    .bar(subset=["Success_Rate"], color=["#c0392b", "#1e8449"], vmin=80, vmax=100)
    .bar(subset=["Volume"], color="#d6e4f0"),
    use_container_width=True,
    height=320,
)

st.divider()

st.markdown("#### Strategic Observations & Flags")

observations = [
    ("Top Revenue Generator",
     "REDSEADIRECTDEPOSITS leads with ETB 406,068 in charges (highest revenue margin in basis points). "
     "JUBAEXPRESS follows at ETB 156,211. REDSEA handles ultra-high-value transfers averaging ETB 1.09M per transaction."),
    ("CRITICAL ; DEEROSERVICES Failure Rate",
     "18.67% failure rate (126 of 675 txns) ; the highest in the portfolio this week. "
     "Two dominant causes: BLCK errors on Kaafi Micro Finance (77 failures, likely account-level blocks) "
     "and XML validation failures on Cooperative Bank of Oromia (49 failures). Immediate investigation recommended."),
    ("Zero-Revenue Merchants ; BIRRLINK and REMITLYGLOBAL",
     "Both merchants recorded ETB 0.00 in charges. For REMITLYGLOBAL (ETB 50.8M volume, 1,939 txns) this likely "
     "reflects a net-settlement or invoiced billing arrangement. For BIRRLINK (only 20 txns), the arrangement "
     "should be confirmed to avoid revenue leakage."),
    ("Bank of Abyssinia Recurring Issue ; REMITLYGLOBAL",
     "8 of 15 REMITLYGLOBAL failures were creditor agent errors concentrated on Bank of Abyssinia. "
     "This is a persistent integration pattern that warrants a formal escalation to BoA technical team."),
    ("FINPAY APP ; Perfect Week",
     "100% success rate across 596 transactions and ETB 31.9M in volume. "
     "The only merchant with zero failures this cycle."),
    ("REDSEADIRECTDEPOSITS ; Charges on Failed Txns",
     "ETB 5,696.41 in charges were applied to the 9 failed transactions. "
     "Confirm whether these have been or will be refunded to the merchant to avoid a dispute."),
    ("Highest Average Transaction Value",
     "REDSEA leads with ETB 1,088,914.52 per transaction (28 txns) ; a very low-volume, ultra-high-value profile. "
     "REDSEADIRECTDEPOSITS follows at ETB 46,728.22. Both are remittance-oriented merchants."),
]

for title, body in observations:
    st.markdown(f"""
    <div class="observation-box">
      <strong style="color:{MAIN_COLOR};">{title}</strong><br>{body}
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("#### Per-Merchant Detail")

for _, row in df.iterrows():
    with st.expander(f"{row['Merchant']}  ;  {row['Risk']} Risk  |  Success: {row['Success_Rate']:.2f}%"):
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Txns",   f"{row['Total_Txns']:,}")
        d2.metric("Volume (ETB)", f"{row['Volume']:,.2f}")
        d3.metric("Revenue",      f"ETB {row['Revenue']:,.2f}")
        d4.metric("Failed",       str(int(row["Failed"])))

        d5, d6, d7 = st.columns(3)
        d5.metric("Avg Ticket",  f"ETB {row['Avg_Ticket']:,.2f}")
        d6.metric("Avg Charge",  f"ETB {row['Avg_Charge']:,.2f}")
        d7.metric("Channel",     row["Channel"])

        st.markdown(f"**Transaction Types:** {row['TxnTypes']}")
        st.markdown(f"**Top Networks:** {row['Networks']}")
        st.markdown(f"**Top Failures:** {row['Top_Failures']}")
        if row["Notes"]:
            st.markdown(
                f'<div class="flag-box">{row["Notes"]}</div>',
                unsafe_allow_html=True,
            )

st.divider()


def generate_pdf(dataframe, fig_vol, fig_rev, fig_pie, fig_fail, fig_margin, fig_ticket):

    def chart_img(fig, w=700, h=380):
        return io.BytesIO(fig.to_image(format="png", width=w, height=h, scale=2))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)

   
    pdf.add_page()

    # Header
    pdf.set_fill_color(*MAIN_RGB)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_fill_color(*GOLD_RGB)
    pdf.rect(0, 30, 210, 2, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 14)
    pdf.text(10, 13, safe("MERCHANT 360 ; WEEKLY STRATEGIC REPORT"))
    pdf.set_font("Arial", size=8)
    pdf.text(10, 21, safe("Analytics Cycle: April 13 - April 19, 2026  |  7 Merchants  |  Ethiopia (ETB)"))
    pdf.text(10, 27, safe(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"))

    # KPI boxes 
    kpi_items = [
        ("Total Revenue",  f"ETB {dataframe['Revenue'].sum():,.2f}"),
        ("Gross Volume",   f"ETB {dataframe['Volume'].sum()/1e6:.2f}M"),
        ("Total Txns",     f"{dataframe['Total_Txns'].sum():,}"),
        ("Avg Success",    f"{dataframe['Success_Rate'].mean():.1f}%"),
        ("Est. Leakage",   f"ETB {dataframe['Leakage'].sum():,.0f}"),
    ]
    x = 10
    for lbl, val in kpi_items:
        pdf.set_fill_color(245, 246, 250)
        pdf.rect(x, 35, 37, 18, "F")
        pdf.set_fill_color(*GOLD_RGB)
        pdf.rect(x, 35, 37, 1.5, "F")
        pdf.set_xy(x, 38)
        pdf.set_font("Arial", "B", 6)
        pdf.set_text_color(110, 110, 110)
        pdf.cell(37, 4, safe(lbl), 0, 1, "C")
        pdf.set_xy(x, 43)
        pdf.set_font("Arial", "B", 8)
        pdf.set_text_color(*MAIN_RGB)
        pdf.cell(37, 4, safe(val), 0, 1, "C")
        x += 39

    # Chart grid 2x2 (vol, rev, pie, fail)
    imgs = [chart_img(f) for f in (fig_vol, fig_rev, fig_pie, fig_fail)]
    pdf.image(imgs[0], x=10,  y=57, w=93)
    pdf.image(imgs[1], x=107, y=57, w=93)
    pdf.image(imgs[2], x=10,  y=108, w=93)
    pdf.image(imgs[3], x=107, y=108, w=93)

    # Audit table
    pdf.set_xy(10, 162)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(190, 7, safe("Comprehensive Weekly Audit Trail"), ln=True)

    hdrs   = ["Merchant", "Vol (M ETB)", "Revenue", "Txns", "Failed", "Success%", "Avg Ticket"]
    widths = [36, 28, 28, 16, 16, 24, 32]

    pdf.set_font("Arial", "B", 7)
    pdf.set_fill_color(*MAIN_RGB)
    pdf.set_text_color(255, 255, 255)
    for h, w in zip(hdrs, widths):
        pdf.cell(w, 7, safe(h), 1, 0, "C", True)
    pdf.ln()

    pdf.set_font("Arial", size=7)
    for i, (_, row) in enumerate(dataframe.iterrows()):
        if row["Risk"] == "High":
            pdf.set_fill_color(253, 235, 233)
        elif row["Risk"] == "Medium":
            pdf.set_fill_color(254, 249, 231)
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
            f"{row['Avg_Ticket']:,.0f}",
        ]
        for val, w in zip(cells, widths):
            pdf.cell(w, 6, safe(val), 1, 0, "C", True)
        pdf.ln()


    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB)
    pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB)
    pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Strategic Observations & Flags ; Week of April 13-19, 2026"))

    obs_pdf = [
        ("Top Revenue Generator",
         "REDSEADIRECTDEPOSITS: ETB 406,068 (highest BPS margin). JUBAEXPRESS: ETB 156,211. "
         "REDSEA handles ultra-high-value txns averaging ETB 1.09M each."),
        ("CRITICAL ; DEEROSERVICES Failure Rate",
         "18.67% failure rate (126/675 txns). BLCK errors on Kaafi Micro Finance (77 failures) "
         "and XML validation failures on Cooperative Bank of Oromia (49 failures). Immediate action required."),
        ("Zero-Revenue Merchants ; BIRRLINK and REMITLYGLOBAL",
         "Both show ETB 0.00 charges. REMITLYGLOBAL (ETB 50.8M, 1,939 txns) likely on net-settlement. "
         "BIRRLINK arrangement needs confirmation to avoid revenue leakage."),
        ("Bank of Abyssinia ; Recurring Issue",
         "8/15 REMITLYGLOBAL failures are creditor agent errors on Bank of Abyssinia. "
         "Formal escalation to BoA technical team recommended."),
        ("FINPAY APP ; Perfect Week",
         "100% success rate, 596 transactions, ETB 31.9M volume. Zero failures this cycle."),
        ("REDSEADIRECTDEPOSITS ; Charges on Failed Txns",
         "ETB 5,696.41 in charges applied to 9 failed transactions. Confirm refund processing status."),
        ("Highest Average Transaction Value",
         "REDSEA leads at ETB 1,088,914.52 per txn. REDSEADIRECTDEPOSITS follows at ETB 46,728.22. "
         "Both are remittance-oriented merchants."),
    ]

    y_pos = 27
    for title, body in obs_pdf:
        if y_pos > 265:
            pdf.add_page()
            y_pos = 15
        pdf.set_fill_color(*GOLD_RGB)
        pdf.rect(10, y_pos, 2.5, 16, "F")
        pdf.set_xy(15, y_pos + 1)
        pdf.set_font("Arial", "B", 9)
        pdf.set_text_color(*MAIN_RGB)
        pdf.cell(183, 5, safe(title), ln=True)
        pdf.set_xy(15, y_pos + 8)
        pdf.set_font("Arial", size=8)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(183, 4, safe(body))
        y_pos += 25

    pdf.add_page()
    pdf.set_fill_color(*MAIN_RGB)
    pdf.rect(0, 0, 210, 20, "F")
    pdf.set_fill_color(*GOLD_RGB)
    pdf.rect(0, 20, 210, 2, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 11)
    pdf.text(10, 13, safe("Per-Merchant Breakdown ; April 13-19, 2026"))

    # margin + ticket charts side by side
    m_img = chart_img(fig_margin)
    t_img = chart_img(fig_ticket)
    pdf.image(m_img, x=10,  y=25, w=93)
    pdf.image(t_img, x=107, y=25, w=93)

    y_pos = 80
    for _, row in dataframe.iterrows():
        if y_pos > 248:
            pdf.add_page()
            y_pos = 15

        # Merchant header bar
        pdf.set_fill_color(*MAIN_RGB)
        pdf.rect(10, y_pos, 190, 7, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 8)
        pdf.text(12, y_pos + 5,
                 safe(f"{row['Merchant']}  ;  [{row['Risk']} Risk]  ;  Success: {row['Success_Rate']:.1f}%"))

        # Two detail rows
        pdf.set_text_color(0, 0, 0)
        detail_rows = [
            [("Channel", row["Channel"]),
             ("Txn Types", row["TxnTypes"]),
             ("Total Txns", f"{int(row['Total_Txns']):,}"),
             ("Failed", str(int(row["Failed"]))),
             ("Volume", f"ETB {row['Volume']:,.0f}")],
            [("Revenue", f"ETB {row['Revenue']:,.2f}"),
             ("Avg Ticket", f"ETB {row['Avg_Ticket']:,.2f}"),
             ("Avg Charge", f"ETB {row['Avg_Charge']:,.2f}"),
             ("Top Failures", str(row["Top_Failures"])[:45])],
        ]
        row_y = y_pos + 9
        for drow in detail_rows:
            cw = 190 // len(drow)
            x_pos = 10
            for lbl, val in drow:
                pdf.set_xy(x_pos, row_y)
                pdf.set_font("Arial", "B", 6)
                pdf.set_text_color(120, 120, 120)
                pdf.cell(cw, 3.5, safe(lbl + ":"), 0, 0)
                pdf.set_xy(x_pos, row_y + 3.5)
                pdf.set_font("Arial", size=7)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(cw, 4, safe(str(val)), 0, 0)
                x_pos += cw
            row_y += 9

        # Notes strip
        if row["Notes"]:
            pdf.set_fill_color(253, 248, 235)
            note_h = 8
            pdf.rect(10, row_y, 190, note_h, "F")
            pdf.set_fill_color(*GOLD_RGB)
            pdf.rect(10, row_y, 2, note_h, "F")
            pdf.set_xy(14, row_y + 2)
            pdf.set_font("Arial", size=7)
            pdf.set_text_color(80, 60, 20)
            pdf.cell(184, 4, safe(str(row["Notes"])[:110]), 0, 0)
            row_y += note_h

        y_pos = row_y + 5

    return pdf.output(dest="S")

st.sidebar.markdown("### FinPay Analytics")
st.sidebar.markdown("**Cycle:** Apr 13 to Apr 19, 2026")
st.sidebar.markdown(f"**Merchants:** {len(df)}")
st.sidebar.markdown(f"**Total Volume:** ETB {df['Volume'].sum()/1e6:.2f}M")
st.sidebar.markdown(f"**Total Revenue:** ETB {df['Revenue'].sum():,.2f}")
st.sidebar.divider()

if st.sidebar.button("Download Strategic PDF"):
    try:
        pdf_bytes = generate_pdf(
            df, fig_vol, fig_rev, fig_pie, fig_fail, fig_margin, fig_ticket
        )
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode("latin-1")
        b64 = base64.b64encode(pdf_bytes).decode()
        href = (
            f'<a href="data:application/octet-stream;base64,{b64}" '
            f'download="Merchant360_Apr13_19_2026.pdf" '
            f'style="text-decoration:none; color:white; background:{MAIN_COLOR}; '
            f'padding:12px 16px; border-radius:5px; display:inline-block; font-size:13px;">'
            f'Save PDF Report</a>'
        )
        st.sidebar.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"PDF error: {e}")

st.sidebar.divider() 
st.sidebar.markdown("**Risk Legend**")
st.sidebar.markdown("Red ; Revenue/failure anomaly")
st.sidebar.markdown("Yellow ; Elevated failure rate")
st.sidebar.markdown("Green ; Normal operating range")

# streamlit run app.py
# .\venv\Scripts\activate