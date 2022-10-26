"""empty message

Revision ID: a3abc5bf0de8
Revises: 7a78bad453a0
Create Date: 2022-10-25 20:50:31.694661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3abc5bf0de8'
down_revision = '7a78bad453a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_captcha', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('email_captcha', sa.Column('user_type', sa.Enum('student', 'teacher', 'admin'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email_captcha', 'user_type')
    op.drop_column('email_captcha', 'user_id')
    # ### end Alembic commands ###
