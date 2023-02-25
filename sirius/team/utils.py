from authorization.models import Role, Permission, Membership

def init_roles(team, user):
    admin_role = Role.objects.create(role_name='Admin', team_id=team, role_description='Admin')
    admin_permissions = Permission.objects.all().values('pk')
    permission_string = ""
    for permission in admin_permissions:
        permission_string += str(permission['pk']) + ","
    admin_role.permissions = permission_string
    admin_role.save()
    member_role = Role.objects.create(role_name='Member', team_id=team, role_description='Member')
    member_permissions = "6,10,14,18,22,26"
    member_role.permissions = member_permissions
    member_role.save()
    Membership.objects.create(user_id=user, team_id=team, role_id=admin_role)