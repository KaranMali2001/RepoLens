from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.clerk_services import ClerkTokenVerifier
from concurrent.futures import ThreadPoolExecutor
from app.config.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request
import asyncio
from sqlalchemy.future import select
from app.services.github_services import GithubService
from app.models.github_commit import Github_Commits
from app.models.projects import Projects
from app.helpers.commit_diff import summarize_commit_diff

executor = ThreadPoolExecutor(max_workers=10)
verifier = ClerkTokenVerifier()

github = GithubService()
router = APIRouter(prefix="/github", tags=["github"])


@router.post("/commits")
async def get_commits(
    req: Request,
    db: AsyncSession = Depends(get_session),
    token_data: dict = Depends(verifier.verify_token),
):
    print("inside Get Commits routeeeeeeeeee")
    clerk_id = token_data["sub"]
    body = await req.json()

    result = await db.execute(
        select(Projects.github_url).where(Projects.id == body["project_id"])
    )

    github_url = result.scalar_one_or_none()
    print("github_url agsdagag scalerrr", github_url)
    try:
        commit_data = await asyncio.get_event_loop().run_in_executor(
            executor, github.get_latest_commits, github_url
        )

        commit_hash = [c["commit_hash"] for c in commit_data]

        unprocessed_commits = await filterUnprocessedCommits(
            body["project_id"], db, commit_hash
        )
        print("unprocessed_commits", len(unprocessed_commits))
        tasks = [
            summarize_commit_diff(commit_hash, github_url)
            for commit_hash in unprocessed_commits
        ]
        summerized_commits_list = await asyncio.gather(*tasks)
        if commit_hash is not None:
            return JSONResponse(status_code=200, content=commit_hash)
    except Exception as e:
        print("Error ", e)
        return JSONResponse(
            status_code=500, content={"message": "Error fetching projects"}
        )


async def filterUnprocessedCommits(
    project_id: int, db: AsyncSession, commit_hash: list
):
    print("inside filterunprocessed commits", project_id)
    try:
        print("inside filterunprocessed commits", project_id)
        result = await db.execute(
            select(Github_Commits.commit_hash).where(
                Github_Commits.project_id == project_id
            )
        )
        commits = set(result.scalars().all())
        unprocessed_commits = [hash for hash in commit_hash if hash not in commits]

        print("commits", unprocessed_commits)
        return unprocessed_commits
    except Exception as e:
        print("Error getting commits:", e)
        return None
