import httpx
import os
import asyncio
from app.services.gemini_services import ai_summerize
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

async def get_changed_files_path(commit_hash: str, github_url: str):
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
        
        changed_files = []
        diff_text = res.text
        
        # Split diff into sections by diff headers
        diff_sections = diff_text.split("diff --git ")
        
        for section in diff_sections[1:]:  # Skip first empty section
            
            file_line = section.split("\n")[0]
            _, file_path = file_line.split(" b/", 1)
            changed_files.append(file_path)

        return changed_files
    except Exception as e:
        print("Error getting commit diff file path", e)
        raise ValueError("Error getting commit diff file path ")

