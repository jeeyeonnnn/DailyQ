from app.core.model import Region
from app.core.db import database

class RegionRepository:
    def get_main_regions(self):
        with database.session_factory() as db:
            return db.query(
                Region.main_id,
                Region.main
            ).group_by(Region.main).all()

    def get_sub_regions(self, region_id: int):
        with database.session_factory() as db:
            return db.query(
                Region.id,
                Region.sub
            ).filter(Region.main_id == region_id).all()

repository = RegionRepository()