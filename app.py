
import streamlit as st
import pickle
import json
import pandas as pd
from decision_engine import confidence_gate, decision_engine

# Load assets
model = pickle.load(open("maternal_risk_model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))
schema = json.load(open("feature_schema.json"))

st.set_page_config(page_title="MaternalPulse AI", page_icon="🤰")

st.title("🤰 MaternalPulse AI")
st.write("💖 Hi Mom, please take care of me!")

# Input form
age = st.number_input("Age", 18, 45, 28)
sbp = st.number_input("Systolic BP", 90, 200, 120)
dbp = st.number_input("Diastolic BP", 60, 140, 80)
bs = st.number_input("Blood Sugar", 70, 250, 100)
bmi = st.number_input("BMI", 15.0, 45.0, 22.0)
hr = st.number_input("Heart Rate", 60, 140, 80)
temp = st.number_input("Body Temp", 35.0, 40.0, 36.8)
kicks = st.number_input("Kick Count", 0, 30, 15)
leak = st.selectbox("Fluid Leakage", ["No", "Yes"])

if st.button("Check My Health"):
    data = pd.DataFrame([{
        "Age": age,
        "Systolic BP": sbp,
        "Diastolic": dbp,
        "BS": bs,
        "BMI": bmi,
        "Heart Rate": hr,
        "Body Temp": temp,
        "Kick Count": kicks,
        "Fluid Leakage": leak
    }])

    pred = model.predict(data)
    proba = model.predict_proba(data)[0]
    risk = le.inverse_transform(pred)[0]

    final_risk, conf, note = confidence_gate(risk, proba)
    decision = decision_engine(data.iloc[0], final_risk)

    st.subheader("🧠 Result")
    st.write("Risk Level:", final_risk)
    st.write("Confidence:", round(conf*100, 2), "%")

    st.subheader("👶 Baby Says")
    if final_risk == "HIGH":
        st.error("Mom, please see a doctor soon ❤️")
    elif final_risk == "MEDIUM":
        st.warning("Mom, take rest and eat well 💛")
    else:
        st.success("Mom, I am safe and happy 💖")

    st.subheader("🧪 Recommendations")
    for r in decision["recommendations"]:
        st.write("-", r)
