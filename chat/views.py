from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
import json
from .models import Chat

@login_required(login_url='/login/')
def index(request):
    return render(request,'chat/index.html')



@login_required()
def room(request,room_name):
    username=request.user.username
    user=request.user
    chat_model=Chat.objects.filter(room_name=room_name)
    members=Chat.objects.get(room_name=room_name).members.all()
    
    if not chat_model.exists():
        chat= Chat.objects.create(room_name=room_name)
        chat.members.add(user)
    else:
        chat_model[0].members.add(user)

    context={
        'room_name':room_name,
        'username':mark_safe(json.dumps(username)),
        'members':members
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