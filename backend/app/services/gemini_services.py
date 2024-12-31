import os

import time
import json

from langchain.schema import Document


from app.config.gemini import Gemini

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

SUMMARY_CODE_PROMPT = """
You are onboarding a junior software engineer and explaining to them the purpose of the #{doc.metadata.source} file. This file plays a crucial role in the project’s functionality. Please provide a summary of the code snippet below, keeping the following points in mind:

Purpose: Explain the overall purpose of the file and its importance in the context of the larger project.
Key Components: Identify and describe the key components of the code. This could include variables, functions, classes, or any important logic.
Flow: Outline the flow of the code, focusing on how the different components interact.
External Dependencies: If there are any external dependencies or libraries, explain their role in the functionality of the code.
Effect on the System: Describe how the code affects the system as a whole. Does it manipulate data, manage user requests, or interact with other parts of the system?
Assumptions: If applicable, mention any assumptions the code makes, such as the existence of certain data or the presence of particular configurations.
Potential Improvements: If you think there are any areas that could be improved for better clarity or efficiency, mention them briefly.
Be clear and concise, and ensure that the explanation is suitable for someone new to the project or to software engineering in general. Keep the summary between 250-400 words.

HERE IS THE CODE:
{code}

"""

gemini = Gemini(model_name="gemini-1.5-flash")
model = gemini.get_model()


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


async def summary_code(doc: Document):
    print("inside summary code")
    try:
        trimmed_doc = doc.page_content[0:30000]
        print("wating for response ..........")
        res = await model.generate_content_async(
            SUMMARY_CODE_PROMPT.format(doc=doc, code=trimmed_doc),
            generation_config={
                "temperature": 0.2,
            },
        )

        if not res.text:
            raise Exception("No response from Gemini")
        summary = json.loads(res.text)
        print("parsed data", parsed_data)
        embedding = await generateEmbeddings(summary)
        # save summary , embedding and source code to db
        # just return the ids of embeddings
        return {
            "summary": summary,
            "source_code": json.dumps(doc.page_content),
            "embedding": embedding,
            "metadata": doc.metadata,
        }

    except Exception as e:
        print("Exception summerizing commit diff from gemini:", e)
        raise e


import google.generativeai as genai


async def generateEmbeddings(summary):

    print("Inside Generate Embeddings")
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        print("Configured Gemini for text embedding")
        result = genai.embed_content(model="models/text-embedding-004", content=summary)

        embedding = result["embedding"]

        return embedding

    except Exception as e:
        print("Error Generating Embeddings:", e)
        raise e
