import re
from collections import Counter

# -----------------------------
# 1. Known semantic patterns
# -----------------------------
KNOWN_PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "url": r"^https?://[^\s]+$",
    "ipv4": r"^(?:\d{1,3}\.){3}\d{1,3}$",
    "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
}


# -----------------------------
# 2. Detect known patterns
# -----------------------------
def detect_semantic(texts):
    for name, pattern in KNOWN_PATTERNS.items():
        if all(re.fullmatch(pattern, t) for t in texts):
            return name, pattern
    return None, None


# -----------------------------
# 3. Token classifier
# -----------------------------
def classify_char(ch):
    if ch.islower():
        return "lower"
    if ch.isupper():
        return "upper"
    if ch.isdigit():
        return "digit"
    if ch.isspace():
        return "space"
    return "symbol"


# -----------------------------
# 4. Build structural regex
# -----------------------------
def build_structure(text):
    out = []
    i = 0

    while i < len(text):
        ch = text[i]
        t = classify_char(ch)

        if t == "lower":
            pattern, matcher = r"[a-z]", str.islower
        elif t == "upper":
            pattern, matcher = r"[A-Z]", str.isupper
        elif t == "digit":
            pattern, matcher = r"\d", str.isdigit
        elif t == "space":
            pattern, matcher = r"\s", str.isspace
        else:
            out.append(re.escape(ch))
            i += 1
            continue

        count = 1
        while i + count < len(text) and classify_char(text[i + count]) == t:
            count += 1

        out.append(pattern if count == 1 else f"{pattern}{{{count}}}")
        i += count

    return "^" + "".join(out) + "$"


# -----------------------------
# 5. Multi-sample generalization
# -----------------------------
def merge_patterns(patterns):
    # simple probabilistic merge (character-level consensus)
    max_len = max(len(p) for p in patterns)
    result = []

    for i in range(max_len):
        chars = [p[i] for p in patterns if i < len(p)]

        if not chars:
            continue

        most_common = Counter(chars).most_common(1)[0][0]
        result.append(most_common)

    return "^" + "".join(result) + "$"


# -----------------------------
# 6. Smart inference engine
# -----------------------------
def infer_regex(samples):
    if isinstance(samples, str):
        samples = [samples]

    # STEP 1: semantic detection
    name, pattern = detect_semantic(samples)
    if pattern:
        return f"{name} pattern detected:\n{pattern}"

    # STEP 2: structural regex per sample
    structured = [build_structure(s) for s in samples]

    # STEP 3: single sample → return structure
    if len(samples) == 1:
        return structured[0]

    # STEP 4: multi-sample inference
    return merge_patterns(structured)


# -----------------------------
# 7. RUN
# -----------------------------
print("Enter samples (empty line to stop):")

samples = []
while True:
    s = input("> ")
    if not s:
        break
    samples.append(s)

print("\nGenerated Regex:\n")
print(infer_regex(samples))