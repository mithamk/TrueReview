from analysis_engine.config import SEVERITY_MAP

def classify_bug(text):
    t = text.lower()

    if any(k in t for k in ["security", "vulnerability", "exploit"]):
        return "critical"
    elif any(k in t for k in ["fix", "bug", "error", "issue", "fail"]):
        return "high"
    elif any(k in t for k in ["patch", "update", "improve"]):
        return "medium"
    else:
        return "low"

def classify_bug_severity(pr):
    classified = []

    for commit in pr["commits"]:
        label = classify_bug(commit["message"])
        score = SEVERITY_MAP[label]

        classified.append({
            "message": commit["message"],
            "severity": label,
            "score": score
        })

    return classified