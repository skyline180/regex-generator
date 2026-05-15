import re

def generate_regex(text):
    groups = []
    i = 0

    while i < len(text):
        ch = text[i]

        # Character type detection
        if ch.islower():
            pattern = r"[a-z]"
            matcher = str.islower

        elif ch.isupper():
            pattern = r"[A-Z]"
            matcher = str.isupper

        elif ch.isdigit():
            pattern = r"\d"
            matcher = str.isdigit

        elif ch.isspace():
            pattern = r"\s"
            matcher = str.isspace

        else:
            groups.append(re.escape(ch))
            i += 1
            continue

        # Count consecutive same-type chars
        count = 1
        while i + count < len(text) and matcher(text[i + count]):
            count += 1

        # Build regex part
        if count == 1:
            groups.append(pattern)
        else:
            groups.append(f"{pattern}{{{count}}}")

        i += count

    return "^" + "".join(groups) + "$"


# User input
user_input = input("Enter text: ")

# Generate regex
regex_pattern = generate_regex(user_input)

print("\nGenerated Regex:")
print(regex_pattern)