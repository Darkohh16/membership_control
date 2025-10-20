from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    #auth
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #principal
    path('core/', include('core.urls')),

    #miembros
    path('socios/', include('socios.urls')),
]
