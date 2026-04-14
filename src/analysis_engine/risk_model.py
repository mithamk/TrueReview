def compute_risk(pr):
    comments = pr.get("classified_comments", [])
    accepted = pr.get("accepted", False)

    if not comments:
        return 0, 0

    prevented_risk = 0
    missed_risk = 0

    for c in comments:
        severity = c["score"]

        # 🔥 Ignore non-actionable comments
        if severity == 0:
            continue

        # 🔍 Debug (optional)
        print("DEBUG COMMENT:", c.get("text", ""))
        print("DEBUG SEVERITY:", severity)

        if severity >= 2:
            if accepted:
                prevented_risk += severity
            else:
                missed_risk += severity

    return prevented_risk, missed_risk