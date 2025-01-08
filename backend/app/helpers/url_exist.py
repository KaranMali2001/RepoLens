from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.github_commit import Github_Commits
from app.models.repo_embeddings import Repo_Embeddings


async def github_url_exists(db: AsyncSession, github_url: str):
    try:
        result = await db.execute(
            select(Github_Commits).where(Github_Commits.github_url == github_url)
        )
        print("result from url exists", result)
        return result.scalars().all()
    except Exception as e:
        print("Error checking url exists:", e)
        return None


async def repo_embeddings_exists(db: AsyncSession, repo_url: str):
    try:
        res = await db.execute(
            select(Repo_Embeddings.lasy_synced).where(
                Repo_Embeddings.repo_url == repo_url
            )
        )
        return res.scalars().all()
    except Exception as e:
        print("Error checking url exists:", e)
        raise ValueError("Error while checking repo embeddings")
