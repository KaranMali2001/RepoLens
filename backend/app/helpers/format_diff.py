def format_diff(diff_content: str) -> str:

    lines = diff_content.split("\n")
    formatted_lines = []

    for line in lines:

        if line.startswith(("diff --git", "+++", "---", "+", "-")):

            if line.startswith(("+", "-")):
                stripped = line[1:].strip()
                if not stripped:
                    continue

            if len(line) > 150:
                line = line[:150] + "..."

            formatted_lines.append(line)

    return "\n".join(formatted_lines)
