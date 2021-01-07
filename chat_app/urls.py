
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/',include('chat.urls')),
    path('login/',views.mylogin,name='mylogin'),
]
if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)