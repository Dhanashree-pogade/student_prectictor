import streamlit as st
import pickle
import numpy as np
from pathlib import Path

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Student Success Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f7f9fc 0%, #eef4ff 100%);
    }

    .hero {
        padding: 2.2rem 2.4rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #173b7a 0%, #2563eb 55%, #4f8cff 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.20);
    }

    .hero h1 {
        font-size: 2.6rem;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 1.05rem;
        margin: 0.55rem 0 0;
        opacity: 0.92;
    }

    .section-card {
        background: rgba(255,255,255,0.92);
        padding: 1.35rem;
        border-radius: 18px;
        border: 1px solid #e5eaf2;
        box-shadow: 0 6px 20px rgba(30, 41, 59, 0.06);
        margin-bottom: 1rem;
    }

    .result-pass {
        padding: 1.4rem;
        border-radius: 18px;
        background: #ecfdf3;
        border: 1px solid #a7f3d0;
        color: #065f46;
        text-align: center;
    }

    .result-fail {
        padding: 1.4rem;
        border-radius: 18px;
        background: #fff1f2;
        border: 1px solid #fecdd3;
        color: #9f1239;
        text-align: center;
    }

    .metric-box {
        background: white;
        border: 1px solid #e5eaf2;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(30, 41, 59, 0.05);
    }

    .small-note {
        color: #64748b;
        font-size: 0.9rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3rem;
        font-weight: 700;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load model
# -----------------------------
MODEL_PATH = Path(__file__).parent / "model.pkl"


@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


try:
    model = load_model()
except Exception:
    st.error(
        "Unable to load `model.pkl`. Make sure `model.pkl` is in the "
        "same folder as `app.py`."
    )
    st.stop()


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 Student Success Predictor</h1>
    <p>
        Predict whether a student is likely to pass based on
        academic performance and attendance.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Student Information
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("👤 Student Information")

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
        help="Select the department encoding used by your model."
    )

    department = int(department_label.split()[-1])

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Academic Performance
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("📚 Academic Performance")

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

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Prediction Button
# -----------------------------
st.markdown("### 🔮 Prediction")

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


# -----------------------------
# Prediction
# -----------------------------
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

        if prediction_text in {
            "1", "pass", "passed", "true", "yes"
        }:
            result = "PASS"
            passed = True

        elif prediction_text in {
            "0", "fail", "failed", "false", "no"
        }:
            result = "FAIL"
            passed = False

        else:
            try:
                passed = int(prediction) == 1
                result = "PASS" if passed else "FAIL"
            except Exception:
                passed = False
                result = str(prediction).upper()


        # -----------------------------
        # Probability
        # -----------------------------
        probability = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(features)[0]

            classes = list(
                getattr(model, "classes_", [])
            )

            try:
                predicted_index = classes.index(prediction)

            except ValueError:
                predicted_index = int(
                    np.argmax(probabilities)
                )

            probability = (
                float(probabilities[predicted_index]) * 100
            )


        # -----------------------------
        # Result
        # -----------------------------
        if passed:

            st.markdown(
                """
                <div class="result-pass">
                    <h2>🎉 Predicted Outcome: PASS</h2>
                    <p>
                        The model predicts that this student
                        is likely to pass.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="result-fail">
                    <h2>⚠️ Predicted Outcome: FAIL</h2>
                    <p>
                        The model predicts that this student
                        may be at risk of failing.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


        # -----------------------------
        # Confidence
        # -----------------------------
        if probability is not None:

            st.markdown("### 📊 Model Confidence")

            st.progress(
                min(
                    max(probability / 100, 0.0),
                    1.0
                )
            )

            st.metric(
                "Prediction Probability",
                f"{probability:.1f}%"
            )


        # -----------------------------
        # Student Snapshot
        # -----------------------------
        st.markdown("### 📌 Student Snapshot")

        metrics = st.columns(5)

        values = [
            ("Age", f"{age}"),
            ("Study / Day", f"{study_hours:.1f} h"),
            ("Attendance", f"{attendance:.0f}%"),
            ("Midterm", f"{midterm:.0f}"),
            ("Final", f"{final_score:.0f}")
        ]

        for col, (label, value) in zip(
            metrics,
            values
        ):

            with col:

                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="small-note">
                            {label}
                        </div>
                        <strong>
                            {value}
                        </strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # -----------------------------
        # Quick Insight
        # -----------------------------
        st.markdown("### 💡 Quick Insight")

        if attendance < 75:

            st.warning(
                "Attendance is below 75%. Improving attendance "
                "may support better academic performance."
            )

        elif final_score < 50 or midterm < 50:

            st.warning(
                "One or more exam scores are below 50. "
                "Focus on revision and targeted practice."
            )

        elif study_hours < 2:

            st.info(
                "Study time is relatively low. A consistent "
                "daily study routine may help."
            )

        else:

            st.success(
                "The student's academic indicators look "
                "reasonably strong."
            )


    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "🎓 Student Success Predictor • "
    "Powered by your Naive Bayes model"
)
