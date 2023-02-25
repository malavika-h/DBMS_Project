from django.urls import path
from .views import *

app_name = 'session'

urlpatterns = [
    path('timetable/', timetable, name='timetable'),
    path('calendar/', calendar, name='calendar'),
    
    path('notices/', notice_board, name='notice_board'),
    path('notice/update/<int:n_pk>/', update_notice, name='update_notice'),
    path('notice/delete/<int:n_pk>/', delete_notice, name='delete_notice'),
    path('notice/create/', create_notice, name='create_notice'),
    
    path('event/create/', create_event, name='create_event'),
    path('event/update/<int:e_pk>/', update_event, name='update_event'),
    path('event/delete/<int:e_pk>/', delete_event, name='delete_event'),
    path('event/<int:e_pk>', event_detail, name='event_detail'),

    path('class/create/', create_class, name='create_class'),
    path('class/update/<int:c_pk>/', update_class, name='update_class'),
    path('class/delete/<int:c_pk>/', delete_class, name='delete_class'),
    path('class/<int:c_pk>/', class_detail, name='class_detail'),
    path('event/feedback/<int:e_pk>/', event_feedback, name='event_feedback'),
]