from langchain_community.document_loaders import GitLoader
from langchain.schema import Document
import os
import git
from app.services.github_services import GithubService

github = GithubService()
loaded_documents = []


def load_github_repo(repo_url):

    branch_name = github.get_branch(repo_url)
    cwd = os.getcwd()
    repoPath = cwd + "/" + "temp" + repo_url

    try:

        loader = GitLoader(repo_path=repoPath, clone_url=repo_url, branch=branch_name)
        docs = loader.load()

        metadatas = [doc.metadata for doc in docs]
        formatted_docs = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in docs
        ]

        global loaded_documents
        loaded_documents.extend(formatted_docs)
        os.removedirs(repoPath)
        return loaded_documents

    except Exception as e:
        print(f"Error loading documents from {repo_url}: {e}")
