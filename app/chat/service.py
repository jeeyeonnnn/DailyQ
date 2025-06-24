from datetime import datetime, timedelta
from pytz import timezone

from app.chat.repository import repository
from app.chat.dto.response import ChatRoomResponse
from app.chat.dto.service import ChatDetail, UserInfo
from app.core.setting import setting

class ChatService:
    def get_chat_list(self, user_id: int):
        chat_rooms = repository.get_chat_list(user_id)
        user_chat_list, now = [], datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

        for chat_room in chat_rooms:
            other_id = chat_room.user_1_id if chat_room.user_1_id != user_id else chat_room.user_2_id
            other_info = repository.get_chat_room_user_info(other_id)
            last_message, unread_count = repository.get_last_message_and_unread_count(chat_room.id, user_id)

            user_chat_list.append(
                ChatRoomResponse(
                    user_id=other_info.id,
                    nickname=other_info.name,
                    level=other_info.level,
                    profile=f'https://{setting.S3_BUCKET_NAME}.s3.{setting.S3_REGION}.amazonaws.com/{other_info.profile}',
                    last_message=last_message,
                    last_message_time=self.get_time_diff(now, chat_room.last_message_time),
                    unread_count=unread_count
                )
            )
        return user_chat_list

    def get_time_diff(self, now, last_message_time) -> str:
        diff = now - last_message_time

        if now.year != last_message_time.year:
            return last_message_time.strftime('%Y-%m-%d')
        elif diff.days > 6:
            return last_message_time.strftime('%m월 %d일')
        elif diff.days > 0:
            return f'{diff.days}일 전'
        else:
            total_seconds = int(diff.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            if hours > 0:
                return f'{hours}시간 전'
            elif minutes > 0:
                return f'{minutes}분 전'
            else:
                return '방금 전'

    def get_chat_detail(self, user_id: int, other_id: int):
        self.check_is_exist_chat_room(user_id, other_id)
        now = datetime.now(timezone('Asia/Seoul'))
        user_1_id, user_2_id = min(user_id, other_id), max(user_id, other_id)

        # 채팅방 진입 시 읽음 처리
        repository.update_chat_read(user_1_id, user_2_id, other_id)

        other_info = repository.get_user_info(other_id)
        chats = repository.get_chat_detail(user_1_id, user_2_id)

        chat_detail = []
        for chat in chats:
            chat_detail.append(
                ChatDetail(
                    content=chat.content,
                    is_user_send=True if chat.sender_id == user_id else False,
                    created_at=self.get_chat_detail_time_diff(now, chat.created_at)
                )
            )
        
        return chat_detail, UserInfo(
            nickname=other_info.name,
            level=other_info.level,
            profile=f'https://{setting.S3_BUCKET_NAME}.s3.{setting.S3_REGION}.amazonaws.com/{other_info.profile}'
        )
       
    def get_chat_detail_time_diff(self, now, last_message_time) -> str:
        if (
            now.year == last_message_time.year 
            and now.month == last_message_time.month 
            and now.day == last_message_time.day
        ):
            return last_message_time.strftime("%p %I:%M")
        else:
            return last_message_time.strftime('%m월 %d일')

    def send_chat(self, user_id: int, other_id: int, content: str):
        self.check_is_exist_chat_room(user_id, other_id)
        repository.send_chat(user_id, other_id, content)

    def check_is_exist_chat_room(self, user_id: int, other_id: int):
        return repository.check_is_exist_chat_room(
            min(user_id, other_id),
            max(user_id, other_id)
        )


service = ChatService()