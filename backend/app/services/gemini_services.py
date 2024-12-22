import os
from app.config.gemini import Gemini
import time

gemini = Gemini()
model = gemini.get_model()
ANALYSIS_PROMPT = """
Analyze the following git commit difference and provide a clear, point-wise explanation of the changes made.
Focus on the actual code changes and their impact. Format each point as a separate item.

Git Diff:
{diff}

Please """


async def ai_summerize(commit_diff: str):
    print("inside ai summerize")
    try:
        start_time = time.time()
        print("start time", start_time)

        print("wating for response ..........")
        res = await model.generate_content_async(
            ANALYSIS_PROMPT.format(diff=commit_diff)
        )
        end_time = time.time()  # End time

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print("res from Gemini", elapsed_time)
        if not res.text:
            raise Exception("No response from Gemini")

        changes = [
            point.strip().lstrip("•-*").strip()
            for point in res.text.split("\n")
            if point.strip() and not point.strip().isspace()
        ]
        return changes
    except Exception as e:
        print("Error summerizing commit diff from gemini:", e)
        raise e
