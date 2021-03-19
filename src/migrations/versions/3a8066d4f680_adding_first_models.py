"""Adding first models

Revision ID: 3a8066d4f680
Revises: 
Create Date: 2021-03-18 21:14:51.966498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a8066d4f680"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(length=4), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("precision", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol"),
    )
    op.create_index(op.f("ix_currency_id"), "currency", ["id"], unique=False)
    op.create_table(
        "exchange",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_exchange_id"), "exchange", ["id"], unique=False)
    op.create_table(
        "currency_pair",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exchange_id", sa.Integer(), nullable=True),
        sa.Column("currency_a_id", sa.Integer(), nullable=True),
        sa.Column("currency_b_id", sa.Integer(), nullable=True),
        sa.Column("symbol", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["currency_a_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency_b_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["exchange_id"],
            ["exchange.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol"),
    )
    op.create_index(op.f("ix_currency_pair_id"), "currency_pair", ["id"], unique=False)
    op.create_table(
        "candlestick",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("open", sa.DECIMAL(precision=16, scale=8), nullable=False),
        sa.Column("high", sa.DECIMAL(precision=16, scale=8), nullable=False),
        sa.Column("low", sa.DECIMAL(precision=16, scale=8), nullable=False),
        sa.Column("close", sa.DECIMAL(precision=16, scale=8), nullable=False),
        sa.Column("volume", sa.DECIMAL(precision=16, scale=8), nullable=False),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.Column("currency_pair_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["currency_pair_id"],
            ["currency_pair.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_candlestick_id"), "candlestick", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_candlestick_id"), table_name="candlestick")
    op.drop_table("candlestick")
    op.drop_index(op.f("ix_currency_pair_id"), table_name="currency_pair")
    op.drop_table("currency_pair")
    op.drop_index(op.f("ix_exchange_id"), table_name="exchange")
    op.drop_table("exchange")
    op.drop_index(op.f("ix_currency_id"), table_name="currency")
    op.drop_table("currency")
    # ### end Alembic commands ###
