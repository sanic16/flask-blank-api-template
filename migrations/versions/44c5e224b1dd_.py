"""empty message

Revision ID: 44c5e224b1dd
Revises: 
Create Date: 2024-02-16 19:24:49.752193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44c5e224b1dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=75), nullable=False),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('birthDate', sa.Date(), nullable=True),
    sa.Column('firstName', sa.String(length=50), nullable=True),
    sa.Column('lastName', sa.String(length=50), nullable=True),
    sa.Column('department', sa.String(length=25), nullable=True),
    sa.Column('municipality', sa.String(length=25), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('phoneNumber', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
