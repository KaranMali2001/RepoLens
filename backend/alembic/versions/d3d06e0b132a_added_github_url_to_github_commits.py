"""added github_url to Github Commits

Revision ID: d3d06e0b132a
Revises: 66af900f1a32
Create Date: 2024-12-23 15:49:44.641763

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d3d06e0b132a"
down_revision: Union[str, None] = "66af900f1a32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "github_commits", sa.Column("github_url", sa.String(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("github_commits", "github_url")
    # ### end Alembic commands ###