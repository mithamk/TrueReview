from sentence_transformers import SentenceTransformer, util

def is_non_actionable(text):
    t = text.lower().strip()

    if len(t) < 5:
        return True

    keywords = [
        "thanks", "thank you", "nice", "great", "welcome",
        "👍", ":+1:", "ok", "yes", "no problem"
    ]

    return any(k in t for k in keywords)

# Load model (fast + good quality)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Labels
LABELS = [
    "bug or error in code",
    "code improvement suggestion",
    "code style or formatting issue",
    "security vulnerability",
    "non actionable comment"
]

# Precompute label embeddings (IMPORTANT for speed)
label_embeddings = model.encode(LABELS, convert_to_tensor=True)


def classify_comment(text):
    if not text.strip():
        return "non actionable comment"

    # 🔴 FILTER FIRST (VERY IMPORTANT)
    if is_non_actionable(text):
        return "non actionable comment"

    text_embedding = model.encode(text, convert_to_tensor=True)

    scores = util.cos_sim(text_embedding, label_embeddings)[0]
    best_idx = scores.argmax().item()

    return LABELS[best_idx]

def map_severity(label, text):
    t = text.lower()

    # conversational / non-risk intent
    conversational = [
        "sorry", "thanks", "i think", "maybe",
        "i feel", "i wonder", "i got this",
        "what do you think", "not sure"
    ]

    if any(k in t for k in conversational):
        return 0

    if label == "security vulnerability":
        return 4

    elif label == "bug or error in code":
        return 3

    elif label == "code improvement suggestion":
        return 2

    elif label == "code style or formatting issue":
        return 1

    return 0