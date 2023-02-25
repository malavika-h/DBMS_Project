from django.urls import path
from .views import *
from django.urls.conf import include

app_name = 'team'

urlpatterns = [
    path('create/', create_team, name='create_team'),
    path('<pk>/new-team/', create_sub_team, name='create_sub_team'),
    path('<pk>/info/', team_info, name='team_info'),
    path('<pk>/send-invite/<user>/', send_invite, name='send_invite'),
    path('send-join-request/', send_join_request, name='send_join_request'),
    path('<pk>/invites/', invites, name='invites'),
    path('<pk>/join-requests/', join_requests, name='join_requests'),
    path('accept-invite/<pk>/', accept_invite, name='accept_invite'),
    path('accept-join-request/<pk>/', accept_join_request, name='accept_join_request'),
    path('decline-join-request/<pk>/', decline_join_request, name='decline_join_request'),
    path('decline-invite/<pk>/', decline_invite, name='decline_invite'),
    path('leave-team/<pk>/', leave_team, name='leave_team'),
    path('decline-join-request/<pk>/', decline_join_request, name='decline_join_request'),
    path('<pk>/delete', delete_team, name='delete_team'),
    path('<pk>/get_todo_list', get_todo_list, name='get_todo_list'),
    path('<pk>/add_item', create_an_item, name='create_an_item'),
    path('<pk>/edit_item/<id>', edit_an_item, name='edit_an_item'),
    path('<pk>/toggle/<id>', toggle_status, name='toggle_status'),
    path('<pk>/view-analytics/', view_analytics, name='view_analytics'),
    path('<pk>/', include('session.urls', namespace="session"))
]