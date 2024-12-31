"""allowd  project_id in Github Commits to be

Revision ID: b23b979e38b3
Revises: e7aea48799cb
Create Date: 2024-12-29 11:58:52.835075

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b23b979e38b3"
down_revision: Union[str, None] = "e7aea48799cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "github_commits", "project_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "github_commits", "project_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###