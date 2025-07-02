from sqlalchemy import case, and_, or_, func, desc
from datetime import datetime
from pytz import timezone

from app.core.db import database
from app.core.model import ChatRoom, Chat, User, Profile

class ChatRepository:
    def get_chat_list(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                ChatRoom.id,
                ChatRoom.user_1_id,
                ChatRoom.user_2_id,
                func.max(Chat.created_at).label('last_message_time')
            ).select_from(ChatRoom)\
            .join(Chat, Chat.room_id == ChatRoom.id)\
            .filter(
                or_(
                    ChatRoom.user_1_id == user_id,
                    ChatRoom.user_2_id == user_id
                )
            ).group_by(ChatRoom.id).order_by(desc('last_message_time')).all()
            

    def get_chat_detail(self, user_id: int, user_1_id: int, user_2_id: int):
        with database.session_factory() as db:
            room = db.query(ChatRoom).filter(
                ChatRoom.user_1_id == user_1_id,
                ChatRoom.user_2_id == user_2_id
            ).one()
            
            chat = db.query(
                Chat.content,
                Chat.created_at,
                Chat.sender_id
            ).filter(Chat.room_id == room.id)\
            .order_by(Chat.created_at.asc())
            
            if user_id == user_1_id and room.user_1_out is not None:
                chat = chat.filter(Chat.id > room.user_1_out)
            elif user_id == user_2_id and room.user_2_out is not None:
                chat = chat.filter(Chat.id > room.user_2_out)
                
            return chat.all()

    def get_chat_room_user_info(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                User.id,
                User.name,
                User.level,
                Profile.ranking.label('profile')
            ).select_from(User)\
            .join(Profile, and_(
                Profile.pet_type == User.pet_type,
                Profile.level == User.level
            ))\
            .filter(User.id == user_id).one()

    def get_user_info(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                User.id,
                User.name,
                User.level,
                Profile.chat.label('profile')
            ).select_from(User)\
            .join(Profile, and_(
                Profile.pet_type == User.pet_type,
                Profile.level == User.level
            ))\
            .filter(User.id == user_id).one()

    def update_chat_read(self, user_1_id: int, user_2_id: int, other_id: int):
        with database.session_factory() as db:
            chats = db.query(Chat.id).filter(
                ChatRoom.user_1_id == user_1_id,
                ChatRoom.user_2_id == user_2_id,
                Chat.sender_id == other_id,
                Chat.is_read == 0
            ).all()

            for chat in chats:
                db.query(Chat).filter(Chat.id == chat.id).update({Chat.is_read: 1})
            db.commit()

    def send_chat(self, user_id: int, other_id: int, content: str):
        with database.session_factory() as db:
            now = datetime.now(timezone('Asia/Seoul'))
            chat_room = db.query(ChatRoom).filter(
                or_(
                    and_(
                        ChatRoom.user_1_id == user_id,
                        ChatRoom.user_2_id == other_id
                    ),
                    and_(
                        ChatRoom.user_1_id == other_id,
                        ChatRoom.user_2_id == user_id
                    )
            )).one()
            
            if chat_room.is_reported == 1:
                return False

            db.add(Chat(
                room_id=chat_room.id,
                sender_id=user_id,
                content=content,
                created_at=now,
                is_read=0
            ))
            db.commit()

            return True

    def check_is_exist_chat_room(self, user_1_id: int, user_2_id: int):
        with database.session_factory() as db:
            if db.query(ChatRoom).filter(
                or_(
                    and_(ChatRoom.user_1_id == user_1_id, ChatRoom.user_2_id == user_2_id),
                    and_(ChatRoom.user_1_id == user_2_id, ChatRoom.user_2_id == user_1_id)
                )).one_or_none() is None:

                db.add(ChatRoom(
                    user_1_id=user_1_id,
                    user_2_id=user_2_id,
                    created_at=datetime.now(timezone('Asia/Seoul'))
                ))
                db.commit()
                
    def get_last_message_and_unread_count(self, room_id: int, user_id: int):
        with database.session_factory() as db:
            last_message = db.query(Chat)\
                .filter(Chat.room_id == room_id)\
                .order_by(desc(Chat.created_at))\
                .first().content

            unread_count = db.query(Chat)\
                .filter(Chat.room_id == room_id, Chat.sender_id != user_id, Chat.is_read == 0)\
                .count()
            return last_message, unread_count
    
    def report_chat(self, user_id: int, other_id: int):
        with database.session_factory() as db:
            room = db.query(ChatRoom).filter(or_(
                and_(ChatRoom.user_1_id == user_id, ChatRoom.user_2_id == other_id),
                and_(ChatRoom.user_1_id == other_id, ChatRoom.user_2_id == user_id)
            )).one()
            
            room.is_reported = 1
            db.commit()
            
    def get_is_reported(self, user_1_id: int, user_2_id: int):
        with database.session_factory() as db:
            return db.query(ChatRoom.is_reported).filter(
                ChatRoom.user_1_id == user_1_id, 
                ChatRoom.user_2_id == user_2_id
            ).one().is_reported
            
    def is_user_get_out_chat_room(self, room_id: int, user_id: int):
        with database.session_factory() as db:
            room = db.query(ChatRoom).filter(
                ChatRoom.id == room_id
            ).one()
            
            last_chat_id = db.query(Chat).filter(
                Chat.room_id == room_id
            ).order_by(desc(Chat.id)).first().id
            
            if room.user_1_id == user_id and room.user_1_out is not None:
                if last_chat_id <= room.user_1_out:
                    return True
            elif room.user_2_id == user_id and room.user_2_out is not None:
                if last_chat_id <= room.user_2_out:
                    return True
            return False
            
    def get_out_chat(self, user_id: int, other_id: int):
        with database.session_factory() as db:
            room = db.query(ChatRoom).filter(
                or_(
                    and_(ChatRoom.user_1_id == user_id, ChatRoom.user_2_id == other_id),
                    and_(ChatRoom.user_1_id == other_id, ChatRoom.user_2_id == user_id)
                )
            ).one()
            
            last_chat_id = db.query(Chat).filter(
                Chat.room_id == room.id
            ).order_by(desc(Chat.id)).first().id
            
            if room.user_1_id == user_id:
                room.user_1_out = last_chat_id
            else:
                room.user_2_out = last_chat_id
                
            db.commit()

    def post_out_chat(self, user_id: int, other_id: int):
        with database.session_factory() as db:
            chats = db.query(Chat.id).select_from(Chat)\
                .join(ChatRoom, Chat.room_id == ChatRoom.id)\
                .filter(
                    or_(
                        and_(ChatRoom.user_1_id == user_id, ChatRoom.user_2_id == other_id),
                        and_(ChatRoom.user_1_id == other_id, ChatRoom.user_2_id == user_id)
                    ),
                    Chat.sender_id == other_id,
                    Chat.is_read == 0
                ).all()

            for chat in chats:
                db.query(Chat).filter(Chat.id == chat.id).update({Chat.is_read: 1})
            db.commit()

                
repository = ChatRepository()