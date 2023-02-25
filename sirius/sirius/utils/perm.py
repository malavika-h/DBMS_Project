from signal import raise_signal
from authorization.models import Permission, Membership
from django.http import HttpResponseForbidden

def has_perm(action, relation, user, team):
    if user.is_superuser:
        return True
    permission = Permission.objects.get(action=action, relation=relation)
    if permission:
        permission = permission.pk
    else:
        return False
    membership = Membership.objects.get(user_id=user, team_id=team)
    if membership:
        user_permissions = membership.role_id.permissions.strip(',').split(',')
    if str(permission) in user_permissions:
        return True
    return False

def get_perms(user, team):
    perms = []
    if team:
        user_permissions = Membership.objects.get(user_id=user, team_id=team).role_id.permissions.strip(',').split(',')
        for permission in user_permissions:
            if permission:
                perm = Permission.objects.get(pk=permission)
                perms.append(perm.action + '-' + perm.relation)
    return perms

def display_perms(roles):
    perms_dict = {}
    for role in roles:
        perms_list = []
        perms = role['permissions'].strip(',').split(',')
        for permission in perms:
            if permission.isnumeric():
                perms_list.append(int(permission))
        perms_dict[int(role['pk'])] = perms_list
    return perms_dict

# def permList(perms):
#     perms = []
#     for permission in perms:
#         if permission:
#             perm = Permission.objects.get(pk=permission)
#             perms.append(perm.action + '-' + perm.relation)
#     return perms