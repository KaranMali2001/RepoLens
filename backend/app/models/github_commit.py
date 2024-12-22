from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship


class Github_Commits(Base):
    __tablename__ = "github_commits"
    id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    commit_hash = Column(String, nullable=False)
    commit_author = Column(String, nullable=False)
    commit_message = Column(String, nullable=False)
    commit_date = Column(DateTime, nullable=False)
    commit_summary = Column(String, nullable=False)
    commit_avatar_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    project = relationship("Projects", back_populates="github_commits")
