# # consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.layers import get_channel_layer
# from .models import Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         # Get the user_id from the WebSocket URL parameter
#         self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
#         self.group_name = f"group_{self.user_id}"

#         # Join the WebSocket group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Send the last 10 messages to the WebSocket
#         await self.send_messages()

#     async def disconnect(self, close_code):
#         # Leave the WebSocket group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         # Save message to database
#         new_message = Message.objects.create(
#             sender=self.user,
#             content=message,
#             group=self.group_name
#         )

#         # Broadcast the message to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': {
#                     'id': new_message.id,
#                     'sender': new_message.sender.username,
#                     'content': new_message.content,
#                     'timestamp': new_message.timestamp,
#                 }
#             }
#         )

#     # Handle incoming messages from the WebSocket group
#     async def chat_message(self, event):
#         message = event['message']
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     async def send_messages(self):
#         # Retrieve the last 10 messages from the group for the user
#         messages = Message.objects.filter(group=self.group_name).order_by('-timestamp')[:10]
#         messages_data = [{
#             'id': msg.id,
#             'sender': msg.sender.username,
#             'content': msg.content,
#             'timestamp': msg.timestamp
#         } for msg in messages]
        
#         # Send messages to WebSocket
#         await self.send(text_data=json.dumps({
#             'messages': messages_data
#         }))
