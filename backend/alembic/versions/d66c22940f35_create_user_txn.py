"""create user & txn

Revision ID: d66c22940f35
Revises: 2e8e3cd11de5
Create Date: 2024-12-15 17:55:10.210300

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d66c22940f35"
down_revision: Union[str, None] = "2e8e3cd11de5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=True),
        sa.Column("clerk_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("credits", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("clerk_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_clerk_id"), "users", ["clerk_id"], unique=False)
    op.create_table(
        "txns",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("clerk_id", sa.String(), nullable=False),
        sa.Column("txn_type", sa.String(), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("payment_id", sa.String(), nullable=False),
        sa.Column("payment_method", sa.String(), nullable=True),
        sa.Column("credits_added", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["clerk_id"],
            ["users.clerk_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("payment_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("txns")
    op.drop_index(op.f("ix_users_clerk_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
