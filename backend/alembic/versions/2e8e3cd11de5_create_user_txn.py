"""create user & txn

Revision ID: 2e8e3cd11de5
Revises: 2f22f01c7f58
Create Date: 2024-12-15 17:51:42.252360

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e8e3cd11de5"
down_revision: Union[str, None] = "2f22f01c7f58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
