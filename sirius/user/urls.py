from django.contrib import admin
from django.urls import path

from . import views
from session.views import user_calendar, user_bulletin

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('settings/', views.accountsettings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('bulletin/', user_bulletin, name='bulletin'),
    path('<u_pk>/dashboard/', views.dashboard, name='dashboard'),
    path('<u_pk>/calendar/', user_calendar, name='calendar'),
    # path('<u_pk>/settings/', views.settings, name='settings'),
]