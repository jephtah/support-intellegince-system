"""
Create initial support_tickets table

Revision ID: 001_initial_support_tickets
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_support_tickets'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """create support_tickets table"""
    
    op.create_table('support_tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('original_queue', sa.String(length=100), nullable=True),
        sa.Column('original_priority', sa.String(length=50), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True, default='en'),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('tag_1', sa.String(length=100), nullable=True),
        sa.Column('tag_2', sa.String(length=100), nullable=True),
        sa.Column('tag_3', sa.String(length=100), nullable=True),
        sa.Column('tag_4', sa.String(length=100), nullable=True),
        sa.Column('tag_5', sa.String(length=100), nullable=True),
        sa.Column('tag_6', sa.String(length=100), nullable=True),
        sa.Column('tag_7', sa.String(length=100), nullable=True),
        sa.Column('tag_8', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                 server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=True, default=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # basic indexes
    op.create_index(op.f('ix_support_tickets_id'), 'support_tickets', ['id'], unique=False)
    op.create_index('ix_support_tickets_category', 'support_tickets', ['category'], unique=False)


def downgrade() -> None:
    """drop table"""
    
    op.drop_index('ix_support_tickets_category', table_name='support_tickets')
    op.drop_index(op.f('ix_support_tickets_id'), table_name='support_tickets')
    op.drop_table('support_tickets')