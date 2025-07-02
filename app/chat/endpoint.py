from typing import List
from fastapi import APIRouter, Depends, WebSocket, BackgroundTasks, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse

from app.core.auth import auth
from app.chat.service import service
from app.chat.dto.response import ChatRoomResponse, ChatDetailResponse
from app.chat.dto.request import ChatSendRequest, ChatReportRequest
from app.core.socket import ConnectionManager

manager = ConnectionManager()

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
                '### - 채팅 이력이 없는 경우 빈리스트 반환 \n'
                '### - 신고 상태의 채팅방인 경우 is_reported 값이 True \n',
    response_model=ChatDetailResponse
)
def get_chat_room(
    user_id: int,
    user_idx=Depends(auth.auth_wrapper)
):
    is_reported, chat_detail, user_info = service.get_chat_detail(user_idx, user_id)
    return ChatDetailResponse(
        is_reported=is_reported,
        user_info=user_info,
        chat_detail=chat_detail
    )


@router.post(
    path='/send',
    summary='채팅 전송',
    description='## ✔️️ [채팅 전송] \n'
                '### - 유저의 채팅을 전송 \n'
                '### - 신고 상태의 채팅방인 경우 채팅을 전송할 수 없음 \n'
                '''
                status_code = 400
                {
                    "message": "채팅을 전송할 수 없습니다."
                }
                ''',
    response_model=None
)
def send_chat(
    request: ChatSendRequest,
    user_idx=Depends(auth.auth_wrapper),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    status = service.send_chat(user_idx, request.user_id, request.content)
    
    if status:
        background_tasks.add_task(
            manager.send_to_user,
            request.user_id,
            {
                "user_id": user_idx,
                "content": request.content,
                "is_user_send": False,
                "created_at": "방금 전"
            }
        )
        return JSONResponse(status_code=201, content={"message": "Message sent successfully"})
    return JSONResponse(status_code=400, content={"message": "채팅을 전송할 수 없습니다."})
    
@router.post(
    path='/report',
    summary='채팅 신고',
    description='## ✔️️ [채팅 신고] \n'
                '### - 유저의 채팅을 신고 \n'
                '### - 신고 후 채팅 내역은 존재하지만, 더 이상 채팅을 보낼 수 없음 \n'
)
def report_chat(
    request: ChatReportRequest,
    user_idx=Depends(auth.auth_wrapper)
):
    service.report_chat(user_idx, request.user_id)
    return JSONResponse(status_code=201, content={"message": "Reported successfully"})

@router.post(
    path='/get-out',
    summary='채팅방 나가기',
    description='## ✔️️ [채팅방 나가기] \n'
                '### - 유저의 채팅방을 나가기 \n'
)
def get_out_chat(
    request: ChatReportRequest,
    user_idx=Depends(auth.auth_wrapper)
):
    service.get_out_chat(user_idx, request.user_id)
    return JSONResponse(status_code=201, content={"message": "Get out successfully"})


@router.post(
    path='/out',
    summary='채팅방 나가기 (읽음 처리를 위함)',
    description='## ✔️️ [채팅방 나가기 (읽음 처리를 위함)] \n'
                '### - 유저의 채팅방 읽음 처리 \n'
)
def post_out_chat(
    request: ChatReportRequest,
    user_idx=Depends(auth.auth_wrapper)
):
    service.post_out_chat(user_idx, request.user_id)
    return JSONResponse(status_code=201, content={"message": "Get out successfully"})

    
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    token: str = Query(None)
):
    if token is not None:
        user_idx = auth.decode_token(token)
        print(f'WebSocket 연결 시도 : {user_idx}')
        await manager.connect(user_idx, websocket)
        print(f'WebSocket 연결 성공 : {user_idx}')
        try:
            while True:
                await websocket.receive_text()  # 그냥 기다리기만
        except WebSocketDisconnect:
            manager.disconnect(user_idx)
            print(f'WebSocket 연결 종료 : {user_idx}')