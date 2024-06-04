"""delete column day

Revision ID: 11d1ad46cc6d
Revises: 5a97de88469e
Create Date: 2024-05-23 22:59:48.532468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d1ad46cc6d'
down_revision = '5a97de88469e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedules', schema=None) as batch_op:
        batch_op.drop_column('day_of_week')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedules', schema=None) as batch_op:
        batch_op.add_column(sa.Column('day_of_week', sa.VARCHAR(length=255), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
