"""add unique constraint to investors email

Revision ID: 3dbad96b910e
Revises: f0e32b9c1338
Create Date: 2026-04-27 10:01:52.466552+00:00

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3dbad96b910e"
down_revision: Union[str, Sequence[str], None] = "f0e32b9c1338"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_investors_email", "investors", ["email"])


def downgrade() -> None:
    op.drop_constraint("uq_investors_email", "investors", type_="unique")
