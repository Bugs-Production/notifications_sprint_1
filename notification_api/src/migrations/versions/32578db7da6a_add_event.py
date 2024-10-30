"""add_event

Revision ID: 32578db7da6a
Revises: 925ebd32553c
Create Date: 2024-10-30 22:36:30.077665

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32578db7da6a"
down_revision: Union[str, None] = "925ebd32553c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("data", sa.Text(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "REGISTRATION",
                "REFRESH_TOKEN_UPDATE",
                "LIKE",
                "SERIES",
                "NEW_FILMS",
                "NEWS",
                "SALE",
                "PROMOTION",
                name="eventtypesenum",
            ),
            nullable=False,
        ),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column(
            "channel",
            sa.Enum("EMAIL", "WEBSOCKET", name="channelenum"),
            nullable=False,
        ),
        sa.Column("send_date", sa.DateTime(), nullable=True),
        sa.Column("send_to", sa.JSON(), nullable=True),
        sa.Column("send_from", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("INIT", "SUCCESS", "FAILED", name="eventstatusenum"),
            nullable=False,
        ),
        sa.Column("template", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("events")
    op.execute("DROP TYPE eventtypesenum;")
    op.execute("DROP TYPE channelenum;")
    op.execute("DROP TYPE eventstatusenum;")
    # ### end Alembic commands ###
