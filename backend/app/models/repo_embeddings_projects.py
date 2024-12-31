from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey


class Repo_Embeddings_Projects(Base):
    __tablename__ = "repo_embeddings_projects"
    id = Column(Integer, primary_key=True)
    repo_embeddings_id = Column(
        Integer, ForeignKey("repo_embeddings.id"), nullable=False
    )
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
