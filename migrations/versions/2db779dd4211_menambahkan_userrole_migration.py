"""Menambahkan UserRole  migration.

Revision ID: 2db779dd4211
Revises: b7983e23ab79
Create Date: 2024-04-20 14:56:35.060284

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2db779dd4211'
down_revision = 'b7983e23ab79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
    sa.Column('id_user_role', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_user_role')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', postgresql.ENUM('admin', 'member', name='user_role_enum'), autoincrement=False, nullable=False))

    op.drop_table('user_roles')
    # ### end Alembic commands ###
