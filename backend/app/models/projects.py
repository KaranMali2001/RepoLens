from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, autoincrement=True, primary_key=True)
    clerk_id = Column(String, ForeignKey("users.clerk_id"), nullable=False)
    name = Column(String(150), nullable=False)
    credits_required = Column(Integer, nullable=False)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    github_url = Column(String, nullable=False)
    description = Column(String)
    last_synced = Column(DateTime, nullable=True)
    user = relationship("Users", back_populates="projects")
    github_commits = relationship("Github_Commits", back_populates="project")
    repo_embeddings = relationship(  # Changed from repositories to repo_embeddings
        "Repo_Embeddings",
        secondary="repo_embeddings_projects",
        back_populates="projects",
    )
