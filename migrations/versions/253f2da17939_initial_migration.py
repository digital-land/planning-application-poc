"""initial migration

Revision ID: 253f2da17939
Revises:
Create Date: 2023-07-11 16:55:09.189745

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "253f2da17939"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "planning_application",
        sa.Column("reference", sa.String(), nullable=False),
        sa.Column("entity", sa.BigInteger(), nullable=True),
        sa.Column("dataset", sa.String(), nullable=True),
        sa.Column("geojson", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("geometry", sa.String(), nullable=True),
        sa.Column("json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("organisation_entity", sa.BigInteger(), nullable=True),
        sa.Column("point", sa.String(), nullable=True),
        sa.Column("prefix", sa.String(), nullable=True),
        sa.Column("typology", sa.String(), nullable=True),
        sa.Column("entry_date", sa.Date(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("reference"),
    )
    op.create_table(
        "planning_application_log",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("reference", sa.String(), nullable=True),
        sa.Column("entry_date", sa.Date(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["reference"],
            ["planning_application.reference"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("planning_application_log")
    op.drop_table("planning_application")
    # ### end Alembic commands ###
