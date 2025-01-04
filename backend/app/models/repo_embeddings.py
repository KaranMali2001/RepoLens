from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.types import UserDefinedType
from app.config.database import Base
from sqlalchemy.orm import relationship


class Vector(UserDefinedType):
    def __init__(self, dim):
        self.dim = dim

    def get_col_spec(self):
        return f"vector({self.dim})"


class Repo_Embeddings(Base):
    __tablename__ = "repo_embeddings"
    id = Column(Integer, primary_key=True)
    repo_url = Column(String, nullable=False)
    summary_embedding = Column(Vector(768), nullable=True, index=True)
    source_code = Column(String)
    file_name = Column(String)
    summary = Column(String)
    last_synced=Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    projects = relationship(
        "Projects",
        secondary="repo_embeddings_projects",
        back_populates="repo_embeddings",
    )
