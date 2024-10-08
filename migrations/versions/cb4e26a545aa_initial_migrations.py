"""Initial Migrations

Revision ID: cb4e26a545aa
Revises: 
Create Date: 2024-09-14 14:20:50.017826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb4e26a545aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('staff_name', sa.String(), nullable=False),
    sa.Column('staff_date', sa.Date(), nullable=False),
    sa.Column('staff_datetime', sa.DateTime(), nullable=True),
    sa.Column('staff_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=255), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=False),
    sa.Column('fte', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_set')
    op.drop_table('user')
    op.drop_table('team')
    op.drop_table('staff')
    # ### end Alembic commands ###
