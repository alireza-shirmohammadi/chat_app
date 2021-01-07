from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    room_name=models.CharField(max_length=100)
    members=models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    room_name=models.ForeignKey(Chat,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.author.username

    def last_message(self,room_name):
        room=Chat.objects.filter(room_name=room_name).first()
        return Message.objects.filter(room_name=room).order_by("-timestamp")
