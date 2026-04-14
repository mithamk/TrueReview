from analysis_engine.semantic_classifier import classify_comment, map_severity


def classify_comments(pr):
    classified = []

    all_comments = pr.get("comments", []) + pr.get("review_comments", [])

    for c in all_comments:
        text = c.get("text", "").strip()

        if not text:
            continue

        label = classify_comment(text)
        severity = map_severity(label,text)

        classified.append({
            "text": text,
            "label": label,
            "score": severity
        })

    return classified