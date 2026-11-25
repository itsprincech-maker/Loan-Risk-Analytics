
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Business Analysis | Loan Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background-color: #10213B;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

h1, h2, h3 {
    color: #142B4A;
    font-weight: 700;
}

p, label {
    color: #52627A;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5EAF2;
    padding: 20px 22px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(20, 43, 74, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #142B4A;
    font-weight: 750;
}

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E5EAF2;
    border-radius: 14px;
    padding: 10px;
}

div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 12px;
}

.stDownloadButton button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

.stDownloadButton button:hover {
    background-color: #1D4ED8;
    color: white;
}

hr {
    border-color: #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA LOADING ----------------

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "loan_cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Credit_History"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Loan_Status"] = df["Loan_Status"].astype(str).str.strip()
    return df


df = load_data()


# ---------------- CHART STYLE ----------------

def style_chart(fig, height=350):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),
        title=dict(
            font=dict(size=16, color="#142B4A"),
            x=0.02
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=25, r=25, t=65, b=35),
        xaxis=dict(
            showgrid=False,
            linecolor="#E2E8F0"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EDF1F7",
            linecolor="#E2E8F0"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


# ---------------- HEADER ----------------

st.markdown(
    "<h1>Business Analysis</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "Understand customer segments, approval patterns, credit history "
    "and financial trends through interactive analytics."
)

st.markdown("---")


# ---------------- FILTERS ----------------

st.sidebar.markdown("## 📊 Analysis Controls")
st.sidebar.caption("Customize your business analysis")

education = st.sidebar.multiselect(
    "Education",
    sorted(df["Education"].dropna().unique()),
    default=sorted(df["Education"].dropna().unique())
)

property_area = st.sidebar.multiselect(
    "Property Area",
    sorted(df["Property_Area"].dropna().unique()),
    default=sorted(df["Property_Area"].dropna().unique())
)

credit_history = st.sidebar.multiselect(
    "Credit History",
    sorted(df["Credit_History"].dropna().unique()),
    default=sorted(df["Credit_History"].dropna().unique())
)

st.sidebar.markdown("---")
st.sidebar.caption("Loan Risk Analytics | Business Intelligence")


filtered = df[
    df["Education"].isin(education)
    & df["Property_Area"].isin(property_area)
    & df["Credit_History"].isin(credit_history)
].copy()


# ---------------- HELPER FUNCTION ----------------

def approval_chart(data, category, title, x_label):

    summary = (
        data.groupby(category, dropna=False)
        .agg(
            Applications=("Loan_Status", "size"),
            Approved=("Loan_Status", lambda x: (x == "Y").sum())
        )
        .reset_index()
    )

    summary["Approval Rate"] = (
        summary["Approved"] / summary["Applications"] * 100
    )

    summary[category] = (
        summary[category].fillna("Unknown").astype(str)
    )

    fig = px.bar(
        summary,
        x=category,
        y="Approval Rate",
        text="Approval Rate",
        color=category,
        labels={
            category: x_label,
            "Approval Rate": "Approval Rate (%)"
        },
        color_discrete_sequence=[
            "#2563EB", "#0F766E", "#7C3AED",
            "#D97706", "#0891B2"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, 110]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)


# ---------------- DATA CHECK ----------------

if filtered.empty:
    st.warning("No applications match the selected filters.")
    st.stop()


# ---------------- KPI SUMMARY ----------------

total = len(filtered)
approved = (filtered["Loan_Status"] == "Y").sum()
rejected = (filtered["Loan_Status"] == "N").sum()
approval_rate = approved / total * 100

st.markdown("### Business Performance Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Applications", f"{total:,}")
c2.metric("Approved Loans", f"{approved:,}")
c3.metric("Rejected Loans", f"{rejected:,}")
c4.metric("Approval Rate", f"{approval_rate:.2f}%")

st.markdown("---")


# ---------------- DEMOGRAPHIC ANALYSIS ----------------

st.markdown("### 1. Customer Demographics Analysis")

col1, col2 = st.columns(2)

with col1:
    approval_chart(
        filtered,
        "Education",
        "Education vs Loan Approval",
        "Education"
    )

with col2:
    approval_chart(
        filtered,
        "Property_Area",
        "Property Area vs Loan Approval",
        "Property Area"
    )

col3, col4 = st.columns(2)

with col3:
    approval_chart(
        filtered,
        "Married",
        "Marital Status vs Loan Approval",
        "Marital Status"
    )

with col4:
    approval_chart(
        filtered,
        "Gender",
        "Gender vs Loan Approval",
        "Gender"
    )

st.markdown("---")


# ---------------- CREDIT HISTORY ----------------

st.markdown("### 2. Credit History Risk Analysis")

credit_summary = (
    filtered.groupby("Credit_History", dropna=False)
    .agg(
        Applications=("Loan_Status", "size"),
        Approved=("Loan_Status", lambda x: (x == "Y").sum()),
        Rejected=("Loan_Status", lambda x: (x == "N").sum())
    )
    .reset_index()
)

credit_summary["Approval Rate"] = (
    credit_summary["Approved"] /
    credit_summary["Applications"] * 100
)

display_credit = credit_summary.copy()
display_credit["Credit_History"] = (
    display_credit["Credit_History"]
    .map({1.0: "Good Credit History", 0.0: "Poor Credit History"})
    .fillna("Unknown")
)

st.dataframe(
    display_credit,
    use_container_width=True,
    hide_index=True
)

fig_credit = px.bar(
    display_credit,
    x="Credit_History",
    y="Approval Rate",
    color="Credit_History",
    text="Approval Rate",
    color_discrete_sequence=["#0F766E", "#DC6B35", "#64748B"]
)

fig_credit.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_credit.update_layout(
    showlegend=False,
    yaxis_range=[0, 110]
)

st.plotly_chart(
    style_chart(fig_credit),
    use_container_width=True
)

st.markdown("---")


# ---------------- INCOME ANALYSIS ----------------

st.markdown("### 3. Income Analysis")

income_df = filtered.dropna(subset=["ApplicantIncome"]).copy()

income_df["Income Group"] = pd.cut(
    income_df["ApplicantIncome"],
    bins=[-float("inf"), 2500, 5000, 10000, float("inf")],
    labels=[
        "Low Income",
        "Medium Income",
        "High Income",
        "Very High Income"
    ]
)

approval_chart(
    income_df,
    "Income Group",
    "Applicant Income vs Loan Approval",
    "Income Group"
)


# ---------------- COAPPLICANT ANALYSIS ----------------

co_df = filtered.dropna(subset=["CoapplicantIncome"]).copy()

co_df["Coapplicant Group"] = pd.cut(
    co_df["CoapplicantIncome"],
    bins=[-0.01, 0, 2000, 5000, float("inf")],
    labels=[
        "No Coapplicant Income",
        "Low Income",
        "Medium Income",
        "High Income"
    ]
)

approval_chart(
    co_df,
    "Coapplicant Group",
    "Coapplicant Income vs Loan Approval",
    "Coapplicant Income Group"
)

st.markdown("---")


# ---------------- LOAN AMOUNT ANALYSIS ----------------

st.markdown("### 4. Loan Amount Analysis")

loan_df = filtered.dropna(subset=["LoanAmount"]).copy()

loan_df["Loan Group"] = pd.cut(
    loan_df["LoanAmount"],
    bins=[-float("inf"), 100, 200, 300, float("inf")],
    labels=[
        "Small Loan",
        "Medium Loan",
        "Large Loan",
        "Very Large Loan"
    ]
)

approval_chart(
    loan_df,
    "Loan Group",
    "Loan Amount vs Loan Approval",
    "Loan Amount Group"
)

st.markdown("---")


# ---------------- FAMILY & EMPLOYMENT ----------------

st.markdown("### 5. Family & Employment Analysis")

col5, col6 = st.columns(2)

with col5:
    approval_chart(
        filtered,
        "Dependents",
        "Dependents vs Loan Approval",
        "Number of Dependents"
    )

with col6:
    approval_chart(
        filtered,
        "Self_Employed",
        "Employment Status vs Loan Approval",
        "Self Employed"
    )


# ---------------- EXPORT ----------------

st.markdown("---")
st.markdown("### Download Business Analysis Data")

st.write(
    "Export the filtered loan application records for further analysis."
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Business Analysis CSV",
    data=csv,
    file_name="loan_business_analysis.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Loan Risk Analytics | Business Intelligence Module"
)
