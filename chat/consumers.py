import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message,Chat
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        author=data['username']
        message=data['message']
        room_name=data['room_name']
        room=Chat.objects.filter(room_name=room_name).first()
        user=User.objects.filter(username=author).first()
        message_model=Message.objects.create(author=user,content=message,room_name=room)
        result=self.message_serializer(message_model)
        result=eval(result)

        self.sent_to_chat_message(result)

    def fetch_message(self, data):
        room_name=data['room_name']

        qs=Message.last_message(self,room_name)

        message_json=self.message_serializer(qs)
        content={
            'message':eval(message_json),
            'command':'fetch_message'
        }
        self.chat_message(content)


    def image(self,data):
        self.sent_to_chat_message(data)

    def message_serializer(self, qs):

        ser=MessageSerializer(qs, many=(lambda qs:True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        content=JSONRenderer().render(ser.data)
        return content




    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    commands = {
        'new_message':new_message,
        'fetch_message':fetch_message,
        'img':image
    }





    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict.get('message',None)
        command = text_data_dict['command']


        self.commands[command](self,text_data_dict)





    def sent_to_chat_message(self,message):
        command = message.get("command", None)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'content':message['content'],
                'command':(lambda command : "img" if( command == "img") else "new_message")(command),
                '__str__':message['__str__']

            }
        )


    def chat_message(self,event):

        self.send(text_data=json.dumps(event))