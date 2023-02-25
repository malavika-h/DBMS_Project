from django.urls import path
from .views import *

app_name = 'authorization'

urlpatterns = [
    path('role/create/', create_role, name='create_role'),
    path('roles/', show_roles, name='show_roles'),
    path('roles/update/', update_roles, name='update_roles'),
    path('permissions/', show_permissions, name='show_permissions'),
    path('permissions/update/', update_permissions, name='update_permissions'),
    path('role/<r_pk>/delete/', delete_role, name='delete_role'),
    path('role/<r_pk>/update/', update_role, name='update_role'),

]