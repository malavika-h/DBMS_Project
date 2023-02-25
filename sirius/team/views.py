from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from team.models import Team, JoinRequest, Invite, Item
from .forms import TeamCreationForm, JoinRequestForm, ItemForm
from authorization.models import Membership, Permission, Role
from session.models import Feedback, Session
from sirius.utils.perm import get_perms, has_perm
from sirius.utils.console_context import get_console_data
from .utils import init_roles
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from wordcloud import WordCloud, STOPWORDS

@login_required(login_url='user:signin')
def create_team(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.save()
            init_roles(team, request.user)
            return redirect('team:team_info', pk=form.instance.id)
    else:
        form = TeamCreationForm()
    return render(request, 'new_team.html', {'form': form})

@login_required(login_url='user:signin')
def create_sub_team(request, pk):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('parent_id'):
                if not has_perm('C', 'T', request.user, form.cleaned_data.get('parent_id')):
                    return HttpResponseForbidden()
            team = form.save(commit=False)
            if Team.objects.filter(id=pk).count() == 0:
                raise form.ValidationError("Parent team does not exist")
            if not has_perm('C', 'T', request.user, pk):
                return HttpResponseForbidden()
            else:
                parent = Team.objects.get(id=pk)
                team.parent_id = parent
            team.save()
            init_roles(team, request.user)
            return redirect('team:team_info', pk=form.instance.pk)
    else:
        form = TeamCreationForm()
    return render(request, 'create_sub_team.html', {'form': form, 'console': get_console_data(pk, request.user)})

@login_required(login_url='user:signin')
def team_info(request, pk):
    members = Membership.objects.filter(team_id=pk).values('created_at', 'alumni', 'user_id__pk', 'user_id__first_name', 'user_id__last_name', 'user_id__username', 'role_id__pk', 'role_id__role_name')
    children = Team.objects.filter(parent_id=pk).values('name', 'id')
    return render(request, 'team_info.html', {
        'members': members,
        'children': children,
        'console': get_console_data(pk, request.user)
    })

@login_required(login_url='user:signin')
def send_invite(request, pk, user):
    if request.method == 'POST':
        if not has_perm('C', 'I', request.user, pk):
            return HttpResponseForbidden()
        if Invite.objects.filter(status = 'P', team_id=pk, invited=user).exists():
            return redirect('team:team_info', pk=pk)
        invite = Invite(team_id=Team.objects.get(id=pk), created_by=request.user, invited=get_user_model().objects.get(pk=user))
        invite.save()
        return redirect('team:team_info', pk=pk)
    return redirect('team:team_info', pk=pk)

@login_required(login_url='user:signin')
def send_join_request(request):
    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            request.session['join_form_errors'] = form.errors
    return redirect('user:dashboard', u_pk=request.user.pk)

@login_required(login_url='user:signin')
def invites(request, pk):
    if not has_perm('R', 'I', request.user, pk):
        return HttpResponseForbidden()
    invites = Invite.objects.filter(team_id=pk, status='P').values('invited__first_name', 'invited__last_name', 'invited__email', 'invited__pk', 'created_at', 'status', 'pk', 'created_by__first_name', 'created_by__last_name', 'created_by__email', 'created_by__pk')
    return render(request, 'invites.html', {'invites': invites, 'console': get_console_data(pk, request.user)})

@login_required(login_url='user:signin')
def join_requests(request, pk):
    if not has_perm('R', 'JR', request.user, pk):
        return HttpResponseForbidden()
    requests = JoinRequest.objects.filter(team_id=pk, status='P').values('user_id__first_name', 'user_id__last_name', 'user_id__username', 'user_id__pk', 'created_at', 'status', 'pk')
    return render(request, 'join_requests.html', {'requests': requests, 'console': get_console_data(pk, request.user)})

@login_required(login_url='user:signin')
def accept_invite(request, pk):
    if request.method == 'POST':
        invite = Invite.objects.get(pk=pk)
        if not has_perm('U', 'I', request.user, invite.team_id.id):
            return HttpResponseForbidden()
        invite.status = 'A'
        invite.save()
        membership = Membership(team_id=invite.team_id, user_id=invite.invited)
        membership.save()
        return redirect('team:team_info', pk=invite.team_id.id)

@login_required(login_url='user:signin')
def accept_join_request(request, pk):
    if request.method == 'POST':
        join_request = JoinRequest.objects.get(pk=pk)
        if not has_perm('U', 'JR', request.user, join_request.team_id.id):
            return HttpResponseForbidden()
        join_request.status = 'A'
        join_request.save()
        membership = Membership.objects.filter(team_id=join_request.team_id, user_id=join_request.user_id).first()
        if not membership:
            membership = Membership(team_id=join_request.team_id, user_id=join_request.user_id, )
            role = Role.objects.filter(team_id=join_request.team_id, role_name='Member').first()
            membership.role_id = role
            membership.save()
        return redirect('team:team_info', pk=join_request.team_id.id)

@login_required(login_url='user:signin')
def decline_invite(request, pk):
    if request.method == 'POST':
        invite = Invite.objects.get(pk=pk)
        if not has_perm('U', 'I', request.user, invite.team_id.id):
            return HttpResponseForbidden()
        invite.status = 'R'
        invite.save()
        return redirect('user:dashboard', u_pk=invite.team_id.id)

@login_required(login_url='user:signin')
def decline_join_request(request, pk):
    if request.method == 'POST':
        join_request = JoinRequest.objects.get(pk=pk)
        if not has_perm('U', 'JR', request.user, join_request.team_id.id):
            return HttpResponseForbidden()
        join_request.status = 'R'
        join_request.save()
        return redirect('user:dashboard', u_pk=join_request.team_id.id)

@login_required(login_url='user:signin')
def leave_team(request, pk):
    membership = Membership.objects.get(user_id=request.user.pk, team_id=pk)
    membership.delete()
    return redirect('user:dashboard', u_pk=request.user.pk)

@login_required(login_url='user:signin')
def permissions(request, pk):
    if not has_perm('R', 'P', request.user, pk):
        return HttpResponseForbidden()
    perms = Permission.objects.filter(team_id=pk).values('user_id__first_name', 'user_id__last_name', 'user_id__pk', 'team_id__name', 'team_id__id', 'permission_name', 'pk')
    return render(request, 'permissions.html', {'perms': perms, 'console': get_console_data(pk, request.user)})

@login_required(login_url='user:signin')
def delete_team(request, pk):
    team = Team.objects.get(id=pk)
    if not has_perm('D', 'T', request.user, pk):
        return HttpResponseForbidden()
    team.delete()
    return redirect('user:dashboard', u_pk=request.user.pk)

@login_required(login_url='user:signin')
def get_todo_list(request, pk):
    #items = Item.objects.using('users').get(team_id=pk)
    items = Item.objects.using('users').filter(team_id=pk)
    return render(request, 'todo_list.html', {'console': get_console_data(pk, request.user), 'items': items})

@login_required(login_url='user:signin')
def create_an_item(request, pk):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            t=form.save()
            t.team_id=pk
            t.save()
            t.save(using='users')
            return redirect('team:get_todo_list', pk=pk)
    else:
        form = ItemForm()
    return render(request, "item_form.html", {'console': get_console_data(pk, request.user), 'form': form})

@login_required(login_url='user:signin')
def edit_an_item(request, pk, id):
    item = get_object_or_404(Item, pk=id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            t=form.save()
            t.save(using='users')
            return redirect('team:get_todo_list', pk=pk)
    else:
        form = ItemForm(instance=item)
    return render(request, "item_form.html", {'console': get_console_data(pk, request.user), 'form': form})

@login_required(login_url='user:signin')
def toggle_status(request, pk, id):
    item = get_object_or_404(Item, pk=id)
    item.done = not item.done
    item.save(using='users')
    return redirect('team:get_todo_list', pk=pk)

@login_required(login_url='user:signin')
def view_analytics(request, pk):
    if not has_perm('V', 'A', request.user, pk):
        return HttpResponseForbidden()
    allevent = Feedback.objects.filter(teamid=pk).values()
    df = pd.DataFrame(list(allevent))
    desc = df['feedback']
    comment_words = ''
    for val in desc:
        comment_words = comment_words + " " + str(val)
    stopwords = set(STOPWORDS)
 
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)
    
    # plotting the word cloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    imgdata1 = StringIO()
    plt.savefig(imgdata1, format='svg')
    imgdata1.seek(0)
    data1 = imgdata1.getvalue()
    df.drop(['id', 'teamid','feedback'], axis=1, inplace=True)
    #print(df)
    crosstb = pd.crosstab(df.eventid, df.score)
    #print(crosstb)
    barplot = crosstb.plot.bar(rot=0)
    imgdata = StringIO()
    barplot.figure.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return render(request, 'feedback_analytics.html', {'console': get_console_data(pk, request.user),'data':data, 'data1':data1})