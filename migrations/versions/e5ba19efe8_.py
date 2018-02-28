"""empty message

Revision ID: e5ba19efe8
Revises: feff04be79
Create Date: 2018-02-12 20:01:43.867587

"""

# revision identifiers, used by Alembic.
revision = 'e5ba19efe8'
down_revision = 'feff04be79'

from alembic import op


def upgrade():
    with op.batch_alter_table('club_club') as batch_op:
        batch_op.alter_column('is_show', new_column_name='is_shown')


def downgrade():
    with op.batch_alter_table('club_club') as batch_op:
        batch_op.alter_column('is_shown', new_column_name='is_show')
