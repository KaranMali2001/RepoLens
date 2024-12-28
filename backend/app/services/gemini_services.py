import os
from app.config.gemini import Gemini
import time
import json

gemini = Gemini()
model = gemini.get_model()
ANALYSIS_PROMPT = """Analyze the Git commit difference and extract 5-6 key changes.

Input:
Diff: {diff}
Commit Hash: {commit_hash}

Requirements:
- Return ONLY a JSON array with exactly one object containing 5-6 detailed change descriptions
- Each change should be a clear, specific point about what was modified
- Focus on functional changes, not formatting or whitespace
- Keep each point concise but descriptive

Output Format:
[
  "changes": [
    "Added user authentication middleware to protect API endpoints",
    "Implemented password hashing using bcrypt with 10 rounds",
    "Created new database schema for user profiles",
    "Added input validation for registration form",
    "Set up error handling for auth failures"
  ],
  "commit_hash": "<commit_hash>"
]

Parse the following diff and generate the response:"""


async def ai_summerize(commit_diff: str, commit_hash: str):
    print("inside ai summerize")
    try:

        print("wating for response ..........")
        res = await model.generate_content_async(
            ANALYSIS_PROMPT.format(diff=commit_diff, commit_hash=commit_hash),
            generation_config={
                "temperature": 0.2,
            },
        )

        if not res.text:
            raise Exception("No response from Gemini")
        parsed_data = json.loads(res.text)
        # print("parsed data", parsed_data)
        return parsed_data

    except Exception as e:
        print("Error summerizing commit diff from gemini:", e)
        raise e
