
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Model Performance | Loan Analytics",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# PROFESSIONAL DESIGN
# --------------------------------------------------

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
    color: white !important;
}

h1, h2, h3 {
    color: #142B4A;
    font-weight: 700;
}

p {
    color: #52627A;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5EAF2;
    padding: 20px;
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
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 14px;
    padding: 10px;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
}

hr {
    border-color: #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

comparison_path = DATA_DIR / "model_comparison.csv"
evaluation_path = DATA_DIR / "model_evaluation.csv"
importance_path = DATA_DIR / "feature_importance.csv"


# --------------------------------------------------
# CHART STYLE
# --------------------------------------------------

def style_chart(fig, height=400):

    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),
        title=dict(
            font=dict(size=17, color="#142B4A"),
            x=0.02
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=30, r=30, t=65, b=40),
        xaxis=dict(
            showgrid=False,
            linecolor="#E2E8F0"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EDF1F7",
            linecolor="#E2E8F0"
        )
    )

    return fig


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("# Model Performance & Evaluation")

st.markdown(
    "Compare machine learning algorithms, evaluate predictive "
    "performance and understand the factors influencing loan approval."
)

st.markdown("---")


# --------------------------------------------------
# LOAD COMPARISON DATA
# --------------------------------------------------

if not comparison_path.exists():

    st.error("model_comparison.csv not found in the data folder.")
    st.stop()

comparison = pd.read_csv(comparison_path)


# --------------------------------------------------
# IDENTIFY MODEL COLUMN
# --------------------------------------------------

model_column = next(
    (
        col for col in comparison.columns
        if col.lower() in ["model", "model_name", "algorithm"]
    ),
    comparison.columns[0]
)

numeric_columns = comparison.select_dtypes(
    include="number"
).columns.tolist()

if not numeric_columns:

    st.error("No numeric performance metrics found.")
    st.stop()


# --------------------------------------------------
# NORMALIZE METRICS FOR DISPLAY
# --------------------------------------------------

metric_aliases = {
    "accuracy": "Accuracy",
    "precision": "Precision",
    "recall": "Recall",
    "f1": "F1 Score",
    "f1_score": "F1 Score",
    "roc_auc": "ROC-AUC",
    "roc-auc": "ROC-AUC"
}

def find_metric(alias):

    return next(
        (
            col for col in numeric_columns
            if col.lower().replace(" ", "_") == alias
        ),
        None
    )


accuracy_col = find_metric("accuracy")
precision_col = find_metric("precision")
recall_col = find_metric("recall")
f1_col = (
    find_metric("f1")
    or find_metric("f1_score")
)
roc_col = (
    find_metric("roc_auc")
    or find_metric("roc-auc")
)


# --------------------------------------------------
# BEST MODEL
# --------------------------------------------------

ranking_metric = f1_col or accuracy_col or numeric_columns[0]

best_index = comparison[ranking_metric].idxmax()

best_model_name = comparison.loc[
    best_index, model_column
]

best_model_score = comparison.loc[
    best_index, ranking_metric
]


# --------------------------------------------------
# MODEL PERFORMANCE OVERVIEW
# --------------------------------------------------

st.markdown("### Model Performance Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Models Evaluated",
    f"{len(comparison)}"
)

c2.metric(
    "Best Model",
    str(best_model_name)
)

c3.metric(
    f"Best {ranking_metric}",
    f"{best_model_score:.4f}"
)

if accuracy_col:
    c4.metric(
        "Best Accuracy",
        f"{comparison[accuracy_col].max():.4f}"
    )
else:
    c4.metric(
        "Evaluation Metric",
        ranking_metric
    )


st.markdown("---")


# --------------------------------------------------
# MODEL COMPARISON TABLE
# --------------------------------------------------

st.markdown("### 1. Machine Learning Model Comparison")

display_comparison = comparison.copy()

st.dataframe(
    display_comparison,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# MODEL COMPARISON CHART
# --------------------------------------------------

st.markdown("### 2. Performance Metrics Comparison")

selected_metrics = st.multiselect(
    "Select metrics to compare",
    numeric_columns,
    default=numeric_columns
)

if selected_metrics:

    plot_data = comparison.melt(
        id_vars=[model_column],
        value_vars=selected_metrics,
        var_name="Metric",
        value_name="Score"
    )

    fig = px.bar(
        plot_data,
        x=model_column,
        y="Score",
        color="Metric",
        barmode="group",
        text_auto=".3f",
        color_discrete_sequence=[
            "#2563EB",
            "#0F766E",
            "#7C3AED",
            "#D97706",
            "#0891B2"
        ]
    )

    fig.update_layout(
        xaxis_title="Machine Learning Model",
        yaxis_title="Performance Score",
        legend_title="Metrics"
    )

    fig = style_chart(fig, 450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("Select at least one metric to display the comparison.")


st.markdown("---")


# --------------------------------------------------
# INDIVIDUAL MODEL PERFORMANCE
# --------------------------------------------------

st.markdown("### 3. Best Model Performance")

if accuracy_col and precision_col and recall_col and f1_col:

    best_row = comparison.loc[best_index]

    metric_values = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score"
        ],
        "Score": [
            best_row[accuracy_col],
            best_row[precision_col],
            best_row[recall_col],
            best_row[f1_col]
        ]
    })

    fig_best = px.bar(
        metric_values,
        x="Metric",
        y="Score",
        text="Score",
        color="Metric",
        color_discrete_sequence=[
            "#2563EB",
            "#0F766E",
            "#7C3AED",
            "#D97706"
        ]
    )

    fig_best.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )

    fig_best.update_layout(
        showlegend=False,
        yaxis_range=[0, 1.15],
        yaxis_title="Performance Score"
    )

    st.plotly_chart(
        style_chart(fig_best),
        use_container_width=True
    )

else:

    st.info(
        "Accuracy, Precision, Recall and F1 Score columns "
        "are required for this detailed chart."
    )


st.markdown("---")


# --------------------------------------------------
# DETAILED EVALUATION
# --------------------------------------------------

st.markdown("### 4. Detailed Model Evaluation")

if evaluation_path.exists():

    evaluation = pd.read_csv(evaluation_path)

    st.dataframe(
        evaluation,
        use_container_width=True,
        hide_index=True
    )

    numeric_eval = evaluation.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_eval:

        evaluation_model_column = next(
            (
                col for col in evaluation.columns
                if col.lower() in [
                    "model", "model_name", "algorithm"
                ]
            ),
            None
        )

        if evaluation_model_column:

            evaluation_metrics = st.multiselect(
                "Select detailed evaluation metrics",
                numeric_eval,
                default=numeric_eval
            )

            if evaluation_metrics:

                evaluation_plot = evaluation.melt(
                    id_vars=[evaluation_model_column],
                    value_vars=evaluation_metrics,
                    var_name="Metric",
                    value_name="Score"
                )

                fig_eval = px.bar(
                    evaluation_plot,
                    x=evaluation_model_column,
                    y="Score",
                    color="Metric",
                    barmode="group",
                    text_auto=".3f",
                    color_discrete_sequence=[
                        "#2563EB",
                        "#0F766E",
                        "#7C3AED",
                        "#D97706",
                        "#0891B2"
                    ]
                )

                st.plotly_chart(
                    style_chart(fig_eval),
                    use_container_width=True
                )

else:

    st.info(
        "Detailed evaluation file is not available yet."
    )


st.markdown("---")


# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

st.markdown("### 5. Feature Importance Analysis")

if importance_path.exists():

    importance = pd.read_csv(importance_path)

    feature_col = next(
        (
            col for col in importance.columns
            if col.lower() in [
                "feature", "features", "feature_name"
            ]
        ),
        importance.columns[0]
    )

    value_col = next(
        (
            col for col in importance.columns
            if col.lower() in [
                "importance",
                "feature_importance",
                "importance_score"
            ]
        ),
        None
    )

    if value_col:

        importance[value_col] = pd.to_numeric(
            importance[value_col],
            errors="coerce"
        )

        importance = importance.dropna(
            subset=[value_col]
        )

        importance = importance.sort_values(
            value_col,
            ascending=False
        )

        col1, col2 = st.columns([2, 1])

        with col1:

            top_features = importance.head(15).sort_values(
                value_col,
                ascending=True
            )

            fig_importance = px.bar(
                top_features,
                x=value_col,
                y=feature_col,
                orientation="h",
                text=value_col,
                color=value_col,
                color_continuous_scale=[
                    "#BFDBFE",
                    "#2563EB"
                ]
            )

            fig_importance.update_traces(
                texttemplate="%{text:.3f}",
                textposition="outside"
            )

            fig_importance.update_layout(
                xaxis_title="Importance Score",
                yaxis_title="Feature",
                coloraxis_showscale=False
            )

            st.plotly_chart(
                style_chart(fig_importance, 550),
                use_container_width=True
            )

        with col2:

            st.markdown("#### Top Features")

            st.dataframe(
                importance.head(10),
                use_container_width=True,
                hide_index=True
            )

        st.caption(
            "Feature importance represents the influence or magnitude "
            "of model features. For Logistic Regression, absolute "
            "coefficients indicate magnitude, not causal influence."
        )

    else:

        st.warning(
            "Importance score column not found in feature_importance.csv."
        )

else:

    st.info(
        "Feature importance file is not available."
    )


# --------------------------------------------------
# BEST MODEL SUMMARY
# --------------------------------------------------

st.markdown("---")
st.markdown("### Final Model Selection")

st.success(
    f"Best performing model: {best_model_name} "
    f"based on {ranking_metric}."
)

st.info(
    "Model performance is evaluated using historical data. "
    "Actual loan approval decisions depend on additional factors "
    "and the lender's policies."
)


# --------------------------------------------------
# EXPORT
# --------------------------------------------------

st.markdown("### Download Model Evaluation Data")

csv = comparison.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Model Comparison CSV",
    data=csv,
    file_name="model_performance_report.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Loan Risk Analytics | Machine Learning Evaluation Module"
)

st.success("Model Performance page loaded successfully.")
