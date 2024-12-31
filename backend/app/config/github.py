from github import Github
import os
import datetime
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class GithubAuth:
    @lru_cache(maxsize=10)
    def __init__(self):
        PAT = os.environ.get("GITHUB_PAT")

        if PAT is None:
            raise ValueError("GITHUB_PAT environment variable is not set")
        try:
            self.g: Github = Github(PAT)

            print("Github auth created successfully", self.g)
        except Exception as e:
            print("Error creating github auth:", e)
            raise ValueError("Error creating github auth")

    def __call__(self):
        if not self.check_rate_limit(self.g):
            raise ValueError("Rate limit reached")
        return self.g

    @staticmethod
    def check_rate_limit(g: Github):
        print("Checking rate limit")
        rate_limit = g.get_rate_limit()
        remaining = rate_limit.core.remaining

        print("Rate limit remaining:", remaining)

        if remaining == 0:
            print("Rate limit reached")
            time_to_reset = rate_limit.reset - datetime.datetime.now()
            print("Time to reset:", time_to_reset)
            if time_to_reset.total_seconds() < 60:
                print("Rate limit reset in less than 1 minute")
                return True
            else:
                print("Rate limit reset in more than 1 minute")
                return False
        else:
            return True
