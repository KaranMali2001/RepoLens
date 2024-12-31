from app.services.langChain_services import load_github_repo
import asyncio
from langchain.schema import Document
from app.services.gemini_services import summary_code
from sqlalchemy.ext.asyncio import AsyncSession


async def index_repo(project_id: int, repo_url: str, db: AsyncSession):
    docs = await asyncio.get_event_loop().run_in_executor(
        executor, load_github_repo, repo_url
    )
    result = await getEmbeddings(docs, repo_url, db)

    print("inside index repo", docs)


async def getEmbeddings(docs: list[Document], repo_url: str, db: AsyncSession):
    print("Inside Get Embeddings")
    task = [summary_code(doc) for doc in docs]
    result = await asyncio.gather(*task)
    res = await db.execute(insert)
    print(result[0]["summary"])
    return result
