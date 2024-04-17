"""empty message

Revision ID: e8f4ae7ebe50
Revises: 36d35387fbde
Create Date: 2024-04-17 18:10:04.496080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f4ae7ebe50'
down_revision = '36d35387fbde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('encryptedPass', sa.String(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('encryPassWithKey', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('encrypted_passwords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('encrypted_text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('encrypted_passwords')
    op.drop_table('users')
    # ### end Alembic commands ###
