import re

KNOWN_PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "url": r"^https?://[^\s/$.?#].[^\s]*$",
    "ipv4": r"^(?:\d{1,3}\.){3}\d{1,3}$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    "phone": r"^\+?\d[\d\s\-()]{7,}$",
}

def structural_regex(text):
    result = "^"
    i = 0

    while i < len(text):
        ch = text[i]

        if ch.islower():
            p = "[a-z]"
            fn = str.islower

        elif ch.isupper():
            p = "[A-Z]"
            fn = str.isupper

        elif ch.isdigit():
            p = r"\d"
            fn = str.isdigit

        elif ch.isspace():
            p = r"\s"
            fn = str.isspace

        else:
            result += re.escape(ch)
            i += 1
            continue

        count = 1
        while i + count < len(text) and fn(text[i + count]):
            count += 1

        result += f"{p}{{{count}}}" if count > 1 else p
        i += count

    return result + "$"


def infer_regex(text):
    for name, pattern in KNOWN_PATTERNS.items():
        if re.fullmatch(pattern, text):
            return f"{name}: {pattern}"

    return structural_regex(text)


# User input
text = input("Enter text: ")

print(infer_regex(text))