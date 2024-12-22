from app.config.github import GithubAuth
from sqlalchemy.ext.asyncio import AsyncSession
from github import Github
from itertools import islice


class GithubService:
    def __init__(self):
        github_auth = GithubAuth()
        self.g: Github = github_auth()

    def get_latest_commits(self, github_url: str):
        print("inside get commits", self.g, github_url)

        try:
            # gets latest 15 commits from github
            if "github.com" in github_url:
                url = github_url.split("github.com/")[1]
                repo = self.g.get_repo(url)
                print("\n repo", repo)
                github_commits = repo.get_commits().get_page(0)

                commit_data = []
                for c in github_commits[:1]:
                    commit_data.append(
                        {
                            "commit_hash": c.sha,
                            "commit_author": c.commit.author.name,
                            "commit_message": c.commit.message,
                            "commit_date": c.commit.author.date,
                            "commit_avatar_url": c.author.avatar_url,
                        }
                    )
                return commit_data
            else:
                print("Error: Invalid github url")
                return None
        except Exception as e:
            print("Error getting commits:", e)
            return None
