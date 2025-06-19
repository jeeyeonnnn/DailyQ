from typing import List

from fastapi import APIRouter
from starlette import status

from app.region.dto.service import MainRegion, SubRegion
from app.region.service import service


router = APIRouter(tags=['☑️ Region : 지역 관련 API 모음'], prefix='/region')

@router.get(
    path="",
    summary="지역 목록 조회",
    description="지역 목록을 조회합니다.",
    response_model=List[MainRegion],
    status_code=status.HTTP_200_OK
)
def get_main_regions():
    return service.get_main_regions()


@router.get(
    path="/{region_id}/sub-regions",
    summary="지역 하위 목록 조회",
    description="지역 하위 목록을 조회합니다.",
    response_model=List[SubRegion],
    status_code=status.HTTP_200_OK
)
def get_sub_regions(region_id: int):
    return service.get_sub_regions(region_id)