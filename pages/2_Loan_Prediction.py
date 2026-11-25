
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Loan Prediction | Loan Analytics",
    page_icon="🏦",
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
    max-width: 1450px;
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
    padding: 22px;
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

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #E5EAF2;
    border-radius: 15px;
    padding: 25px;
}

.stButton button,
.stFormSubmitButton button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 650;
    padding: 10px 18px;
}

.stFormSubmitButton button:hover {
    background-color: #1D4ED8;
    color: white;
}

div[data-testid="stProgress"] > div > div {
    background-color: #2563EB;
}

hr {
    border-color: #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("# Loan Approval Prediction")

st.markdown(
    "Evaluate an applicant's loan eligibility using the trained "
    "Machine Learning model and applicant financial information."
)

st.markdown("---")


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "loan_cleaned.csv"
MODEL_PATH = BASE_DIR / "models" / "best_loan_model.pkl"


# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

def prepare_features(data):

    data = data.copy()

    data["Dependents"] = (
        data["Dependents"].astype(str).str.strip()
    )

    data["TotalIncome"] = (
        data["ApplicantIncome"] + data["CoapplicantIncome"]
    )

    data["TotalIncomeLog"] = np.log1p(data["TotalIncome"])

    data["LoanAmountLog"] = np.log1p(data["LoanAmount"])

    data["LoanIncomeRatio"] = (
        data["LoanAmount"] / data["TotalIncome"]
    )

    data["DependentsNumeric"] = (
        data["Dependents"]
        .replace({"3+": "3"})
        .astype(int)
    )

    data["IncomePerDependent"] = (
        data["TotalIncome"] /
        (data["DependentsNumeric"] + 1)
    )

    data["LoanBurden"] = np.select(
        [
            data["LoanIncomeRatio"] < 0.20,
            data["LoanIncomeRatio"] < 0.40
        ],
        [
            "Low",
            "Medium"
        ],
        default="High"
    )

    return data


# --------------------------------------------------
# LOAD MODEL AND SCALER
# --------------------------------------------------

@st.cache_resource
def load_artifacts():

    if not DATA_PATH.exists():
        raise FileNotFoundError("loan_cleaned.csv not found.")

    if not MODEL_PATH.exists():
        raise FileNotFoundError("best_loan_model.pkl not found.")

    training_data = pd.read_csv(DATA_PATH)

    training_data = prepare_features(training_data)

    training_data["Loan_Status"] = (
        training_data["Loan_Status"]
        .astype(str)
        .str.strip()
        .map({"Y": 1, "N": 0})
    )

    encoded_data = pd.get_dummies(
        training_data,
        drop_first=True,
        dtype=int
    )

    X = encoded_data.drop(columns=["Loan_Status"])
    y = encoded_data["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()
    scaler.fit(X_train)

    model = joblib.load(MODEL_PATH)

    return model, scaler, X.columns.tolist()


# --------------------------------------------------
# LOAD ARTIFACTS
# --------------------------------------------------

try:

    model, scaler, feature_columns = load_artifacts()

except Exception as e:

    st.error(f"Unable to load model or preprocessing data: {e}")
    st.stop()


# --------------------------------------------------
# MODEL STATUS
# --------------------------------------------------

st.success("Machine Learning model loaded successfully.")

st.markdown("### Applicant Information")

st.caption(
    "Complete the following sections to generate a loan approval prediction."
)


# --------------------------------------------------
# APPLICANT INPUT FORM
# --------------------------------------------------

with st.form("loan_prediction_form"):

    st.markdown("#### Personal & Employment Details")

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        married = st.selectbox(
            "Marital Status",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Number of Dependents",
            ["0", "1", "2", "3+"]
        )

    with col2:

        education = st.selectbox(
            "Education",
            ["Graduate", "Not Graduate"]
        )

        self_employed = st.selectbox(
            "Self Employed",
            ["Yes", "No"]
        )

        property_area = st.selectbox(
            "Property Area",
            ["Urban", "Semiurban", "Rural"]
        )

    st.markdown("---")
    st.markdown("#### Financial Information")

    col3, col4 = st.columns(2)

    with col3:

        applicant_income = st.number_input(
            "Applicant Monthly Income",
            min_value=1,
            value=5000,
            step=500
        )

        coapplicant_income = st.number_input(
            "Coapplicant Monthly Income",
            min_value=0,
            value=0,
            step=500
        )

        loan_amount = st.number_input(
            "Loan Amount (Dataset Units)",
            min_value=1,
            value=150,
            step=10
        )

    with col4:

        loan_term = st.selectbox(
            "Loan Term (Months)",
            [360, 180, 240, 120, 60, 36, 12]
        )

        credit_history = st.selectbox(
            "Credit History",
            [1.0, 0.0],
            format_func=lambda x: (
                "Good Credit History (1)" if x == 1.0
                else "No Good Credit History (0)"
            )
        )

        st.info(
            "Credit History: 1 represents a good credit history; "
            "0 represents no good credit history."
        )

    st.markdown("---")

    submitted = st.form_submit_button(
        "Predict Loan Approval",
        use_container_width=True
    )


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if submitted:

    applicant = pd.DataFrame([{
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }])

    try:

        # Feature engineering
        applicant = prepare_features(applicant)

        # One-hot encoding
        applicant_encoded = pd.get_dummies(
            applicant,
            drop_first=True,
            dtype=int
        )

        # Match training columns
        applicant_encoded = applicant_encoded.reindex(
            columns=feature_columns,
            fill_value=0
        )

        # Scaling
        applicant_scaled = scaler.transform(
            applicant_encoded
        )

        # Prediction
        prediction = model.predict(applicant_scaled)[0]

        # Probability
        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                applicant_scaled
            )[0]

            positive_index = list(model.classes_).index(1)

            approval_probability = (
                probabilities[positive_index] * 100
            )

            rejection_probability = 100 - approval_probability

        else:
            raise ValueError(
                "The selected model does not support probability prediction."
            )

        # Result section
        st.markdown("---")
        st.markdown("## Prediction Result")

        if prediction == 1:

            st.success("Loan Status Prediction: APPROVED")

        else:

            st.error("Loan Status Prediction: REJECTED")

        # Probability cards
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Approval Probability",
                f"{approval_probability:.2f}%"
            )

        with col2:
            st.metric(
                "Rejection Probability",
                f"{rejection_probability:.2f}%"
            )

        # Visual probability
        st.markdown("### Approval Probability")

        st.progress(
            int(round(approval_probability)),
            text=f"{approval_probability:.2f}% approval probability"
        )

        # Applicant summary
        st.markdown("### Applicant Summary")

        summary1, summary2, summary3 = st.columns(3)

        summary1.metric(
            "Total Monthly Income",
            f"{applicant_income + coapplicant_income:,}"
        )

        summary2.metric(
            "Loan Amount",
            f"{loan_amount:,}"
        )

        summary3.metric(
            "Loan Term",
            f"{loan_term} months"
        )

        st.info(
            "This result is a machine learning prediction based on "
            "historical training data. It is not an actual bank approval "
            "decision or a guarantee of loan eligibility."
        )

    except Exception as e:

        st.error(f"Prediction error: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Loan Risk Analytics | Machine Learning Prediction Module"
)
