import streamlit as st
import pickle
import numpy as np
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Student Success Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    /* ---------- Main page ---------- */
    .stApp {
        background: linear-gradient(135deg, #f6f9ff 0%, #eef4ff 100%);
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- Force readable Streamlit text ---------- */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp .stMarkdown,
    .stApp .stMarkdown p {
        color: #172033 !important;
    }

    .stApp label {
        font-weight: 600 !important;
    }

    /* ---------- Hero ---------- */
    .hero {
        padding: 2.6rem 2.8rem;
        border-radius: 26px;
        background: linear-gradient(
            135deg,
            #173b7a 0%,
            #2563eb 55%,
            #4f8cff 100%
        );
        color: white !important;
        margin-bottom: 1.6rem;
        box-shadow: 0 14px 35px rgba(37, 99, 235, 0.22);
    }

    .hero h1 {
        color: white !important;
        font-size: 2.65rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.8px;
    }

    .hero p {
        color: rgba(255,255,255,0.92) !important;
        font-size: 1.05rem !important;
        margin: 0.65rem 0 0 !important;
    }

    /* ---------- Section headings ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin: 1.3rem 0 0.9rem 0;
        padding: 0.85rem 1rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.92);
        border: 1px solid #dfe7f3;
        box-shadow: 0 5px 16px rgba(30, 41, 59, 0.06);
    }

    .section-title .icon {
        font-size: 1.45rem;
    }

    .section-title .title {
        color: #172033 !important;
        font-size: 1.25rem;
        font-weight: 800;
    }

    /* ---------- Inputs ---------- */
    .stNumberInput,
    .stSelectbox,
    .stSlider {
        margin-bottom: 0.4rem;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
    }

    input {
        color: #172033 !important;
    }

    /* Slider text/value */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-testid="stThumbValue"] {
        color: #172033 !important;
    }

    /* ---------- Prediction button ---------- */
    div.stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 12px;
        font-weight: 800;
        font-size: 1rem;
        border: none;
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: white !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #4338ca);
        color: white !important;
        border: none;
    }

    /* ---------- Result cards ---------- */
    .result-pass {
        padding: 1.5rem;
        margin-top: 1rem;
        border-radius: 18px;
        background: #ecfdf3;
        border: 1px solid #a7f3d0;
        color: #065f46 !important;
        text-align: center;
    }

    .result-pass h2,
    .result-pass p {
        color: #065f46 !important;
    }

    .result-fail {
        padding: 1.5rem;
        margin-top: 1rem;
        border-radius: 18px;
        background: #fff1f2;
        border: 1px solid #fecdd3;
        color: #9f1239 !important;
        text-align: center;
    }

    .result-fail h2,
    .result-fail p {
        color: #9f1239 !important;
    }

    /* ---------- Metric cards ---------- */
    .metric-box {
        background: white;
        border: 1px solid #e1e8f2;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(30, 41, 59, 0.06);
    }

    .metric-label {
        color: #64748b !important;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        color: #172033 !important;
        font-size: 1.1rem;
        font-weight: 800;
    }

    .small-note {
        color: #64748b !important;
        font-size: 0.9rem;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: #64748b !important;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================
MODEL_PATH = Path(__file__).parent / "model.pkl"


@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


try:
    model = load_model()
except Exception:
    st.error(
        "Unable to load model.pkl. Make sure model.pkl is in the "
        "same folder as app.py."
    )
    st.stop()


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🎓 Student Success Predictor</h1>
    <p>
        Predict whether a student is likely to pass based on
        academic performance and attendance.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# STUDENT INFORMATION
# =========================================================
st.markdown("""
<div class="section-title">
    <span class="icon">👤</span>
    <span class="title">Student Information</span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Age",
        min_value=10,
        max_value=80,
        value=20,
        step=1
    )

with col2:
    gender_label = st.selectbox(
        "Gender",
        ["Male", "Female"],
        help="Encoded as 0 = Male and 1 = Female."
    )

    gender = 0 if gender_label == "Male" else 1

with col3:
    department_label = st.selectbox(
        "Department",
        [
            "Department 0",
            "Department 1",
            "Department 2",
            "Department 3"
        ],
        help="Select the department encoding used by the model."
    )

    department = int(department_label.split()[-1])


# =========================================================
# ACADEMIC PERFORMANCE
# =========================================================
st.markdown("""
<div class="section-title">
    <span class="icon">📚</span>
    <span class="title">Academic Performance</span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    study_hours = st.number_input(
        "Study Hours / Day",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5
    )

with col2:
    attendance = st.slider(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0
    )

with col3:
    assignments = st.number_input(
        "Assignments Completed",
        min_value=0,
        max_value=100,
        value=8,
        step=1
    )

with col4:
    midterm = st.slider(
        "Midterm Score",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0
    )

final_score = st.slider(
    "Final Score",
    min_value=0.0,
    max_value=100.0,
    value=65.0,
    step=1.0
)


# =========================================================
# PREDICTION
# =========================================================
st.markdown("""
<div class="section-title">
    <span class="icon">🔮</span>
    <span class="title">Prediction</span>
</div>
""", unsafe_allow_html=True)

predict_col, info_col = st.columns([1, 2])

with predict_col:
    predict_clicked = st.button(
        "🚀 Predict Student Outcome",
        type="primary"
    )

with info_col:
    st.markdown(
        '<p class="small-note">'
        'The prediction is generated directly from your Naive Bayes model.'
        '</p>',
        unsafe_allow_html=True
    )


# =========================================================
# RUN PREDICTION
# =========================================================
if predict_clicked:

    features = np.array([[
        age,
        gender,
        department,
        study_hours,
        attendance,
        assignments,
        midterm,
        final_score
    ]], dtype=float)

    try:
        prediction = model.predict(features)[0]
        prediction_text = str(prediction).strip().lower()

        if prediction_text in {"pass", "passed", "1", "true", "yes"}:
            passed = True
            result = "PASS"

        elif prediction_text in {"fail", "failed", "0", "false", "no"}:
            passed = False
            result = "FAIL"

        else:
            passed = prediction_text == "pass"
            result = str(prediction).upper()

        probability = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            classes = list(getattr(model, "classes_", []))

            try:
                predicted_index = classes.index(prediction)
            except ValueError:
                predicted_index = int(np.argmax(probabilities))

            probability = float(
                probabilities[predicted_index]
            ) * 100

        if passed:
            st.markdown("""
            <div class="result-pass">
                <h2>🎉 Predicted Outcome: PASS</h2>
                <p>
                    The model predicts that this student is likely to pass.
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="result-fail">
                <h2>⚠️ Predicted Outcome: FAIL</h2>
                <p>
                    The model predicts that this student may be at risk
                    of failing.
                </p>
            </div>
            """, unsafe_allow_html=True)

        if probability is not None:
            st.markdown("### 📊 Model Confidence")

            st.progress(
                min(max(probability / 100, 0.0), 1.0)
            )

            st.metric(
                "Prediction Probability",
                f"{probability:.1f}%"
            )

        st.markdown("### 📌 Student Snapshot")

        metrics = st.columns(5)

        values = [
            ("Age", f"{age}"),
            ("Study / Day", f"{study_hours:.1f} h"),
            ("Attendance", f"{attendance:.0f}%"),
            ("Midterm", f"{midterm:.0f}"),
            ("Final", f"{final_score:.0f}")
        ]

        for col, (label, value) in zip(metrics, values):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### 💡 Quick Insight")

        if attendance < 75:
            st.warning(
                "Attendance is below 75%. Improving attendance may support "
                "better academic performance."
            )

        elif final_score < 50 or midterm < 50:
            st.warning(
                "One or more exam scores are below 50. Focus on revision "
                "and targeted practice."
            )

        elif study_hours < 2:
            st.info(
                "Study time is relatively low. A consistent daily study "
                "routine may help."
            )

        else:
            st.success(
                "The student's academic indicators look reasonably strong."
            )

    except Exception as e:
        st.error(f"Prediction failed: {e}")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    '<div class="footer">'
    '🎓 Student Success Predictor • Powered by your Naive Bayes model'
    '</div>',
    unsafe_allow_html=True
)
