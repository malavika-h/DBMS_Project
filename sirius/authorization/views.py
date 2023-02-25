from django.shortcuts import render,redirect
from .forms import RoleCreationForm
from django.contrib.auth.decorators import login_required
from .models import Role
from authorization.models import Membership, Permission
from team.models import Team
from sirius.utils.perm import has_perm, display_perms
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from sirius.utils.console_context import get_console_data

@login_required(login_url='user:signin')
def create_role(request, team_pk):
    if request.method == 'POST':
        if not has_perm('C', 'R', request.user, team_pk):
            return HttpResponseForbidden()
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            request.session['create_role_errors'] = form.errors
        return redirect('authorization:show_roles', team_pk)
    return Http404()
        
@login_required(login_url='user:signin')
def show_roles(request, team_pk):
    members = Membership.objects.filter(team_id=team_pk).values('pk', 'user_id__pk', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'role_id__role_name', 'role_id__role_description', 'role_id__pk')
    roles = Role.objects.filter(team_id=team_pk).values('pk', 'role_name', 'role_description')
    role_form = RoleCreationForm()
    create_role_errors = request.session.get('create_role_errors')
    if create_role_errors:
        for field, err in create_role_errors.items():
            role_form.errors[field] = err
        del request.session['create_role_errors']
    return render(request, 'show_roles.html', {
        'members': members,
        'roles': roles,
        'console': get_console_data(team_pk, request.user),
        'role_form': role_form
    })


@login_required(login_url='user:signin')
def update_roles(request, team_pk):
    if request.method == 'POST':
        if not has_perm('U', 'R', request.user, team_pk):
            return HttpResponseForbidden()
        for key, role_id in request.POST.items():
            if key.startswith('role-'):
                member_pk = key.split('-')[1]
                membership = Membership.objects.get(pk=member_pk)
                membership.role_id = Role.objects.get(pk=role_id)
                membership.save()
        return redirect('authorization:show_roles', team_pk=team_pk)
    return Http404()


@login_required(login_url='user:signin')
def show_permissions(request, team_pk):
    if not has_perm('R', 'R', request.user, team_pk):
        return HttpResponseForbidden()
    roles = Role.objects.filter(team_id__id=team_pk).values('pk', 'role_name', 'role_description', 'permissions')
    all_permissions = Permission.objects.all()
    return render(request, 'show_permissions.html', {
        'console': get_console_data(team_pk, request.user),
        'roles': roles,
        'all_permissions': all_permissions,
        'role_based_perms': display_perms(roles)
    })

@login_required(login_url='user:signin')
def update_permissions(request, team_pk):
    if request.method == 'POST':
        if not has_perm('U', 'R', request.user, team_pk):
            return HttpResponseForbidden()
        role_pk = request.POST['role-pk']
        perm_string = request.POST['perm-string']
        if not perm_string or not role_pk:
            return HttpResponseBadRequest('Invalid request')
        role = Role.objects.get(pk=role_pk)
        if not role:
            return HttpResponseBadRequest('Invalid request')
        if str(role.team_id.id) != str(team_pk):
            return HttpResponseBadRequest('Invalid request')
        role.permissions = perm_string
        role.save()
        return redirect('authorization:show_permissions', team_pk=team_pk)
    return Http404()

@login_required(login_url='user:signin')
def delete_role(request, team_pk, r_pk):
    if not has_perm('D', 'R', request.user, team_pk):
        return HttpResponseForbidden()
    role = Role.objects.get(pk=r_pk)
    if str(role.team_id.id) != str(team_pk):
        return HttpResponseBadRequest('Invalid request')
    if not role:
        return HttpResponseBadRequest('Invalid request')
    if role.role_name == "Admin" or role.role_name == "Member":
        return HttpResponseBadRequest(f'Cannot delete {role.role_name} role')
    curr_members = Membership.objects.filter(team_id__id=team_pk).filter(role_id__pk=r_pk)
    member_role = Role.objects.get(team_id__id=team_pk, role_name = "Member")
    for member in curr_members:
        member.role_id = member_role
        member.save()
    role.delete()
    return redirect('authorization:show_roles', team_pk=team_pk)

@login_required(login_url='user:signin')
def update_role(request, team_pk, r_pk):
    if request.method == 'POST':
        if not has_perm('U', 'R', request.user, team_pk):
            return HttpResponseForbidden()
        role = Role.objects.get(pk=r_pk)
        if str(role.team_id.id) != str(team_pk):
            return HttpResponseBadRequest('Invalid request')
        if not role:
            return HttpResponseBadRequest('Invalid request')
        form = RoleCreationForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
        else:
            request.session['update_role_errors'] = form.errors
        return redirect('authorization:show_roles', team_pk=team_pk)
    return Http404()