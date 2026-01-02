
def confidence_gate(risk_level, risk_proba):
    confidence = max(risk_proba)
    if risk_level == "HIGH" and confidence < 0.75:
        return "MEDIUM", confidence, "Downgraded due to low confidence"
    return risk_level, confidence, "Normal confidence"


def decision_engine(user_input, risk_level):
    recommendations = []
    alerts = []

    if user_input.get("Kick Count", 10) < 10:
        recommendations.append("Ultrasound scan (AFI check)")

    if user_input.get("BS", 100) > 140:
        recommendations.append("Lipid Profile Test")

    if user_input.get("BMI", 22) > 30:
        recommendations.append("Thyroid Test")

    if risk_level == "HIGH":
        alerts.append("PHC Alert")
        alerts.append("ASHA Visit")

    return {
        "recommendations": recommendations,
        "alerts": alerts
    }
