import httpx
import os
from app.services.gemini_services import ai_summerize


async def summarize_commit_diff(commit_hash: str, github_url: str):
    try:
        commit_hash = "d4964f301d0c0f6a185ee9c1690f5ae898a04cda"
        github_url = "https://github.com/KaranMali2001/MatchUp"
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
            if res.status_code != 200:
                raise Exception("Error fetching commit diff")
            summery = await ai_summerize(res.text)
            print("summery from ai in summerize commit diff", summery)
            return summery
    except Exception as e:
        print("Error getting commit diff:", e)
        raise e
