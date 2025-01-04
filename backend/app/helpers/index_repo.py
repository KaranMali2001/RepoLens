import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.services.langChain_services import load_github_repo
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain.schema import Document
from app.services.gemini_services import summary_code
from sqlalchemy.ext.asyncio import AsyncSession
from app.helpers.url_exist import github_url_exists,repo_embeddings_exists
from app.helpers.commit_diff import get_changed_files_path
from app.services.github_services import GithubService
executor = ThreadPoolExecutor(max_workers=10)


github= GithubService()
async def index_repo( repo_url: str,db: AsyncSession):
    #get latest synced date from db
    latest_synced= await repo_embeddings_exists(db,repo_url)
    if latest_synced is not None:
        print("Repo already exist")
        res= github.get_latest_commits(repo_url,1)
        latest_commit_date=res[0]['commit_date']
        latest_commit_hash=res[0]['commit_hash']
        print("latest commit date",latest_commit_hash)
        #check latest Commit_date with last synced date in the repo from db
        if latest_commit_date>latest_synced is not None:
            #get latest path of the file that has been chaned
            file_paths= await get_changed_files_path(latest_commit_hash,repo_url)
            print("file paths",file_paths)
            docs = await asyncio.get_event_loop().run_in_executor(
                executor, load_github_repo, repo_url,file_paths
            )
            print("docsssssssssssssssssss from load git hub repo",docs)
            if len(docs)==0:
                print("no docs found")
                return
            task = [summary_code(doc) for doc in docs]
            result = await asyncio.gather(*task)
             #update the last synced date in db & update the embbedings in db
            
            
    else:
        docs= await asyncio.get_event_loop().run_in_executor(
            executor,load_github_repo,repo_url
        )
        task = [summary_code(doc) for doc in docs]
        result = await asyncio.gather(*task)
            #update the last synced date in db & create the embbedings in db
            
        
  
    


async def getEmbeddings(docs: list[Document], repo_url: str,db: AsyncSession):
   
   
    
    print("finallllllllllllllllllll result",result[0]['summary']['summary'])
    return result

asyncio.run(index_repo(repo_url="https://github.com/KaranMali2001/algoForshuffling"))