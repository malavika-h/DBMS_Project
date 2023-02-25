from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('user/', include('user.urls')),
    path('team/', include('team.urls')),
    # path('session/', include('session.urls')),
    path('authorization/<team_pk>/', include('authorization.urls'))
]
