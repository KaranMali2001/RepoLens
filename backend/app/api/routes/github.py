from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.clerk_services import ClerkTokenVerifier
from concurrent.futures import ThreadPoolExecutor
from app.config.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request
import asyncio
from sqlalchemy import update
from sqlalchemy.future import select
from app.services.github_services import GithubService
from app.models.github_commit import Github_Commits
from app.models.projects import Projects
from app.helpers.commit_diff import summarize_commit_diff
from app.helpers.url_exist import github_url_exists
import time
import json
from sqlalchemy import insert
from app.models.response.github_commits import CommitResponse


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
    try:
        result = await db.execute(
            select(Projects.github_url).where(Projects.id == body["project_id"])
        )

        github_url = result.scalar_one_or_none()
        print("github Url", github_url)
        # commit_res = await db.execute(
        #     select(Github_Commits).where(Github_Commits.github_url == github_url)
        # )

        # Optimize this code check the hash with given url in Db that they are summerized or not
        # if not commit_res.fetchall():
        # get the summairezed Commits from database
        start_time = time.time()

        commit_data = await asyncio.get_event_loop().run_in_executor(
            executor, github.get_latest_commits, github_url, 6
        )

        commit_hash = [c["commit_hash"] for c in commit_data]

        unprocessed_commits = await filterUnprocessedCommits(
            body["project_id"], db, commit_hash
        )
        print("unprocessed commits", len(unprocessed_commits))
        # TODO: Optimize this code check the hash with given url in Db that they are summerized or not

        if len(unprocessed_commits) == 0:
            print(len(unprocessed_commits))
            # check condition for empty summery in db ,empty summary shoud not be saved in db
            #
            res = await db.execute(
                select(Github_Commits).where(
                    Github_Commits.project_id == body["project_id"]
                )
            )
            commits = res.scalars().all()
            data = [
                {
                    **CommitResponse.from_orm(commit).dict(),
                    "commit_date": commit.commit_date.isoformat(),  # Convert datetime to string
                    "created_at": commit.created_at.isoformat(),  # Convert datetime to string
                    "updated_at": commit.updated_at.isoformat(),  # Convert datetime to string
                }
                for commit in commits
            ]
            print(data, type(data))

            return JSONResponse(status_code=200, content=json.dumps(data))
        for c in commit_data:
            new_commit = Github_Commits(
                project_id=body["project_id"],
                github_url=github_url,
                commit_hash=c["commit_hash"],
                commit_author=c["commit_author"],
                commit_message=c["commit_message"],
                commit_date=c["commit_date"],
                commit_summary=c["commit_summary"],
                commit_avatar_url=c["commit_avatar_url"],
            )
            db.add(new_commit)
            await db.commit()

        tasks = [
            summarize_commit_diff(commit_hash, github_url)
            for commit_hash in unprocessed_commits
        ]

        summerized_commits_list = await asyncio.gather(*tasks)
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print("res from Gemini", elapsed_time, summerized_commits_list)
        for commit in summerized_commits_list:

            try:
                print(
                    ".............................................",
                    commit["commit_hash"],
                )
                # print("inside for loop of updating commit summary",type(commit) ,"\n",commit)
                print("before updating summary................", commit["changes"])
                db_commit = await db.execute(
                    update(Github_Commits)
                    .where(Github_Commits.commit_hash == commit["commit_hash"])
                    .values(
                        commit_summary=json.dumps(commit["changes"]),
                    )
                )

                await db.commit()

            except Exception as e:
                print("Error updating commit summary", e)
                raise e
        res = await db.execute(
            select(Github_Commits)
            .where(Github_Commits.project_id == body["project_id"])
            .limit(5)
        )
        commits = res.scalars().all()
        print("COMMISTS",commits)
        data = [
            {
                **CommitResponse.from_orm(commit).dict(),
                "commit_date": commit.commit_date.isoformat(),  # Convert datetime to string
                "created_at": commit.created_at.isoformat(),  # Convert datetime to string
                "updated_at": commit.updated_at.isoformat(),  # Convert datetime to string
            }
            for commit in commits
        ]
        return JSONResponse(status_code=200, content=json.dumps(data))
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
