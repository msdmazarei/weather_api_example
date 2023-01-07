"""populate agg_weather table

Revision ID: 68980d3d9078
Revises: 3372461b8024
Create Date: 2023-01-06 20:53:07.940137

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "68980d3d9078"
down_revision = "3372461b8024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO agg_weather_report 
        (station, measure_year, max_temperature, min_temperature, total_precipitation_cm)
        SELECT station, EXTRACT(YEAR FROM measure_date) as measure_year, avg(max_temperature) as max_temperature, avg(min_temperature) as min_temperature, sum(precipitation_mm) / 10::float as total_precipitation_cm
        FROM weather
        GROUP BY 1,2;
        """
    )


def downgrade() -> None:
    op.execute(
        """
    DELETE FROM agg_weather_report;
    """
    )
