"""Adds skin

Revision ID: 7f22bc3a6e81
Revises: 76f396b0cab8
Create Date: 2023-06-13 23:31:44.734729

"""
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f22bc3a6e81'
down_revision = '76f396b0cab8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scorerecord', sa.Column('character_skin', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scorerecord', 'character_skin')
    # ### end Alembic commands ###
