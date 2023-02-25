from django import forms
from .models import Team, JoinRequest, Item
from authorization.models import Membership

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
    # def clean(self):
    #     name = self.cleaned_data.get('name')
        # parent_id = self.cleaned_data.get('parent_id')
        # if parent_id is not None:
        #     if Team.objects.filter(id=parent_id).count() == 0:
        #         raise forms.ValidationError('Parent team does not exist')

class MembershipCreationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('team_id', 'user_id', 'alumni', 'role_id')
    def clean(self):
        team_id = self.cleaned_data.get('team_id')
        user_id = self.cleaned_data.get('user_id')
        if Membership.objects.filter(team_id=team_id, user_id=user_id).count():
            raise forms.ValidationError('User is already a member of this team')

class JoinRequestForm(forms.ModelForm):
    team_id = forms.CharField()
    class Meta:
        widgets = {
            'user_id': forms.HiddenInput(),
        }
        model = JoinRequest
        fields = ('team_id','user_id')

    def clean_team_id(self):
        team_id = self.cleaned_data.get('team_id')
        if not Team.objects.filter(id=team_id).exists():
            raise forms.ValidationError('Invalid id')
        team = Team.objects.get(id=team_id)
        return team
    
    def clean(self):
        team_id = self.cleaned_data.get('team_id')
        user_id = self.cleaned_data.get('user_id')
        if Membership.objects.filter(team_id=team_id, user_id=user_id).count():
            raise forms.ValidationError('You are already a member of this team')
        if JoinRequest.objects.filter(status='P', team_id=team_id, user_id=user_id).exists():
            raise forms.ValidationError('A request is already pending')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'done')
        

        