# ============================================================
# FULL PIPELINE: Comment → Bug → Risk → Effectiveness
# ------------------------------------------------------------
# Updated for:
# ✔ New Person 3 architecture
# ✔ Explanation + Confidence + Label
# ✔ Robust PR-level processing
# ============================================================

print("🚀 STARTING PIPELINE")

import json
import os

from analysis_engine.comment_classifier import classify_comments
from analysis_engine.bug_severity import classify_bug_severity
from analysis_engine.risk_model import compute_risk
from analysis_engine.scoring import compute_effectiveness


def run_full_pipeline():
    print("📂 Pipeline running...\n")

    input_path = "data/analyzed_dataset.json"
    output_path = "data/final_scores.json"

    # =============================
    # Load dataset
    # =============================
    if not os.path.exists(input_path):
        print(f"❌ ERROR: File not found → {input_path}")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    print(f"✅ Loaded {len(data)} PRs\n")

    results = []

    # =============================
    # Process each PR
    # =============================
    for pr in data:
        pr_id = pr.get("pr_id", "UNKNOWN")

        print(f"🔹 Processing PR: {pr_id}")

        # -------------------------
        # Step 1: Comment classification
        # -------------------------
        pr["classified_comments"] = classify_comments(pr)

        print(f"   💬 Classified comments: {len(pr['classified_comments'])}")

        # -------------------------
        # Step 2: Bug severity classification
        # -------------------------
        pr["bug_severity"] = classify_bug_severity(pr)

        print(f"   🐞 Bug entries: {len(pr['bug_severity'])}")

        # -------------------------
        # Step 3: Risk modeling
        # -------------------------
        prevented, missed = compute_risk(pr)

        pr["prevented_risk"] = prevented
        pr["missed_risk"] = missed

        print(f"   ⚠️ Risk → Prevented: {prevented}, Missed: {missed}")

        # -------------------------
        # Step 4: Effectiveness scoring
        # -------------------------
        result = compute_effectiveness(pr)

        print(f"   📊 Score: {result['score']} | Confidence: {result['confidence']}")

        # -------------------------
        # Store result
        # -------------------------
        results.append({
    "pr_id": pr_id,
    "effectiveness_score": round(result["score"], 2),
    "confidence": round(result["confidence"], 2),
    "label": result["label"],
    "explanation": result["reasons"],
    "meta": {
        "comments": len(pr.get("classified_comments", [])),
        "bugs": len(pr.get("bug_severity", [])),
        "churn": pr.get("churn", 0)
    }
})
        print("")

    # =============================
    # Save results
    # =============================
    if len(results) == 0:
        print("⚠️ WARNING: No results generated!")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Pipeline completed successfully!")
    print(f"📁 Results saved to: {output_path}")

    if len(results) > 0:
        scores = [r["effectiveness_score"] for r in results]

        print("📊 Avg Score:", round(sum(scores)/len(scores), 2))
        print("📊 Max Score:", max(scores))
        print("📊 Min Score:", min(scores))
# ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":
    run_full_pipeline()