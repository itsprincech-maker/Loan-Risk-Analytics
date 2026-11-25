
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Loan Risk Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #F4F7FB;
    color: #172B4D;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10233F;
}

section[data-testid="stSidebar"] * {
    color: #E8EFF8;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: #FFFFFF;
    border-radius: 8px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172B4D;
}

/* Headings */
h1 {
    color: #10233F !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #17365D !important;
    font-weight: 650 !important;
}

/* KPI Cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 22px 20px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 12px rgba(16, 35, 63, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #10233F !important;
    font-weight: 750;
}

/* Charts and containers */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 10px;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
}

/* Buttons */
.stDownloadButton button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

.stDownloadButton button:hover {
    background: #1D4ED8;
    color: white;
}

/* Divider */
hr {
    border-color: #DCE4EF;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATA LOADING
# =====================================================

DATA_PATH = Path(__file__).parent / "data" / "loan_cleaned.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Loan_Status"] = (
        df["Loan_Status"].astype(str).str.strip()
    )

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error("loan_cleaned.csv not found in the data folder.")
    st.stop()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🏦 Loan Analytics")
    st.caption("FINANCIAL INTELLIGENCE PLATFORM")

    st.markdown("---")

    st.markdown("### 🎛️ Dashboard Filters")

    def add_filter(column, label):
        options = sorted(
            df[column].dropna().unique().tolist()
        )

        return st.multiselect(
            label,
            options,
            default=options,
            key=f"filter_{column}"
        )

    education_filter = add_filter(
        "Education", "Education"
    )

    property_filter = add_filter(
        "Property_Area", "Property Area"
    )

    gender_filter = add_filter(
        "Gender", "Gender"
    )

    married_filter = add_filter(
        "Married", "Marital Status"
    )

    credit_filter = add_filter(
        "Credit_History", "Credit History"
    )

    st.markdown("---")

    st.markdown("### 📌 About Dashboard")

    st.caption(
        "Analyze loan applications, approval trends "
        "and applicant risk patterns."
    )

    st.markdown("---")

    st.caption("Built with Python | Streamlit | Plotly")


# =====================================================
# 5. FILTER DATA
# =====================================================

filtered_df = df[
    df["Education"].isin(education_filter)
    & df["Property_Area"].isin(property_filter)
    & df["Gender"].isin(gender_filter)
    & df["Married"].isin(married_filter)
    & df["Credit_History"].isin(credit_filter)
].copy()


# =====================================================
# 6. HEADER
# =====================================================

st.markdown(
    "<p style='color:#2563EB; font-weight:700; "
    "letter-spacing:2px; font-size:12px;'>"
    "FINANCIAL ANALYTICS / OVERVIEW"
    "</p>",
    unsafe_allow_html=True
)

st.title("Loan Approval & Risk Analytics")

st.markdown(
    "<p style='color:#64748B; font-size:16px;'>"
    "Monitor loan applications, understand approval "
    "patterns and explore customer risk indicators."
    "</p>",
    unsafe_allow_html=True
)

st.markdown("---")


# =====================================================
# 7. KPI CALCULATIONS
# =====================================================

total_applications = len(filtered_df)

approved = (
    filtered_df["Loan_Status"] == "Y"
).sum()

rejected = (
    filtered_df["Loan_Status"] == "N"
).sum()

approval_rate = (
    approved / total_applications * 100
    if total_applications > 0 else 0
)

rejection_rate = (
    rejected / total_applications * 100
    if total_applications > 0 else 0
)

avg_income = filtered_df["ApplicantIncome"].mean()
avg_loan = filtered_df["LoanAmount"].mean()


# =====================================================
# 8. KPI CARDS
# =====================================================

st.subheader("📊 Business Overview")

st.caption("Key performance indicators based on selected filters.")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Applications",
    f"{total_applications:,}"
)

c2.metric(
    "Approved Loans",
    f"{approved:,}"
)

c3.metric(
    "Rejected Loans",
    f"{rejected:,}"
)

c4.metric(
    "Approval Rate",
    f"{approval_rate:.2f}%"
)

c5, c6, c7 = st.columns(3)

c5.metric(
    "Rejection Rate",
    f"{rejection_rate:.2f}%"
)

c6.metric(
    "Average Applicant Income",
    f"{avg_income:,.0f}" if pd.notna(avg_income) else "N/A"
)

c7.metric(
    "Average Loan Amount",
    f"{avg_loan:,.2f}" if pd.notna(avg_loan) else "N/A"
)


# =====================================================
# 9. CHART HELPER
# =====================================================

def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="Arial",
            color="#334155"
        ),
        title_font=dict(
            size=17,
            color="#10233F"
        ),
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=35
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="white",
            font_color="#10233F"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E8F0"
    )

    fig.update_yaxes(
        gridcolor="#EDF1F7",
        zeroline=False
    )

    return fig


# =====================================================
# 10. APPROVAL DISTRIBUTION
# =====================================================

st.markdown("---")
st.subheader("📈 Loan Approval Distribution")

if total_applications > 0:

    status_data = pd.DataFrame({
        "Status": ["Approved", "Rejected"],
        "Applications": [approved, rejected]
    })

    fig1 = px.pie(
        status_data,
        names="Status",
        values="Applications",
        hole=0.65,
        color="Status",
        color_discrete_map={
            "Approved": "#16A34A",
            "Rejected": "#EF4444"
        }
    )

    fig1.update_traces(
        textinfo="percent+label",
        textfont_size=13
    )

    fig1 = style_chart(fig1)

    fig1.update_layout(
        title="Approved vs Rejected Applications",
        showlegend=True
    )

    st.plotly_chart(fig1, use_container_width=True)

else:
    st.info("No applications available for selected filters.")


# =====================================================
# 11. APPROVAL RATE HELPER
# =====================================================

def calculate_approval(data, column):
    return (
        data.groupby(column)["Loan_Status"]
        .apply(lambda x: (x == "Y").mean() * 100)
        .reset_index(name="Approval Rate")
    )


# =====================================================
# 12. CREDIT HISTORY & EDUCATION
# =====================================================

st.markdown("---")
st.subheader("🔍 Applicant Profile Analysis")

col1, col2 = st.columns(2)

with col1:

    credit_data = calculate_approval(
        filtered_df.dropna(subset=["Credit_History"]),
        "Credit_History"
    )

    if not credit_data.empty:

        credit_data["Credit_History"] = (
            credit_data["Credit_History"].map({
                1: "Good Credit History",
                0: "Poor Credit History"
            }).fillna(credit_data["Credit_History"].astype(str))
        )

        fig2 = px.bar(
            credit_data,
            x="Credit_History",
            y="Approval Rate",
            color="Credit_History",
            text_auto=".2f",
            color_discrete_sequence=["#2563EB", "#60A5FA"],
            title="Approval Rate by Credit History"
        )

        fig2.update_layout(showlegend=False)
        fig2.update_yaxes(range=[0, 100])

        st.plotly_chart(
            style_chart(fig2),
            use_container_width=True
        )

with col2:

    education_data = calculate_approval(
        filtered_df,
        "Education"
    )

    if not education_data.empty:

        fig3 = px.bar(
            education_data,
            x="Education",
            y="Approval Rate",
            color="Education",
            text_auto=".2f",
            color_discrete_sequence=["#2563EB", "#93C5FD"],
            title="Approval Rate by Education"
        )

        fig3.update_layout(showlegend=False)
        fig3.update_yaxes(range=[0, 100])

        st.plotly_chart(
            style_chart(fig3),
            use_container_width=True
        )


# =====================================================
# 13. PROPERTY AREA & INCOME
# =====================================================

st.markdown("---")
st.subheader("💼 Financial & Property Analysis")

col3, col4 = st.columns(2)

with col3:

    property_data = calculate_approval(
        filtered_df,
        "Property_Area"
    )

    if not property_data.empty:

        fig4 = px.bar(
            property_data,
            x="Property_Area",
            y="Approval Rate",
            color="Property_Area",
            text_auto=".2f",
            color_discrete_sequence=[
                "#2563EB", "#60A5FA", "#93C5FD"
            ],
            title="Approval Rate by Property Area"
        )

        fig4.update_layout(showlegend=False)
        fig4.update_yaxes(range=[0, 100])

        st.plotly_chart(
            style_chart(fig4),
            use_container_width=True
        )

with col4:

    income_df = filtered_df.dropna(
        subset=["ApplicantIncome"]
    ).copy()

    income_df["Income Group"] = pd.cut(
        income_df["ApplicantIncome"],
        bins=[
            -float("inf"),
            2500,
            5000,
            10000,
            float("inf")
        ],
        labels=[
            "Low Income",
            "Medium Income",
            "High Income",
            "Very High Income"
        ]
    )

    income_data = calculate_approval(
        income_df,
        "Income Group"
    )

    if not income_data.empty:

        fig5 = px.bar(
            income_data,
            x="Income Group",
            y="Approval Rate",
            color="Income Group",
            text_auto=".2f",
            color_discrete_sequence=[
                "#1D4ED8", "#3B82F6",
                "#60A5FA", "#93C5FD"
            ],
            title="Approval Rate by Applicant Income"
        )

        fig5.update_layout(showlegend=False)
        fig5.update_yaxes(range=[0, 100])

        st.plotly_chart(
            style_chart(fig5),
            use_container_width=True
        )


# =====================================================
# 14. LOAN AMOUNT ANALYSIS
# =====================================================

st.markdown("---")
st.subheader("💰 Loan Amount Analysis")

loan_df = filtered_df.dropna(
    subset=["LoanAmount"]
).copy()

loan_df["Loan Group"] = pd.cut(
    loan_df["LoanAmount"],
    bins=[
        -float("inf"),
        100,
        200,
        300,
        float("inf")
    ],
    labels=[
        "Small Loan",
        "Medium Loan",
        "Large Loan",
        "Very Large Loan"
    ]
)

loan_data = calculate_approval(
    loan_df,
    "Loan Group"
)

if not loan_data.empty:

    fig6 = px.bar(
        loan_data,
        x="Loan Group",
        y="Approval Rate",
        color="Loan Group",
        text_auto=".2f",
        color_discrete_sequence=[
            "#1D4ED8", "#3B82F6",
            "#60A5FA", "#93C5FD"
        ],
        title="Approval Rate by Loan Amount"
    )

    fig6.update_layout(showlegend=False)
    fig6.update_yaxes(range=[0, 100])

    st.plotly_chart(
        style_chart(fig6),
        use_container_width=True
    )


# =====================================================
# 15. DATA TABLE
# =====================================================

st.markdown("---")
st.subheader("📋 Loan Application Records")

st.caption(
    f"Showing {len(filtered_df):,} records based on selected filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="loan_analysis_filtered.csv",
    mime="text/csv"
)


# =====================================================
# 16. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:15px 0;">

        <h4 style="color:#10233F;">
            🏦 Loan Approval & Risk Analytics
        </h4>

        <p style="color:#64748B; font-size:13px;">
            Financial Intelligence Dashboard
            | Python | Streamlit | Pandas | Plotly
        </p>

        <p style="color:#94A3B8; font-size:11px;">
            Academic Portfolio Project
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
