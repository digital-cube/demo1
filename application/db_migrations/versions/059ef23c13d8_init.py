"""init

Revision ID: 059ef23c13d8
Revises: 
Create Date: 2020-11-07 15:31:59.024174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '059ef23c13d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_storage_created'), 'storage', ['created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_storage_created'), table_name='storage')
    op.drop_table('storage')
    # ### end Alembic commands ###
