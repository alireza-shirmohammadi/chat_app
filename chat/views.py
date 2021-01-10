from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
import json
from .models import Chat
import datetime
from user.models import User_profile
@login_required(login_url='/login/')
def index(request):
    b=User_profile.objects.all()
    return render(request,'chat/index.html')



@login_required()
def room(request,room_name):
    username=request.user.username
    user=request.user
    chat_model=Chat.objects.filter(room_name=room_name)
    members=Chat.objects.get(room_name=room_name).members.all()
    b=User_profile.objects.filter(user__in=members)
    users_profile=User_profile.objects.filter(user__in=members)
    user_profile = User_profile.objects.filter(user=user)[0]
    print(user_profile)

    if not chat_model.exists():
        chat= Chat.objects.create(room_name=room_name)
        chat.members.add(user)
    else:
        chat_model[0].members.add(user)

    context={
        'room_name':room_name,
        'username':mark_safe(json.dumps(username)),
        'members':members,
        'users_profile':users_profile,
        'user_profile': user_profile
    }

    return render(request, 'chat/room.html', context)


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if  email != '' and password != '':
            try:
                u=User.objects.get(email=email).username
            except :
                return redirect('mylogin')
            user = authenticate(username=u, password=password)
            if user is not None:
                login(request,user)
                return redirect('index')


    return render(request,'login/login.html')