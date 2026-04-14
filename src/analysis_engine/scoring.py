from analysis_engine.config import WEIGHTS


def generate_explanation(A, PR, MS, B, C):
    reasons = []

    if MS > 3:
        reasons.append("High missed risk")

    if PR > 5:
        reasons.append("Strong risk prevention")

    if B > 5:
        reasons.append("High bug impact")

    if C > 3:
        reasons.append("High churn (instability)")

    if A == 0:
        reasons.append("PR not accepted")

    if not reasons:
        reasons.append("Balanced review performance")

    return reasons


def compute_effectiveness(pr):
    comments = pr.get("classified_comments", [])

    # 🔴 EDGE CASE
    if len(comments) == 0:
        return {
            "score": 0,
            "confidence": 0.2,
            "label": "No Data",
            "reasons": ["No review activity"]
        }

    # 🔹 Signals
    A = 1 if pr.get("accepted") else 0
    PR = pr.get("prevented_risk", 0)
    MS = pr.get("missed_risk", 0)
    C = pr.get("churn", 0)

    bug_scores = [b["score"] for b in pr.get("bug_severity", [])]
    B = sum(bug_scores)

    # 🔹 Normalize signals (VERY IMPORTANT)
    total_risk = PR + MS + 1
    PR_norm = PR / total_risk
    MS_norm = MS / total_risk

    B_norm = min(B / 10, 1)
    C_norm = min(C / 5, 1)

    # 🔹 Final score
    score = (
        WEIGHTS["acceptance"] * A +
        WEIGHTS["prevented"] * PR_norm -
        WEIGHTS["missed"] * MS_norm -
        WEIGHTS["bug"] * B_norm -
        WEIGHTS["churn"] * C_norm
    )

    # 🔹 Clamp (stability)
    score = max(0, min(score * 1.3, 1))

    # 🔹 Confidence (signal strength)
    confidence = max(0.3, min((PR + 1) / (PR + MS + 2), 1))

    # 🔹 Label
    if score > 0.7:
        label = "Effective"
    elif score > 0.4:
        label = "Moderate"
    else:
        label = "Ineffective"

    # 🔹 Explanation
    reasons = generate_explanation(A, PR, MS, B, C)

    return {
        "score": round(score, 2),
        "confidence": round(confidence, 2),
        "label": label,
        "reasons": reasons
    }