import httpx
import os
from app.services.gemini_services import ai_summerize
import asyncio
from app.helpers.format_diff import format_diff
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=10)


async def summarize_commit_diff(commit_hash: str, github_url: str):
    try:
        commit_hash = commit_hash
        github_url = github_url
        commit_diff_url = f"{github_url}/commit/{commit_hash}.diff"
        print("commit diff url", commit_diff_url)
        async with httpx.AsyncClient() as client:
            res = await client.get(
                commit_diff_url,
                headers={
                    "Accept": "application/vnd.github.v3.diff",
                    "Authorization": f"token {os.environ.get('GITHUB_PAT')}",
                },
            )
            print("res from github is ", res)
            loop = asyncio.get_event_loop()
            formatted_diff = await loop.run_in_executor(
                thread_pool, format_diff, res.text
            )
            # print("\n \n \n formatted diff", formatted_diff)

            if res.status_code != 200:
                raise Exception("Error fetching commit diff")
            summery = await ai_summerize(formatted_diff, commit_hash)
            print("summery from ai in summerize commit diff", type(summery))
            return summery
    except Exception as e:
        print("Error getting commit diff:", e)
        raise e
