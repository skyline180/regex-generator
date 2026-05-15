import re

def text_to_pattern(text):
    pattern = "^"
    i = 0

    while i < len(text):
        ch = text[i]

        # Detect character type
        if ch.islower():
            char_type = "[a-z]"
            check = str.islower

        elif ch.isupper():
            char_type = "[A-Z]"
            check = str.isupper

        elif ch.isdigit():
            char_type = "[0-9]"
            check = str.isdigit

        else:
            # Escape special regex chars
            pattern += re.escape(ch)
            i += 1
            continue

        # Count consecutive same-type chars
        count = 1
        while i + count < len(text) and check(text[i + count]):
            count += 1

        # Add to regex
        if count == 1:
            pattern += char_type
        else:
            pattern += f"{char_type}{{{count}}}"

        i += count

    pattern += "$"
    return pattern


# Example
text = input("Enter text: ")
print(text_to_pattern(text))