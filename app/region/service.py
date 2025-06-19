from app.region.repository import repository
from app.region.dto.service import MainRegion, SubRegion

class RegionService:
    def get_main_regions(self):
        regions = []
        for region in repository.get_main_regions():
            regions.append(MainRegion(id=region.main_id, name=region.main))

        return regions
    
    def get_sub_regions(self, region_id: int):
        regions = []
        for region in repository.get_sub_regions(region_id):
            regions.append(SubRegion(id=region.id, name=region.sub))

        return regions

service = RegionService()