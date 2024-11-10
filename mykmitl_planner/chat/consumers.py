# planner/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "messages"
        self.room_group_name = f"chat_{self.room_name}"

        # เข้าร่วมกลุ่มห้อง
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # ออกจากกลุ่มห้อง
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        student_id = data['student']
        staff_id = data['staff']
        content = data['content']
        sender = data['sender']

        # สร้าง Message ใหม่
        message = Message.objects.create(
            student_id=student_id,
            staff_id=staff_id,
            content=content,
            sender=sender
        )

        # ส่งข้อความไปยังห้อง
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'student': student_id,
                    'staff': staff_id,
                    'content': content,
                    'sender': sender,
                    'timestamp': str(message.timestamp),
                    'status': message.status
                }
            }
        )

    async def chat_message(self, event):
        # ส่งข้อความไปยัง WebSocket client
        await self.send(text_data=json.dumps(event['message']))
