"""Added users table

Revision ID: d6abe79eec68
Revises:
Create Date: 2023-07-18 05:22:44.655016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6abe79eec68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('first_name', sa.String(length=255), nullable=False),
                    sa.Column('last_name', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=320), nullable=False),
                    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
