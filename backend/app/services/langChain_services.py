from langchain_community.document_loaders import GitLoader
from langchain.schema import Document
import os
import git
from app.services.github_services import GithubService
import shutil
from typing import Optional

github = GithubService()

loaded_documents = []


def load_github_repo(repo_url: str, file_paths: Optional[list[str]] = None):

    branch_name = github.get_branch(repo_url)
    cwd = os.getcwd()
    repo_name = repo_url.split("/")[-1].replace(".git", "")  # Extract repo name
    repo_path = os.path.join(cwd, "temp", repo_name)

    try:

        loader = GitLoader(repo_path=repo_path, clone_url=repo_url, branch=branch_name)
        docs = loader.load()
        print("Fileeeeeeeeeeeeeeeee Pathssssssssssssssssss", file_paths)
        if file_paths is None:
            metadatas = [doc.metadata for doc in docs]
            formatted_docs = [
                Document(page_content=doc.page_content, metadata=doc.metadata)
                for doc in docs
            ]

            global loaded_documents
            loaded_documents.extend(formatted_docs)
            shutil.rmtree(os.path.join(cwd, "temp"))

            return loaded_documents
        else:
            filtered_docs = []
            for doc in docs:
                doc_path = doc.metadata.get("file_path")

                for path in file_paths:

                    if doc_path == path:
                        print("inside If")
                        filtered_docs.append(doc)
                        break
            formatted_docs = [
                Document(page_content=doc.page_content, metadata=doc.metadata)
                for doc in filtered_docs
            ]

            loaded_documents.extend(formatted_docs)
            shutil.rmtree(os.path.join(cwd, "temp"))

            return loaded_documents

    except Exception as e:
        print(f"Error loading documents from {repo_url}: {e}")
        shutil.rmtree(os.path.join(cwd, "temp"))
        raise ValueError(f"Error loading documents from {repo_url}: {e}")
