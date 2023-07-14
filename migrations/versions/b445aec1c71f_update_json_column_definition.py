"""update json column definition

Revision ID: b445aec1c71f
Revises: fc6ee1027637
Create Date: 2023-07-14 13:57:10.833726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b445aec1c71f"
down_revision = "fc6ee1027637"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "CREATE INDEX json_idx ON planning_application USING btree (CAST((json) AS TEXT));"
    )


def downgrade():
    op.execute("DROP INDEX json_idx;")
