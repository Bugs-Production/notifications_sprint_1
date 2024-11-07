"""add_event

Revision ID: 7c93652ae4b6
Revises: 925ebd32553c
Create Date: 2024-11-06 10:25:10.419620

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c93652ae4b6"
down_revision: Union[str, None] = "925ebd32553c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("data", sa.Text(), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "REGISTRATION",
                "REFRESH_TOKEN_UPDATE",
                "SERIES",
                "NEW_FILMS",
                "NEWS",
                "PROMOTION",
                "MOVIE_RECOMMENDATION",
                "LIKE_NOTIFICATION",
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
        sa.Column("template", sa.Text(), nullable=True),
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
