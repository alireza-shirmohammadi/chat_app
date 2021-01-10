from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
import datetime
from chat_app import settings



class User_profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='user')
    phone=models.IntegerField()
    ip=models.TextField(default='',blank=True,null=True)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False