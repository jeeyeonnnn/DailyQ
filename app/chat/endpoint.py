from fastapi import APIRouter
from typing import List
from fastapi import Depends

from app.core.auth import auth
from app.chat.service import service
from app.chat.dto.response import ChatRoomResponse, ChatDetailResponse
from app.chat.dto.request import ChatSendRequest


router = APIRouter(tags=['☑️ Chat : 채팅 관련 API 모음'], prefix='/chat')

@router.get(
    path='/list',
    summary='채팅 목록 조회',
    description='## ✔️️ [채팅 목록 조회] \n'
                '### - 유저의 채팅 목록을 조회 \n'
                '### - 채팅 목록은 최근 메시지 시간 기준 내림차순으로 정렬 \n'
                '### - 채팅 이력이 없는 경우 빈리스트 반환 \n',
    response_model=List[ChatRoomResponse]
)
def get_chat_list(
    user_id=Depends(auth.auth_wrapper)
):
    return service.get_chat_list(user_id)


@router.get(
    path='/detail',
    summary='채팅 내역 조회',
    description='## ✔️️ [채팅 내역 조회] \n'
                '### - 유저의 채팅 내역을 조회 \n'
                '### - 채팅 내역은 최근 메시지 시간 기준 내림차순으로 정렬 \n'
                '### - 채팅 이력이 없는 경우 빈리스트 반환 \n',
    response_model=ChatDetailResponse
)
def get_chat_room(
    user_id: int,
    user_idx=Depends(auth.auth_wrapper)
):
    chat_detail, user_info = service.get_chat_detail(user_idx, user_id)
    return ChatDetailResponse(
        user_info=user_info,
        chat_detail=chat_detail
    )


@router.post(
    path='/send',
    summary='채팅 전송',
    description='## ✔️️ [채팅 전송] \n'
                '### - 유저의 채팅을 전송 \n',
    response_model=None
)
def send_chat(
    request: ChatSendRequest,
    user_idx=Depends(auth.auth_wrapper)
):
    return service.send_chat(user_idx, request.user_id, request.content)